'''Apport package hook for Network Manager

(c) 2008 Canonical Ltd.
Contributors:
Matt Zimmerman <mdz@canonical.com>
Martin Pitt <martin.pitt@canonical.com>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
the full text of the license.
'''

import os
import subprocess

# TODO:
# - HAL info for modem devices
# - Trim down HAL dumps to only the relevant info

attach_files = { 'IfupdownConfig' : '/etc/network/interfaces',
                 'WpaSupplicantLog' : '/var/log/wpa_supplicant.log' }
                 
attach_commands = { 'Syslog' : ['egrep',' (NetworkManager|dhclient|kernel):','/var/log/syslog'],
                    'Gconf' : ['gconftool-2','-R','/system/networking']
                    }

def _command_output(command, input = None, stderr = subprocess.STDOUT):
    '''Try to execute given command (array) and return its stdout, or return
    a textual error if it failed.'''

    try:
       sp = subprocess.Popen(command,
                             stdout=subprocess.PIPE, stderr=stderr, close_fds=True)
    except OSError, e:
       return 'Error: ' + str(e)

    out = sp.communicate(input)[0]
    if sp.returncode == 0:
       return out.strip()
    else:
       return 'Error: command %s failed with exit code %i: %s' % (
           str(command), sp.returncode, out)

def _read_file(file):
    try:
        return open(file).read().strip()
    except Exception, e:
        return 'Error: ' + str(e)

def _network_interfaces():
    output = _command_output(['hal-find-by-capability','--capability','net'])
    udis = output.split('\n')
    interfaces = {}
    for udi in udis:
        interface = _command_output(['hal-get-property','--udi',udi,'--key','net.interface'])
        device = _command_output(['hal-get-property','--udi',udi,'--key','net.originating_device'])

        interfaces[interface] = device

    return interfaces
                
def _device_details(device):
    return _command_output(['lshal','-u',device])

def add_info(report):
    for name, path in attach_files.items():
        if os.path.exists(path):
            report[name] = _read_file(path)

    for name, command in attach_commands.items():
        output = _command_output(command)
        report[name] = output

    for interface, device in _network_interfaces().items():
        key = 'NetDevice.%s' % interface
        report[key] = _device_details(device)

    # It would be neat if we could just set the driver-* tags in LP
    # per https://wiki.ubuntu.com/DebuggingNetworkManager
    interesting_modules = ['ndiswrapper','ath_hal','b44']
    interesting_modules_loaded = []
    for line in open('/proc/modules'):
        module = line.split()[0]
        if module in interesting_modules:
            interesting_modules_loaded.append(module)

    if interesting_modules_loaded:
        report['InterestingModules'] = ' '.join(interesting_modules_loaded)

if __name__ == '__main__':
    report = {}
    add_info(report)
    for key in report:
        print '%s: %s' % (key, report[key].split('\n', 1)[0])
