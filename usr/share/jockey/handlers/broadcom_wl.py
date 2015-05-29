# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: GPL v2 or later

import re, os.path, logging, subprocess
from glob import glob

from jockey.oslib import OSLib
from jockey.handlers import KernelModuleHandler

# dummy stub for xgettext
def _(x): return x

class BroadcomWLHandler(KernelModuleHandler):
    '''Handler for Broadcom Wifi chipsets which use the wl module.'''

    def __init__(self, ui):
        self.bl_file = os.path.join(os.path.dirname(
            OSLib.inst.module_blacklist_file), 'blacklist-bcm43.conf')
        self._free = False
        KernelModuleHandler.__init__(self, ui, 'wl',
            name=_('Broadcom STA wireless driver'))

    def enabled(self):
        km =  KernelModuleHandler.enabled(self)
        bcm = OSLib.inst.module_blacklisted('bcm43xx')
        b43 = OSLib.inst.module_blacklisted('b43')
        b43_legacy = OSLib.inst.module_blacklisted('b43legacy')
        b43_loaded = KernelModuleHandler.module_loaded('b43xx') or \
                     KernelModuleHandler.module_loaded('b43')   or \
                     KernelModuleHandler.module_loaded('b43legacy')
        logging.debug('BroadcomWLHandler enabled(): kmod %s, bcm43xx: %s, b43: %s, b43legacy: %s' % (
            km and 'enabled' or 'disabled',
            bcm and 'blacklisted' or 'enabled',
            b43 and 'blacklisted' or 'enabled',
            b43_legacy and 'blacklisted' or 'enabled'))

        return (km and not b43_loaded) or (km and bcm and b43 and b43_legacy)

    def used(self):
        '''Return if the handler is currently in use.'''

        return KernelModuleHandler.used(self) and self.enabled() and \
            not (KernelModuleHandler.module_loaded('b43') or
            KernelModuleHandler.module_loaded('b43legacy') or
            KernelModuleHandler.module_loaded('bcm43xx'))

    def enable(self):
        '''Disable b43 drivers, so that wl can become active.
        
        This also adds a workaround for loading wl first if b44 is used.
        '''
        if not os.path.exists(self.bl_file):
            f = open(self.bl_file, 'w')
            f.write('''blacklist bcm43xx
blacklist b43
blacklist b43legacy
blacklist ssb
''')
            if KernelModuleHandler.module_loaded('b44'):
                f.write('''# load wl before b44 so that both work
blacklist b44
install wl modprobe -r b43 b44 b43legacy ssb; modprobe --ignore-install wl $CMDLINE_OPTS; modprobe --ignore-install b44
''')

            f.close()
            OSLib.inst._load_module_blacklist()
            subprocess.call(['/usr/sbin/update-initramfs', '-u'])

        KernelModuleHandler.enable(self)

    def disable(self):
        '''Unblacklist b43 drivers again, so that they trump wl.'''

        if os.path.exists(self.bl_file):
            os.unlink(self.bl_file)
            OSLib.inst._load_module_blacklist()
            subprocess.call(['/usr/sbin/update-initramfs', '-u'])

        KernelModuleHandler.disable(self)
