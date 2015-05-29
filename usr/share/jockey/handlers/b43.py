# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: GPL v2 or later

import re, os.path, logging, subprocess
from glob import glob

from jockey.oslib import OSLib
from jockey.handlers import KernelModuleHandler

class B43Handler(KernelModuleHandler):
    '''Handler for Broadcom Wifi chipsets which use the b43 module and
    b43-fwcutter.'''

    def __init__(self, ui):
        KernelModuleHandler.__init__(self, ui, 'b43')
        self.package = 'b43-fwcutter'

    def enabled(self):
        '''Return if the handler is enabled.
        
        'Enabled' means that the user agreed to use this driver if it is
        applicable.
        '''
        return KernelModuleHandler.enabled(self) and \
            len(glob('/lib/firmware/b43/*.fw')) > 0

    def used(self):
        '''Return if the handler is currently in use.'''

        return KernelModuleHandler.used(self) and \
            len(glob('/lib/firmware/b43/*.fw')) > 0

    def id(self):
        '''Return an unique identifier of the handler.'''

        i = 'firmware:' + self.module
        if self.driver_vendor:
            i += ':' + self.driver_vendor.replace(' ', '_')
        return i

    def enable(self):
        '''Remove blacklist produced by BroadcomWLHandler.'''

        bl_file = '/etc/modprobe.d/blacklist-bcm43.conf'
        if os.path.exists(bl_file):
            os.unlink(bl_file)
            OSLib.inst._load_module_blacklist()
            subprocess.call(['/usr/sbin/update-initramfs', '-u'])

        KernelModuleHandler.enable(self)
        if os.path.exists('/usr/share/b43-fwcutter/install_bcm43xx_firmware.sh'):
            subprocess.call(['/usr/share/b43-fwcutter/install_bcm43xx_firmware.sh'])

class B43LegacyHandler(B43Handler):
    '''Handler for Broadcom Wifi chipsets which use the b43legacy module and
    b43-fwcutter.'''

    def __init__(self, ui):
        KernelModuleHandler.__init__(self, ui, 'b43legacy')
        self.package = 'b43-fwcutter'
