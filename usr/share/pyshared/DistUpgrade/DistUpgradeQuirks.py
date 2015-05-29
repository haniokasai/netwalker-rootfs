# DistUpgradeQuirks.py 
#  
#  Copyright (c) 2004-2008 Canonical
#  
#  Author: Michael Vogt <michael.vogt@ubuntu.com>
# 
#  This program is free software; you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA

import glob
import logging
import os
import os.path
import re
import shutil
import string
import sys
import subprocess
from subprocess import PIPE, Popen, call
from hashlib import md5

from DistUpgradeGettext import gettext as _
from DistUpgradeGettext import ngettext
import gettext

from computerjanitor.plugin import PluginManager

class DistUpgradeQuirks(object):
    """
    This class collects the various quirks handlers that can
    be hooked into to fix/work around issues that the individual
    releases have
    """
    
    def __init__(self, controller, config):
        self.controller = controller
        self._view = controller._view
        self.config = config
        self.uname = Popen(["uname","-r"],stdout=PIPE).communicate()[0].strip()
        self.plugin_manager = PluginManager(self.controller, ["./plugins"])

    # the quirk function have the name:
    #  $Name (e.g. PostUpgrade)
    #  $todist$Name (e.g. intrepidPostUpgrade)
    #  $from_$fromdist$Name (e.g. from_dapperPostUpgrade)
    def run(self, quirksName):
        """
        Run the specific quirks handler, the follow handlers are supported:
        - PostInitialUpdate: run *before* the sources.list is rewritten but
                             after a initial apt-get update
        - PostDistUpgradeCache: run *after* the dist-upgrade was calculated
                                in the cache
        - StartUpgrade: before the first package gets installed (but the
                        download is finished)
        - PostUpgrade: run *after* the upgrade is finished successfully and 
                       packages got installed
        - PostCleanup: run *after* the cleanup (orphaned etc) is finished
        """
        # first check for matching plugins
        for condition in [
            quirksName,
            "%s%s" %  (self.config.get("Sources","To"), quirksName),
            "from_%s%s" % (self.config.get("Sources","From"), quirksName)
            ]:
            for plugin in self.plugin_manager.get_plugins(condition):
                logging.debug("running quirks plugin %s" % plugin)
                plugin.do_cleanup_cruft()
        
        # run the handler that is common to all dists
        funcname = "%s" % quirksName
        func = getattr(self, funcname, None)
        if func is not None:
            logging.debug("quirks: running %s" % funcname)
            func()

        # run the quirksHandler to-dist
        funcname = "%s%s" % (self.config.get("Sources","To"), quirksName)
        func = getattr(self, funcname, None)
        if func is not None:
            logging.debug("quirks: running %s" % funcname)
            func()

        # now run the quirksHandler from_${FROM-DIST}Quirks
        funcname = "from_%s%s" % (self.config.get("Sources","From"), quirksName)
        func = getattr(self, funcname, None)
        if func is not None:
            logging.debug("quirks: running %s" % funcname)
            func()

    # individual quirks handler when the dpkg run is finished ---------
    def PostCleanup(self):
        " run after cleanup " 
        logging.debug("running Quirks.PostCleanup")

    def from_dapperPostUpgrade(self):
        " this works around quirks for dapper->hardy upgrades "
        logging.debug("running Controller.from_dapperQuirks handler")
        self._rewriteFstab()
        self._checkAdminGroup()
        
    def intrepidPostUpgrade(self):
        " this applies rules for the hardy->intrepid upgrade "
	logging.debug("running Controller.intrepidQuirks handler")
        self._addRelatimeToFstab()

    def gutsyPostUpgrade(self):
        """ this function works around quirks in the feisty->gutsy upgrade """
        logging.debug("running Controller.gutsyQuirks handler")

    def feistyPostUpgrade(self):
        """ this function works around quirks in the edgy->feisty upgrade """
        logging.debug("running Controller.feistyQuirks handler")
        self._rewriteFstab()
        self._checkAdminGroup()

    # quirks when run when the initial apt-get update was run -------

    # fglrx is broken in intrepid (no support for xserver 1.5)
    def jauntyPostInitialUpdate(self):
        " quirks that are run before the upgrade to jaunty "
        logging.debug("running %s" %  sys._getframe().f_code.co_name
)
        # this is to deal with the fact that support for some of the cards
        # that fglrx used to support got dropped
        if (self._checkVideoDriver("fglrx") and 
            not self._supportInModaliases("fglrx")):
             res = self._view.askYesNoQuestion(_("Upgrading may reduce desktop "
                                         "effects, and performance in games "
                                         "and other graphically intensive "
                                         "programs."),
                                       _("This computer is currently using "
                                         "the AMD 'fglrx' graphics driver. "
                                         "No version of this driver is "
                                         "available that works with your "
                                         "hardware in Ubuntu "
                                         "9.04.\n\nDo you want to continue?"))
             if res == False:
                 self.controller.abort()
             # if the user wants to continue we remove the fglrx driver
             # here because its no use (no support for this card)
             logging.debug("remove xorg-driver-fglrx,xorg-driver-fglrx-envy,fglrx-kernel-source")
             l=self.controller.config.getlist("Distro","PostUpgradePurge")
             l.append("xorg-driver-fglrx")
             l.append("xorg-driver-fglrx-envy")
             l.append("fglrx-kernel-source")
             l.append("fglrx-amdcccle")
             l.append("xorg-driver-fglrx-dev")
             l.append("libamdxvba1")
             self.controller.config.set("Distro","PostUpgradePurge",",".join(l))

    # quirks when the cache upgrade calculation is finished
    def from_dapperPostDistUpgradeCache(self):
        self.hardyPostDistUpgradeCache()
        self.gutsyPostDistUpgradeCache()
        self.feistyPostDistUpgradeCache()
        self.edgyPostDistUpgradeCache()

    def jauntyPostDistUpgradeCache(self):
        """ 
        this function works around quirks in the 
        intrepid->jaunty upgrade calculation
        """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # bug 332328 - make sure pidgin-libnotify is upgraded
        for pkg in ["pidgin-libnotify"]:
            if (self.controller.cache.has_key(pkg) and
                self.controller.cache[pkg].isInstalled and
                not self.controller.cache[pkg].markedUpgrade):
                logging.debug("forcing '%s' upgrade" % pkg)
                self.controller.cache[pkg].markUpgrade()
        # deal with kipi/gwenview/kphotoalbum
        for pkg in ["gwenview","digikam"]:
            if (self.controller.cache.has_key(pkg) and
                self.controller.cache[pkg].isInstalled and
                not self.controller.cache[pkg].markedUpgrade):
                logging.debug("forcing libkipi '%s' upgrade" % pkg)
                if self.controller.cache.has_key("libkipi0"):
                    logging.debug("removing  libkipi0)")
                    self.controller.cache["libkipi0"].markDelete()
                self.controller.cache[pkg].markUpgrade()
        
    def intrepidPostDistUpgradeCache(self):
        """ 
        this function works around quirks in the 
        hardy->intrepid upgrade 
        """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # check if a key depends of kubuntu-kde4-desktop is installed
        # and transition in this case as well
        deps_found = False
        if self.config.getlist(frompkg,"KeyDependencies"):
            deps_found = True
            for pkg in self.config.getlist(frompkg,"KeyDependencies"):
                deps_found &= (self.controller.cache.has_key(pkg) and
                               self.controller.cache[pkg].isInstalled)
        if deps_found:
            logging.debug("transitioning %s to %s (via key depends)" % (frompkg, topkg))
            self.controller.cache[topkg].markInstall()
        # now check for nvidia and show a warning if needed
        cache = self.controller.cache
        for pkgname in ["nvidia-glx-71","nvidia-glx-96"]:
            if (cache.has_key(pkgname) and 
                cache[pkgname].markedInstall and
                self._checkVideoDriver("nvidia")):
                logging.debug("found %s video driver" % pkgname)
                res = self._view.askYesNoQuestion(_("Upgrading may reduce desktop "
                                        "effects, and performance in games "
                                        "and other graphically intensive "
                                        "programs."),
                                      _("This computer is currently using "
                                        "the NVIDIA 'nvidia' "
                                        "graphics driver. "
                                        "No version of this driver is "
                                        "available that works with your "
                                        "video card in Ubuntu "
                                        "8.10.\n\nDo you want to continue?"))
                if res == False:
                    self.controller.abort()
                # if the user continue, do not install the broken driver
                # so that we can transiton him to the free "nv" one after
                # the upgrade
                self.controller.cache[pkgname].markKeep()
        # check if we have sse
        for pkgname in ["nvidia-glx-173","nvidia-glx-177"]:
            if (cache.has_key(pkgname) and 
                cache[pkgname].markedInstall and
                self._checkVideoDriver("nvidia")):
                logging.debug("found %s video driver" % pkgname)
                if not self._cpuHasSSESupport():
                    logging.warning("nvidia driver that needs SSE but cpu has no SSE support")
                    res = self._view.askYesNoQuestion(_("Upgrading may reduce desktop "
                                        "effects, and performance in games "
                                        "and other graphically intensive "
                                        "programs."),
                                      _("This computer is currently using "
                                        "the NVIDIA 'nvidia' "
                                        "graphics driver. "
                                        "No version of this driver is "
                                        "available that works with your "
                                        "video card in Ubuntu "
                                        "8.10.\n\nDo you want to continue?"))
                    if res == False:
                        self.controller.abort()
                    # if the user continue, do not install the broken driver
                    # so that we can transiton him to the free "nv" one after
                    # the upgrade
                    self.controller.cache[pkgname].markKeep()
        # kdelibs4-dev is unhappy (#279621)
        fromp = "kdelibs4-dev"
        to = "kdelibs5-dev"
        if (self.controller.cache.has_key(fromp) and 
            self.controller.cache[fromp].isInstalled and
            self.controller.cache.has_key(to)):
            self.controller.cache.markInstall(to, "kdelibs4-dev -> kdelibs5-dev transition")

    def hardyPostDistUpgradeCache(self):
        """ 
        this function works around quirks in the 
        {dapper,gutsy}->hardy upgrade 
        """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # deal with gnome-translator and help apt with the breaks
        if (self.controller.cache.has_key("nautilus") and
            self.controller.cache["nautilus"].isInstalled and
            not self.controller.cache["nautilus"].markedUpgrade):
            # uninstallable and gutsy apt is unhappy about this
            # breaks because it wants to upgrade it and gives up
            # if it can't
            for broken in ("link-monitor-applet"):
                if self.controller.cache.has_key(broken) and self.controller.cache[broken].isInstalled:
                    self.controller.cache[broken].markDelete()
            self.controller.cache["nautilus"].markInstall()
        # evms gives problems, remove it if it is not in use
        self._checkAndRemoveEvms()
        # give the language-support-* packages a extra kick
        # (if we have network, otherwise this will not work)
        if self.config.get("Options","withNetwork") == "True":
            for pkg in self.controller.cache:
                if (pkg.name.startswith("language-support-") and
                    pkg.isInstalled and
                    not pkg.markedUpgrade):
                    self.controller.cache.markInstall(pkg.name,"extra language-support- kick")

    def gutsyPostDistUpgradeCache(self):
        """ this function works around quirks in the feisty->gutsy upgrade """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # lowlatency kernel flavour vanished from feisty->gutsy
        try:
            (version, build, flavour) = self.uname.split("-")
            if (flavour == 'lowlatency' or 
                flavour == '686' or
                flavour == 'k7'):
                kernel = "linux-image-generic"
                if not (self.controller.cache[kernel].isInstalled or self.controller.cache[kernel].markedInstall):
                    logging.debug("Selecting new kernel '%s'" % kernel)
                    self.controller.cache[kernel].markInstall()
        except Exception, e:
            logging.warning("problem while transitioning lowlatency kernel (%s)" % e)
        # fix feisty->gutsy utils-linux -> nfs-common transition (LP: #141559)
        try:
            for line in map(string.strip, open("/proc/mounts")):
                if line == '' or line.startswith("#"):
                    continue
                try:
                    (device, mount_point, fstype, options, a, b) = line.split()
                except Exception, e:
                    logging.error("can't parse line '%s'" % line)
                    continue
                if "nfs" in fstype:
                    logging.debug("found nfs mount in line '%s', marking nfs-common for install " % line)
                    self.controller.cache["nfs-common"].markInstall()
                    break
        except Exception, e:
            logging.warning("problem while transitioning util-linux -> nfs-common (%s)" % e)

    def feistyPostDistUpgradeCache(self):
        """ this function works around quirks in the edgy->feisty upgrade """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # ndiswrapper changed again *sigh*
        for (fr, to) in [("ndiswrapper-utils-1.8","ndiswrapper-utils-1.9")]:
            if self.controller.cache.has_key(fr) and self.controller.cache.has_key(to):
                if self.controller.cache[fr].isInstalled and not self.controller.cache[to].markedInstall:
                    try:
                        self.controller.cache.markInstall(to,"%s->%s quirk upgrade rule" % (fr, to))
                    except SystemError, e:
                        logging.warning("Failed to apply %s->%s install (%s)" % (fr, to, e))
            

    def edgyPostDistUpgradeCache(self):
        """ this function works around quirks in the dapper->edgy upgrade """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        for pkg in self.controller.cache:
            # deal with the python2.4-$foo -> python-$foo transition
            if (pkg.name.startswith("python2.4-") and
                pkg.isInstalled and
                not pkg.markedUpgrade):
                basepkg = "python-"+pkg.name[len("python2.4-"):]
                if (self.controller.cache.has_key(basepkg) and 
                    self.controller.cache[basepkg].candidateDownloadable and
                    not self.controller.cache[basepkg].markedInstall):
                    try:
                        self.controller.cache.markInstall(basepkg,
                                         "python2.4->python upgrade rule")
                    except SystemError, e:
                        logging.debug("Failed to apply python2.4->python install: %s (%s)" % (basepkg, e))
            # xserver-xorg-input-$foo gives us trouble during the upgrade too
            if (pkg.name.startswith("xserver-xorg-input-") and
                pkg.isInstalled and
                not pkg.markedUpgrade):
                try:
                    self.controller.cache.markInstall(pkg.name, "xserver-xorg-input fixup rule")
                except SystemError, e:
                    logging.debug("Failed to apply fixup: %s (%s)" % (pkg.name, e))
            
        # deal with held-backs that are unneeded
        for pkgname in ["hpijs", "bzr", "tomboy"]:
            if (self.controller.cache.has_key(pkgname) and self.controller.cache[pkgname].isInstalled and
                self.controller.cache[pkgname].isUpgradable and not self.controller.cache[pkgname].markedUpgrade):
                try:
                    self.controller.cache.markInstall(pkgname,"%s quirk upgrade rule" % pkgname)
                except SystemError, e:
                    logging.debug("Failed to apply %s install (%s)" % (pkgname,e))
        # libgl1-mesa-dri from xgl.compiz.info (and friends) breaks the
	# upgrade, work around this here by downgrading the package
        if self.controller.cache.has_key("libgl1-mesa-dri"):
            pkg = self.controller.cache["libgl1-mesa-dri"]
            # the version from the compiz repo has a "6.5.1+cvs20060824" ver
            if (pkg.candidateVersion == pkg.installedVersion and
                "+cvs2006" in pkg.candidateVersion):
                for ver in pkg._pkg.VersionList:
                    # the "official" edgy version has "6.5.1~20060817-0ubuntu3"
                    if "~2006" in ver.VerStr:
			# ensure that it is from a trusted repo
			for (VerFileIter, index) in ver.FileList:
				indexfile = self.controller.cache._list.FindIndex(VerFileIter)
				if indexfile and indexfile.IsTrusted:
					logging.info("Forcing downgrade of libgl1-mesa-dri for xgl.compz.info installs")
		                        self.controller.cache._depcache.SetCandidateVer(pkg._pkg, ver)
					break
                                    
        # deal with general if $foo is installed, install $bar
        for (fr, to) in [("xserver-xorg-driver-all","xserver-xorg-video-all")]:
            if self.controller.cache.has_key(fr) and self.controller.cache.has_key(to):
                if self.controller.cache[fr].isInstalled and not self.controller.cache[to].markedInstall:
                    try:
                        self.controller.cache.markInstall(to,"%s->%s quirk upgrade rule" % (fr, to))
                    except SystemError, e:
                        logging.debug("Failed to apply %s->%s install (%s)" % (fr, to, e))
                    
    def dapperPostDistUpgradeCache(self):
        """ this function works around quirks in the breezy->dapper upgrade """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        if (self.controller.cache.has_key("nvidia-glx") and self.controller.cache["nvidia-glx"].isInstalled and
            self.controller.cache.has_key("nvidia-settings") and self.controller.cache["nvidia-settings"].isInstalled):
            logging.debug("nvidia-settings and nvidia-glx is installed")
            self.controller.cache.markRemove("nvidia-settings")
            self.controller.cache.markInstall("nvidia-glx")

    def from_hardyPostDistUpgradeCache(self):
        """ this function works around quirks in upgrades from hardy """
        logging.debug("running %s" %  sys._getframe().f_code.co_name)
        # evms got removed after hardy, warn and abort
        if self._usesEvmsInMounts():
            logging.error("evms in use in /etc/fstab")
            self._view.error(_("evms in use"),
                             _("Your system uses the 'evms' volume manager "
                               "in /proc/mounts. "
                               "The 'evms' software is no longer supported, "
                               "please switch it off and run the upgrade "
                               "again when this is done."))
            self.controller.abort()

    # run right before the first packages get installed
    def StartUpgrade(self):
        self._applyPatches()
        self._removeOldApportCrashes()
        self._removeBadMaintainerScripts()
    def jauntyStartUpgrade(self):
        self._createPycentralPkgRemove()
        # hal/NM triggers problem, if the old (intrepid) hal gets
        # triggered for a restart this causes NM to drop all connections
        # because (old) hal thinks it has no devices anymore (LP: #327053)
        ap = "/var/lib/dpkg/info/hal.postinst"
        if os.path.exists(ap):
            # intrepid md5 of hal.postinst (jaunty one is different)
            # md5 jaunty 22c146857d751181cfe299a171fc11c9
            md5sum = "146145275900af343d990a4dea968d7c"
            if md5(open(ap).read()).hexdigest() == md5sum:
                logging.debug("removing bad script '%s'" % ap)
                os.unlink(ap)


    # helpers
    def _removeBadMaintainerScripts(self):
        " remove bad/broken maintainer scripts (last resort) "
        # apache: workaround #95325 (edgy->feisty)
        # pango-libthai #103384 (edgy->feisty)
        bad_scripts = ["/var/lib/dpkg/info/apache2-common.prerm",
                       "/var/lib/dpkg/info/pango-libthai.postrm",
                       ]
        for ap in bad_scripts:
            if os.path.exists(ap):
                logging.debug("removing bad script '%s'" % ap)
                os.unlink(ap)

    def _createPycentralPkgRemove(self):
        """
        intrepid->jaunty, create /var/lib/pycentral/pkgremove flag file
        to help python-central so that it removes all preinst links
        on upgrade
        """
        logging.debug("adding pkgremove file")
        if not os.path.exists("/var/lib/pycentral/"):
            os.makedirs("/var/lib/pycentral")
        open("/var/lib/pycentral/pkgremove","w")

    def _removeOldApportCrashes(self):
        " remove old apport crash files "
        try:
            for f in glob.glob("/var/crash/*.crash"):
                logging.debug("removing old crash file '%s'" % f)
                os.unlink(f)
        except Exception, e:
            logging.warning("error during unlink of old crash files (%s)" % e)

    def _cpuHasSSESupport(self, cpuinfo="/proc/cpuinfo"):
        " helper that checks if the given cpu has sse support "
        if not os.path.exists(cpuinfo):
            return False
        for line in open(cpuinfo):
            if line.startswith("flags") and not " sse" in line:
                return False
        return True

    def _usesEvmsInMounts(self):
        " check if evms is used in /proc/mounts "
        logging.debug("running _usesEvmsInMounts")
        for line in open("/proc/mounts"):
            line = line.strip()
            if line == '' or line.startswith("#"):
                continue
            try:
                (device, mount_point, fstype, options, a, b) = line.split()
            except Exception, e:
                logging.error("can't parse line '%s'" % line)
                continue
            if "evms" in device:
                logging.debug("found evms device in line '%s', skipping " % line)
                return True
        return False

    def _checkAndRemoveEvms(self):
        " check if evms is in use and if not, remove it "
        logging.debug("running _checkAndRemoveEvms")
        if self._usesEvmsInMounts():
            return False
        # if not in use, nuke it
        for pkg in ["evms","libevms-2.5","libevms-dev",
                    "evms-ncurses", "evms-ha",
                    "evms-bootdebug",
                    "evms-gui", "evms-cli",
                    "linux-patch-evms"]:
            if self.controller.cache.has_key(pkg) and self.controller.cache[pkg].isInstalled:
                self.controller.cache[pkg].markDelete()
        return True

    def _addRelatimeToFstab(self):
        " add the relatime option to ext2/ext3 filesystems on upgrade "
        logging.debug("_addRelatime")
        replaced = False
        lines = []
        for line in open("/etc/fstab"):
            line = line.strip()
            if line == '' or line.startswith("#"):
                lines.append(line)
                continue
            try:
                (device, mount_point, fstype, options, a, b) = line.split()
            except Exception, e:
                logging.error("can't parse line '%s'" % line)
                lines.append(line)
                continue
            if (("ext2" in fstype or
                 "ext3" in fstype) and 
                (not "noatime" in options) and
                (not "relatime" in options) ):
                logging.debug("adding 'relatime' to line '%s' " % line)
                line = line.replace(options,"%s,relatime" % options)
                logging.debug("replaced line is '%s' " % line)
                replaced=True
            lines.append(line)
        # we have converted a line
        if replaced:
            logging.debug("writing new /etc/fstab")
            f=open("/etc/fstab.intrepid","w")
            f.write("\n".join(lines))
            # add final newline (see LP: #279093)
            f.write("\n")
            f.close()
            os.rename("/etc/fstab.intrepid","/etc/fstab")
        return True
        

    def _rewriteFstab(self):
        " convert /dev/{hd?,scd0} to /dev/cdrom for the feisty upgrade "
        logging.debug("_rewriteFstab()")
        replaced = 0
        lines = []
        # we have one cdrom to convert
        for line in open("/etc/fstab"):
            line = line.strip()
            if line == '' or line.startswith("#"):
                lines.append(line)
                continue
            try:
                (device, mount_point, fstype, options, a, b) = line.split()
            except Exception, e:
                logging.error("can't parse line '%s'" % line)
                lines.append(line)
                continue
            # edgy kernel has /dev/cdrom -> /dev/hd?
            # feisty kernel (for a lot of chipsets) /dev/cdrom -> /dev/scd0
            # this breaks static mounting (LP#86424)
            #
            # we convert here to /dev/cdrom only if current /dev/cdrom
            # points to the device in /etc/fstab already. this ensures
            # that we don't break anything or that we get it wrong
            # for systems with two (or more) cdroms. this is ok, because
            # we convert under the old kernel
            if ("iso9660" in fstype and
                device != "/dev/cdrom" and
                os.path.exists("/dev/cdrom") and
                os.path.realpath("/dev/cdrom") == device
                ):
                logging.debug("replacing '%s' " % line)
                line = line.replace(device,"/dev/cdrom")
                logging.debug("replaced line is '%s' " % line)
                replaced += 1
            lines.append(line)
        # we have converted a line (otherwise we would have exited already)
        if replaced > 0:
            logging.debug("writing new /etc/fstab")
            shutil.copy("/etc/fstab","/etc/fstab.edgy")
            f=open("/etc/fstab","w")
            f.write("\n".join(lines))
            # add final newline (see LP: #279093)
            f.write("\n")
            f.close()
        return True

    def _checkAdminGroup(self):
        " check if the current sudo user is in the admin group "
        logging.debug("_checkAdminGroup")
        import grp
        try:
            admin_group = grp.getgrnam("admin").gr_mem
        except KeyError, e:
            logging.warning("System has no admin group (%s)" % e)
            subprocess.call(["addgroup","--system","admin"])
        # double paranoia
        try:
            admin_group = grp.getgrnam("admin").gr_mem
        except KeyError, e:
            logging.warning("adding the admin group failed (%s)" % e)
            return
        # if the current SUDO_USER is not in the admin group
        # we add him - this is no security issue because
        # the user is already root so adding him to the admin group
        # does not change anything
        if (os.environ.has_key("SUDO_USER") and
            not os.environ["SUDO_USER"] in admin_group):
            admin_user = os.environ["SUDO_USER"]
            logging.info("SUDO_USER=%s is not in admin group" % admin_user)
            cmd = ["usermod","-a","-G","admin",admin_user]
            res = subprocess.call(cmd)
            logging.debug("cmd: %s returned %i" % (cmd, res))

    def _checkVideoDriver(self, name):
        " check if the given driver is in use in xorg.conf "
        XORG="/etc/X11/xorg.conf"
        if not os.path.exists(XORG):
            return False
        for line in open(XORG):
            s=line.split("#")[0].strip()
            # check for fglrx driver entry
            if (s.lower().startswith("driver") and
                s.endswith('"%s"' % name)):
                return True
        return False

    def _applyPatches(self, patchdir="./patches"):
        """
        helper that applies the patches in patchdir. the format is
        _path_to_file.md5sum
        
        and it will apply the diff to that file if the md5sum
        matches
        """
        if not os.path.exists(patchdir):
            logging.debug("no patchdir")
            return
        if not ("PATH" in os.environ and
                [p for p in os.environ["PATH"].split(":")
                 if os.path.exists(os.path.join(p,"patch"))]):
            logging.debug("no binary 'patch' found in PATH")
            return
        for f in os.listdir(patchdir):
            # skip, not a patch file, they all end with .$md5sum
            if not "." in f:
                continue
            logging.debug("check if patch '%s' needs to be applied" % f)
            (encoded_path, md5sum) = string.split(f, ".", 1)
            # FIXME: this is not clever and needs quoting support for
            #        filenames with "_" in the name
            path = encoded_path.replace("_","/")
            if (os.path.exists(path) and
                md5(open(path).read()).hexdigest() == md5sum):
                logging.info("applying '%s'" % f)
                # dry-run first, then patch if ok
                res = call(["patch","--dry-run","-s","-p0","-i",
                            patchdir+"/"+f])
                if res == 0:
                    res = call(["patch","-p0","-s","-i",patchdir+"/"+f])
                    logging.info("applied '%s' with %i status" % (f,res))
                else:
                    logging.warning("dry run failed, ignoring patch '%s'" % f)
                    
    def _supportInModaliases(self, xorgdrivername, modaliasesdir="./modaliases", lspci=None):
        """ 
        Check if xorgdriver will work on this hardware

        This helper will check with the modaliasesdir if the given 
        xorgdriver will work on this hardware (or the hardware given
        via the lspci argument)
        """
        if not lspci:
            lspci = set()
            p = subprocess.Popen(["lspci","-n"],stdout=subprocess.PIPE)
            for line in p.communicate()[0].split("\n"):
                if line:
                    lspci.add(line.split()[2])
        for filename in os.listdir(modaliasesdir):
            for line in open(os.path.join(modaliasesdir,filename)):
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                (key, pciid, xorgdriver, pkgname) = line.split()
                if xorgdriver != xorgdrivername:
                    continue
                m = re.match("pci:v0000(.+)d0000(.+)sv.*", pciid)
                if m:
                    matchid = "%s:%s" % (m.group(1), m.group(2))
                    if matchid.lower() in lspci:
                        logging.debug("found system pciid '%s' in modaliases" % matchid)
                        return True
        logging.debug("checking for %s support in modaliases but none found" % xorgdrivername)
        return False
                    


