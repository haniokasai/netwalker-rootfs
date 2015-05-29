#!/usr/bin/python


#nice apt-get -s -o Debug::NoLocking=true upgrade | grep ^Inst 

import apt_pkg
import os
import sys
from optparse import OptionParser
import gettext

SYNAPTIC_PINFILE = "/var/lib/synaptic/preferences"

def _(msg):
    return gettext.dgettext("update-notifier", msg)

class OpNullProgress(object):
    def update(self, percent):
        pass
    def done(self):
        pass

def clean(cache,depcache):
    # mvo: looping is too inefficient with the new auto-mark code
    #for pkg in cache.Packages:
    #    depcache.MarkKeep(pkg)
    depcache.Init()

def saveDistUpgrade(cache,depcache):
    """ this functions mimics a upgrade but will never remove anything """
    depcache.Upgrade(True)
    if depcache.DelCount > 0:
        clean(cache,depcache)
    depcache.Upgrade()

def _handleException(type, value, tb):
    sys.stderr.write("E: "+ _("Unkown Error: '%s' (%s)") % (type,value))
    sys.exit(-1)


def isSecurityUpgrade(ver):
    " check if the given version is a security update (or masks one) "
    for (file, index) in ver.FileList:
        if (file.Archive.endswith("-security") and
            file.Origin == "Ubuntu"):
            return True
    return False
    
def run(options=None):
    # be nice
    os.nice(19)
    # FIXME: do a ionice here too?
    
    # init
    apt_pkg.init()

    # force apt to build its caches in memory for now to make sure
    # that there is no race when the pkgcache file gets re-generated
    apt_pkg.Config.Set("Dir::Cache::pkgcache","")

    # get caches
    try:
        cache = apt_pkg.GetCache(OpNullProgress())
    except SystemError, e:
        sys.stderr.write("E: "+ _("Error: Opening the cache (%s)") % e)
        sys.exit(-1)
    depcache = apt_pkg.GetDepCache(cache)

    # read the pin files
    depcache.ReadPinFile()
    # read the synaptic pins too
    if os.path.exists(SYNAPTIC_PINFILE):
        depcache.ReadPinFile(SYNAPTIC_PINFILE)

    # init the depcache
    depcache.Init()

    if depcache.BrokenCount > 0:
        sys.stderr.write("E: "+ _("Error: BrokenCount > 0"))
        sys.exit(-1)

# do the upgrade (not dist-upgrade!)
    try:
        saveDistUpgrade(cache,depcache)
    except SystemError, e:
        sys.stderr.write("E: "+ _("Error: Marking the upgrade (%s)") % e)
        sys.exit(-1)

    # check for upgrade packages, we need to do it this way
    # because of ubuntu #7907
    upgrades = 0
    security_updates = 0
    for pkg in cache.Packages:
        if depcache.MarkedInstall(pkg) or depcache.MarkedUpgrade(pkg):
            inst_ver = pkg.CurrentVer
            cand_ver = depcache.GetCandidateVer(pkg)
            # check if this is really a upgrade or a false positive
            # (workaround for ubuntu #7907)
	    if cand_ver != inst_ver:
                # check for security upgrades
                upgrades = upgrades + 1	
                if isSecurityUpgrade(cand_ver):
                    security_updates += 1
                # now check for security updates that are masked by a 
                # canidate version from another repo (-proposed or -updates)
                for ver in pkg.VersionList:
                    if (inst_ver and apt_pkg.VersionCompare(ver.VerStr, inst_ver.VerStr) <= 0):
                        #print "skipping '%s' " % ver.VerStr
                        continue
                    if isSecurityUpgrade(ver):
                        security_updates += 1
                        break

    # print the number of upgrades
    if options and options.show_package_names:
        pkgs = filter(lambda pkg: depcache.MarkedInstall(pkg) or depcache.MarkedUpgrade(pkg), cache.Packages)
        sys.stderr.write("\n".join(map(lambda p: p.Name, pkgs)))
    elif options and options.readable_output:
        print gettext.dngettext("update-notifier",
                                "%i package can be updated.",
                                "%i packages can be updated.",
                                upgrades) % upgrades
        print gettext.dngettext("update-notifier",
                                "%i update is a security update.",
                                "%i updates are security updates.",
                                security_updates)  % security_updates
    else:
        # print the number of regular upgrades and the number of 
        # security upgrades
        sys.stderr.write("%s;%s" % (upgrades,security_updates))

    # return the number of upgrades (if its used as a module)
    return(upgrades,security_updates)


if __name__ == "__main__":        
    # setup a exception handler to make sure that uncaught stuff goes
    # to the notifier
    sys.excepthook = _handleException
    
    # gettext
    APP="update-notifier"
    DIR="/usr/share/locale"
    gettext.bindtextdomain(APP, DIR)
    gettext.textdomain(APP)

    # check arguments
    parser = OptionParser()
    parser.add_option("-p",
                      "--package-names",
                      action="store_true",
                      dest="show_package_names",
                      help=_("Show the packages that are going to be installed/upgraded"))
    parser.add_option("--human-readable",
                      "--human-readable",
                      action="store_true",
                      dest="readable_output",
                      help=_("Show human readable output on stdout"))
    (options, args) = parser.parse_args()

    # run it
    run(options)
