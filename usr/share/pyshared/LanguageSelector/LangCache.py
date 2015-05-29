
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt
import apt_pkg

from xml.etree.ElementTree import ElementTree

from gettext import gettext as _

class LanguagePackageStatus(object):
    def __init__(self, pkg_template):
        self.pkgname_template = pkg_template
        self.available = False
        self.installed = False
        self.doChange = False


# the language-support information
class LanguageInformation(object):
    def __init__(self):
        self.language = None
        self.languageCode = None
        # langPack/support status 
        self.languagePkgList = {}
        self.languagePkgList["languagePack"] = LanguagePackageStatus("language-pack-%s")
        #self.languagePkgList["languageSupport"] = LanguagePackageStatus("language-support-%s")
        self.languagePkgList["languageSupportWritingAids"] = LanguagePackageStatus("language-support-writing-%s")
        self.languagePkgList["languageSupportTranslations"] = LanguagePackageStatus("language-support-translations-%s")
        self.languagePkgList["languageSupportInputMethods"] = LanguagePackageStatus("language-support-input-%s")
        self.languagePkgList["languageSupportFonts"] = LanguagePackageStatus("language-support-fonts-%s")
        self.languagePkgList["languageSupportExtra"] = LanguagePackageStatus("language-support-extra-%s")
        
    @property
    def inconsistent(self):
        " returns True if only parts of the language support packages are installed "
        if (not self.notInstalled and not self.fullInstalled) : return True
        return False
    @property
    def fullInstalled(self):
        " return True if all of the available language support packages are installed "
        for pkg in self.languagePkgList.values() :
            if not pkg.available : continue
            if not ((pkg.installed and not pkg.doChange) or (not pkg.installed and pkg.doChange)) : return False
        return True
    @property
    def notInstalled(self):
        " return True if none of the available language support packages are installed "
        for pkg in self.languagePkgList.values() :
            if not pkg.available : continue
            if not ((not pkg.installed and not pkg.doChange) or (pkg.installed and pkg.doChange)) : return False
        return True
    @property
    def changes(self):
        " returns true if anything in the state of the language packs/support changes "
        for pkg in self.languagePkgList.values() :
            if (pkg.doChange) : return True
        return False
    def __str__(self):
        return "%s (%s)" % (self.language, self.languageCode)

# the pkgcache stuff
class ExceptionPkgCacheBroken(Exception):
    pass

class LanguageSelectorPkgCache(apt.Cache):

    # packages that need special translation packs (not covered by
    # the normal langpacks) 
    pkg_translations = [
        ("kdelibs-data", "language-pack-kde-"),
        ("libgnome2-common", "language-pack-gnome-"),
#        ("firefox-2", "mozilla-firefox-locale-"),
#        ("thunderbird", "language-support-translations-"),
#        ("openoffice.org", "language-support-translations-"),
#        ("openoffice.org", "language-support-translations-"),
        ("libsword5c2a", "sword-language-pack-")
    ]

    def __init__(self, localeinfo, progress):
        apt.Cache.__init__(self, progress)
        if self._depcache.BrokenCount > 0:
            raise ExceptionPkgCacheBroken()
        self._localeinfo = localeinfo
        # keep the lists 
        self.to_inst = []
        self.to_rm = []

    @property
    def havePackageLists(self):
        " verify that a network package lists exists "
        for metaindex in self._list.List:
            for indexfile in metaindex.IndexFiles:
                if indexfile.ArchiveURI("").startswith("cdrom:"):
                    continue
                if indexfile.ArchiveURI("").startswith("http://security.ubuntu.com"):
                    continue
                if indexfile.Exists and indexfile.HasPackages:
                    return True
        return False

    def clear(self):
        """ clear the selections """
        self._depcache.Init()
        
    def getChangesList(self):
        to_inst = []
        to_rm = []
        for pkg in self.getChanges():
            if pkg.markedInstall or pkg.markedUpgrade:
                to_inst.append(pkg.name)
            if pkg.markedDelete:
                to_rm.append(pkg.name)
        return (to_inst,to_rm)

    def _getPkgList(self, languageCode):
        """ helper that returns the list of needed pkgs for the language """
        # normal langpack+support first
        pkg_list = ["language-support-input-%s"%languageCode,\
                    "language-support-writing-%s"%languageCode,\
                    "language-support-fonts-%s"%languageCode,\
                    "language-support-translations-%s"%languageCode,\
                    "language-support-extra-%s"%languageCode,\
                      "language-pack-%s"%languageCode]
        # see what additional pkgs are needed
        for (pkg, translation) in self.pkg_translations:
            if self.has_key(pkg) and self[pkg].isInstalled:
                pkg_list.append(translation+languageCode)
        return pkg_list
        
    def tryChangeDetails(self, li):
        " change the status of the support details (fonts, input methods) "
        #print li
        for item in li.languagePkgList.values():
            if item.doChange:
                try:
                    if item.installed:
                        self[item.pkgname_template % li.languageCode].markDelete()
                    else:
                        self[item.pkgname_template % li.languageCode].markInstall()
                except SystemError:
                    pass
        # Check for additional translation packages
        item = li.languagePkgList["languagePack"]
        if ((item.installed and not item.doChange) or (item.available and not item.installed and item.doChange)):
            for (pkg, translation) in self.pkg_translations:
                if self.has_key(pkg) and \
                   self[pkg].isInstalled and \
                   self.has_key(translation+li.languageCode) and \
                   not self[translation+li.languageCode].isInstalled:
                   self[translation+li.languageCode].markInstall()
                   #print ("Will pull: %s" % translation+li.languageCode)
        elif ((not item.installed and not item.doChange) or (item.installed and item.doChange)) :
            for (pkg, translation) in self.pkg_translations:
                if self.has_key(pkg) and \
                   self[pkg].isInstalled and \
                   self.has_key(translation+li.languageCode) and \
                   self[translation+li.languageCode].isInstalled:
                   self[translation+li.languageCode].markDelete()
                   #print ("Will remove: %s" % translation+li.languageCode)
        return

    def tryInstallLanguage(self, languageCode):
        """ mark the given language for install """
        to_inst = []
        for name in self._getPkgList(languageCode):
            if self.has_key(name):
                try:
                    self[name].markInstall()
                    to_inst.append(name)
                except SystemError:
                    pass
                try:
                    self[name].markInstall()
                    to_inst.append(name)
                except SystemError:
                    pass

    def tryRemoveLanguage(self, languageCode):
        """ mark the given language for remove """
        to_rm = []
        for name in self._getPkgList(languageCode):
            if self.has_key(name):
                try:
                    # purge
                    self[name].markDelete(True)
                    to_rm.append(name)
                except SystemError:
                    pass
    
    def getLanguageInformation(self):
        """ returns a list with language packs/support packages """
        res = []
        for (code,lang) in self._localeinfo._lang.items():
            li = LanguageInformation()
            li.languageCode = code
            li.language = lang
            for langpkg_status in li.languagePkgList.values() :
                pkgname = langpkg_status.pkgname_template % code
                langpkg_status.available = self.has_key(pkgname)
                if langpkg_status.available:
                    langpkg_status.installed = self[pkgname].isInstalled
            if len(filter(lambda s: s.available, li.languagePkgList.values())) > 0:
                res.append(li)
        return res


if __name__ == "__main__":

    from LocaleInfo import LocaleInfo
    datadir = "/usr/share/language-selector"
    li = LocaleInfo("%s/data/languagelist" % datadir)

    lc = LanguageSelectorPkgCache(li,apt.progress.OpProgress())
    print "available language information"
    print ", ".join(["%s" %x for x in lc.getLanguageInformation()])

    print "Trying to install 'zh'"
    lc.tryInstallLanguage("zh")
    print lc.getChangesList()

    print "Trying to remove it again"
    lc.tryRemoveLanguage("zh")
    print lc.getChangesList()
