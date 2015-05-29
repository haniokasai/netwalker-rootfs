# -*- coding: utf-8 -*-
# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: GPL v2 or later

import XKit.xorgparser
from jockey.xorg_driver import XorgDriverHandler

# dummy stub for xgettext
def _(x): return x

class FglrxDriver(XorgDriverHandler):
    def __init__(self, backend):
        self._free = False
        XorgDriverHandler.__init__(self, backend, 'fglrx', 'xorg-driver-fglrx',
            'fglrx', 'ati', add_modules=['glx'], disable_modules=[],
            name=_('ATI/AMD proprietary FGLRX graphics driver'),
            description=_('3D-accelerated proprietary graphics driver for '
                'ATI cards.'),
            rationale=_('This driver is required to fully utilise the 3D '
                'potential of some ATI graphics cards, as well as provide '
                '2D acceleration of newer cards.'))

    def enable_config_hook(self):
        # TODO: this method should look for the right Screen section(s) and
        # if none can be found, use section 0. use get_devices_from_serverlayout()

        # X.org does not work otherwise
        if len(self.xorg_conf.globaldict['Screen']) == 0:
            self.xorg_conf.makeSection('Screen', identifier='Default Screen')
        
        self.xorg_conf.addOption('Screen', 'DefaultDepth', '24', position=0, prefix='')
        
        # make sure that RGB path is not in the xorg.conf otherwise xorg will crash
        it = 0
        for section in self.xorg_conf.globaldict['Files']:
            try:
                self.xorg_conf.removeOption('Files', 'RgbPath', position=it)
            except (XKit.xorgparser.OptionException):
                pass
            it += 1
        
        # remove any Disable "dri2" otherwise amdcccle will crash
        module_sections = self.xorg_conf.globaldict['Module']
        have_modules = len(module_sections) > 0
        
        if have_modules:
            for section in module_sections:
                self.xorg_conf.removeOption('Module', 'Disable', value='dri2', position=section)

    def disable(self):
        # make sure that fglrx-kernel-source is removed too
        XorgDriverHandler.disable(self)
        kernel_source = 'fglrx-kernel-source'
        self.backend.remove_package(kernel_source)
        return False

    def enables_composite(self):
        '''Return whether this driver supports the composite extension.'''

        if not self.xorg_conf:
            return False

        # the radeon X.org driver supports composite nowadays, so don't force
        # installation of fglrx upon those users. Treat absent driver
        # configuration as radeon, since that's what X.org should autodetect.
        # Only suggest fglrx if people use something else, like vesa.
        try:
            if self.xorg_conf.getDriver('Device', 0) in ['fglrx', 'ati', 'radeon', None]:
                return False
        except (XKit.xorgparser.OptionException, XKit.xorgparser.SectionException), error:
            return False # unconfigured driver -> defaults to ati

        return True

