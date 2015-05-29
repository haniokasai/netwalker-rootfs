#!/usr/bin/python

import os.path
import sys
import time
import gconf

def msg(type, primary, secondary=""):
    sys.stderr.write("[%s] %s: %s\n" % (os.path.basename(sys.argv[0]),
                                        type, primary))
    if secondary:
	    sys.stderr.write("%s\n\n" % secondary)

def error(primary, secondary=""):
    msg("ERROR", primary, secondary)
    
def info(primary, secondary=""):
    msg("INFO", primary, secondary)

def log_excepthook(exc_type, exc_obj, exc_tb):
    import traceback
    l = traceback.format_exception(exc_type, exc_obj, exc_tb)
    error("exception","".join(l))
    
def associate_schemas_in_dir(client, engine, profile_dir, schema_dir):
    """ 
    helper that takes a gconf schema dir and creates a new profile dir
    based on the schema, useful for e.g. adding a applet to the panel
    """
    for e in client.all_entries(schema_dir):
        schema_key = os.path.basename(e.get_key())
        key = os.path.join(profile_dir, schema_key)
        engine.associate_schema(key, e.get_key())
    client.suggest_sync()

if __name__ == "__main__":
    sys.excepthook = log_excepthook
    info("started")

    if not os.path.exists("/usr/lib/indicator-applet/indicator-applet"):
        info("no indicator applet binary installed, exiting")
        sys.exit(0)

    engine = gconf.engine_get_default()
    client = gconf.client_get_for_engine(engine)
    #info("engine",engine)
    #info("client",client)

    # make sure this is auto-run only once
    client.set_bool("/apps/panel/need_add_indicator_applet", False)
    #info("set /apps/panel/need_add_indicator_applet to false")

    # search for the notification area applet
    applets = client.all_dirs("/apps/panel/applets")
    notification_pos = None
    notification_panel = None
    notification_right_stick = False
    for d in applets:
        #info("looking at: %s" % d)
        if (client.get_string(os.path.join(d,"bonobo_iid")) == "OAFIID:GNOME_IndicatorApplet"):
            info("Already has a indicator applet",
                 "Your panel already has a indicator applet")
            sys.exit(0)
        if (client.get_string(os.path.join(d,"bonobo_iid")) == "OAFIID:GNOME_NotificationAreaApplet"):
            notification_pos = client.get_int(os.path.join(d,"position"))
            notification_panel = client.get_string(os.path.join(d,"toplevel_id"))
            notification_right_stick = client.get_bool(os.path.join(d,"panel_right_stick"))
    # check if we found the notification area
    if (notification_pos is None or 
        notification_pos == 0 or
        notification_panel is None):
        error("Could not find notification area",
              "Please add the indicator applet manually")
        sys.exit(1)
 
    info("New post: ", notification_pos)
    info("New panel: ", notification_panel)

    # create a new indicator applet
    applet_name = "applet_indicator_auto_added"
    new_applet_name = os.path.join("/apps/panel/applets/",applet_name)
    associate_schemas_in_dir(client, engine, new_applet_name,
                             "/schemas/apps/panel/objects")
    client.set_string(os.path.join(new_applet_name, "bonobo_iid"), 
                      "OAFIID:GNOME_IndicatorApplet")
    client.set_string(os.path.join(new_applet_name, "toplevel_id"), 
                      notification_panel)
    client.set_string(os.path.join(new_applet_name, "object_type"), 
                      "bonobo-applet")
    client.set_bool(os.path.join(new_applet_name, "panel_right_stick"), 
                      notification_right_stick)
    # position depends on if tray_applet is right stick or not
    if notification_right_stick:
	notification_pos += 1
    else:
	notification_pos -= 1
    client.set_int(os.path.join(new_applet_name, "position"), 
                      notification_pos)
    l=client.get_list("/apps/panel/general/applet_id_list", gconf.VALUE_STRING)
    l.append(applet_name)
    client.set_list("/apps/panel/general/applet_id_list", gconf.VALUE_STRING, l)
    client.suggest_sync()

    # show nice information
    info("Configuration updated",
         "Your panel configuration is updated. ")

