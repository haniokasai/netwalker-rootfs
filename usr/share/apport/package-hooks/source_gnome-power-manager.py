'''apport package hook for gnome-power-manager

(c) 2009 Canonical Ltd.
Author: Steve Beattie <sbeattie@ubuntu.com>
'''

from apport.hookutils import *
from os import path

def attach_hal_capability_present(report, cap, capid):
    match_error = re.compile("^Error")
    if not match_error.match(hal_find_by_capability(cap)[0]):
        report[capid] = "Present"
        found = True
    else:
        report[capid] = "Not Present"
        found = False
    return found

def add_info(report):
    attach_hal_capability_present(report, 'ac_adapter', 'ACAdapter')
    attach_hal_capability_present(report, 'laptop_panel', 'LaptopPanel')
    attach_hal_capability_present(report, 'cpufreq_control', 'CPUScaling')

    if attach_hal_capability_present(report, 'battery', 'Battery'):
        battery_info = ''
        for udi in hal_find_by_capability('battery'):
            battery_info += hal_dump_udi(udi)
        report[BatteryInfo] = battery_info
	
    attach_hardware(report) 

    attach_gconf(report, 'gnome-power-manager')
