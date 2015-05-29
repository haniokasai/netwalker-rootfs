# -*- coding: utf-8 -*-
## Copyright (C) 2001-2008 Alberto Milone <albertomilone@alice.it>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import gtk, gobject, sys, dbus, logging
import ScreenResolution
from ScreenResolution.policykit import PolicyKitAuthentication

POLICY_KIT_ACTION = 'com.ubuntu.screenresolution.mechanism.dontzap'
SERVICE_NAME   = 'com.ubuntu.ScreenResolution.Mechanism'
OBJECT_PATH    = '/'
INTERFACE_NAME = 'com.ubuntu.ScreenResolution.Mechanism'
usage = 'python policy-dontzap.py --enable'

import os
import sys


def get_dontzap_service(widget=None):
    '''
    returns a dbus interface to the screenresolution mechanism
    '''
    policy_auth = PolicyKitAuthentication()    

    granted = policy_auth.obtain_authorization(POLICY_KIT_ACTION, widget)
    logging.debug("granted = %s" % granted)

    if not granted:
        return None
    
    service_object = dbus.SystemBus().get_object(SERVICE_NAME, OBJECT_PATH)
    service = dbus.Interface(service_object, INTERFACE_NAME)

    return service

def main(enable):
    if enable not in ['--enable', '--disable']:
        logging.error("called with wrong arguments = %s" % str(enable))
        return False
    
    conf = get_dontzap_service()
    if not conf:
        # dbus_cant_connect
        logging.error("cannot connect to dbus service")
        sys.exit(1)
    logging.debug("setting dontzap to %s" % enable)
    exit_code = conf.setDontZap(enable)
    logging.debug("exit status: %d" % exit_code)

    # All went well if exit_code == 0
    return exit_code


if __name__ == "__main__":
    if len(sys.argv) > 1:
        operation_status = main(sys.argv[1])
    else:
        operation_status = 1
    
    sys.exit(operation_status)

