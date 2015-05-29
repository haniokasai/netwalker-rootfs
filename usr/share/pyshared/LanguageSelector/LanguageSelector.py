# (c) 2006 Canonical
# Author: Michael Vogt <michael.vogt@ubuntu.com>
#
# Released under the GPL
#

import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt
import apt_pkg
import os.path
import shutil
import subprocess
import thread
import time
import gettext
import sys
import string
import tempfile
import re

import FontConfig
from gettext import gettext as _
from LocaleInfo import LocaleInfo

from LangCache import *                


# the language-selector abstraction
class LanguageSelectorBase(object):
    """ base class for language-selector code """
    def __init__(self, datadir=""):
        self._datadir = datadir
        # load the localeinfo "database"
        self._localeinfo = LocaleInfo("%s/data/languagelist" % self._datadir)
        self._cache = None

    def openCache(self, progress):
        self._cache = LanguageSelectorPkgCache(self._localeinfo, progress)

    def getMissingLangPacks(self):
        """
        return a list of langauge packs that are not installed
        but should be installed
        """
        missing = []
        for langInfo in  self._cache.getLanguageInformation():
            #print langInfo.languageCode
            trans_package = "language-pack-%s" % langInfo.languageCode
            # we have a langpack installed, see if we have all of them
            if (self._cache.has_key(trans_package) and 
                self._cache[trans_package].isInstalled):
                #print "IsInstalled: %s " % trans_package
                for (pkg, translation) in self._cache.pkg_translations:
                    missing += self.missingTranslationPkgs(pkg, translation+langInfo.languageCode)

        # now check for a missing default language support
        default_lang = self.getSystemDefaultLanguage()
        # if there is no default lang, return early
        if default_lang is None:
            return missing
        if "_" in default_lang:
            default_lang = default_lang.split("_")[0]
        trans_package = "language-pack-%s" % default_lang
        if (self._cache.has_key(trans_package) and 
            not self._cache[trans_package].isInstalled):
            missing += [trans_package]
            for (pkg, translation) in self._cache.pkg_translations:
                missing += self.missingTranslationPkgs(pkg, translation+default_lang)
        support_packages = LanguageSelectorPkgCache._getPkgList(self._cache, default_lang)
        for support_package in support_packages:
            if (self._cache.has_key(support_package) and 
                not self._cache[support_package].isInstalled):
                missing.append(support_package)

        return missing

    def getUserDefaultLanguage(self):
        fname = os.path.expanduser("~/.dmrc")
        if os.path.exists(fname):
            for line in open(fname):
                match = re.match(r'Language=(.*)$',line)
                if match:
                    if "." in match.group(1):
                        return match.group(1).split(".")[0]
                    else:
                        return match.group(1)
        return None

    def getSystemDefaultLanguage(self):
        conffiles = ["/etc/default/locale", "/etc/environment"]
        for fname in conffiles:
            if os.path.exists(fname):
                for line in open(fname):
                    match = re.match(r'LANG="(.*)"$',line)
                    if match:
                        if "." in match.group(1):
                            return match.group(1).split(".")[0]
                        else:
                            return match.group(1)
        return None

    def runAsRoot(self, cmd):
        " abstract interface for the frontends to run specific commands as root"
        # compatibilty code for frontends that already run as root
        if os.getuid() == 0:
            return subprocess.call(cmd)
        # 
        raise AttributeError, "this method needs to be overwriten by the subclass"

    def setSystemDefaultLanguage(self, defaultLanguageCode):
        " this updates the system default language "
        conffiles = ["/etc/default/locale", "/etc/environment"]
        for fname in conffiles:
            out = tempfile.NamedTemporaryFile()        
            foundLanguage = False  # the LANGUAGE var
            foundLang = False      # the LANG var
            if os.path.exists(fname):
                # look for the line
                for line in open(fname):
                    tmp = string.strip(line)
                    if tmp.startswith("LANGUAGE="):
                        foundLanguage = True
                        line="LANGUAGE=\"%s\"\n" % self._localeinfo.makeEnvString(defaultLanguageCode)
                        #print line
                    if tmp.startswith("LANG="):
                        foundLang = True
                        # we always write utf8 languages
                        line="LANG=\"%s.UTF-8\"\n" % defaultLanguageCode
                    out.write(line)
                    #print line
            # if we have not found them add them
            if foundLanguage == False:
                line="LANGUAGE=\"%s\"\n" % self._localeinfo.makeEnvString(defaultLanguageCode)
                out.write(line)
            if foundLang == False:
                line="LANG=\"%s.UTF-8\"\n" % defaultLanguageCode
                out.write(line)
            out.flush()
            self.runAsRoot(["/bin/cp",out.name, fname])

        # now set the fontconfig-voodoo
        fc = FontConfig.FontConfigHack()
        #print defaultLanguageCode
        #print fc.getAvailableConfigs()
        if defaultLanguageCode in fc.getAvailableConfigs():
            self.runAsRoot(["fontconfig-voodoo", "-f",
                            "--set=%s" % defaultLanguageCode])
        else:
            self.runAsRoot(["fontconfig-voodoo","-f","--remove-current"])

    def setUserDefaultLanguage(self, defaultLanguageCode):
        " this updates the user default language "
        fname = os.path.expanduser("~/.dmrc")
        out = tempfile.NamedTemporaryFile()        
        foundLang = False      # the Language var
        if os.path.exists(fname):
            # look for the line
            for line in open(fname):
                tmp = string.strip(line)
                if tmp.startswith("Language="):
                    foundLang = True
                    # we always write utf8 languages
                    line="Language=%s.UTF-8\n" % defaultLanguageCode
                out.write(line)
        # if we have not found them add them
        if foundLang == False:
            line="Language=%s.UTF-8\n" % defaultLanguageCode
            out.write(line)
        out.flush()
        shutil.copy(out.name, fname)
        os.chmod(fname, 0644)

        # FIXME: This should be set on a per user base in ~/.fonts.conf
        ## now set the fontconfig-voodoo
        #fc = FontConfig.FontConfigHack()
        ##print defaultLanguageCode
        ##print fc.getAvailableConfigs()
        #f defaultLanguageCode in fc.getAvailableConfigs():
        #    self.runAsRoot(["fontconfig-voodoo", "-f",
        #                    "--set=%s" % defaultLanguageCode])
        #else:
        #    self.runAsRoot(["fontconfig-voodoo","-f","--remove-current"])

    def missingTranslationPkgs(self, pkg, translation_pkg):
        """ this will check if the given pkg is installed and if
            the needed translation package is installed as well

            It returns a list of packages that need to be 
            installed
        """

        # FIXME: this function is called too often and it's too slow
        # -> see ../TODO for ideas how to fix it
        missing = []
        # check if the pkg itself is available and installed
        if not self._cache.has_key(pkg):
            return missing
        if not self._cache[pkg].isInstalled:
            return missing

        # match every packages that looks similar to translation_pkg
        # 
        for pkg in self._cache:
            if (pkg.name == translation_pkg or
                pkg.name.startswith(translation_pkg+"-")):
                if not pkg.isInstalled and pkg.candidateVersion != None:
                    missing.append(pkg.name)
        return missing
        

if __name__ == "__main__":
    lsb = LanguageSelectorBase(datadir="..")
    lsb.openCache(apt.progress.OpProgress())
    print lsb.verifyPackageLists()

