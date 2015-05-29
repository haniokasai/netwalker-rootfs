# -*- coding: utf-8 -*-
#       ui.py
#       
#       Copyright 2008 Alberto Milone <albertomilone@alice.it>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gettext

class AbstractUI:
    '''Abstract user interface.

    This encapsulates the entire program logic and all strings, but does not
    implement any concrete user interface.
    '''
    def __init__(self):
        '''
        Initialize system.
        '''
        self.gettext_domain = 'screen-resolution-extra'

        gettext.textdomain(self.gettext_domain)

        self.init_strings()
    
    def _(self, str, convert_keybindings=False):
        '''Keyboard accelerator aware gettext() wrapper.
        
        This optionally converts keyboard accelerators to the appropriate
        format for the frontend.

        All strings in the source code should use the '_' prefix for key
        accelerators (like in GTK). For inserting a real '_', use '__'.
        '''
        # KDE compatible conversion
        result = unicode(gettext.gettext(str), 'UTF-8')

        if convert_keybindings:
            result = self.convert_keybindings(result)

        return result
    
    def init_strings(self):
        '''Initialize all static strings which are used in UI implementations.'''

        self.string_permission_text = self._('Monitor Resolution Settings has detected that the virtual resolution \
must be set in your configuration file in order to apply your settings.\
\n\nWould you like Screen Resolution to set the virtual resolution for you? (Recommended)')
        
        self.string_dbus_cant_connect = self._('Could not connect to Monitor Resolution Settings DBUS service.')
        
        self.string_operation_complete = self._('Please log out and log back in again.  You will then be able to use Monitor Resolution Settings to setup your monitors')
        
        self.string_cant_apply_settings = self._('Monitor Resolution Settings can\'t apply your settings.')
        
        self.string_title = self._('Monitor Resolution Settings')
        
