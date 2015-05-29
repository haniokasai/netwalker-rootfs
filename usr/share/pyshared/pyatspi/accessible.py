'''
Creates functions at import time that are mixed into the 
Accessibility.Accessible base class to make it more Pythonic.

Based on public domain code originally posted at 
U{http://wwwx.cs.unc.edu/~parente/cgi-bin/RuntimeClassMixins}.

@var _ACCESSIBLE_CACHE: Pairs hash values for accessible objects to 
  L{_PropertyCache} bags. We do not store actual accessibles in the dictionary
  because that would +1 their ref counts and cause __del__ to never be called
  which is the method we rely on to properly invalidate cache entries.
@type _ACCESSIBLE_CACHE: dictionary
@var _CACHE_LEVEL: Current level of caching enabled. Checked dynamically by
  L{_AccessibleMixin}
@type _CACHE_LEVEL: integer

@author: Peter Parente
@organization: IBM Corporation
@copyright: Copyright (c) 2005, 2007 IBM Corporation
@license: LGPL

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.

Portions of this code originally licensed and copyright (c) 2005, 2007
IBM Corporation under the BSD license, available at
U{http://www.opensource.org/licenses/bsd-license.php}
'''
import new
import types
import ORBit
import Accessibility
import constants
import utils
import registry
import weakref

_ACCESSIBLE_CACHE = weakref.WeakValueDictionary()
_ACCESSIBLE_USER_DATA = weakref.WeakValueDictionary()
_CACHE_LEVEL = None

class _PropertyCache:
  def wipe(self):
      self.__dict__ = {}

class _UserData:
  value = None

def getCacheLevel():
  '''
  Gets the current level of caching.
  
  @return: None indicating no caching is in effect. 
    L{constants.CACHE_INTERFACES} indicating all interface query results are
    cached. L{constants.CACHE_PROPERTIES} indicating all basic accessible
    properties are cached.
  @rtype: integer
  '''
  return _CACHE_LEVEL

def setCacheLevel(val):
  '''
  Sets the desired level of caching for all accessible objects created after
  this function is invoked. Immediately clears the current accessible cache.
  
  @param val: None indicating no caching is in effect. 
    L{constants.CACHE_INTERFACES} indicating all interface query results are
    cached. L{constants.CACHE_PROPERTIES} indicating all basic accessible
    properties are cached plus all interfaces.
  @type val: integer
  '''
  global _CACHE_LEVEL
  if _CACHE_LEVEL != val:
    # empty our accessible cache  
    _ACCESSIBLE_CACHE.clear()
    # need to register/unregister for listeners depending on caching level
    if val == constants.CACHE_PROPERTIES:
      r = registry.Registry()
      r.registerEventListener(_updateCache, *constants.CACHE_EVENTS)
    else:
      r = registry.Registry()
      r.deregisterEventListener(_updateCache, *constants.CACHE_EVENTS)
  _CACHE_LEVEL = val
  
def clearCache():
  '''Forces a clear of the entire cache.'''
  _ACCESSIBLE_CACHE.clear()
  
def printCache(template='%s'):
  '''
  Prints the contents of the cache.
  
  @param template: Format string to use when printing
  @type template: string
  '''
  print template % _ACCESSIBLE_CACHE

def _updateCache(event):
  '''
  Invalidates an entry in the cache when the hash value of a source of an event
  matches an entry in the cache.
  
  @param event: One of the L{constants.CACHE_EVENTS} event types
  @type event: L{event.Event}
  '''
  try:
    _ACCESSIBLE_CACHE[hash(event.source)].wipe()
  except KeyError:
    return

def _getAndCache(acc, value_name, get_method):
  '''
  If property caching is enabled, use the cached proprty, or get the 
  property and cache it. If property caching is disabled, simply get the 
  property.

  @param value_name: The name of the value, like 'role' or 'description'.
  @type value_name: string
  @param get_method: Method used to get the property, should not have any 
  arguments.
  @type get_method: callable
  @return: Value of property we are retrieving.
  @rtype: object
  '''
  if _CACHE_LEVEL != constants.CACHE_PROPERTIES:
    return get_method()
    
  cache = _ACCESSIBLE_CACHE
  h = hash(acc)

  try:
    pc = acc._property_cache
  except AttributeError:
    try:
      pc = cache[h]
    except KeyError:
      # no cached info for this accessible yet
      pc = _PropertyCache()
      cache[h] = pc
    acc._property_cache = pc  
    
  try:
    value = getattr(pc, value_name)
  except AttributeError:
    # no cached property of this type
    value = get_method()
    setattr(pc, value_name, value)
    
  return value
  

def _makeQuery(interface):
  '''
  Builds a function querying to a specific interface and returns it.
  
  @param interface: Class representing an AT-SPI interface
  @type interface: class
  @return: Function querying to the given interface
  @rtype: function
  '''
  def _inner(self):
    '''
    Queries an object for another interface.
  
    @return: An object with the desired interface
    @rtype: object
    @raise NotImplementedError: When the desired interface is not supported    
    '''
    iid = utils.getInterfaceIID(interface)
    try:
      i = self._icache[iid]
    except KeyError:
      # interface not cached
      caching = True
    except AttributeError:
      # determine if we're caching
      caching = _CACHE_LEVEL is not None
      if caching:
        # initialize the cache
        self._icache = {}
    else:
      # check if our cached result was an interface, or an indicator that the
      # interface is not supported
      if i is None:
        raise NotImplementedError
      else:
        return i

    try:
      # do the query remotely
      i = self.queryInterface(iid)
      if i is not None:
        i = i._narrow(interface)
    except Exception, e:
      raise LookupError(e)      
    if i is None:
      # cache that the interface is not supported
      if caching:
        self._icache[iid] = None
      raise NotImplementedError
    
    if caching:
      # cache the narrow'ed result, but only if we're caching for this object
      self._icache[iid] = i
    return i
  
  return _inner

def _makeExceptionHandler(func):
  '''
  Builds a function calling the one it wraps in try/except statements catching
  CORBA exceptions.
  
  @return: Function calling the method being wrapped
  @rtype: function
  '''
  def _inner(self, *args, **kwargs):
    try:
      # try calling the original func
      return func(self, *args, **kwargs)
    except ORBit.CORBA.NO_IMPLEMENT, e:
      # raise Python exception
      raise NotImplementedError(e)
    except ORBit.CORBA.Exception, e:
      # raise Python exception
      raise LookupError(e)
  return _inner

def _mixInterfaces(cls, interfaces):
  '''
  Add methods for querying to interfaces other than the base accessible to
  the given class.
  
  @param cls: Class to mix interface methods into
  @type cls: class
  @param interfaces: Classes representing AT-SPI interfaces
  @type interfaces: list of class
  '''
  # create functions in this module for all interfaces listed in constants
  for interface in interfaces:
    # build name of converter from the name of the interface
    name = 'query%s' % utils.getInterfaceName(interface)
    # build a function that queries to the given interface
    func = _makeQuery(interface)
    # build a new method that is a clone of the original function
    method = new.function(func.func_code, func.func_globals, name, 
                          func.func_defaults, func.func_closure)
    # add the method to the given class
    setattr(cls, name, method)

def _mixExceptions(cls):
  '''
  Wraps all methods and properties in a class with handlers for CORBA 
  exceptions.
  
  @param cls: Class to mix interface methods into
  @type cls: class
  '''
  # get a method type as a reference from a known method
  method_type = Accessibility.Accessible.getRole.__class__
  # loop over all names in the new class
  for name in cls.__dict__.keys():
    obj = cls.__dict__[name]
    # check if we're on a protected or private method
    if name.startswith('_'):
      continue
    # check if we're on a method
    elif isinstance(obj, method_type):
      # wrap the function in an exception handler
      method = _makeExceptionHandler(obj)
      # add the wrapped function to the class
      setattr(cls, name, method)
    # check if we're on a property
    elif isinstance(obj, property):
      # wrap the getters and setters
      if obj.fget:
        func = getattr(cls, obj.fget.__name__)
        getter = _makeExceptionHandler(func)
      else:
        getter = None
      if obj.fset:
        func = getattr(cls, obj.fset.__name__)
        setter = _makeExceptionHandler(func)
      else:
        setter = None
      setattr(cls, name, property(getter, setter))

def _mixClass(cls, new_cls, ignore=[]):
  '''
  Adds the methods in new_cls to cls. After mixing, all instances of cls will
  have the new methods. If there is a method name clash, the method already in
  cls will be prefixed with '_mix_' before the new method of the same name is 
  mixed in.
  
  @note: _ is not the prefix because if you wind up with __ in front of a 
  variable, it becomes private and mangled when an instance is created. 
  Difficult to invoke from the mixin class.

  @param cls: Existing class to mix features into
  @type cls: class
  @param new_cls: Class containing features to add
  @type new_cls: class
  @param ignore: Ignore these methods from the mixin
  @type ignore: iterable
  '''
  # loop over all names in the new class
  for name, func in new_cls.__dict__.items():
    if name in ignore:
      continue
    if isinstance(func, types.FunctionType):
      # build a new function that is a clone of the one from new_cls
      method = new.function(func.func_code, func.func_globals, name, 
                            func.func_defaults, func.func_closure)
      try:
        # check if a method of the same name already exists in the target
        old_method = getattr(cls, name)
      except AttributeError:
        pass
      else:
        # rename the old method so we can still call it if need be
        setattr(cls, '_mix_'+name, old_method)
      # add the clone to cls
      setattr(cls, name, method)
    elif isinstance(func, staticmethod):
      try:
        # check if a method of the same name already exists in the target
        old_method = getattr(cls, name)
      except AttributeError:
        pass
      else:
        # rename the old method so we can still call it if need be
        setattr(cls, '_mix_'+name, old_method)
      setattr(cls, name, func)
    elif isinstance(func, property):
      try:
        # check if a method of the same name already exists in the target
        old_prop = getattr(cls, name)
      except AttributeError:
        pass
      else:
        # IMPORTANT: We save the old property before overwriting it, even 
        # though we never end up calling the old prop from our mixin class.
        # If we don't save the old one, we seem to introduce a Python ref count
        # problem where the property get/set methods disappear before we can
        # use them at a later time. This is a minor waste of memory because
        # a property is a class object and we only overwrite a few of them.
        setattr(cls, '_mix_'+name, old_prop)
      setattr(cls, name, func)

class _AccessibleMixin(object):
  '''
  Defines methods to be added to the Accessibility.Accessible class. The
  features defined here will be added to the Accessible class at run time so
  that all instances of Accessible have them (i.e. there is no need to
  explicitly wrap an Accessible in this class or derive a new class from it.)
  
  @cvar SLOTTED_CLASSES: Mapping from raw Accessibility class to a new class
    having the slots defined by L{SLOTS}
  @type SLOTTED_CLASSES: dictionary
  @cvar SLOTS: All slots to create
  @type SLOTS: tuple
  '''
  SLOTTED_CLASSES = {}
  SLOTS = ('_icache', '_property_cache', '_user_data')
  
  def __new__(cls):
    '''
    Creates a new class mimicking the one requested, but with extra named 
    defined in __slots__. The _cache attribute is used internally for interface
    caching. The user_data field may be populated with whatever data structure
    a client wishes to use. Neither is set to a default value by default.
    
    Note that we can't simply mix __slots__ into this class because __slots__
    has an effect only at class creation time. 
    
    We also do not completely obliterate __slots__ to allow __dict__ to be
    instantiated as normal as reducing the initialization and memory overhead
    of the millions of accessible objects that are created is a good thing for
    many clients.
    
    @param cls: Accessibility object class
    @type cls: class
    @return: Instance of the new class
    @rtype: object
    '''
    try:
      # check if we've already created a new version of the class
      new_cls = _AccessibleMixin.SLOTTED_CLASSES[cls]
    except KeyError:
      # create the new class if not
      new_cls = type(cls.__name__, (cls,), 
                     {'__module__' : cls.__module__, 
                      '__slots__' : _AccessibleMixin.SLOTS})
      _AccessibleMixin.SLOTTED_CLASSES[cls] = new_cls
    obj = cls._mix___new__(new_cls)
    return obj
  
  def __del__(self):
    '''    
    Decrements the reference count on the accessible object when there are no
    Python references to this object. This provides automatic reference
    counting for AT-SPI objects. Also removes this object from the cache if
    we're caching properties. 
    '''
    try:
      self.unref()
    except Exception:
      pass
    
  def __iter__(self):
    '''
    Iterator that yields one accessible child per iteration. If an exception is
    encountered, None is yielded instead.
    
    @return: A child accessible
    @rtype: Accessibility.Accessible
    '''
    for i in xrange(self.childCount):
      try:
        yield self.getChildAtIndex(i)
      except LookupError:
        yield None
    
  def __str__(self):
    '''
    Gets a human readable representation of the accessible.
    
    @return: Role and name information for the accessible
    @rtype: string
    '''
    try:
      return '[%s | %s]' % (self.getRoleName(), self.name)
    except Exception:
      return '[DEAD]'
    
  def __nonzero__(self):
    '''
    @return: True, always
    @rtype: boolean
    '''
    return True
    
  def __getitem__(self, index):
    '''
    Thin wrapper around getChildAtIndex.
    
    @param index: Index of desired child
    @type index: integer
    @return: Accessible child
    @rtype: Accessibility.Accessible
    '''
    n = self.childCount
    if index >= n:
      raise IndexError
    elif index < -n:
      raise IndexError
    elif index < 0:
      index += n
    return self.getChildAtIndex(index)
  
  def __len__(self):
    '''
    Thin wrapper around childCount.
    
    @return: Number of child accessibles
    @rtype: integer
    '''
    return self.childCount
  
  def _get_user_data(self):
    '''
    Get user_data from global dictionay fo this accessible.

    @return: Any data the user assigned, or None.
    @rtype: object
    '''
    global _ACCESSIBLE_USER_DATA
    h = hash(self)
    
    try:
      ud = self._user_data
    except AttributeError:
      try:
        ud = _ACCESSIBLE_USER_DATA[h]
      except KeyError:
        # no cached info for this object yet
        ud = _UserData()
        _ACCESSIBLE_USER_DATA[h] = ud

    self._user_data = ud
    return ud.value

  def _set_user_data(self, value):
    '''
    Set arbitrary data to user_data.

    @param value: Value to set in user_data
    @type value: object
    '''
    global _ACCESSIBLE_USER_DATA
    h = hash(self)
    
    try:
      ud = self._user_data
    except AttributeError:
      try:
        ud = _ACCESSIBLE_USER_DATA[h]
      except KeyError:
        # no cached info for this object yet
        ud = _UserData()
        _ACCESSIBLE_USER_DATA[h] = ud

    self._user_data = ud
    ud.value = value

  user_data = property(_get_user_data, _set_user_data)

  def _get_name(self):
    '''
    Gets the name of the accessible from the cache if it is available, 
    otherwise, fetches it remotely.
    
    @return: Name of the accessible
    @rtype: string
    '''
    return _getAndCache(self, 'name', self._get_name)

  name = property(_get_name, Accessibility.Accessible._set_name)

  def _get_parent(self):
    '''
    Gets the parent of the accessible from the cache if it is available, 
    otherwise, fetches it remotely.
    
    @return: Parent of the accessible
    @rtype: Accessibility.Accessible
    '''
    return _getAndCache(self, 'parent', self._get_parent)

  parent = property(_get_parent)
  
  def getRoleName(self):
    '''
    Gets the unlocalized role name of the accessible from the cache if it is 
    available, otherwise, fetches it remotely.
    
    @return: Role name of the accessible
    @rtype: string
    '''
    return _getAndCache(self, 'rolename', self._mix_getRoleName)

  def getRole(self):
    '''
    Gets the role of the accessible from the cache if it is 
    available, otherwise, fetches it remotely.
    
    @return: Role of the accessible
    @rtype: Accessibility.Role
    '''
    return _getAndCache(self, 'role', self._mix_getRole)

  def _get_description(self):
    '''    
    Gets the description of the accessible from the cache if it is available,
    otherwise, fetches it remotely.
    
    @return: Description of the accessible
    @rtype: string
    '''
    return _getAndCache(self, 'description', self._get_description)
    
  description = property(_get_description, 
                         Accessibility.Accessible._set_description)
  
  def getIndexInParent(self):
    '''
    Gets the index of this accessible in its parent. Uses the implementation of
    this method provided by the Accessibility.Accessible object, but checks the
    bound of the value to ensure it is not outside the range of childCount 
    reported by this accessible's parent.
    
    @return: Index of this accessible in its parent
    @rtype: integer
    '''
    i = self._mix_getIndexInParent()
    try:
      # correct for out-of-bounds index reporting
      return min(self.parent.childCount-1, i)
    except AttributeError:
      # return sentinel if there is no parent
      return -1

  def getApplication(self):
    '''
    Gets the most-parent accessible (the application) of this
    accessible. Tries using the getApplication method introduced in
    AT-SPI 1.7.0 first before resorting to traversing parent links.
    
    @warning: Cycles involving more than the previously traversed accessible 
      are not detected by this code.
    @return: Application object
    @rtype: Accessibility.Application
    '''
    try:
      app = self._mix_getApplication()
    except AttributeError:
      app = None

    # Some toolkits (e.g., Java) do not support getApplication yet and
    # will return None as a result.
    #
    if app:
      return app

    # If we didn't find anything, traverse up the tree, making sure to
    # attempt to turn the thing we found into an Application object.
    #
    curr = self
    try:
      while curr.parent is not None and (not curr.parent == curr):
        curr = curr.parent
      curr.ref()
      return curr._narrow(Accessibility.Application)
    except:
      return None

class _RelationMixin(object):
  '''
  Defines methods to be added to the Relation class. At this time it only
  overrides L{_RelationMixin.getTarget} which by the IDL's standard is
  supposed to return CORBA.Objects but we expect LAccessibility.Accessible
  objects (see http://bugzilla.gnome.org/show_bug.cgi?id=435833). 
  This seems to be a problem especially with the Java implementation of CORBA.
  '''
  def getTarget(self, index):
    '''
    Overrides the regular getTarget to return Accessibility.Accessible
    objects.

    @return: The 'nth' target of this Relation.
    @rtype: Accessibility.Accessible
    '''
    target = self._mix_getTarget(index)
    if not isinstance(target, Accessibility.Accessible):
      target = target._narrow(Accessibility.Accessible)
    target.ref()
    return target

class _UnrefMixin(object):
  '''
  This mixin addresses the issue we have with unreferencing non-primitives.
  '''
  def __del__(self):
    '''
    Unrefence the instance when Python GCs it. Why do we need this twice?
    '''
    try:
      self.unref()
    except Exception:
      pass

# 1. mix the exception handlers into all queryable interfaces
map(_mixExceptions, constants.ALL_INTERFACES)
# 2. mix the exception handlers into other Accessibility objects
map(_mixExceptions, [Accessibility.StateSet])
# 3. mix the new functions
_mixClass(Accessibility.Accessible, _AccessibleMixin,
          ['_get_name', '_get_description', '_get_parent'])
# 4. mix queryInterface convenience methods
_mixInterfaces(Accessibility.Accessible, constants.ALL_INTERFACES)
# 5. mix Relation class
_mixClass(Accessibility.Relation, _RelationMixin)
# 6. mix in neccessary unrefs
map(lambda cls: _mixClass(cls, _UnrefMixin), 
    (Accessibility.StateSet,Accessibility.Relation))
