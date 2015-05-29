#
# frontend.py: frontend interface for ufw
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
import os
import sys
import warnings

from ufw.common import UFWError
import ufw.util
from ufw.util import error, warn
from ufw.backend_iptables import UFWBackendIptables

def allowed_command(cmd):
    '''Return command if it is allowed, otherwise raise an exception'''
    allowed_cmds = ['enable', 'disable', 'help', '--help', 'default', \
                    'logging', 'status', 'version', '--version', 'allow', \
                    'deny', 'reject', 'limit', 'reload', 'show' ]

    if not cmd.lower() in allowed_cmds:
        raise ValueError()

    return cmd.lower()

def parse_command(argv):
    '''Parse command. Returns tuple for action, rule, ip_version and dryrun.'''
    action = ""
    rule = ""
    type = ""
    from_type = "any"
    to_type = "any"
    from_service = ""
    to_service = ""
    dryrun = False
    insert_pos = ""
    logtype = ""
    loglevel = ""

    if len(argv) > 1 and argv[1].lower() == "--dry-run":
        dryrun = True
        argv.remove(argv[1])

    remove = False
    if len(argv) > 1 and argv[1].lower() == "delete":
        remove = True
        argv.remove(argv[1])

    nargs = len(argv)

    if nargs < 2:
        raise ValueError()

    if argv[1].lower() in ['insert']:
        action = argv[1].lower()
    else:
        action = allowed_command(argv[1])

    if action == "insert":
        if nargs < 4:
            raise ValueError()
        insert_pos = argv[2]

        # Using position '0' adds rule at end, which is potentially confusing
        # for the end user
        if insert_pos == "0":
            err_msg = _("Cannot insert rule at position '%s'") % (insert_pos)
            raise UFWError(err_msg)

        # strip out 'insert NUM' and parse as normal
        del argv[2]
        del argv[1]
        action = allowed_command(argv[1])
        nargs = len(argv)

        # error if use insert with non-rule commands
        if action != "allow" and action != "deny" and action != "reject" and \
           action != "limit":
            raise ValueError()

    if action == "logging":
        if nargs < 3:
            raise ValueError()
        elif argv[2].lower() == "off":
            action = "logging-off"
        elif argv[2].lower() == "on" or argv[2].lower() == "low" or \
             argv[2].lower() == "medium" or argv[2].lower() == "high" or \
             argv[2].lower() == "full":
            action = "logging-on"
            if argv[2].lower() != "on":
                action += "_" + argv[2].lower()
        else:
            raise ValueError()

    if action == "status" and nargs > 2:
        if argv[2].lower() == "verbose":
            action = "status-verbose"
        elif argv[2].lower() == "numbered":
            action = "status-numbered"

    if action == "show":
        if nargs == 2:
            raise ValueError()
        elif argv[2].lower() == "raw":
            action = "show-raw"

    if action == "default":
        if nargs < 3:
            raise ValueError()
        elif argv[2].lower() == "deny":
            action = "default-deny"
        elif argv[2].lower() == "allow":
            action = "default-allow"
        elif argv[2].lower() == "reject":
            action = "default-reject"
        else:
            raise ValueError()

    if action == "allow" or action == "deny" or action == "reject" or \
       action == "limit":
        if nargs > 2 and (argv[2].lower() == "log" or \
                          argv[2].lower() == 'log-all'):
            if nargs < 4:
                raise ValueError()
            logtype = argv[2].lower()

            # strip out 'log' or 'log-all' and parse as normal
            del argv[2]
            nargs = len(argv)

        if nargs < 3 or nargs > 12:
            raise ValueError()

        rule_action = action
        if logtype != "":
            rule_action += "_" + logtype
        rule = ufw.common.UFWRule(rule_action, "any", "any")
        if remove:
            rule.remove = remove
        elif insert_pos != "":
            try:
                rule.set_position(insert_pos)
            except Exception:
                raise
        if nargs == 3:
            # Short form where only app or port/proto is given
            if ufw.applications.valid_profile_name(argv[2]):
                # Check if name collision with /etc/services. If so, use
                # /etc/services instead of application profile
                try:
                    ufw.util.get_services_proto(argv[2])
                except Exception:
                    type = "both"
                    rule.dapp = argv[2]
                    rule.set_port(argv[2], "dst")
            if rule.dapp == "":
                try:
                    (port, proto) = ufw.util.parse_port_proto(argv[2])
                except UFWError:
                    err_msg = _("Bad port")
                    raise UFWError(err_msg)

                if not re.match('^\d([0-9,:]*\d+)*$', port):
                    if ',' in port or ':' in port:
                        err_msg = _("Port ranges must be numeric")
                        raise UFWError(err_msg)
                    to_service = port

                try:
                    rule.set_protocol(proto)
                    rule.set_port(port, "dst")
                    type = "both"
                except UFWError:
                    err_msg = _("Bad port")
                    raise UFWError(err_msg)
        elif nargs % 2 != 0:
            err_msg = _("Wrong number of arguments")
            raise UFWError(err_msg)
        elif not 'from' in argv and not 'to' in argv:
            err_msg = _("Need 'to' or 'from' clause")
            raise UFWError(err_msg)
        else:
            # Full form with PF-style syntax
            keys = [ 'proto', 'from', 'to', 'port', 'app' ]

            # quick check
            if argv.count("to") > 1 or \
               argv.count("from") > 1 or \
               argv.count("proto") > 1 or \
               argv.count("port") > 2 or \
               argv.count("app") > 2 or \
               argv.count("app") > 0 and argv.count("proto") > 0:
                err_msg = _("Improper rule syntax")
                raise UFWError(err_msg)

            i = 1
            loc = ""
            for arg in argv[1:]:
                if i % 2 == 0 and argv[i] not in keys:
                    err_msg = _("Invalid token '%s'") % (argv[i])
                    raise UFWError(err_msg)
                if arg == "proto":
                    if i+1 < nargs:
                        try:
                            rule.set_protocol(argv[i+1])
                        except Exception:
                            raise
                    else:
                        err_msg = _("Invalid 'proto' clause")
                        raise UFWError(err_msg)
                elif arg == "from":
                    if i+1 < nargs:
                        try:
                            faddr = argv[i+1].lower()
                            if faddr == "any":
                                faddr = "0.0.0.0/0"
                                from_type = "any"
                            else:
                                if ufw.util.valid_address(faddr, "6"):
                                    from_type = "v6"
                                else:
                                    from_type = "v4"
                            rule.set_src(faddr)
                        except Exception:
                            raise
                        loc = "src"
                    else:
                        err_msg = _("Invalid 'from' clause")
                        raise UFWError(err_msg)
                elif arg == "to":
                    if i+1 < nargs:
                        try:
                            saddr = argv[i+1].lower()
                            if saddr == "any":
                                saddr = "0.0.0.0/0"
                                to_type = "any"
                            else:
                                if ufw.util.valid_address(saddr, "6"):
                                    to_type = "v6"
                                else:
                                    to_type = "v4"
                            rule.set_dst(saddr)
                        except Exception:
                            raise
                        loc = "dst"
                    else:
                        err_msg = _("Invalid 'to' clause")
                        raise UFWError(err_msg)
                elif arg == "port" or arg == "app":
                    if i+1 < nargs:
                        if loc == "":
                            err_msg = _("Need 'from' or 'to' with '%s'") % \
                                        (arg)
                            raise UFWError(err_msg)

                        tmp = argv[i+1]
                        if arg == "app":
                            if loc == "src":
                                rule.sapp = tmp
                            else:
                                rule.dapp = tmp
                        elif not re.match('^\d([0-9,:]*\d+)*$', tmp):
                            if ',' in tmp or ':' in tmp:
                                err_msg = _("Port ranges must be numeric")
                                raise UFWError(err_msg)

                            if loc == "src":
                                from_service = tmp
                            else:
                                to_service = tmp
                        try:
                            rule.set_port(tmp, loc)
                        except Exception:
                            raise
                    else:
                        err_msg = _("Invalid 'port' clause")
                        raise UFWError(err_msg)
                i += 1

            # Figure out the type of rule (IPv4, IPv6, or both) this is
            if from_type == "any" and to_type == "any":
                type = "both"
            elif from_type != "any" and to_type != "any" and \
                 from_type != to_type:
                err_msg = _("Mixed IP versions for 'from' and 'to'")
                raise UFWError(err_msg)
            elif from_type != "any":
                type = from_type
            elif to_type != "any":
                type = to_type

    # Adjust protocol
    if to_service != "" or from_service != "":
        proto = ""
        if to_service != "":
            try:
                proto = ufw.util.get_services_proto(to_service)
            except Exception:
                err_msg = _("Could not find protocol")
                raise UFWError(err_msg)
        if from_service != "":
            if proto == "any" or proto == "":
                try:
                    proto = ufw.util.get_services_proto(from_service)
                except Exception:
                    err_msg = _("Could not find protocol")
                    raise UFWError(err_msg)
            else:
                try:
                    tmp = ufw.util.get_services_proto(from_service)
                except Exception:
                    err_msg = _("Could not find protocol")
                    raise UFWError(err_msg)
                if proto == "any" or proto == tmp:
                    proto = tmp
                elif tmp == "any":
                    pass
                else:
                    err_msg = _("Protocol mismatch (from/to)")
                    raise UFWError(err_msg)

        # Verify found proto with specified proto
        if rule.protocol == "any":
            rule.set_protocol(proto)
        elif proto != "any" and rule.protocol != proto:
            err_msg = _("Protocol mismatch with specified protocol %s") % \
                        (rule.protocol)
            raise UFWError(err_msg)

    # Verify protocol not specified with application rule
    if rule and rule.protocol != "any" and \
       (rule.sapp != "" or rule.dapp != ""):
        app = ""
        if rule.dapp:
            app = rule.dapp
        else:
            app = rule.sapp
        err_msg = _("Improper rule syntax ('%s' specified with app rule)") % \
                   (rule.protocol)
        raise UFWError(err_msg)

    return (action, rule, type, dryrun)


def parse_application_command(argv):
    '''Parse applications command. Returns tuple for action and profile name'''
    name = ""
    action = ""
    dryrun = False
    addnew = False

    if len(argv) < 3 or argv[1].lower() != "app":
        raise ValueError()

    argv.remove("app")
    nargs = len(argv)

    if len(argv) > 1 and argv[1].lower() == "--dry-run":
        dryrun = True
        argv.remove(argv[1])

    app_cmds = ['list', 'info', 'default', 'update']

    if not argv[1].lower() in app_cmds:
        raise ValueError()
    else:
        action = argv[1].lower()

    if action == "info" or action == "update":
        if nargs >= 4 and argv[2] == "--add-new":
            addnew = True
            argv.remove("--add-new")
            nargs = len(argv)

        if nargs < 3:
            raise ValueError()

        # Handle quoted name with spaces in it by stripping Python's ['...']
        # list as string text.
        name = str(argv[2]).strip("[']")

        if addnew:
            action += "-with-new"

    if action == "list" and nargs != 2:
        raise ValueError()

    if action == "default":
        if nargs < 3:
            raise ValueError()
        if argv[2].lower() == "allow":
            action = "default-allow"
        elif argv[2].lower() == "deny":
            action = "default-deny"
        elif argv[2].lower() == "reject":
            action = "default-reject"
        elif argv[2].lower() == "skip":
            action = "default-skip"
        else:
            raise ValueError()

    return (action, name, dryrun)


def get_command_help():
    '''Print help message'''
    msg = _('''
Usage: ''') + ufw.common.programName + _(''' COMMAND

Commands:
 enable				enables the firewall
 disable			disables the firewall
 default ARG			set default policy to ALLOW, DENY or REJECT
 logging ARG			set logging to OFF, ON or LEVEL
 allow|deny|reject ARG		add allow, deny or reject RULE
 delete RULE		 	delete the RULE
 insert NUM RULE	 	insert RULE at NUM
 status 			show firewall status
 status numbered		show firewall status as numbered list of RULES
 show ARG			show firewall report
 version			display version information

Application profile commands:
 app list			list application profiles
 app info PROFILE		show information on PROFILE
 app update PROFILE		update PROFILE
 app default ARG		set profile policy to ALLOW, DENY, REJECT or
				SKIP
''')
    return (msg)


class UFWFrontend:
    '''UI'''
    def __init__(self, dryrun, backend_type="iptables"):
        if backend_type == "iptables":
            try:
                self.backend = UFWBackendIptables(dryrun)
            except Exception:
                raise
        else:
            raise UFWError("Unsupported backend type '%s'" % (backend_type))

        self._init_input_strings()

    def _init_input_strings(self):
        '''Initialize input strings for translations'''
        self.no = _("n")
        self.yes = _("y")
        self.yes_full = _("yes")

    def set_enabled(self, enabled):
        '''Toggles ENABLED state in of <config_dir>/ufw/ufw.conf'''
        res = ""

        str = "no"
        if enabled:
            str = "yes"

        changed = False
        if (enabled and not self.backend._is_enabled()) or \
           (not enabled and self.backend._is_enabled()):
            changed = True

        # Update the config files when toggling enable/disable
        if changed:
            try:
                self.backend.set_default(self.backend.files['conf'], \
                                         "ENABLED", str)
            except UFWError, e:
                error(e.value)

        error_str = ""
        if enabled:
            try:
                self.backend.start_firewall()
            except UFWError, e:
                if changed:
                    error_str = e.value

            if error_str != "":
                # Revert config files when toggling enable/disable and
                # firewall failed to start
                try:
                    self.backend.set_default(self.backend.files['conf'], \
                                             "ENABLED", "no")
                except UFWError, e:
                    error(e.value)

                # Report the error
                error(error_str)

            res = _("Firewall is active and enabled on system startup")
        else:
            try:
                self.backend.stop_firewall()
            except UFWError, e:
                error(e.value)

            res = _("Firewall stopped and disabled on system startup")

        return res

    def set_default_policy(self, policy):
        '''Sets default policy of firewall'''
        res = ""
        try:
            res = self.backend.set_default_policy(policy)
            if self.backend._is_enabled():
                self.backend.stop_firewall()
                self.backend.start_firewall()
        except UFWError, e:
            error(e.value)

        return res

    def set_loglevel(self, level):
        '''Sets log level of firewall'''
        res = ""
        try:
            res = self.backend.set_loglevel(level)
        except UFWError, e:
            error(e.value)

        return res

    def get_status(self, verbose=False, show_count=False):
        '''Shows status of firewall'''
        try:
            out = self.backend.get_status(verbose, show_count)
        except UFWError, e:
            error(e.value)

        return out

    def get_show_raw(self):
        '''Shows raw output of firewall'''
        try:
            out = self.backend.get_running_raw()
        except UFWError, e:
            error(e.value)

        return out

    def set_rule(self, rule, ip_version):
        '''Updates firewall with rule'''
        res = ""
        err_msg = ""
        tmp = ""
        rules = []

        if rule.dapp == "" and rule.sapp == "":
            rules.append(rule)
        else:
            tmprules = []
            try:
                if rule.remove:
                    if ip_version == "v4":
                        tmprules = self.backend.get_app_rules_from_system(rule, False)
                    elif ip_version == "v6":
                        tmprules = self.backend.get_app_rules_from_system(rule, True)
                    elif ip_version == "both":
                        tmprules = self.backend.get_app_rules_from_system(rule, False)
                        tmprules6 = self.backend.get_app_rules_from_system(rule, True)
                        # Only add rules that are different by more than v6 (we
                        # will handle 'ip_version == both' specially, below).
                        for x in tmprules:
                            for y in tmprules6:
                                prev6 = y.v6
                                y.v6 = False
                                if not x.match(y):
                                    y.v6 = prev6
                                    tmprules.append(y)
                    else:
                        err_msg = _("Invalid IP version '%s'") % (ip_version)
                        raise UFWError(err_msg)

                    # Don't process removal of non-existing application rules
                    if len(tmprules) == 0 and not self.backend.dryrun:
                        tmp =  _("Could not delete non-existent rule")
                        if ip_version == "v4":
                            res = tmp
                        elif ip_version == "v6":
                            res = tmp + " (v6)"
                        elif ip_version == "both":
                            res = tmp + "\n" + tmp + " (v6)"
                        return res

                    for tmp in tmprules:
                        r = tmp.dup_rule()
                        r.remove = rule.remove
                        r.set_action(rule.action)
                        r.set_logtype(rule.logtype)
                        rules.append(r)
                else:
                    rules = self.backend.get_app_rules_from_template(rule)
                    # Reverse the order of rules for inserted rules, so they
                    # are inserted in the right order
                    if rule.position > 0:
                        rules.reverse()
            except Exception:
                raise

        count = 0
        set_error = False
        pos_err_msg = _("Invalid position '")
        num_v4 = self.backend.get_rules_count(False)
        num_v6 = self.backend.get_rules_count(True)
        for i, r in enumerate(rules):
            count = i
            if r.position > num_v4 + num_v6:
                pos_err_msg += str(r.position) + "'"
                raise UFWError(pos_err_msg)
            try:
                if self.backend.use_ipv6():
                    if ip_version == "v4":
                        if r.position > num_v4:
                            pos_err_msg += str(r.position) + "'"
                            raise UFWError(pos_err_msg)
                        r.set_v6(False)
                        tmp = self.backend.set_rule(r)
                    elif ip_version == "v6":
                        if r.position > num_v4:
                            r.set_position(r.position - num_v4)
                        elif r.position != 0 and r.position <= num_v4:
                            pos_err_msg += str(r.position) + "'"
                            raise UFWError(pos_err_msg)
                        r.set_v6(True)
                        tmp = self.backend.set_rule(r)
                    elif ip_version == "both":
                        user_pos = r.position # user specified position
                        r.set_v6(False)
                        if not r.remove and user_pos > num_v4:
			    # The user specified a v6 rule, so try to find a
			    # match in the v4 rules and use its position.
                            p = self.backend.find_other_position(user_pos - \
                                                                 num_v4, True)
                            if p > 0:
                                r.set_position(p)
                            else:
                                # If not found, then add the rule
                                r.set_position(0)
                        tmp = self.backend.set_rule(r)

                        # We need to readjust the position since the number
                        # the number of ipv4 rules increased
                        if not r.remove and user_pos > 0:
                            num_v4 = self.backend.get_rules_count(False)
                            r.set_position(user_pos + 1)

                        r.set_v6(True)
                        if not r.remove and r.position > 0 and \
                           r.position <= num_v4:
			    # The user specified a v4 rule, so try to find a
			    # match in the v6 rules and use its position.
                            p = self.backend.find_other_position(r.position, \
                                                                 False)
                            if p > 0:
                                # Subtract count since the list is reversed
                                r.set_position(p - count)
                            else:
                                # If not found, then add the rule
                                r.set_position(0)
                        if tmp != "":
                            tmp += "\n"

                        # Readjust position to send to set_rule
                        if not r.remove and r.position > num_v4:
                            r.set_position(r.position - num_v4)

                        tmp += self.backend.set_rule(r)
                    else:
                        err_msg = _("Invalid IP version '%s'") % (ip_version)
                        raise UFWError(err_msg)
                else:
                    if ip_version == "v4" or ip_version == "both":
                        r.set_v6(False)
                        tmp = self.backend.set_rule(r)
                    elif ip_version == "v6":
                        err_msg = _("IPv6 support not enabled")
                        raise UFWError(err_msg)
                    else:
                        err_msg = _("Invalid IP version '%s'") % (ip_version)
                        raise UFWError(err_msg)
            except UFWError, e:
                err_msg = e.value
                set_error = True
                break

            if r.updated:
                warn_msg = _("Rule changed after normalization")
                warnings.warn(warn_msg)

        if not set_error:
            # Just return the last result if no error
            res += tmp
        elif len(rules) == 1:
            # If no error, and just one rule, error out
            error(err_msg)
        else:
	    # If error and more than one rule, delete the successfully added
	    # rules in reverse order
            undo_error = False
            indexes = range(count+1)
            indexes.reverse()
            for j in indexes:
                if count > 0 and rules[j]:
                    backout_rule = rules[j].dup_rule()
                    backout_rule.remove = True
                    try:
                        self.set_rule(backout_rule, ip_version)
                    except Exception:
                        # Don't fail, so we can try to backout more
                        undo_error = True
                        warn_msg = _("Could not back out rule '%s'") % \
                                     r.format_rule()
                        warn(warn_msg)

            err_msg += _("\nError applying application rules.")
            if undo_error:
                err_msg += _(" Some rules could not be unapplied.")
            else:
                err_msg += _(" Attempted rules successfully unapplied.")

            raise UFWError(err_msg)

        return res

    def do_action(self, action, rule, ip_version):
        '''Perform action on rule. action, rule and ip_version are usually
           based on return values from parse_command().
        '''
        res = ""
        if action.startswith("logging-on"):
            tmp = action.split('_')
            if len(tmp) > 1:
                res = self.set_loglevel(tmp[1])
            else:
                res = self.set_loglevel("on")
        elif action == "logging-off":
            res = self.set_loglevel("off")
        elif action == "default-allow":
            res = self.set_default_policy("allow")
        elif action == "default-deny":
            res = self.set_default_policy("deny")
        elif action == "default-reject":
            res = self.set_default_policy("reject")
        elif action == "status":
            res = self.get_status()
        elif action == "status-verbose":
            res = self.get_status(True)
        elif action == "show-raw":
            res = self.get_show_raw()
        elif action == "status-numbered":
            res = self.get_status(False, True)
        elif action == "enable":
            res = self.set_enabled(True)
        elif action == "disable":
            res = self.set_enabled(False)
        elif action == "reload":
            if self.backend._is_enabled():
                self.set_enabled(False)
                self.set_enabled(True)
                res = _("Firewall reloaded")
            else:
                res = _("Firewall not enabled (skipping reload)")
        elif action == "allow" or action == "deny" or action == "reject" or \
             action == "limit":
            # allow case insensitive matches for application rules
            try:
                if rule.dapp != "":
                    tmp = self.backend.find_application_name(rule.dapp)
                    if tmp != rule.dapp:
                        rule.dapp = tmp
                        rule.set_port(tmp, "dst")
                if rule.sapp != "":
                    tmp = self.backend.find_application_name(rule.sapp)
                    if tmp != rule.sapp:
                        rule.sapp = tmp
                        rule.set_port(tmp, "src")
            except UFWError, e:
                error(e.value)
            res = self.set_rule(rule, ip_version)
        else:
            err_msg = _("Unsupported action '%s'") % (action)
            raise UFWError(err_msg)

        return res

    def set_default_application_policy(self, policy):
        '''Sets default application policy of firewall'''
        res = ""
        try:
            res = self.backend.set_default_application_policy(policy)
        except UFWError, e:
            error(e.value)

        return res

    def get_application_list(self):
        '''Display list of known application profiles'''
        names = self.backend.profiles.keys()
        names.sort()
        rstr = _("Available applications:")
        for n in names:
            rstr += "\n  %s" % (n)
        return rstr

    def get_application_info(self, pname):
        '''Display information on profile'''
        names = []
        if pname == "all":
            names = self.backend.profiles.keys()
            names.sort()
        else:
            if not ufw.applications.valid_profile_name(pname):
                err_msg = _("Invalid profile name")
                raise UFWError(err_msg)
            names.append(pname)

        rstr = ""
        for name in names:
            if not self.backend.profiles.has_key(name) or \
               not self.backend.profiles[name]:
                err_msg = _("Could not find profile '%s'") % (name)
                raise UFWError(err_msg)

            if not ufw.applications.verify_profile(name, \
               self.backend.profiles[name]):
                err_msg = _("Invalid profile")
                raise UFWError(err_msg)

            rstr += _("Profile: %s\n") % (name)
            rstr += _("Title: %s\n") % (ufw.applications.get_title(\
                                        self.backend.profiles[name]))

            rstr += _("Description: %s\n\n") % \
                                            (ufw.applications.get_description(\
                                             self.backend.profiles[name]))

            ports = ufw.applications.get_ports(self.backend.profiles[name])
            if len(ports) > 1 or ',' in ports[0]:
                rstr += _("Ports:")
            else:
                rstr += _("Port:")

            for p in ports:
                rstr += "\n  %s" % (p)

            if name != names[len(names)-1]:
                rstr += "\n\n--\n\n"

        return ufw.util.wrap_text(rstr)

    def application_update(self, profile):
        '''Refresh application profile'''
        rstr = ""
        allow_reload = True
        trigger_reload = False

        if self.backend.do_checks and ufw.util.under_ssh():
            # Don't reload the firewall if running under ssh
            allow_reload = False

        if profile == "all":
            profiles = self.backend.profiles.keys()
            profiles.sort()
            for p in profiles:
                (tmp, found) = self.backend.update_app_rule(p)
                if found:
                    if tmp != "":
                        tmp += "\n"
                    rstr += tmp
                    trigger_reload = found
        else:
            (rstr, trigger_reload) = self.backend.update_app_rule(profile)
            if rstr != "":
                rstr += "\n"

        if trigger_reload and self.backend._is_enabled():
            if allow_reload:
                try:
                    self.backend._reload_user_rules()
                except Exception:
                    raise
                rstr += _("Firewall reloaded")
            else:
                rstr += _("Skipped reloading firewall")

        return rstr

    def application_add(self, profile):
        '''Refresh application profile'''
        rstr = ""
        policy = ""

        if profile == "all":
            err_msg = _("Cannot specify 'all' with '--add-new'")
            raise UFWError(err_msg)

        default = self.backend.defaults['default_application_policy']
        if default == "skip":
            ufw.util.debug("Policy is '%s', not adding profile '%s'" % \
                           (policy, profile))
            return rstr
        elif default == "accept":
            policy = "allow"
        elif default == "drop":
            policy = "deny"
        elif default == "reject":
            policy = "reject"
        else:
            err_msg = _("Unknown policy '%s'") % (default)
            raise UFWError(err_msg)

        args = [ 'ufw' ]
        if self.backend.dryrun:
            args.append("--dry-run")

        args += [ policy, profile ]
        try:
            (action, rule, ip_version, self.backend.dryrun) = \
                parse_command(args)
        except Exception:
            raise

        rstr = self.do_action(action, rule, ip_version)
        return rstr

    def do_application_action(self, action, profile):
        '''Perform action on profile. action and profile are usually based on
           return values from parse_applications_command().
        '''
        res = ""
        if action == "default-allow":
            res = self.set_default_application_policy("allow")
        elif action == "default-deny":
            res = self.set_default_application_policy("deny")
        elif action == "default-reject":
            res = self.set_default_application_policy("reject")
        elif action == "default-skip":
            res = self.set_default_application_policy("skip")
        elif action == "list":
            res = self.get_application_list()
        elif action == "info":
            res = self.get_application_info(profile)
        elif action == "update" or action == "update-with-new":
            str1 = self.application_update(profile)
            str2 = ""
            if action == "update-with-new":
                str2 = self.application_add(profile)

            if str1 != "" and str2 != "":
                str1 += "\n"
            res = str1 + str2
        else:
            err_msg = _("Unsupported action '%s'") % (action)
            raise UFWError(err_msg)

        return res

    def continue_under_ssh(self):
        '''If running under ssh, prompt the user for confirmation'''
        proceed = True
        if self.backend.do_checks and ufw.util.under_ssh():
            prompt = _("Command may disrupt existing ssh connections.")
            prompt += _(" Proceed with operation (%s|%s)? ") % \
                       (self.yes, self.no)
            os.write(sys.stdout.fileno(), prompt)
            ans = sys.stdin.readline().lower().strip()
            if ans != "y" and ans != self.yes and ans != self.yes_full:
                proceed = False

        return proceed

