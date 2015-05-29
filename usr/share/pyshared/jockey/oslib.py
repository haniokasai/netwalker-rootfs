# -*- coding: UTF-8 -*-
# (c) 2007 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''Encapsulate operations which are Linux distribution specific.'''

import fcntl, os, subprocess, sys, logging, re, tempfile
from glob import glob

import warnings
warnings.simplefilter('ignore', FutureWarning)
import apt

class _CapturedInstallProgress(apt.InstallProgress):
    def fork(self):
        '''Reroute stdout/stderr to files, so that we can log them'''

        self.stdout = tempfile.TemporaryFile()
        self.stderr = tempfile.TemporaryFile()
        p = os.fork()
        if p == 0:
            os.dup2(self.stdout.fileno(), sys.stdout.fileno())
            os.dup2(self.stderr.fileno(), sys.stderr.fileno())
        return p

class OSLib:
    '''Encapsulation of operating system/Linux distribution specific operations.'''

    # global default instance
    inst = None

    def __init__(self, client_only=False):
        '''Set default paths and load the module blacklist.
        
        Distributors might want to override some default paths.
        If client_only is True, this only initializes functionality which is
        needed by clients, and which can be done without special privileges.
        '''
        # relevant stuff for clients and backend
        self._get_os_version()
        self.hal_get_property_path = '/usr/bin/hal-get-property'

        if client_only:
            return

        # below follows stuff which is only necessary for the backend

        # default paths

        # /sys/ path; the main purpose of changing this is for test
        # suites, but some vendors might have /sys in a nonstandard place
        self.sys_dir = '/sys'

        # path to a modprobe.d configuration file where kernel modules are
        # enabled and disabled with blacklisting
        self.module_blacklist_file = '/etc/modprobe.d/blacklist-local.conf'

        # path to modinfo binary
        self.modinfo_path = '/sbin/modinfo'

        # path to modprobe binary
        self.modprobe_path = '/sbin/modprobe'

        # path to kernel's list of loaded modules
        self.proc_modules = '/proc/modules'

        # default path to custom handlers
        self.handler_dir = '/usr/share/jockey/handlers'

        # default paths to modalias files (directory entries will consider all
        # files in them)
        self.modaliases = [
            '/lib/modules/%s/modules.alias' % os.uname()[2],
            '/usr/share/jockey/modaliases/',
        ]

        # path to X.org configuration file
        self.xorg_conf_path = '/etc/X11/xorg.conf'

        self.set_backup_dir()

        # cache file for previously seen/newly used handlers lists (for --check)
        self.check_cache = os.path.join(self.backup_dir, 'check')

        self._load_module_blacklist()

        self.apt_show_cache = {}
        self.apt_sources = '/etc/apt/sources.list'
        self.apt_jockey_source = '/etc/apt/sources.list.d/jockey.list'

    # 
    # The following package related functions use PackageKit; if that does not
    # work for your distribution, they must be reimplemented
    #

    def _apt_show(self, package):
        '''Return apt-cache show output, with caching.
        
        Return None if the package does not exist.
        '''
        try:
            return self.apt_show_cache[package]
        except KeyError:
            apt = subprocess.Popen(['apt-cache', 'show', package],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = apt.communicate()[0].strip()
            if apt.returncode == 0 and out:
                result = out
            else:
                result = None
            self.apt_show_cache[package] = result
            return result

    def is_package_free(self, package):
        '''Return if given package is free software.'''

        # TODO: this only works for packages in the official archive
        out = self._apt_show(package)
        if out:
            for l in out.splitlines():
                if l.startswith('Section:'):
                    s = l.split()[-1]
                    return not (s.startswith('restricted') or s.startswith('multiverse'))

        raise ValueError, 'package %s does not exist' % package

    def package_installed(self, package):
        '''Return if the given package is installed.'''

        dpkg = subprocess.Popen(["dpkg-query", "-W", "-f${Status}", package],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = dpkg.communicate()[0]
        return dpkg.returncode == 0 and out.split()[-1] == "installed"

    def package_description(self, package):
        '''Return a tuple (short_description, long_description) for a package.
        
        This should raise a ValueError if the package is not available.
        '''
        out = self._apt_show(package)
        if out:
            lines = out.splitlines()
            start = 0
            while start < len(lines)-1:
                if lines[start].startswith('Description:'):
                    break
                start += 1

            short = lines[start].split(' ', 1)[1]
            long = ''
            for l in lines[start+1:]:
                if l == ' .':
                    long += '\n\n'
                elif l.startswith(' '):
                    long += l.lstrip()
                else:
                    break

            return (short, long)

        raise ValueError, 'package %s does not exist' % package

    def package_files(self, package):
        '''Return a list of files shipped by a package.
        
        This should raise a ValueError if the package is not installed.
        '''
        pkcon = subprocess.Popen(['dpkg', '-L', package],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = pkcon.communicate()[0]
        if pkcon.returncode == 0:
            return out.splitlines()
        else:
            raise ValueError, 'package %s is not installed' % package

    # 
    # The following functions MUST be implemented by distributors
    #

    def install_package(self, package, progress_cb):
        '''Install the given package.

        As this is called in the backend, this must happen noninteractively.
        For progress reporting, progress_cb(phase, current, total) is called
        regularly, with 'phase' being 'download' or 'install'. If the callback
        returns True, the installation is attempted to get cancelled (this
        will probably succeed in the 'download' phase, but not in 'install').
        Passes '-1' for current and/or total if time cannot be determined.

        If this succeeds, subsequent package_installed(package) calls must
        return True.

        Any installation failure should be raised as a SystemError.
        '''
        class MyFetchProgress(apt.FetchProgress):
            def __init__(self, callback):
                apt.FetchProgress.__init__(self)
                self.callback = callback

            def pulse(self):
                return not self.callback('download', int(self.percent/2+.5), 100)

        class MyInstallProgress(_CapturedInstallProgress):
            def __init__(self, callback):
                _CapturedInstallProgress.__init__(self)
                self.callback = callback

            def statusChange(self, pkg, percent, status):
                logging.debug('install progress statusChange %s %f' % (pkg, percent))
                self.callback('install', int(percent/2+50.5), 100)

        logging.debug('Installing package: %s', package)
        if progress_cb:
            progress_cb('download', 0, 100.0)

        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        os.environ['PATH'] = '/sbin:/usr/sbin:/bin:/usr/bin'
        apt.apt_pkg.Config.Set('DPkg::options::','--force-confnew')

        c = apt.Cache()
        try:
            try:
                c[package].markInstall()
            except KeyError:
                logging.debug('Package %s does not exist, aborting', package)
                return False
            inst_p = progress_cb and MyInstallProgress(progress_cb) or None
            c.commit(progress_cb and MyFetchProgress(progress_cb) or None, inst_p)
            if inst_p:
                inst_p.stdout.seek(0)
                out = inst_p.stdout.read()
                inst_p.stdout.close()
                inst_p.stderr.seek(0)
                err = inst_p.stderr.read()
                inst_p.stderr.close()

                if out:
                    logging.debug(out)
                if err:
                    logging.error(err)
        except apt.cache.FetchCancelledException, e:
            return False
        except (apt.cache.LockFailedException, apt.cache.FetchFailedException), e:
            logging.warning('Package fetching failed: %s', str(e))
            raise SystemError, str(e)
        return True

    def remove_package(self, package, progress_cb):
        '''Uninstall the given package.

        As this is called in the backend, this must happen noninteractively.
        For progress reporting, progress_cb(current, total) is called
        regularly. Passes '-1' for current and/or total if time cannot be
        determined.

        If this succeeds, subsequent package_installed(package) calls must
        return False.

        Any removal failure should be raised as a SystemError.
        '''
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        os.environ['PATH'] = '/sbin:/usr/sbin:/bin:/usr/bin'
        
        class MyInstallProgress(_CapturedInstallProgress):
            def __init__(self, callback):
                _CapturedInstallProgress.__init__(self)
                self.callback = callback

            def statusChange(self, pkg, percent, status):
                logging.debug('remove progress statusChange %s %f' % (pkg, percent))
                self.callback(percent, 100.0)

        logging.debug('Removing package: %s', package)

        c = apt.Cache()
        try:
            try:
                c[package].markDelete()
            except KeyError:
                logging.debug('Package %s does not exist, aborting', package)
                return False
            inst_p = progress_cb and MyInstallProgress(progress_cb) or None
            c.commit(None, inst_p)
            if inst_p:
                inst_p.stdout.seek(0)
                out = inst_p.stdout.read()
                inst_p.stdout.close()
                inst_p.stderr.seek(0)
                err = inst_p.stderr.read()
                inst_p.stderr.close()

                if out:
                    logging.debug(out)
                if err:
                    logging.error(err)
        except apt.cache.LockFailedException, e:
            logging.debug('could not lock apt cache, aborting: %s', str(e))
            raise SystemError, str(e)

        return True

    def packaging_system(self):
        '''Return packaging system.

        Currently defined values: apt
        '''
        # apt
        if os.path.exists('/etc/apt/sources.list') or os.path.exists(
            '/etc/apt/sources.list.d'):
            return 'apt'

        raise NotImplementedError, 'local packaging system is unknown'

    def add_repository(self, repository):
        '''Add a repository.

        The format for repository is distribution specific. This function
        should also download/update the package index for this repository.

        This should throw a ValueError if the repository is invalid or
        inaccessible.
        '''
        if self.repository_enabled(repository):
            logging.debug('add_repository(%s): already active', repository)
            return

        if os.path.exists(self.apt_jockey_source):
            backup = self.apt_jockey_source + '.bak'
            os.rename(self.apt_jockey_source, backup)
        else:
            backup = None
        f = open(self.apt_jockey_source, 'w')
        print >> f, repository.strip()
        f.close()

        try:
            # TODO: progress feedback
            c = apt.Cache()
            c.update()
        except SystemError, e:
            logging.error('add_repository(%s): Invalid repository', repository)
            if backup:
                os.rename(backup, self.apt_jockey_source)
            else:
                os.unlink(self.apt_jockey_source)
            raise ValueError(e.message)
        except apt.cache.FetchCancelledException, e:
            return False
        except (apt.cache.LockFailedException, apt.cache.FetchFailedException), e:
            logging.warning('Package fetching failed: %s', str(e))
            raise SystemError, str(e)

    def remove_repository(self, repository):
        '''Remove a repository.

        The format for repository is distribution specific.
        '''
        if not os.path.exists(self.apt_jockey_source):
            return
        result = []
        for line in open(self.apt_jockey_source):
            if line.strip() != repository:
                result.append(line)
        if result:
            f = open(self.apt_jockey_source, 'w')
            f.write('\n'.join(result))
            f.close()
        else:
            os.unlink(self.apt_jockey_source)

    def repository_enabled(self, repository):
        '''Check if given repository is enabled.'''

        for f in [self.apt_sources] + glob(self.apt_sources + '.d/*.list'):
            try:
                logging.debug('repository_enabled(%s): checking %s', repository, f)
                for line in open(f):
                    if line.strip() == repository:
                        logging.debug('repository_enabled(%s): match', repository)
                        return True
            except IOError:
                pass
        logging.debug('repository_enabled(%s): no match', repository)
        return False

    def ui_help_available(self, ui):
        '''Return if help is available.

        This gets the current UI object passed, which can be used to determine
        whether GTK/KDE is used, etc.
        '''
        return os.access('/usr/bin/yelp', os.X_OK)

    def ui_help(self, ui):
        '''The UI's help button was clicked.

        This should open a help HTML page or website, call yelp with an
        appropriate topic, etc. This gets the current UI object passed, which
        can be used to determine whether GTK/KDE is used, etc.
        '''
        if 'gtk' in str(ui.__class__).lower():
            import gobject
            gobject.spawn_async(["yelp", "ghelp:hardware#restricted-manager"],
                flags=gobject.SPAWN_SEARCH_PATH)

    # 
    # The following functions have a reasonable default implementation for
    # Linux, but can be tweaked by distributors
    #

    def set_backup_dir(self):
        '''Setup self.backup_dir, directory where backup files are stored.
        
        This is used for old xorg.conf, DriverDB caches, etc.
        '''
        self.backup_dir = '/var/cache/jockey'
        if not os.path.isdir(self.backup_dir):
            try:
                os.makedirs(self.backup_dir)
            except OSError, e:
                logging.error('Could not create %s: %s, using temporary '
                    'directory; all your caches will be lost!',
                    self.backup_dir, str(e))
                self.backup_dir = tempfile.mkdtemp(prefix='jockey_cache')

    def ignored_modules(self):
        '''Return a set of kernel modules which should be ignored.

        This particularly effects free kernel modules which are shipped by the
        OS vendor by default, and thus should not be controlled with this
        program.  Since this will include the large majority of existing kernel
        modules, implementing this is also important for speed reasons; without
        it, detecting existing modules will take quite long.
        
        Note that modules which are ignored here, but covered by a custom
        handler will still be considered.
        '''
        # try to get a *.ko file list from the main kernel package to avoid testing
        # known-free drivers
        dpkg = subprocess.Popen(['dpkg', '-L', 'linux-image-' + os.uname()[2]],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = dpkg.communicate()[0]
        result = set()
        if dpkg.returncode == 0:
            for l in out.splitlines():
                if l.endswith('.ko'):
                    result.add(os.path.splitext(os.path.basename(l))[0].replace('-', '_'))

        dpkg = subprocess.Popen(['dpkg', '-L', 'linux-ubuntu-modules-' + os.uname()[2]],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = dpkg.communicate()[0]
        if dpkg.returncode == 0:
            for l in out.splitlines():
                if l.endswith('.ko'):
                    result.add(os.path.splitext(os.path.basename(l))[0].replace('-', '_'))

        return result

    def module_blacklisted(self, module):
        '''Check if a module is on the modprobe blacklist.'''

        return module in self._module_blacklist or \
            module in self._module_blacklist_system

    def blacklist_module(self, module, blacklist):
        '''Add or remove a kernel module from the modprobe blacklist.
        
        If blacklist is True, the module is blacklisted, otherwise it is
        removed from the blacklist.
        '''
        if blacklist:
            self._module_blacklist.add(module)
        else:
            try:
                self._module_blacklist.remove(module)
            except KeyError:
                return # no need to save the blacklist

        self._save_module_blacklist()

    def _load_module_blacklist(self):
        '''Initialize self._module_blacklist{,_system}.'''

        self._module_blacklist = set()
        self._module_blacklist_system = set()

        self._read_blacklist_file(self.module_blacklist_file, self._module_blacklist)

        # read other blacklist files (which we will not touch, but evaluate)
        for f in glob('%s/blacklist*' % os.path.dirname(self.module_blacklist_file)):
            if f != self.module_blacklist_file:
                self._read_blacklist_file(f, self._module_blacklist_system)

    @classmethod
    def _read_blacklist_file(klass, path, blacklist_set):
        '''Read a blacklist file and add modules to blacklist_set.'''

        try:
            f = open(path)
        except IOError:
            return

        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            for line in f:
                # strip off comments
                line = line[:line.find('#')].strip()

                if not line.startswith('blacklist'):
                    continue

                module = line[len('blacklist'):].strip()
                if module:
                    blacklist_set.add(module)
        finally:
            f.close()

    def _save_module_blacklist(self):
        '''Save module blacklist.'''

        if len(self._module_blacklist) == 0 and \
            os.path.exists(self.module_blacklist_file):
                os.unlink(self.module_blacklist_file)
                return

        os.umask(022)
        # create directory if it does not exist
        d = os.path.dirname(self.module_blacklist_file)
        if not os.path.exists(d):
            os.makedirs(d)

        f = open(self.module_blacklist_file, 'w')
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            for module in sorted(self._module_blacklist):
                print >> f, 'blacklist', module
        finally:
            f.close()

    def _get_os_version(self):
        '''Initialize self.os_vendor and self.os_version.

        This defaults to reading the values from lsb_release.
        '''
        p = subprocess.Popen(['lsb_release', '-si'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, close_fds=True)
        self.os_vendor = p.communicate()[0].strip()
        p = subprocess.Popen(['lsb_release', '-sr'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, close_fds=True)
        self.os_version = p.communicate()[0].strip()
        assert p.returncode == 0

    def get_system_vendor_product(self):
        '''Return (vendor, product) of the system hardware.

        Either or both can be '' if they cannot be determined.

        The default implementation queries hal.
        '''

        try:
            hal = subprocess.Popen([self.hal_get_property_path, '--udi',
                '/org/freedesktop/Hal/devices/computer', '--key',
                'system.hardware.vendor'], stdout=subprocess.PIPE,
                close_fds=True)
            vendor = hal.communicate()[0].strip()
            assert hal.returncode == 0
        except (OSError, AssertionError):
            vendor = ''

        try:
            hal = subprocess.Popen([self.hal_get_property_path, '--udi',
                '/org/freedesktop/Hal/devices/computer', '--key',
                'system.hardware.product'], stdout=subprocess.PIPE,
                close_fds=True)
            product = hal.communicate()[0].strip()
            assert hal.returncode == 0
        except (OSError, AssertionError):
            product = ''

        return (vendor, product)
