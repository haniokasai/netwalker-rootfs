#
# backend_iptables.py: iptables backend for ufw
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

import os
import re
import sys
import tempfile

from ufw.common import UFWError, UFWRule, config_dir, state_dir, prefix_dir
from ufw.util import warn, debug, msg, cmd, cmd_pipe
import ufw.backend


class UFWBackendIptables(ufw.backend.UFWBackend):
    def __init__(self, d):
        self.comment_str = "# " + ufw.common.programName + "_comment #"

        files = {}
        files['rules'] = os.path.join(state_dir, 'user.rules')
        files['before_rules'] = os.path.join(config_dir, 'ufw/before.rules')
        files['after_rules'] = os.path.join(config_dir, 'ufw/after.rules')
        files['rules6'] = os.path.join(state_dir, 'user6.rules')
        files['before6_rules'] = os.path.join(config_dir, 'ufw/before6.rules')
        files['after6_rules'] = os.path.join(config_dir, 'ufw/after6.rules')
        files['init'] = os.path.join(prefix_dir, 'share/ufw/ufw-init')

        ufw.backend.UFWBackend.__init__(self, "iptables", d, files)

        self.chains = {'before': [], 'user': [], 'after': [], 'misc': []}
        for ver in ['4', '6']:
            chain_prefix = "ufw"
            if ver == "6":
                if self.use_ipv6():
                    chain_prefix += ver
                elif ver == "6":
                    continue

            for loc in ['before', 'user', 'after']:
                for target in ['input', 'output', 'forward']:
                   chain = "%s-%s-logging-%s" % (chain_prefix, loc, target)
                   self.chains[loc].append(chain)
            self.chains['misc'].append(chain_prefix + "-logging-deny")
            self.chains['misc'].append(chain_prefix + "-logging-allow")

    def get_default_policy(self, primary="input"):
        '''Get current policy'''
        policy = "default_" + primary + "_policy"

        rstr = ""
        if self.defaults[policy] == "accept":
            rstr = "allow"
        elif self.defaults[policy] == "reject":
            rstr = "reject"
        else:
            rstr = "deny"

        return rstr

    def get_default_application_policy(self):
        '''Get current policy'''
        rstr = _("New profiles:")
        if self.defaults['default_application_policy'] == "accept":
            rstr += " allow"
        elif self.defaults['default_application_policy'] == "drop":
            rstr += " deny"
        elif self.defaults['default_application_policy'] == "reject":
            rstr += " reject"
        else:
            rstr += " skip"

        return rstr

    def set_default_policy(self, policy):
        '''Sets default policy of firewall'''
        if not self.dryrun:
            if policy != "allow" and policy != "deny" and policy != "reject":
                err_msg = _("Unsupported policy '%s'") % (policy)
                raise UFWError(err_msg)

            old_log_str = ''
            new_log_str = ''
            if policy == "allow":
                self.set_default(self.files['defaults'], \
                                            "DEFAULT_INPUT_POLICY", \
                                            "\"ACCEPT\"")
                old_log_str = 'UFW BLOCK'
                new_log_str = 'UFW ALLOW'
            elif policy == "reject":
                self.set_default(self.files['defaults'], \
                                            "DEFAULT_INPUT_POLICY", \
                                            "\"REJECT\"")
                old_log_str = 'UFW ALLOW'
                new_log_str = 'UFW BLOCK'
            else:
                self.set_default(self.files['defaults'], \
                                            "DEFAULT_INPUT_POLICY", \
                                            "\"DROP\"")
                old_log_str = 'UFW ALLOW'
                new_log_str = 'UFW BLOCK'

            # Switch logging message in catch-all rules
            pat = re.compile(r'' + old_log_str)
            for f in [self.files['after_rules'], self.files['after6_rules']]:
                try:
                    fns = ufw.util.open_files(f)
                except Exception:
                    raise
                fd = fns['tmp']

                for line in fns['orig']:
                    if pat.search(line):
                        os.write(fd, pat.sub(new_log_str, line))
                    else:
                        os.write(fd, line)

                ufw.util.close_files(fns)

        rstr = _("Default policy changed to '%s'\n") % (policy)
        rstr += _("(be sure to update your rules accordingly)")

        return rstr

    def get_running_raw(self):
        '''Show current running status of firewall'''
        if self.dryrun:
            out = "> " + _("Checking raw iptables\n")
            out += "> " + _("Checking raw ip6tables\n")
            return out

        err_msg = _("problem running")

        out = "IPV4:\n"
        for table in ['filter', 'nat', 'mangle', 'raw']:
            (rc, tmp) = cmd(['iptables', '-L', '-n', '-v', '-x', '-t', table])
            out += tmp
            if rc != 0:
                raise UFWError(out)

        out += "\n\nIPV6:\n"
        for table in ['filter', 'mangle', 'raw']:
            (rc, tmp) = cmd(['ip6tables', '-L', '-n', '-v', '-x', '-t', table])
            out += tmp
            if rc != 0:
                raise UFWError(out)

        return out

    def get_status(self, verbose=False, show_count=False):
        '''Show ufw managed rules'''
        out = ""
        out6 = ""
        if self.dryrun:
            out = "> " + _("Checking iptables\n")
            if self.use_ipv6():
                out += "> " + _("Checking ip6tables\n")
            return out

        # Is the firewall loaded at all?
        (rc, out) = cmd(['iptables', '-L', 'ufw-user-input', '-n'])
        if rc != 0:
            return _("Status: inactive")

        err_msg = _("problem running")
        if self.use_ipv6():
            (rc, out6) = cmd(['ip6tables', '-L', 'ufw6-user-input', '-n'])
            if rc != 0:
                raise UFWError(err_msg + " ip6tables")

        if out == "" and out6 == "":
            return _("Status: active")

        str = ""
        rules = self.rules + self.rules6
        count = 1
        app_rules = {}
        for r in rules:
            location = {}
            tuple = ""
            show_proto = True
            if not verbose and (r.dapp != "" or r.sapp != ""):
                show_proto = False
                tuple = r.get_app_tuple()

                if app_rules.has_key(tuple):
                    debug("Skipping found tuple '%s'" % (tuple))
                    continue
                else:
                    app_rules[tuple] = True

            for loc in [ 'dst', 'src' ]:
                location[loc] = ""

                port = ""
                tmp = ""
                if loc == "dst":
                    tmp = r.dst
                    if not verbose and r.dapp != "":
                        port = r.dapp
                        if r.v6 and tmp == "::/0":
                            port += " (v6)"
                    else:
                        port = r.dport
                else:
                    tmp = r.src
                    if not verbose and r.sapp != "":
                        port = r.sapp
                        if r.v6 and tmp == "::/0":
                            port += " (v6)"
                    else:
                        port = r.sport

                if tmp != "0.0.0.0/0" and tmp != "::/0":
                    location[loc] = tmp

                if port != "any":
                    if location[loc] == "":
                        location[loc] = port
                    else:
                        location[loc] += " " + port

                    if show_proto and r.protocol != "any":
                        location[loc] += "/" + r.protocol

                    if verbose:
                        if loc == "dst" and r.dapp != "":
                            location[loc] += " (%s" % (r.dapp)
                            if r.v6 and tmp == "::/0":
                                location[loc] += " (v6)"
                            location[loc] += ")"
                        if loc == "src" and r.sapp != "":
                            location[loc] += " (%s" % (r.sapp)
                            if r.v6 and tmp == "::/0":
                                location[loc] += " (v6)"
                            location[loc] += ")"

                if port == "any":
                    if tmp == "0.0.0.0/0" or tmp == "::/0":
                        location[loc] = "Anywhere"

                        # Show the protocol if Anywhere to Anwhere, have
                        # protocol and source and dest ports are any
                        if show_proto and r.protocol != "any" and \
                           r.dst == r.src and r.dport == r.sport:
                            location[loc] += "/" + r.protocol

                        if tmp == "::/0":
                            location[loc] += " (v6)"
                    else:
                        # Show the protocol if have protocol, and source
                        # and dest ports are any
                        if show_proto and r.protocol != "any" and \
                           r.dport == r.sport:
                            location[loc] += "/" + r.protocol

            if show_count:
                str += "[%2d] " % (count)
            
            log_str = ""
            if r.logtype:
                log_str = " (%s)" % (r.logtype.lower())
            str += "%-26s %-8s%s%s\n" % (location['dst'], r.action.upper(), \
                    location['src'], log_str)
            count += 1

        if str != "":
            header = "\n\n"
            if show_count:
                header += "     "
            header += "%-26s %-8s%s\n" % (_("To"), _("Action"), _("From"))
            if show_count:
                header += "     "
            header += "%-26s %-8s%s\n" % (_("--"), _("------"), _("----"))
            str = header + str

        if verbose:
            (level, logging_str) = self.get_loglevel()
            policy_str = _("Default: %s") % (self.get_default_policy())
            app_policy_str = self.get_default_application_policy()
            return _("Status: active") + "\n%s\n%s\n%s%s" % \
                                                    (logging_str, policy_str, \
                                                     app_policy_str, str)
        else:
            return _("Status: active") + "%s" % (str)

    def stop_firewall(self):
        '''Stops the firewall'''
        err_msg = _("problem running")
        if self.dryrun:
            msg("> " + _("running ufw-init"))
        else:
            (rc, out) = cmd([self.files['init'], 'force-stop'])
            if rc != 0:
                raise UFWError(err_msg + " ufw-init")

    def start_firewall(self):
        '''Starts the firewall'''
        err_msg = _("problem running")
        if self.dryrun:
            msg("> " + _("running ufw-init"))
        else:
            (rc, out) = cmd([self.files['init'], 'start'])
            if rc != 0:
                raise UFWError(err_msg + " ufw-init")

            if not self.defaults.has_key('loglevel') or \
               self.defaults['loglevel'] not in self.loglevels.keys():
                # Add the loglevel if not valid
                try:
                    self.set_loglevel("low")
                except:
                    err_msg = _("Could not set LOGLEVEL")
                    raise UFWError(err_msg)
            else:
                try:
                    self.update_logging(self.defaults['loglevel'])
                except:
                    err_msg = _("Could not load logging rules")
                    raise UFWError(err_msg)

    def _need_reload(self, v6):
        '''Check if all chains exist'''
        if self.dryrun:
            return False

        prefix = "ufw"
        exe = "iptables"
        if v6:
            prefix = "ufw6"
            exe = "ip6tables"

        for chain in [ 'input', 'output', 'forward', 'limit', 'limit-accept' ]:
            if v6 and (chain == "limit" or chain == "limit-accept"):
                continue

            (rc, out) = cmd([exe, '-n', '-L', prefix + "-user-" + chain])
            if rc != 0:
                debug("_need_reload: forcing reload")
                return True

        return False

    def _reload_user_rules(self):
        '''Reload firewall rules file'''
        err_msg = _("problem running")
        if self.dryrun:
            msg("> | iptables-restore")
            if self.use_ipv6():
                msg("> | ip6tables-restore")
        elif self._is_enabled():
            # first flush the user logging chains
            try:
                for c in self.chains['user']:
                    self._chain_cmd(c, ['-F', c])
                    self._chain_cmd(c, ['-Z', c])
            except:
                raise UFWError(err_msg)

            # then restore the system rules
            (rc, out) = cmd_pipe(['cat', self.files['rules']], \
                                 ['iptables-restore', '-n'])
            if rc != 0:
                raise UFWError(err_msg + " iptables")

            if self.use_ipv6():
                (rc, out) = cmd_pipe(['cat', self.files['rules6']], \
                                     ['ip6tables-restore', '-n'])
                if rc != 0:
                    raise UFWError(err_msg + " ip6tables")

    def _get_rules_from_formatted(self, frule, prefix):
        '''Return list of iptables rules appropriate for sending'''
        snippets = []

        # adjust reject and protocol 'all'
        pat_proto = re.compile(r'-p all ')
        pat_port = re.compile(r'port ')
        pat_reject = re.compile(r'-j (REJECT(_log(-all)?)?)')
        if pat_proto.search(frule):
            if pat_port.search(frule):
                if pat_reject.search(frule):
                    snippets.append(pat_proto.sub('-p tcp ', \
                        pat_reject.sub(r'-j \1 --reject-with tcp-reset ', \
                        frule)))
                else:
                    snippets.append(pat_proto.sub('-p tcp ', frule))
                snippets.append(pat_proto.sub('-p udp ', frule))
            else:
                snippets.append(pat_proto.sub('', frule))
        else:
            snippets.append(frule)

        # adjust for logging rules
        pat_log = re.compile(r'(.*)-j ([A-Z]+)_log(-all)?(.*)')
        pat_logall = re.compile(r'-j [A-Z]+_log-all')
        pat_chain = re.compile(r'(-A|-D) ([a-zA-Z0-9\-]+)')
        limit_args = '-m limit --limit 3/min --limit-burst 10'
        for i, s in enumerate(snippets):
            if pat_log.search(s):
                policy = pat_log.sub(r'\2', s).strip()
                if policy.lower() == "accept":
                    policy = "ALLOW"
                elif policy.lower() == "limit":
                    policy = "LIMIT"
                else:
                    policy = "BLOCK"

                lstr = '%s -j LOG --log-prefix "[UFW %s] "' % (limit_args, \
                       policy)
                if not pat_logall.search(s):
                    lstr = '-m state --state NEW ' + lstr
                snippets[i] = pat_log.sub(r'\1-j \2\4', s)
                snippets.insert(i, pat_log.sub(r'\1-j ' + prefix + \
                                               '-user-logging-input', s))
                snippets.insert(i, pat_chain.sub(r'\1 ' + prefix + \
                                                 '-user-logging-input', 
                                                 pat_log.sub(r'\1-j RETURN', \
                                                 s)))
                snippets.insert(i, pat_chain.sub(r'\1 ' + prefix + \
                                                 '-user-logging-input', 
                                                 pat_log.sub(r'\1' + lstr, s)))

        # adjust for limit
        pat_limit = re.compile(r' -j LIMIT')
        for i, s in enumerate(snippets):
            if pat_limit.search(s):
                tmp1 = pat_limit.sub(' -m state --state NEW -m recent --set', \
                                     s)
                tmp2 = pat_limit.sub(' -m state --state NEW -m recent' + \
                                     ' --update --seconds 30 --hitcount 6' + \
                                     ' -j ' + prefix + '-user-limit', s)
                tmp3 = pat_limit.sub(' -j ' + prefix + '-user-limit-accept', s)
                snippets[i] = tmp3
                snippets.insert(i, tmp2)
                snippets.insert(i, tmp1)

        return snippets

    def _get_lists_from_formatted(self, frule, prefix):
        '''Return list of iptables rules appropriate for sending as arguments
           to cmd()
        '''
        snippets = []
        str_snippets = self._get_rules_from_formatted(frule, prefix)

        # split the string such that the log prefix can contain spaces
        pat = re.compile(r'(.*) --log-prefix (".* ")(.*)')
        for i, s in enumerate(str_snippets):
            snippets.append(pat.sub(r'\1', s).split())
            if pat.match(s):
                snippets[i].append("--log-prefix")
                snippets[i].append(pat.sub(r'\2', s).replace('"', ''))
                snippets[i] += pat.sub(r'\3', s).split()

        return snippets

    def _read_rules(self):
        '''Read in rules that were added by ufw.'''
        rfns = [self.files['rules']]
        if self.use_ipv6():
            rfns.append(self.files['rules6'])

        for f in rfns:
            try:
                orig = ufw.util.open_file_read(f)
            except Exception:
                err_msg = _("Couldn't open '%s' for reading") % (f)
                raise UFWError(err_msg)

            pat_tuple = re.compile(r'^### tuple ###\s*')
            for line in orig:
                if pat_tuple.match(line):
                    tuple = pat_tuple.sub('', line)
                    tmp = re.split(r'\s+', tuple.strip())
                    if len(tmp) != 6 and len(tmp) != 8:
                        warn_msg = _("Skipping malformed tuple (bad length): %s") % (tuple)
                        warn(warn_msg)
                        continue
                    else:
                        try:
                            if len(tmp) == 6:
                                rule = UFWRule(tmp[0], tmp[1], tmp[2], tmp[3],
                                               tmp[4], tmp[5])
                            else:
                                rule = UFWRule(tmp[0], tmp[1], tmp[2], tmp[3],
                                               tmp[4], tmp[5])
                                # Removed leading [sd]app_ and unescape spaces
                                pat_space = re.compile('%20')
                                if tmp[6] != "-":
                                    rule.dapp = pat_space.sub(' ', tmp[6])
                                if tmp[7] != "-":
                                    rule.sapp = pat_space.sub(' ', tmp[7])
                        except UFWError:
                            warn_msg = _("Skipping malformed tuple: %s") % \
                                        (tuple)
                            warn(warn_msg)
                            continue
                        if f == self.files['rules6']:
                            rule.set_v6(True)
                            self.rules6.append(rule)
                        else:
                            rule.set_v6(False)
                            self.rules.append(rule)

            orig.close()

    def _write_rules(self, v6=False):
        '''Write out new rules to file to user chain file'''
        rules_file = self.files['rules']
        if v6:
            rules_file = self.files['rules6']

        try:
            fns = ufw.util.open_files(rules_file)
        except Exception:
            raise

        chain_prefix = "ufw"
        rules = self.rules
        if v6:
            chain_prefix = "ufw6"
            rules = self.rules6

        if self.dryrun:
            fd = sys.stdout.fileno()
        else:
            fd = fns['tmp']

        # Write header
        os.write(fd, "*filter\n")
        os.write(fd, ":" + chain_prefix + "-user-input - [0:0]\n")
        os.write(fd, ":" + chain_prefix + "-user-output - [0:0]\n")
        os.write(fd, ":" + chain_prefix + "-user-forward - [0:0]\n")

        if chain_prefix == "ufw":
            # Rate limiting only supported with IPv4
            os.write(fd, ":" + chain_prefix + "-user-limit - [0:0]\n")
            os.write(fd, ":" + chain_prefix + "-user-limit-accept - [0:0]\n")

        os.write(fd, "### RULES ###\n")

        # Write rules
        for r in rules:
            action = r.action
            if r.logtype != "":
                action += "_" + r.logtype

            if r.dapp == "" and r.sapp == "":
                os.write(fd, "\n### tuple ### %s %s %s %s %s %s\n" % \
                     (action, r.protocol, r.dport, r.dst, r.sport, r.src))
            else:
                pat_space = re.compile(' ')
                dapp = "-"
                if r.dapp:
                    dapp = pat_space.sub('%20', r.dapp)
                sapp = "-"
                if r.sapp:
                    sapp = pat_space.sub('%20', r.sapp)
                os.write(fd, "\n### tuple ### %s %s %s %s %s %s %s %s\n" \
                     % (action, r.protocol, r.dport, r.dst, r.sport, r.src, \
                        dapp, sapp))

            rule_str = "-A " + chain_prefix + "-user-input " + \
                       r.format_rule() + "\n"
            for s in self._get_rules_from_formatted(rule_str, chain_prefix):
                os.write(fd, s)

        # Write footer
        os.write(fd, "\n### END RULES ###\n")

        if chain_prefix == "ufw":
            # Rate limiting only supported with IPv4
            os.write(fd, "-A " + chain_prefix + "-user-limit -m limit " + \
                         "--limit 3/minute -j LOG --log-prefix " + \
                         "\"[UFW LIMIT BLOCK] \"\n")
            os.write(fd, "-A " + chain_prefix + "-user-limit -j REJECT\n")
            os.write(fd, "-A " + chain_prefix + "-user-limit-accept -j ACCEPT\n")

        os.write(fd, "COMMIT\n")

        if self.dryrun:
            ufw.util.close_files(fns, False)
        else:
            ufw.util.close_files(fns)

    def set_rule(self, rule, allow_reload=True):
        '''Updates firewall with rule by:
        * appending the rule to the chain if new rule and firewall enabled
        * deleting the rule from the chain if found and firewall enabled
        * inserting the rule if possible and firewall enabled
        * updating user rules file
        * reloading the user rules file if rule is modified
        '''
        rstr = ""

        if rule.v6:
            if not self.use_ipv6():
                err_msg = _("Adding IPv6 rule failed: IPv6 not enabled")
                raise UFWError(err_msg)
            if rule.action == 'limit':
                # Netfilter doesn't have ip6t_recent yet, so skip
                return _("Skipping unsupported IPv6 '") + "%s" % (rule.action) + _("' rule")

        if rule.multi and rule.protocol != "udp" and rule.protocol != "tcp":
            err_msg = _("Must specify 'tcp' or 'udp' with multiple ports")
            raise UFWError(err_msg)

        newrules = []
        found = False
        modified = False
        delete = False

        rules = self.rules
        position = rule.position
        if rule.v6:
            if self.iptables_version < "1.4" and (rule.dapp != "" or rule.sapp != ""):
                return _("Skipping IPv6 application rule. Need at least iptables 1.4")
            rules = self.rules6

        # bail if we have a bad position
        if position < 0 or position > len(rules):
            err_msg = _("Invalid position '%d'") % (position)
            raise UFWError(err_msg)

        if position > 0 and rule.remove:
            err_msg = _("Cannot specify insert and delete")
            raise UFWError(err_msg)
        if position > len(rules):
            err_msg = _("Cannot insert rule at position '%d'") % position
            raise UFWError(err_msg)

        # First construct the new rules list
        try:
            rule.normalize()
        except Exception:
            raise

        count = 1
        inserted = False
        matches = 0
        last = ('', '', '', '')
        for r in rules:
            try:
                r.normalize()
            except Exception:
                raise

            current = (r.dst, r.src, r.dapp, r.sapp)
            if count == position:
                # insert the rule if:
                # 1. the last rule was not an application rule
                # 2. the current rule is not an application rule
                # 3. the last application rule is different than the current
                #    while the new rule is different than the current one
                if (last[2] == '' and last[3] == '' and count > 1) or \
                   (current[2] == '' and current[3] == '') or \
                   last != current:
                    inserted = True
                    newrules.append(rule)
                    last = ('', '', '', '')
                else:
                    position += 1
            last = current
            count += 1

            ret = UFWRule.match(r, rule)
            if ret < 1:
                matches += 1

            if ret == 0 and not found and not inserted:
                # If find the rule, add it if it's not to be removed, otherwise
                # skip it.
                found = True
                if not rule.remove:
                    newrules.append(rule)
            elif ret < 0 and not rule.remove and not inserted:
                # If only the action is different, replace the rule if it's not
                # to be removed.
                found = True
                modified = True
                newrules.append(rule)
            else:
                newrules.append(r)

        if inserted:
            if matches > 0:
                rstr = _("Skipping inserting existing rule")
                if rule.v6:
                    rstr += " (v6)"
                return rstr
        else:
            # Add rule to the end if it was not already added.
            if not found and not rule.remove:
                newrules.append(rule)

            # Don't process non-existing or unchanged pre-exisiting rules
            if not found and rule.remove and not self.dryrun:
                rstr = _("Could not delete non-existent rule")
                if rule.v6:
                    rstr += " (v6)"
                return rstr
            elif found and not rule.remove and not modified:
                rstr = _("Skipping adding existing rule")
                if rule.v6:
                    rstr += " (v6)"
                return rstr

        if rule.v6:
            self.rules6 = newrules
        else:
            self.rules = newrules

        # Update the user rules file
        try:
            self._write_rules(rule.v6)
        except Exception:
            err_msg = _("Couldn't update rules file")
            UFWError(err_msg)

        # We wrote out the rules, so set reasonable string. We will change
        # this below when operating on the live firewall.
        rstr = _("Rules updated")
        if rule.v6:
            rstr = _("Rules updated (v6)")

        # Operate on the chains
        if self._is_enabled() and not self.dryrun:
            flag = ""
            if modified or self._need_reload(rule.v6) or inserted:
                rstr = _("Rule ")
                if inserted:
                    rstr += _("inserted")
                else:
                    rstr += _("updated")
                if rule.v6:
                    rstr += " (v6)"
                if allow_reload:
                    # Reload the chain
                    try:
                        self._reload_user_rules()
                    except Exception:
                        raise
                else:
                    rstr += _(" (skipped reloading firewall)")
            elif found and rule.remove:
                flag = '-D'
                rstr = _("Rule deleted")
            elif not found and not modified and not rule.remove:
                flag = '-A'
                rstr = _("Rule added")

            if flag != "":
                exe = "iptables"
                chain_prefix = "ufw"
                if rule.v6:
                    exe = "ip6tables"
                    chain_prefix = "ufw6"
                    rstr += " (v6)"
                chain = chain_prefix + "-user-input"

                # Is the firewall running?
                err_msg = _("Could not update running firewall")
                (rc, out) = cmd([exe, '-L', chain, '-n'])
                if rc != 0:
                    raise UFWError(err_msg)

                rule_str = "%s %s %s" % (flag, chain, rule.format_rule())
                pat_log = re.compile(r'(-A +)(ufw6?-user-[a-z\-]+)(.*)')
                for s in self._get_lists_from_formatted(rule_str, \
                                                               chain_prefix):
                    (rc, out) = cmd([exe] + s)
                    if rc != 0:
                        msg(out, sys.stderr)
                        UFWError(err_msg)

                    # delete any lingering RETURN rules (needed for upgrades)
                    if flag == "-A" and pat_log.search(" ".join(s)):
                        c = pat_log.sub(r'\2', " ".join(s))
                        (rc, out) = cmd([exe, '-D', c, '-j', 'RETURN'])
                        if rc != 0:
                            debug("FAILOK: " + err_msg)

        return rstr

    def get_app_rules_from_system(self, template, v6):
        '''Return a list of UFWRules from the system based on template rule'''
        rules = []
        app_rules = []

        if v6:
            rules = self.rules6
        else:
            rules = self.rules

        norm = template.dup_rule()
        norm.set_v6(v6)
        norm.normalize()
        tuple = norm.get_app_tuple()

        for r in rules:
            tmp = r.dup_rule()
            tmp.normalize()
            tmp_tuple = tmp.get_app_tuple()
            if tmp_tuple == tuple:
                app_rules.append(tmp)

        return app_rules

    def _chain_cmd(self, chain, args, fail_ok=False):
        '''Perform command on chain'''
        exe = "iptables"
        if chain.startswith("ufw6"):
            exe = "ip6tables"
        (rc, out) = cmd([exe] + args)
        if rc != 0:
           err_msg = _("Could not perform '%s'") % (args)
           if fail_ok:
               debug("FAILOK: " + err_msg)
           else: 
               raise UFWError(err_msg)

    def update_logging(self, level):
        '''Update loglevel of running firewall'''
        if not self._is_enabled():
            return

        if level not in self.loglevels.keys():
            err_msg = _("Invalid log level '%s'") % (level)
            raise UFWError(err_msg)

        # make sure all the chains are here, it's redundant but helps make
        # sure the chains are in a consistent state
        err_msg = _("Could not update running firewall")
        for c in self.chains['before'] + self.chains['user'] + \
           self.chains['after'] + self.chains['misc']:
            try:
                self._chain_cmd(c, ['-L', c, '-n'])
            except:
                raise UFWError(err_msg)

        # Flush all the logging chains except 'user'
        try:
            for c in self.chains['before'] + self.chains['after'] + \
               self.chains['misc']:
                self._chain_cmd(c, ['-F', c])
                self._chain_cmd(c, ['-Z', c])
        except:
            raise UFWError(err_msg)

        if level == "off":
            # when off, insert a RETURN rule at the top of user rules, thus
            # preserving the rules
            for c in self.chains['user']:
                self._chain_cmd(c, ['-D', c, '-j', 'RETURN'], fail_ok=True)
                self._chain_cmd(c, ['-I', c, '-j', 'RETURN'])
            return
        else:
            # when on, remove the RETURN rule at the top of user rules, thus
            # honoring the log rules
            for c in self.chains['user']:
                self._chain_cmd(c, ['-D', c, '-j', 'RETURN'], fail_ok=True)

        limit_args = ['-m', 'limit', '--limit', '3/min', '--limit-burst', '10']

        # log levels of low and higher log blocked packets
        if self.loglevels[level] >= self.loglevels["low"]:
            # Setup the policy violation logging chains
            largs = []
            # log levels under high use limit
            if self.loglevels[level] < self.loglevels["high"]:
                largs = limit_args
            for c in self.chains['after']:
                for t in ['input', 'output', 'forward']:
                    if c.endswith(t):
                        if self.get_default_policy(t) == "reject" or \
                           self.get_default_policy(t) == "deny":
                            msg = "[UFW BLOCK] "
                            try:
                                self._chain_cmd(c, ['-A', c, '-j', 'LOG', \
                                                    '--log-prefix', msg] + largs)
                            except:
                                raise
                        elif self.loglevels[level] >= self.loglevels["medium"]:
                            msg = "[UFW ALLOW] "
                            try:
                                self._chain_cmd(c, ['-A', c, '-j', 'LOG', \
                                                    '--log-prefix', msg] + largs)
                            except:
                                raise

            # Setup the miscellaneous logging chains
            largs = []
            # log levels under high use limit
            if self.loglevels[level] < self.loglevels["high"]:
                largs = limit_args

            for c in self.chains['misc']:
                if c.endswith("allow"):
                    msg = "[UFW ALLOW] "
                elif c.endswith("deny"):
                    msg = "[UFW BLOCK] "
                    if self.loglevels[level] >= self.loglevels["medium"]:
                        # only log INVALID in medium and higher
                        try:
                            self._chain_cmd(c, ['-I', c, '-m', 'state', \
                                                '--state', 'INVALID', \
                                                '-j', 'RETURN'] + largs)
                        except:
                            raise
                try:
                    self._chain_cmd(c, ['-A', c, '-j', 'LOG', \
                                        '--log-prefix', msg] + largs)
                except:
                    raise

        # Setup the audit logging chains
        if self.loglevels[level] >= self.loglevels["medium"]:
            # loglevel full logs all packets without limit
            largs = []

            # loglevel high logs all packets with limit
            if self.loglevels[level] < self.loglevels["full"]:
                largs = limit_args

            # loglevel medium logs all new packets with limit
            if self.loglevels[level] < self.loglevels["high"]:
                largs = ['-m', 'state', '--state', 'NEW'] + limit_args

            msg = "[UFW AUDIT] "
            for c in self.chains['before']:
                try:
                    self._chain_cmd(c, ['-I', c, '-j', 'LOG', \
                                        '--log-prefix', msg] + largs)
                except:
                    raise UFWError(err_msg)


