# -*- coding: utf-8 -*-
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
# Taken from:
# https://code.fluendo.com/remotecontrol/trac/browser/trunk/
#         gnome_lirc_properties/policykit.py?rev=197
#
# modified by Harald Hoyer <harald@redhat.com>
'''
Helper class to do authentication via PolicyKit
'''

import dbus
import os
import logging

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
        '''
        Retreive the D-Bus interface of the PolicyKit 
        authentication agent.
        '''

        if self.__pa:
            return self.__pa
        # retreiving the interface raises DBusException on error:
        self.__pa = dbus.SessionBus().get_object(
            'org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        return self.__pa

    auth_agent = property(__get_auth_agent)
    policy_kit = property(__get_policy_kit)
