# DistUpgradeMain.py 
#  
#  Copyright (c) 2004-2008 Canonical
#  
#  Author: Michael Vogt <michael.vogt@ubuntu.com>
# 
#  This program is free software; you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA

from DistUpgradeController import DistUpgradeController
from DistUpgradeConfigParser import DistUpgradeConfig
import logging
import os
import sys
import glob
import shutil
from datetime import datetime
from optparse import OptionParser
from gettext import gettext as _

def do_commandline():
    " setup option parser and parse the commandline "
    parser = OptionParser()
    parser.add_option("-s", "--sandbox", dest="useAufs", default=False,
                      action="store_true",
                      help=_("Sandbox upgrade using aufs"))
    parser.add_option("-c", "--cdrom", dest="cdromPath", default=None,
                      help=_("Use the given path to search for a cdrom with upgradable packages"))
    parser.add_option("--have-prerequists", dest="havePrerequists",
                      action="store_true", default=False)
    parser.add_option("--with-network", dest="withNetwork",action="store_true")
    parser.add_option("--without-network", dest="withNetwork",action="store_false")
    parser.add_option("--frontend", dest="frontend",default=None,
                      help=_("Use frontend. Currently available: \n"\
                             "DistUpgradeViewText, DistUpgradeViewGtk, DistUpgradeViewKDE"))
    parser.add_option("--mode", dest="mode",default="desktop",
                      help=_("*DEPRECATED* this option will be ignore"))
    parser.add_option("--partial", dest="partial", default=False,
                      action="store_true", 
                      help=_("Perform a partial upgrade only (no sources.list rewriting)"))
    parser.add_option("--datadir", dest="datadir", default=None,
                      help=_("Set datadir"))
    return parser.parse_args()
    
def setup_logging(options, config):
    " setup the logging "
    logdir = config.getWithDefault("Files","LogDir","/var/log/dist-upgrade/")
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    # check if logs exists and move logs into place
    if glob.glob(logdir+"/*.log"):
        now = datetime.now()
        backup_dir = logdir+"/%04i%02i%02i-%02i%02i" % (now.year,now.month,now.day,now.hour,now.minute)
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        for f in glob.glob(logdir+"/*.log"):
            shutil.move(f, os.path.join(backup_dir,os.path.basename(f)))
    fname = os.path.join(logdir,"main.log")
    # do not overwrite the default main.log
    if options.partial:
        fname += ".partial"
    logging.basicConfig(level=logging.DEBUG,
                        filename=fname,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode='w')
    # log what config files are in use here to detect user
    # changes
    logging.info("Using config files '%s'" % config.config_files)
    return logdir
    
def setup_view(options, config, logdir):
    " setup view based on the config and commandline "

    # the commandline overwrites the configfile
    for requested_view in [options.frontend]+config.getlist("View","View"):
        if not requested_view:
            continue
        try:
            view_modul = __import__(requested_view)
            view_class = getattr(view_modul, requested_view)
            break
        except (ImportError, AttributeError, TypeError), e:
            logging.warning("can't import view '%s' (%s)" % (requested_view,e))
            print "can't load %s (%s)" % (requested_view, e)
    else:
        logging.error("No view can be imported, aborting")
        print "No view can be imported, aborting"
        sys.exit(1)
    return view_class(logdir=logdir)

def main():
    " main method "
    
    # commandline setup and config
    (options, args) = do_commandline()
    config = DistUpgradeConfig(".")
    logdir = setup_logging(options, config)

    from DistUpgradeVersion import VERSION
    logging.info("release-upgrader version '%s' started" % VERSION)

    # create view and app objects
    view = setup_view(options, config, logdir)
    app = DistUpgradeController(view, options, datadir=options.datadir)

    # partial upgrade only
    if options.partial:
        if not app.doPartialUpgrade():
            sys.exit(1)
        sys.exit(0)

    # full upgrade
    app.run()

