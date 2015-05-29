#
# common.py: common classes for ufw
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

import re
import socket
import ufw.util
from ufw.util import debug

programName = "ufw"
state_dir = "/var/lib/ufw"
config_dir = "/etc"
prefix_dir = "/usr"

class UFWError(Exception):
    '''This class represents ufw exceptions'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UFWRule:
    '''This class represents firewall rules'''
    def __init__(self, action, protocol, dport="any", dst="0.0.0.0/0",
                 sport="any", src="0.0.0.0/0"):
        # Be sure to update dup_rule accordingly...
        self.remove = False
        self.updated = False
        self.v6 = False
        self.dst = ""
        self.src = ""
        self.dport = ""
        self.sport = ""
        self.protocol = ""
        self.multi = False
        self.dapp = ""
        self.sapp = ""
        self.action = ""
        self.position = 0
        self.logtype = ""
        try:
            self.set_action(action)
            self.set_protocol(protocol)
            self.set_port(dport)
            self.set_port(sport, "src")
            self.set_src(src)
            self.set_dst(dst)
        except UFWError:
            raise

    def __str__(self):
        return self.format_rule()

    def dup_rule(self):
        '''Return a duplicate of a rule'''
        rule = UFWRule(self.action, self.protocol)
        rule.remove = self.remove
        rule.updated = self.updated
        rule.v6 = self.v6
        rule.dst = self.dst
        rule.src = self.src
        rule.dport = self.dport
        rule.sport = self.sport
        rule.multi = self.multi
        rule.dapp = self.dapp
        rule.sapp = self.sapp
        rule.position = self.position
        rule.logtype = self.logtype

        return rule

    def format_rule(self):
        '''Format rule for for later parsing'''
        str = ""

        # Protocol is handled below
        if self.protocol == "any":
            str = " -p all"
        else:
            str = " -p " + self.protocol

            if self.multi:
                str += " -m multiport"
                if self.dport != "any" and self.sport != "any":
                    str += " --dports " + self.dport
                    str += " -m multiport"
                    str += " --sports " + self.sport
                elif self.dport != "any":
                    str += " --dports " + self.dport
                elif self.sport != "any":
                    str += " --sports " + self.sport

        if self.dst != "0.0.0.0/0" and self.dst != "::/0":
            str += " -d " + self.dst
        if not self.multi and self.dport != "any":
            str += " --dport " + self.dport
        if self.src != "0.0.0.0/0" and self.src != "::/0":
            str += " -s " + self.src
        if not self.multi and self.sport != "any":
            str += " --sport " + self.sport

        lstr = ""
        if self.logtype != "":
            lstr = "_" + self.logtype
        if self.action == "allow":
            str += " -j ACCEPT%s" % (lstr)
        elif self.action == "reject":
            str += " -j REJECT%s" % (lstr)
            if self.protocol == "tcp":
                # follow TCP's default and send RST
                str += " --reject-with tcp-reset"
        elif self.action == "limit":
            # Caller needs to change this
            str += " -j LIMIT%s" % (lstr)
        else:
            str += " -j DROP%s" % (lstr)

        if self.dapp != "" or self.sapp != "":
            # Format the comment string, and quote it just in case
            comment = "-m comment --comment '"
            pat_space = re.compile(' ')
            if self.dapp != "":
                comment += "dapp_" + pat_space.sub('%20', self.dapp)
            if self.dapp != "" and self.sapp != "":
                comment += ","
            if self.sapp != "":
                comment += "sapp_" + pat_space.sub('%20', self.sapp)
            comment += "'"

            str += " " + comment

        return str.strip()

    def set_action(self, action):
        '''Sets action of the rule'''
        tmp = action.lower().split('_')
        if tmp[0] == "allow" or tmp[0] == "reject" or tmp[0] == "limit":
            self.action = tmp[0]
        else:
            self.action = "deny"

        logtype = ""
        if len(tmp) > 1:
             logtype = tmp[1]
        self.set_logtype(logtype)

    def set_port(self, port, loc="dst"):
        '''Sets port and location (destination or source) of the rule'''
        err_msg = _("Bad port '%s'") % (port)
        if port == "any":
            pass
        elif loc == "dst" and self.dapp:
            pass
        elif loc == "src" and self.sapp:
            pass
        elif re.match(r'^[,:]', port) or re.match(r'[,:]$', port):
            raise UFWError(err_msg)
        elif (port.count(',') + port.count(':')) > 14:
            # Limitation of iptables
            raise UFWError(err_msg)
        else:
            ports = port.split(',')
            if len(ports) < 1:
                raise UFWError(err_msg)
            elif len(ports) > 1:
                self.multi = True

            tmp = ""
            for p in ports:
                if re.match(r'^\d+:\d+$', p):
                    # Port range
                    self.multi = True
                    ran = p.split(':')
                    if len(ran) != 2:
                        raise UFWError(err_msg)
                    for q in ran:
                        if int(q) < 1 or int(q) > 65535:
                            raise UFWError(err_msg)
                    if int(ran[0]) >= int(ran[1]):
                        raise UFWError(err_msg)
                elif re.match('^\d+$', p):
                    if int(p) < 1 or int(p) > 65535:
                        raise UFWError(err_msg)
                elif re.match(r'^\w[\w\-]+', p):
                    try:
                        p = socket.getservbyname(p)
                    except Exception, (error):
                        raise UFWError(err_msg)
                else:
                    raise UFWError(err_msg)

                if tmp:
                    tmp += "," + str(p)
                else:
                    tmp = str(p)

            port = tmp

        if loc == "src":
            self.sport = str(port)
        else:
            self.dport = str(port)

    def set_protocol(self, protocol):
        '''Sets protocol of the rule'''
        if protocol == "tcp" or protocol == "udp" or protocol == "any":
            self.protocol = protocol
        else:
            err_msg = _("Unsupported protocol '%s'") % (protocol)
            raise UFWError(err_msg)

    def _fix_anywhere(self):
        '''Adjusts src and dst based on v6'''
        if self.v6:
            if self.dst and (self.dst == "any" or self.dst == "0.0.0.0/0"):
                self.dst = "::/0"
            if self.src and (self.src == "any" or self.src == "0.0.0.0/0"):
                self.src = "::/0"
        else:
            if self.dst and (self.dst == "any" or self.dst == "::/0"):
                self.dst = "0.0.0.0/0"
            if self.src and (self.src == "any" or self.src == "::/0"):
                self.src = "0.0.0.0/0"

    def set_v6(self, v6):
        '''Sets whether this is ipv6 rule, and adjusts src and dst 
           accordingly.
        '''
        self.v6 = v6
        self._fix_anywhere()

    def set_src(self, addr):
        '''Sets source address of rule'''
        tmp = addr.lower()

        if tmp != "any" and not ufw.util.valid_address(tmp, "any"):
            err_msg = _("Bad source address")
            raise UFWError(err_msg)
        self.src = tmp
        self._fix_anywhere()

    def set_dst(self, addr):
        '''Sets destination address of rule'''
        tmp = addr.lower()

        if tmp != "any" and not ufw.util.valid_address(tmp, "any"):
            err_msg = _("Bad destination address")
            raise UFWError(err_msg)
        self.dst = tmp
        self._fix_anywhere()

    def set_position(self, num):
        '''Sets the position of the rule'''
        if not re.match(r'^[0-9]+', str(num)):
            err_msg = _("Insert position '%s' is not a valid position") % (num)
            raise UFWError(err_msg)
        self.position = int(num)

    def set_logtype(self, logtype):
        '''Sets logtype of the rule'''
        if logtype.lower() == "log" or logtype.lower() == "log-all" or \
           logtype == "":
            self.logtype = logtype.lower()
        else:
            err_msg = _("Invalid log type '%s'") % (logtype)
            raise UFWError(err_msg)

    def normalize(self):
        '''Normalize src and dst to standard form'''
        changed = False
        if self.src:
            try:
                (self.src, changed) = ufw.util.normalize_address(self.src, \
                                                                 self.v6)
            except Exception:
                raise
                err_msg = _("Could not normalize source address")
                raise UFWError(err_msg)
        if changed:
            self.updated = changed

        if self.dst:
            try:
                (self.dst, changed) = ufw.util.normalize_address(self.dst, \
                                                                   self.v6)
            except Exception:
                err_msg = _("Could not normalize destination address")
                raise UFWError(err_msg)

        if self.dport:
            ports = self.dport.split(',')
            ufw.util.human_sort(ports)
            self.dport = ','.join(ports)

        if self.sport:
            ports = self.sport.split(',')
            ufw.util.human_sort(ports)
            self.sport = ','.join(ports)

        if changed:
            self.updated = changed

    def match(x, y):
        '''Check if rules match
        Return codes:
          0  match
          1  no match
         -1  match all but action
        '''
        if not x or not y:
            raise ValueError()

        dbg_msg = _("No match")
        if x.dport != y.dport:
            debug(dbg_msg)
            return 1
        if x.sport != y.sport:
            debug(dbg_msg)
            return 1
        if x.protocol != y.protocol:
            debug(dbg_msg)
            return 1
        if x.src != y.src:
            debug(dbg_msg)
            return 1
        if x.dst != y.dst:
            debug(dbg_msg)
            return 1
        if x.v6 != y.v6:
            debug(dbg_msg)
            return 1
        if x.dapp != y.dapp:
            debug(dbg_msg)
            return 1
        if x.sapp != y.sapp:
            debug(dbg_msg)
            return 1
        if x.action == y.action and x.logtype == y.logtype:
            dbg_msg = _("Found exact match")
            debug(dbg_msg)
            return 0
        dbg_msg = _("Found non-action/non-logtype match (%s/%s %s/%s)") % \
                    (x.action, y.action, x.logtype, y.logtype)
        debug(dbg_msg)
        return -1

    def get_app_tuple(self):
        '''Returns a tuple to identify an app rule'''
        tuple = ""
        if self.dapp != "" or self.sapp != "":
            tuple = "%s %s %s %s" % (self.dapp, self.dst, self.sapp, self.src)
            if self.dapp == "":
                tuple = "%s %s %s %s" % (self.dport, self.dst, self.sapp, \
                                         self.src)
            if self.sapp == "":
                tuple = "%s %s %s %s" % (self.dapp, self.dst, self.sport, \
                                         self.src)

        return tuple

