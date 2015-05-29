#
# util.py: utility functions for ufw
#
# Copyright (C) 2008-2009 Canonical Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3,
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import errno
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
from tempfile import mkstemp

debugging = False


def get_services_proto(port):
    '''Get the protocol for a specified port from /etc/services'''
    proto = ""
    try:
        socket.getservbyname(port)
    except Exception:
        raise

    try:
        socket.getservbyname(port, "tcp")
        proto = "tcp"
    except Exception:
        pass

    try:
        socket.getservbyname(port, "udp")
        if proto == "tcp":
            proto = "any"
        else:
            proto = "udp"
    except Exception:
        pass

    return proto


def parse_port_proto(str):
    '''Parse port or port and protocol'''
    port = ""
    proto = ""
    tmp = str.split('/')
    if len(tmp) == 1:
        port = tmp[0]
        proto = "any"
    elif len(tmp) == 2:
        port = tmp[0]
        proto = tmp[1]
    else:
        raise ValueError
    return (port, proto)


def valid_address6(addr):
    '''Verifies if valid IPv6 address'''
    if not socket.has_ipv6:
        warn("python does not have IPv6 support.")
        return False

    # quick and dirty test
    if len(addr) > 43 or not re.match(r'^[a-fA-F0-9:\./]+$', addr):
        return False

    net = addr.split('/')
    try:
        socket.inet_pton(socket.AF_INET6, net[0])
    except Exception:
        return False

    if len(net) > 2:
        return False
    elif len(net) == 2:
        # Check netmask specified via '/'
        if not _valid_cidr_netmask(net[1], True):
            return False

    return True


def valid_address4(addr):
    '''Verifies if valid IPv4 address'''
    # quick and dirty test
    if len(addr) > 31 or not re.match(r'^[0-9\./]+$', addr):
        return False

    net = addr.split('/')
    try:
        socket.inet_pton(socket.AF_INET, net[0])
        if not _valid_dotted_quads(net[0], False):
            return False
    except Exception:
        return False

    if len(net) > 2:
        return False
    elif len(net) == 2:
        # Check netmask specified via '/'
        if not valid_netmask(net[1], False):
            return False

    return True


def valid_netmask(nm, v6):
    '''Verifies if valid cidr or dotted netmask'''
    return _valid_cidr_netmask(nm, v6) or _valid_dotted_quads(nm, v6)


#
# valid_address()
#    version="6" tests if a valid IPv6 address
#    version="4" tests if a valid IPv4 address
#    version="any" tests if a valid IP address (IPv4 or IPv6)
#
def valid_address(addr, version="any"):
    '''Validate IP addresses'''
    if version == "6":
        return valid_address6(addr)
    elif version == "4":
        return valid_address4(addr)
    elif version == "any":
        return valid_address4(addr) or valid_address6(addr)

    raise ValueError


def normalize_address(orig, v6):
    '''Convert address to standard form. Use no netmask for IP addresses. If
       If netmask is specified and not all 1's, for IPv4 use cidr if possible, 
       otherwise dotted netmask and for IPv6, use cidr.
    '''
    net = []
    changed = False
    version = "4"
    if v6:
        version = "6"

    if '/' in orig:
        net = orig.split('/')
        # Remove host netmasks
        if v6 and net[1] == "128":
            del net[1]
        elif not v6:
            if net[1] == "32" or net[1] == "255.255.255.255":
                del net[1]
    else:
        net.append(orig)

    if not v6 and len(net) == 2 and _valid_dotted_quads(net[1], v6):
        try:
            net[1] = _dotted_netmask_to_cidr(net[1], v6)
        except Exception:
            # Not valid cidr, so just use the dotted quads
            pass

    addr = net[0]
    if len(net) == 2:
        addr += "/" + net[1]
        if not v6:
            network = _address4_to_network(addr)
            if network != addr:
                dbg_msg = "Using '%s' for address '%s'" % (network, addr)
                debug(dbg_msg)
                addr = network
                changed = True

    if not valid_address(addr, version):
        dbg_msg = "Invalid address '%s'" % (addr)
        debug(dbg_msg)
        raise ValueError

    return (addr, changed)


def open_file_read(f):
    '''Opens the specified file read-only'''
    try:
        orig = open(f, 'r')
    except Exception:
        raise

    return orig


def open_files(f):
    '''Opens the specified file read-only and a tempfile read-write.'''
    try:
        orig = open_file_read(f)
    except Exception:
        raise

    try:
        (tmp, tmpname) = mkstemp()
    except Exception:
        orig.close()
        raise

    return { "orig": orig, "origname": f, "tmp": tmp, "tmpname": tmpname }


def close_files(fns, update = True):
    '''Closes the specified files (as returned by open_files), and update
       original file with the temporary file.
    '''
    fns['orig'].close()
    os.close(fns['tmp'])

    if update:
        try:
            shutil.copystat(fns['origname'], fns['tmpname'])
            shutil.copy(fns['tmpname'], fns['origname'])
        except Exception:
            raise

    try:
        os.unlink(fns['tmpname'])
    except OSError, e:
        raise


def cmd(command):
    '''Try to execute the given command.'''
    debug(command)
    try:
        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError, e:
        return [127, str(e)]

    out = sp.communicate()[0]
    return [sp.returncode,out]


def cmd_pipe(command1, command2):
    '''Try to pipe command1 into command2.'''
    try:
        sp1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
        sp2 = subprocess.Popen(command2, stdin=sp1.stdout)
    except OSError, e:
        return [127, str(e)]

    out = sp2.communicate()[0]
    return [sp2.returncode,out]


def error(msg, exit=True):
    '''Print error message and exit'''
    try:
        print >> sys.stderr, "ERROR: %s" % (msg)
    except IOError:
        pass

    if exit:
        sys.exit(1)


def warn(msg):
    '''Print warning message'''
    try:
        print >> sys.stderr, "WARN: %s" % (msg)
    except IOError:
        pass


def msg(msg, output=sys.stdout):
    '''Print message'''
    try:
        print >> output, "%s" % (msg)
    except IOError:
        pass


def debug(msg):
    '''Print debug message'''
    if debugging:
        try:
            print >> sys.stderr, "DEBUG: %s" % (msg)
        except IOError:
            pass


def word_wrap(text, width):
    '''
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    '''
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )


def wrap_text(text):
    '''Word wrap to a specific width'''
    return word_wrap(text, 75)


def human_sort(list):
    '''Sorts list of strings into numeric order, with text case-insensitive.
       Modifies list in place.

       Eg:
       [ '80', 'a222', 'a32', 'a2', 'b1', '443', 'telnet', '3', 'http', 'ZZZ']

       sorts to:
       ['3', '80', '443', 'a2', 'a32', 'a222', 'b1', 'http', 'telnet', 'ZZZ']
    '''
    norm = lambda t: int(t) if t.isdigit() else t.lower()
    list.sort(key=lambda k: [ norm(c) for c in re.split('([0-9]+)', k)])


def get_ppid(p=os.getpid()):
    '''Finds parent process id for pid based on /proc/<pid>/stat. See
       'man 5 proc' for details.
    '''
    try:
        pid = int(p)
    except:
        raise ValueError("pid must be an integer")

    name = os.path.join("/proc", str(pid), "stat")
    if not os.path.isfile(name):
        raise IOError("Couldn't find '%s'" % (name))

    try:
        ppid = file(name).readlines()[0].split()[3]
    except Exception:
        raise

    return int(ppid)


def under_ssh(pid=os.getpid()):
    '''Determine if current process is running under ssh'''
    try:
        ppid = get_ppid(pid)
    except IOError, e:
        warn_msg = _("Couldn't find pid (is /proc mounted?)")
        warn(warn_msg)
        return False
    except Exception:
        err_msg = _("Couldn't find parent pid for '%s'") % (str(pid))
        raise ValueError(err_msg)

    # pid '1' is 'init' and '0' is the kernel. This should still work when
    # pid randomization is in use, but needs to be checked.
    if pid == 1 or ppid <= 1:
        return False

    path = os.path.join("/proc", str(ppid), "stat")
    if not os.path.isfile(path):
        err_msg = _("Couldn't find '%s'") % (path)
        raise ValueError(err_msg)

    try:
        exe = file(path).readlines()[0].split()[1]
    except:
        err_msg = _("Could not find executable for '%s'") % (path)
        raise ValueError(err_msg)
    debug("under_ssh: exe is '%s'" % (exe))

    if exe == "(sshd)":
        return True
    else:
        return under_ssh(ppid)


#
# Internal helper functions
#
def _valid_cidr_netmask(nm, v6):
    '''Verifies cidr netmasks'''
    num = 32
    if v6:
        num = 128

    if not re.match(r'^[0-9]+$', nm) or int(nm) < 0 or int(nm) > num:
        return False

    return True


def _valid_dotted_quads(nm, v6):
    '''Verifies dotted quad ip addresses and netmasks'''
    if v6:
        return False
    else:
        if re.match(r'^[0-9]+\.[0-9\.]+$', nm):
            quads = re.split('\.', nm)
            if len(quads) != 4:
                return False
            for q in quads:
                if not q or int(q) < 0 or int(q) > 255:
                    return False
        else:
            return False

    return True

#
# _dotted_netmask_to_cidr()
# Returns:
#   cidr integer (0-32 for ipv4 and 0-128 for ipv6)
#
# Raises exception if cidr cannot be found
#
def _dotted_netmask_to_cidr(nm, v6):
    '''Convert netmask to cidr. IPv6 dotted netmasks are not supported.'''
    cidr = ""
    if v6:
        raise ValueError
    else:
        if not _valid_dotted_quads(nm, v6):
            raise ValueError

        mbits = 0
        bits = long(struct.unpack('>L',socket.inet_aton(nm))[0])
        found_one = False
        for n in range(32):
            if (bits >> n) & 1 == 1:
                found_one = True
            else:
                if found_one:
                    mbits = -1
                    break
                else:
                    mbits += 1

        if mbits >= 0 and mbits <= 32:
            cidr = str(32 - mbits)

    if not _valid_cidr_netmask(cidr, v6):
        raise ValueError

    return cidr


#
# _cidr_to_dotted_netmask()
# Returns:
#   dotted netmask string
#
# Raises exception if dotted netmask cannot be found
#
def _cidr_to_dotted_netmask(cidr, v6):
    '''Convert cidr to netmask. IPv6 dotted netmasks not supported.'''
    nm = ""
    if v6:
        raise ValueError
    else:
        if not _valid_cidr_netmask(cidr, v6):
            raise ValueError
        bits = 0L
        for n in range(32):
            if n < int(cidr):
                bits |= 1<<31 - n
        nm = socket.inet_ntoa(struct.pack('>L', bits))

    if not _valid_dotted_quads(nm, v6):
        raise ValueError

    return nm

def _address4_to_network(addr):
    '''Convert an IPv4 address and netmask to a network address'''
    if '/' not in addr:
        debug("_address4_to_network: skipping address without a netmask")
        return addr

    tmp = addr.split('/')
    if len(tmp) != 2 or not _valid_dotted_quads(tmp[0], False):
        raise ValueError

    host = tmp[0]
    orig_nm = tmp[1]

    nm = orig_nm
    if _valid_cidr_netmask(nm, False):
        try:
            nm = _cidr_to_dotted_netmask(nm, False)
        except Exception:
            raise

    # Now have dotted quad host and nm, find the network
    host_bits = long(struct.unpack('>L',socket.inet_aton(host))[0])
    nm_bits = long(struct.unpack('>L',socket.inet_aton(nm))[0])

    network_bits = host_bits & nm_bits
    network = socket.inet_ntoa(struct.pack('>L', network_bits))

    return network + "/" + orig_nm

def get_iptables_version():
    '''Return iptables version'''
    exe = 'iptables'
    (rc, out) = cmd([exe, '-V'])
    if rc != 0:
        raise OSError(errno.ENOENT, "Error running '%s'" % (exe))
    tmp = re.split('\s', out)
    return re.sub('^v', '', tmp[1])

