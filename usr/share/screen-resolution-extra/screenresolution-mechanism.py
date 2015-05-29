#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Fluendo Embedded S.L. (www.fluendo.com)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# taken from:
# https://code.fluendo.com/remotecontrol/trac/browser/trunk/
#         gnome_lirc_properties/backend.py?rev=217
# 
# modified by Harald Hoyer <harald@redhat.com>
#
# modified by Alberto Milone (tseliot) <albertomilone@alice.it>

'''
Processes, which want to access this service have to acquire first
the action id "com.ubuntu.xkit.mechanism.configure" from PolicyKit
'''

import dbus, dbus.service, gobject, logging
import os, os.path
import sys
from XKit import xutils, xorgparser
import time
import shutil
import subprocess

POLICY_KIT_ACTION     = 'com.ubuntu.screenresolution.mechanism.configure'
class PolicyKitAuthentication(object):
    '''
    Helper class to do authentication via PolicyKit
    '''
    def __init__(self):
        super(PolicyKitAuthentication, self).__init__()
        self.__pk = None
        self.__pa = None

    def is_authorized(self, action_id, pid=None):
        '''
        Ask PolicyKit whether we are already authorized.
        '''

        # Check whether the process is authorized:
        if pid == None:
            pid = os.getpid()
            
        pid = dbus.UInt32(pid)
        authorized = self.policy_kit.IsProcessAuthorized(action_id, pid, False)
        logging.debug('%s: authorized=%r', action_id, authorized)

        return ('yes' == authorized)

    def obtain_authorization(self, action_id, widget=None):
        '''
        Try to obtain authoriztation for the specified action.
        '''
        if self.is_authorized(action_id):
            return True

        xid = (widget and widget.get_toplevel().window.xid or 0)
        xid, pid = dbus.UInt32(xid), dbus.UInt32(os.getpid())

        granted = self.auth_agent.ObtainAuthorization(action_id, xid, pid)
        logging.debug('%s: granted=%r', action_id, granted)

        return bool(granted)

    def __get_policy_kit(self):
        '''Retreive the D-Bus interface of PolicyKit.'''

        if self.__pk:
            return self.__pk

        # retreiving the interface raises DBusException on error:
        service = dbus.SystemBus().get_object('org.freedesktop.PolicyKit', '/')
        self.__pk = dbus.Interface(service, 'org.freedesktop.PolicyKit')
        return self.__pk        

    def __get_auth_agent(self):
        "Retreive the D-Bus interface of the PolicyKit authentication agent."

        if self.__pa:
            return self.__pa
        # retreiving the interface raises DBusException on error:
        self.__pa = dbus.SessionBus().get_object(
            'org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        return self.__pa

    auth_agent = property(__get_auth_agent)
    policy_kit = property(__get_policy_kit)


# Modern flavors of dbus bindings have that symbol in dbus.lowlevel,
# for old flavours the internal _dbus_bindings module must be used.

try:
    # pylint: disable-msg=E0611
    from dbus.lowlevel import HANDLER_RESULT_NOT_YET_HANDLED

except ImportError:
    from _dbus_bindings import HANDLER_RESULT_NOT_YET_HANDLED

class AccessDeniedException(dbus.DBusException):
    '''This exception is raised when some operation is not permitted.'''

    _dbus_error_name = 'com.ubuntu.screenresolution.Mechanism.AccessDeniedException'

class UnsupportedException(dbus.DBusException):
    '''This exception is raised when some operation is not supported.'''

    _dbus_error_name = 'com.ubuntu.screenresolution.Mechanism.UnsupportedException'

class UsageError(dbus.DBusException):
    '''This exception is raised when some operation was not used properly.'''

    _dbus_error_name = 'com.ubuntu.screenresolution.Mechanism.UsageError'

class PolicyKitService(dbus.service.Object):
    '''A D-BUS service that uses PolicyKit for authorization.'''

    def _check_permission(self, sender, action=POLICY_KIT_ACTION):
        '''
        Verifies if the specified action is permitted, and raises
        an AccessDeniedException if not.

        The caller should use ObtainAuthorization() to get permission.

        Needs:
        /usr/bin/polkit-auth --user root --grant org.freedesktop.policykit.read

        '''
        if not sender:
            raise AccessDeniedException('Session not authorized by PolicyKit')

        try:
            policy_auth = PolicyKitAuthentication()
            bus = dbus.SystemBus()
            dbus_object = bus.get_object('org.freedesktop.DBus', '/')
            dbus_object = dbus.Interface(dbus_object, 'org.freedesktop.DBus')

            kit = bus.get_object('org.freedesktop.PolicyKit', '/')
            kit = dbus.Interface(kit, 'org.freedesktop.PolicyKit')
            pid = dbus.UInt32(dbus_object.GetConnectionUnixProcessID(sender))

            granted = policy_auth.is_authorized(action, pid)
            logging.info('process authorization: %r', granted)
            print >> sys.stderr,  'process authorization: %r' % granted

            if not granted:
                raise AccessDeniedException('Process not authorized'
                                            ' by PolicyKit')

            granted = policy_auth.policy_kit.IsSystemBusNameAuthorized(action,
                                                                       sender,
                                                                       False)
            logging.info('authorization of system bus name: %r', granted)

            if 'yes' != granted:
                raise AccessDeniedException('Session not '
                                            'authorized by PolicyKit')

        except AccessDeniedException:
            logging.info("AccessDeniedException")
            raise

        except dbus.DBusException, ex:
            logging.info("AccessDeniedException %r",  ex)
            raise AccessDeniedException(ex.message)

class BackendService(PolicyKitService):
    '''A D-Bus service that PolicyKit controls access to.'''

    # pylint: disable-msg=C0103,E0602

    INTERFACE_NAME = 'com.ubuntu.ScreenResolution.Mechanism'
    SERVICE_NAME   = 'com.ubuntu.ScreenResolution.Mechanism'
    IDLE_TIMEOUT   =  30

    def __init__(self, connection=None, path='/'):        
        if connection is None:
            connection = get_service_bus()

        super(BackendService, self).__init__(connection, path)

        self.__name = dbus.service.BusName(self.SERVICE_NAME, connection)
        self.__loop = gobject.MainLoop()
        self.__timeout = 0
        connection.add_message_filter(self.__message_filter)

    def __message_filter(self, connection, message):
        '''
        D-BUS message filter that keeps the service alive,
        as long as it receives message.
        '''

        if self.__timeout:
            self.__start_idle_timeout()

        return HANDLER_RESULT_NOT_YET_HANDLED

    def __start_idle_timeout(self):
        '''Restarts the timeout for terminating the service when idle.'''

        if self.__timeout:
            gobject.source_remove(self.__timeout)

        self.__timeout = gobject.timeout_add(self.IDLE_TIMEOUT * 1000,
                                             self.__timeout_cb)

    def __timeout_cb(self):
        '''Timeout callback that terminates the service when idle.'''

        # Keep service alive, as long as additional objects are exported:
        if self.connection.list_exported_child_objects('/'):
            return True

        print 'Terminating %s due to inactivity.' % self.SERVICE_NAME
        self.__loop.quit()

        return False

    def run(self):
        '''Creates a GLib main loop for keeping the service alive.'''

        print 'Running %s.' % self.SERVICE_NAME
        print ('Terminating it after %d seconds of inactivity.' 
               % self.IDLE_TIMEOUT)

        self.__start_idle_timeout()
        self.__loop.run()


    # pylint: disable-msg=R0913
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='as', out_signature='b',
                         sender_keyword='sender')   
    def setVirtual(self, virtres, sender=None):
        '''
        Replace the first line of this example with a source and a destination file
        '''
        virtual = ' '.join(virtres)
        
        source = '/etc/X11/xorg.conf'
        destination = '/etc/X11/xorg.conf'
        
        if os.path.exists(source):
            #make a backup of the xorg.conf
            backup = source + "." + time.strftime("%Y%m%d%H%M%S")
            shutil.copyfile(source, backup)
        
        try:
            a = xutils.XUtils(source)
        except(IOError, xorgparser.ParseException):#if xorg.conf is missing or broken
            a = xutils.XUtils()#start from scratch
        
        empty = True
        for section in a.globaldict:
            if len(a.globaldict[section]) > 0:
                empty = False
                break

        if empty:
            a.makeSection('Device', 'Configured Video Device')
            a.makeSection('Screen', identifier='Configured Screen Device')
            a.addReference('Screen', 'Device', 'Configured Video Device', position=0)
            a.makeSubSection('Screen', 'Display', position=0)
            a.addSubOption('Screen', 'Display', 'Virtual', value=virtual, position=0)
        
        else:#if xorg.conf exists and is not empty
            devicelen = len(a.globaldict['Device'])
            screenlen = len(a.globaldict['Screen'])
            
            if screenlen == 0:
                screen = a.makeSection('Screen', identifier='Configured Screen Device')
                if devicelen == 0:
                    device = a.makeSection('Device', 'Configured Video Device')
                else:
                    device = 0
                a.addReference('Screen', 'Device', 'Configured Video Device', position=device)
                
                a.makeSubSection('Screen', 'Display', position=0)
                a.addSubOption('Screen', 'Display', 'Virtual', value=virtual, position=0)
                
            else:#if at least 1 Screen section exists
                '''
                Set the virtual section in all the Screen sections
                '''
                for screen in a.globaldict['Screen']:
                    a.makeSubSection('Screen', 'Display', position=screen)
                    a.addSubOption('Screen', 'Display', 'Virtual', value=virtual, position=screen)

        '''
        Write the changes to the destination file
        '''
        a.writeFile(destination)
        return True
    
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='i',
                         sender_keyword='sender')   
    def setDontZap(self, enable, sender=None):
        '''Try to set the DontZap option in the xorg.conf
           and return the exit code of dontzap'''
        dontzap_file = '/usr/bin/dontzap'
        if not os.path.isfile(dontzap_file):
            logging.error('/usr/bin/dontzap does not exist')
            return 1
        
        if enable in ['--enable', '--disable']:
            logging.debug('calling dontzap with %s' % enable)
            retcode = subprocess.call([dontzap_file, enable])
            return retcode
        else:
            logging.error('called with wrong arguments = %s' % enable)
            return 1
    
    
def get_service_bus():
    '''Retrieves a reference to the D-BUS system bus.'''

    return dbus.SystemBus()

def get_service(bus=None):
    '''Retrieves a reference to the D-BUS driven configuration service.'''

    if not bus:
        bus = get_service_bus()

    service = bus.get_object(BackendService.SERVICE_NAME, '/')
    service = dbus.Interface(service, BackendService.INTERFACE_NAME)

    return service

if __name__ == '__main__':
    # Support full tracing when --debug switch is passed:
    import sys
    from sys import argv

    # Integrate DBus with GLib main loops.

    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)

    # Run the service.

    if '--debug' in argv or '-d' in argv:
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger().setLevel(logging.NOTSET)
        
    BackendService().run()

