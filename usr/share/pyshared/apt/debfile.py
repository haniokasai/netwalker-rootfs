# Copyright (c) 2005-2007 Canonical
#
# AUTHOR:
# Michael Vogt <mvo@ubuntu.com>
#
# This file is part of GDebi
#
# GDebi is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# GDebi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GDebi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""Classes for working with locally available Debian packages."""
from gettext import gettext as _
import os
import sys

import apt_inst
import apt_pkg


# Constants for comparing the local package file with the version in the cache
(VERSION_NONE, VERSION_OUTDATED, VERSION_SAME, VERSION_NEWER) = range(4)


class NoDebArchiveException(IOError):
    """Exception which is raised if a file is no Debian archive."""


class DebPackage(object):
    """A Debian Package (.deb file)."""

    _supported_data_members = ("data.tar.gz", "data.tar.bz2", "data.tar.lzma")

    debug = 0

    def __init__(self, filename=None, cache=None):
        self._cache = cache
        self._need_pkgs = []
        self._sections = {}
        self._installed_conflicts = set()
        self._failure_string = ""
        if filename:
            self.open(filename)

    def open(self, filename):
        " open given debfile "
        self.filename = filename
        if not apt_inst.arCheckMember(open(self.filename), "debian-binary"):
            raise NoDebArchiveException(_("This is not a valid DEB archive, "
                                          "missing '%s' member" %
                                          "debian-binary"))
        control = apt_inst.debExtractControl(open(self.filename))
        self._sections = apt_pkg.ParseSection(control)
        self.pkgname = self._sections["Package"]

    def __getitem__(self, key):
        return self._sections[key]

    @property
    def filelist(self):
        """return the list of files in the deb."""
        files = []

        def extract_cb(what, name, *_):
            files.append(name)

        for member in self._supported_data_members:
            if apt_inst.arCheckMember(open(self.filename), member):
                try:
                    apt_inst.debExtract(open(self.filename), extract_cb,
                                        member)
                    break
                except SystemError:
                    return [_("List of files for '%s'could not be read" %
                              self.filename)]
        return files

    def _is_or_group_satisfied(self, or_group):
        """Return True if at least one dependency of the or-group is satisfied.

        This method gets an 'or_group' and analyzes if at least one dependency
        of this group is already satisfied.
        """
        self._dbg(2, "_checkOrGroup(): %s " % (or_group))

        for dep in or_group:
            depname = dep[0]
            ver = dep[1]
            oper = dep[2]

            # check for virtual pkgs
            if not depname in self._cache:
                if self._cache.isVirtualPackage(depname):
                    self._dbg(3, "_isOrGroupSatisfied(): %s is virtual dep" %
                                 depname)
                    for pkg in self._cache.getProvidingPackages(depname):
                        if pkg.isInstalled:
                            return True
                continue

            inst = self._cache[depname]
            instver = inst.installedVersion
            if instver is not None and apt_pkg.CheckDep(instver, oper, ver):
                return True
        return False

    def _satisfy_or_group(self, or_group):
        """Try to satisfy the or_group."""
        for dep in or_group:
            depname, ver, oper = dep

            # if we don't have it in the cache, it may be virtual
            if not depname in self._cache:
                if not self._cache.isVirtualPackage(depname):
                    continue
                providers = self._cache.getProvidingPackages(depname)
                # if a package just has a single virtual provider, we
                # just pick that (just like apt)
                if len(providers) != 1:
                    continue
                depname = providers[0].name

            # now check if we can satisfy the deps with the candidate(s)
            # in the cache
            pkg = self._cache[depname]
            cand = self._cache._depcache.GetCandidateVer(pkg._pkg)
            if not cand:
                continue
            if not apt_pkg.CheckDep(cand.VerStr, oper, ver):
                continue

            # check if we need to install it
            self._dbg(2, "Need to get: %s" % depname)
            self._need_pkgs.append(depname)
            return True

        # if we reach this point, we failed
        or_str = ""
        for dep in or_group:
            or_str += dep[0]
            if dep != or_group[-1]:
                or_str += "|"
        self._failure_string += _("Dependency is not satisfiable: %s\n" %
                                 or_str)
        return False

    def _check_single_pkg_conflict(self, pkgname, ver, oper):
        """Return True if a pkg conflicts with a real installed/marked pkg."""
        # FIXME: deal with conflicts against its own provides
        #        (e.g. Provides: ftp-server, Conflicts: ftp-server)
        self._dbg(3, "_checkSinglePkgConflict() pkg='%s' ver='%s' oper='%s'" %
                     (pkgname, ver, oper))

        pkg = self._cache[pkgname]
        if pkg.isInstalled:
            pkgver = pkg.installedVersion
        elif pkg.markedInstall:
            pkgver = pkg.candidateVersion
        else:
            return False
        #print "pkg: %s" % pkgname
        #print "ver: %s" % ver
        #print "pkgver: %s " % pkgver
        #print "oper: %s " % oper
        if (apt_pkg.CheckDep(pkgver, oper, ver) and not
            self.replaces_real_pkg(pkgname, oper, ver)):
            self._failure_string += _("Conflicts with the installed package "
                                     "'%s'" % pkg.name)
            return True
        return False

    def _check_conflicts_or_group(self, or_group):
        """Check the or-group for conflicts with installed pkgs."""
        self._dbg(2, "_check_conflicts_or_group(): %s " % (or_group))

        or_found = False
        virtual_pkg = None

        for dep in or_group:
            depname = dep[0]
            ver = dep[1]
            oper = dep[2]

            # check conflicts with virtual pkgs
            if not depname in self._cache:
                # FIXME: we have to check for virtual replaces here as
                #        well (to pass tests/gdebi-test8.deb)
                if self._cache.isVirtualPackage(depname):
                    for pkg in self._cache.getProvidingPackages(depname):
                        self._dbg(3, "conflicts virtual check: %s" % pkg.name)
                        # P/C/R on virtal pkg, e.g. ftpd
                        if self.pkgname == pkg.name:
                            self._dbg(3, "conflict on self, ignoring")
                            continue
                        if self._check_single_pkg_conflict(pkg.name, ver, oper):
                            self._installed_conflicts.add(pkg.name)
                continue
            if self._check_single_pkg_conflict(depname, ver, oper):
                self._installed_conflicts.add(depname)
        return bool(self._installed_conflicts)

    @property
    def conflicts(self):
        """List of package names conflicting with this package."""
        key = "Conflicts"
        try:
            return apt_pkg.ParseDepends(self._sections[key])
        except KeyError:
            return []

    @property
    def depends(self):
        """List of package names on which this package depends on."""
        depends = []
        # find depends
        for key in "Depends", "PreDepends":
            try:
                depends.extend(apt_pkg.ParseDepends(self._sections[key]))
            except KeyError:
                pass
        return depends

    @property
    def provides(self):
        """List of virtual packages which are provided by this package."""
        key = "Provides"
        try:
            return apt_pkg.ParseDepends(self._sections[key])
        except KeyError:
            return []

    @property
    def replaces(self):
        """List of packages which are replaced by this package."""
        key = "Replaces"
        try:
            return apt_pkg.ParseDepends(self._sections[key])
        except KeyError:
            return []

    def replaces_real_pkg(self, pkgname, oper, ver):
        """Return True if a given non-virtual package is replaced.

        Return True if the deb packages replaces a real (not virtual)
        packages named (pkgname, oper, ver).
        """
        self._dbg(3, "replacesPkg() %s %s %s" % (pkgname, oper, ver))
        pkg = self._cache[pkgname]
        if pkg.isInstalled:
            pkgver = pkg.installedVersion
        elif pkg.markedInstall:
            pkgver = pkg.candidateVersion
        else:
            pkgver = None
        for or_group in self.replaces:
            for (name, ver, oper) in or_group:
                if (name == pkgname and apt_pkg.CheckDep(pkgver, oper, ver)):
                    self._dbg(3, "we have a replaces in our package for the "
                                 "conflict against '%s'" % (pkgname))
                    return True
        return False

    def check_conflicts(self):
        """Check if there are conflicts with existing or selected packages.

        Check if the package conflicts with a existing or to be installed
        package. Return True if the pkg is OK.
        """
        res = True
        for or_group in self.conflicts:
            if self._check_conflicts_or_group(or_group):
                #print "Conflicts with a exisiting pkg!"
                #self._failure_string = "Conflicts with a exisiting pkg!"
                res = False
        return res

    def compare_to_version_in_cache(self, use_installed=True):
        """Compare the package to the version available in the cache.

        Checks if the package is already installed or availabe in the cache
        and if so in what version, returns one of (VERSION_NONE,
        VERSION_OUTDATED, VERSION_SAME, VERSION_NEWER).
        """
        self._dbg(3, "compareToVersionInCache")
        pkgname = self._sections["Package"]
        debver = self._sections["Version"]
        self._dbg(1, "debver: %s" % debver)
        if pkgname in self._cache:
            if use_installed:
                cachever = self._cache[pkgname].installedVersion
            else:
                cachever = self._cache[pkgname].candidateVersion
            if cachever is not None:
                cmp = apt_pkg.VersionCompare(cachever, debver)
                self._dbg(1, "CompareVersion(debver,instver): %s" % cmp)
                if cmp == 0:
                    return VERSION_SAME
                elif cmp < 0:
                    return VERSION_NEWER
                elif cmp > 0:
                    return VERSION_OUTDATED
        return VERSION_NONE

    def check(self):
        """Check if the package is installable."""
        self._dbg(3, "checkDepends")

        # check arch
        arch = self._sections["Architecture"]
        if  arch != "all" and arch != apt_pkg.Config.Find("APT::Architecture"):
            self._dbg(1, "ERROR: Wrong architecture dude!")
            self._failure_string = _("Wrong architecture '%s'" % arch)
            return False

        # check version
        if self.compare_to_version_in_cache() == VERSION_OUTDATED:
            # the deb is older than the installed
            self._failure_string = _("A later version is already installed")
            return False

        # FIXME: this sort of error handling sux
        self._failure_string = ""

        # check conflicts
        if not self.check_conflicts():
            return False

        # try to satisfy the dependencies
        if not self._satisfy_depends(self.depends):
            return False

        # check for conflicts again (this time with the packages that are
        # makeed for install)
        if not self.check_conflicts():
            return False

        if self._cache._depcache.BrokenCount > 0:
            self._failure_string = _("Failed to satisfy all dependencies "
                                    "(broken cache)")
            # clean the cache again
            self._cache.clear()
            return False
        return True

    def satisfy_depends_str(self, dependsstr):
        """Satisfy the dependencies in the given string."""
        return self._satisfy_depends(apt_pkg.ParseDepends(dependsstr))

    def _satisfy_depends(self, depends):
        """Satisfy the dependencies."""
        # turn off MarkAndSweep via a action group (if available)
        try:
            _actiongroup = apt_pkg.GetPkgActionGroup(self._cache._depcache)
        except AttributeError:
            pass
        # check depends
        for or_group in depends:
            #print "or_group: %s" % or_group
            #print "or_group satified: %s" % self._is_or_group_satisfied(or_group)
            if not self._is_or_group_satisfied(or_group):
                if not self._satisfy_or_group(or_group):
                    return False
        # now try it out in the cache
        for pkg in self._need_pkgs:
            try:
                self._cache[pkg].markInstall(fromUser=False)
            except SystemError, e:
                self._failure_string = _("Cannot install '%s'" % pkg)
                self._cache.clear()
                return False
        return True

    @property
    def missing_deps(self):
        """Return missing dependencies."""
        self._dbg(1, "Installing: %s" % self._need_pkgs)
        if self._need_pkgs is None:
            self.check()
        return self._need_pkgs

    @property
    def required_changes(self):
        """Get the changes required to satisfy the dependencies.

        Returns: a tuple with (install, remove, unauthenticated)
        """
        install = []
        remove = []
        unauthenticated = []
        for pkg in self._cache:
            if pkg.markedInstall or pkg.markedUpgrade:
                install.append(pkg.name)
                # check authentication, one authenticated origin is enough
                # libapt will skip non-authenticated origins then
                authenticated = False
                for origin in pkg.candidateOrigin:
                    authenticated |= origin.trusted
                if not authenticated:
                    unauthenticated.append(pkg.name)
            if pkg.markedDelete:
                remove.append(pkg.name)
        return (install, remove, unauthenticated)

    def _dbg(self, level, msg):
        """Write debugging output to sys.stderr."""
        if level <= self.debug:
            print >> sys.stderr, msg

    def install(self, install_progress=None):
        """Install the package."""
        if install_progress is None:
            return os.system("dpkg -i %s" % self.filename)
        else:
            try:
                install_progress.start_update()
            except AttributeError:
                install_progress.startUpdate()
            res = install_progress.run(self.filename)
            try:
                install_progress.finish_update()
            except AttributeError:
                install_progress.finishUpdate()
            return res


class DscSrcPackage(DebPackage):
    """A locally available source package."""

    def __init__(self, filename=None, cache=None):
        DebPackage.__init__(self, None, cache)
        self._depends = []
        self._conflicts = []
        self._binaries = []
        if filename is not None:
            self.open(filename)

    @property
    def depends(self):
        """Return the dependencies of the package"""
        return self._depends

    @property
    def conflicts(self):
        """Return the dependencies of the package"""
        return self._conflicts

    def open(self, file):
        """Open the package."""
        depends_tags = ["Build-Depends", "Build-Depends-Indep"]
        conflicts_tags = ["Build-Conflicts", "Build-Conflicts-Indep"]

        fobj = open(file)
        tagfile = apt_pkg.ParseTagFile(fobj)
        sec = tagfile.Section
        try:
            while tagfile.Step() == 1:
                for tag in depends_tags:
                    if not sec.has_key(tag):
                        continue
                    self._depends.extend(apt_pkg.ParseSrcDepends(sec[tag]))
                for tag in conflicts_tags:
                    if not sec.has_key(tag):
                        continue
                    self._conflicts.extend(apt_pkg.ParseSrcDepends(sec[tag]))
                if sec.has_key('Source'):
                    self.pkgname = sec['Source']
                if sec.has_key('Binary'):
                    self.binaries = sec['Binary'].split(', ')
                if sec.has_key('Version'):
                    self._sections['Version'] = sec['Version']
        finally:
            del sec
            del tagfile
            fobj.close()

        s = _("Install Build-Dependencies for "
              "source package '%s' that builds %s\n") % (self.pkgname,
              " ".join(self.binaries))
        self._sections["Description"] = s

    def check(self):
        """Check if the package is installable.."""
        if not self.check_conflicts():
            for pkgname in self._installed_conflicts:
                if self._cache[pkgname]._pkg.Essential:
                    raise Exception(_("An essential package would be removed"))
                self._cache[pkgname].markDelete()
        # FIXME: a additional run of the checkConflicts()
        #        after _satisfyDepends() should probably be done
        return self._satisfy_depends(self.depends)


def _test():
    """Test function"""
    from apt.cache import Cache
    from apt.progress import DpkgInstallProgress

    cache = Cache()

    vp = "www-browser"
    #print "%s virtual: %s" % (vp, cache.isVirtualPackage(vp))
    providers = cache.getProvidingPackages(vp)
    print "Providers for %s :" % vp
    for pkg in providers:
        print " %s" % pkg.name

    d = DebPackage(sys.argv[1], cache)
    print "Deb: %s" % d.pkgname
    if not d.check():
        print "can't be satified"
        print d._failure_string
    print "missing deps: %s" % d.missing_deps
    print d.required_changes

    print "Installing ..."
    ret = d.install(DpkgInstallProgress())
    print ret

    #s = DscSrcPackage(cache, "../tests/3ddesktop_0.2.9-6.dsc")
    #s.checkDep()
    #print "Missing deps: ",s.missingDeps
    #print "Print required changes: ", s.requiredChanges

    s = DscSrcPackage(cache=cache)
    d = "libc6 (>= 2.3.2), libaio (>= 0.3.96) | libaio1 (>= 0.3.96)"
    print s._satisfy_depends(apt_pkg.ParseDepends(d))

if __name__ == "__main__":
    _test()
