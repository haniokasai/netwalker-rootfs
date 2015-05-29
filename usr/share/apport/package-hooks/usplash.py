''' apport package hook for usplash

(c) 2007-2009 Canonical Ltd.
Contributors:
Brian Murray <brian@ubuntu.com>
Martin Pitt <martin.pitt@ubuntu.com>

do not file bugs about crashes in libx86, since they are due to buggy BIOSes
and we cannot do anything about them anyway '''

from apport.hookutils import *

def add_info(report):

    attach_file_if_exists(report, '/etc/usplash.conf', 'UsplashConf')
    attach_file_if_exists(report, '/boot/grub/menu.lst', 'MenuLst')
    attach_hardware(report) 

    if report.has_key('StacktraceTop'):
        top_fn = report['StacktraceTop'].splitlines()[0]
        if 'libx86.so' in top_fn or 'run_vm86' in top_fn:
            report['UnreportableReason'] = 'The crash happened in the firmware of \
the computer ("BIOS"), which cannot be influenced by the operating system.'
