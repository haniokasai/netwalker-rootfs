#!/usr/bin/python
#
# this script will exaimne /etc/xorg/xorg.conf and 
# transition from broken proprietary drivers to the free ones
#

import apt
import sys
import os
import os.path
import logging
import time
import shutil
import subprocess
import apt_pkg

XORG_CONF="/etc/X11/xorg.conf"

def remove_input_devices(xorg_source=XORG_CONF, xorg_destination=XORG_CONF):
    logging.debug("remove_input_devices")
    content=[]
    in_input_devices = False
    for raw in open(xorg_source):
        line = raw.strip()
        if (line.lower().startswith("section") and 
            line.lower().split("#")[0].strip().endswith('"inputdevice"')):
            logging.debug("found 'InputDevice' section")
            content.append("# commented out by update-manager, HAL is now used\n")
            content.append("#"+raw)
            in_input_devices=True
        elif line.lower().startswith("endsection") and in_input_devices:
            content.append("#"+raw)
            in_input_devices=False
        elif line.lower().startswith("inputdevice"):
            logging.debug("commenting out '%s' " % line)
            content.append("# commented out by update-manager, HAL is now used\n")
            content.append("#"+raw)
        elif in_input_devices:
            logging.debug("commenting out '%s' " % line)
            content.append("#"+raw)
        else:
            content.append(raw)
    open(xorg_destination+".new","w").write("".join(content))
    os.rename(xorg_destination+".new", xorg_destination)
    return True

def replace_driver_from_xorg(old_driver, new_driver, xorg=XORG_CONF):
    """
    this removes the fglrx driver from the xorg.conf and subsitutes
    it with the ati one
    """
    if not os.path.exists(xorg):
        logging.warning("file %s not found" % xorg)
        return
    content=[]
    for line in open(xorg):
        # remove comments
        s=line.split("#")[0].strip()
        # check for fglrx driver entry
        if (s.lower().startswith("driver") and
            s.endswith('"%s"' % old_driver)):
            logging.debug("line '%s' found" % line)
            line='\tDriver\t"%s"\n' % new_driver
            logging.debug("replacing with '%s'" % line)
        content.append(line)
    # write out the new version
    if open(xorg).readlines() != content:
        logging.info("saveing new %s (%s -> %s)" % (xorg, old_driver, new_driver))
        open(xorg+".xorg_fix","w").write("".join(content))
        os.rename(xorg+".xorg_fix", xorg)

def is_multiseat(xorg_source=XORG_CONF):
    " check if we have a multiseat xorg config "
    def is_serverlayout_line(line):
        return (not line.strip().startswith("#") and
                line.strip().lower().endswith('"serverlayout"'))
    msl = len(filter(is_serverlayout_line, open(xorg_source)))
    logging.debug("is_multiseat: lines %i", msl)
    return msl > 1

if __name__ == "__main__":
    if not os.getuid() == 0:
        print "Need to run as root"
        sys.exit(1)

    # we pretend to be update-manger so that apport picks up when we crash
    sys.argv[0] = "/usr/bin/update-manager"

    # setup logging
    logging.basicConfig(level=logging.DEBUG,
                        filename="/var/log/dist-upgrade/xorg_fix_intrepid.log",
                        filemode='w')
    
    logging.info("%s running" % sys.argv[0])

    if not os.path.exists(XORG_CONF):
        logging.info("No xorg.conf, exiting")
        sys.exit(0)
        
    #make a backup of the xorg.conf
    backup = XORG_CONF + ".dist-upgrade-" + time.strftime("%Y%m%d%H%M")
    logging.debug("creating backup '%s'" % backup)
    shutil.copy(XORG_CONF, backup)

    if (not os.path.exists("/usr/lib/xorg/modules/drivers/fglrx_drv.so") and
        "fglrx" in open(XORG_CONF).read()):
        logging.info("Removing fglrx from %s" % XORG_CONF)
        replace_driver_from_xorg("fglrx","ati")

    if (not os.path.exists("/usr/lib/xorg/modules/drivers/nvidia_drv.so") and
        "nvidia" in open(XORG_CONF).read()):
        logging.info("Removing nvidia from %s" % XORG_CONF)
        replace_driver_from_xorg("nvidia","nv")

    # now run the removeInputDevices() if we have a new xserver
    ver=subprocess.Popen(["dpkg-query","-W","-f=${Version}","xserver-xorg-core"], stdout=subprocess.PIPE).communicate()[0]
    logging.info("xserver-xorg-core version is '%s'" % ver)
    if ver and apt_pkg.VersionCompare(ver, "2:1.5.0") > 0:
        if not is_multiseat():
            remove_input_devices()
        else:
            logging.info("multiseat setup, ignoring")
