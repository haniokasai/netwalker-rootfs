# (c) 2008 Canonical Ltd.
# Author: Martin Pitt <martin.pitt@ubuntu.com>
# License: GPL v2 or later

import logging

from jockey.handlers import KernelModuleHandler
from jockey.xorg_driver import XorgDriverHandler
from jockey.oslib import OSLib
import XKit
from NvidiaDetector.nvidiadetector import NvidiaDetection

# dummy stub for xgettext
def _(x): return x

class NvidiaDriver(XorgDriverHandler):
    def __init__(self, backend):
        self._free = False
        # use "None" as driver_package, since we have several;
        # LocalKernelModulesDriverDB overwrites it later with the correct
        # package from the modalias lists
        XorgDriverHandler.__init__(self, backend, 'nvidia', None,
            'nvidia', 'nv', {'NoLogo': 'True'},
            add_modules=['glx'], disable_modules=[],
            remove_modules=['dri', 'GLcore'],
            name=_('NVIDIA accelerated graphics driver'),
            description=_('3D-accelerated proprietary graphics driver for '
                'NVIDIA cards.'),
            rationale=_('This driver is required to fully utilise '
                'the 3D potential of NVIDIA graphics cards, as well as provide '
                '2D acceleration of newer cards.\n\n'
                'If you wish to enable desktop effects, this driver is '
                'required.\n\n'
                'If this driver is not enabled, you will not be able to '
                'enable desktop effects and will not be able to run software '
                'that requires 3D acceleration, such as some games.'))

        self._recommended = None
        self._do_rebind = False
        
    def id(self):
        '''Return an unique identifier of the handler.'''

        if self.package:
            self.version = self.package.split('-')[-1]
            i = 'xorg:' + self.module + '-' + self.version
        else:
            i = 'xorg:' + self.module
        if self.driver_vendor:
            i += ':' + self.driver_vendor.replace(' ', '_')
        return i

    def available(self):
        if self.package:
            self.version = self.package.split('-')[-1]
            if int(self.version) < 96:
                logging.debug('NVIDIA legacy driver not currently supported')
                return False
        return XorgDriverHandler.available(self)

    def enable_config_hook(self):
        # set DefaultDepth to 24; X.org does not work otherwise
        if len(self.xorg_conf.globaldict['Screen']) == 0:
            screen = self.xorg_conf.makeSection('Screen', identifier='Default Screen')
        
        self.xorg_conf.addOption('Screen', 'DefaultDepth', '24', position=0, prefix='')

        # version 96 needs AddARGBGLXVisuals
        if self.version == '96':
            self.xorg_conf.addOption('Screen', 'AddARGBGLXVisuals', 'True', optiontype='Option', position=0)

        # version 71 needs a couple of extra driver options
        if self.version == '71':
            for opt in ('AllowGLXWithComposite', 'UseEdidFreqs'):
                self.xorg_conf.addOption('Device', opt, 'True', optiontype='Option', position=0)
        
        # make sure that RGB path is not in the xorg.conf otherwise xorg will crash
        it = 0
        for section in self.xorg_conf.globaldict['Files']:
            try:
                self.xorg_conf.removeOption('Files', 'RgbPath', position=it)
            except (XKit.xorgparser.OptionException):
                pass
            it += 1
        
        # remove any Disable "dri2" otherwise nvidia-settings and nvidia-xconfig will fail
        module_sections = self.xorg_conf.globaldict['Module']
        have_modules = len(module_sections) > 0
        
        if have_modules:
            for section in module_sections:
                self.xorg_conf.removeOption('Module', 'Disable', value='dri2', position=section)
    
    def disable(self):
        # make sure that nvidia-VER-kernel-source is removed too
        XorgDriverHandler.disable(self)
        if self.package:
            flavour = self.package.split('-')[-1]#e.g. 177
            kernel_source = 'nvidia-%s-kernel-source' % (flavour)
            self.backend.remove_package(kernel_source)
            if int(flavour) >= 180:
                self.backend.remove_package('nvidia-%s-libvdpau' % flavour)
            try:
                self.backend.remove_package('nvidia-settings')
            except SystemError:
                pass

        return False
    
    def recommended(self):
        if self._recommended == None:
            nd = NvidiaDetection()
            self._recommended = self.package == nd.selectDriver()
        return self._recommended

    def enabled(self):
        #if self.xorg_conf has NoneType, AttributeError will be raised
        try:
            devices = self.xorg_conf.globaldict['Device']
            try:
                driver = self.xorg_conf.getDriver('Device', 0)
            except (XKit.xorgparser.OptionException, XKit.xorgparser.SectionException):
                driver = None
            if len(devices) == 0 or driver != 'nvidia':
                return False
        except AttributeError:
            return False
        return KernelModuleHandler.enabled(self)

    def enables_composite(self):
        '''Return whether this driver supports the composite extension.'''

        # When using an upstream installation, or -new/-legacy etc., we already
        # have composite
        if KernelModuleHandler.module_loaded('nvidia'):
            logging.debug('enables_composite(): already using nvidia driver from nondefault package')
            return False

        # neither vesa nor nv support composite, so safe to say yes here
        return True
