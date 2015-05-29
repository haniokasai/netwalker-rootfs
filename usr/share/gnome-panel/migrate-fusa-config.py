#!/usr/bin/python

import gconf
import os.path
import sys

from gettext import gettext as _
import gettext

#FIXME: add checks here and run without UI if that fails to import
import pygtk
pygtk.require('2.0')
import gtk

def error(primary, secondary):
    d = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    d.set_markup("<b><big>%s</big></b>" % primary)
    d.format_secondary_text(secondary)
    d.run()
    d.destroy()
    
def info(primary, secondary):
    d = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
    d.set_markup("<b><big>%s</big></b>" % primary)
    d.format_secondary_text(secondary)
    d.run()
    d.destroy()

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
    gettext.bindtextdomain("gnome-panel")

    engine = gconf.engine_get_default()
    client = gconf.client_get_for_engine(engine)
    objects = client.all_dirs("/apps/panel/objects")

    logout=None
    logout_panel=None
    for d in objects:
        if client.get_string(os.path.join(d,"action_type")) == "logout":
            logout=os.path.basename(d)
            logout_panel=client.get_string(os.path.join(d,"toplevel_id"))
            break

    # we do not have a logout object or in a non-standard location, fail
    if not logout:
        error(_("No logout button found"),
              _("The logout button can not be found or it is not in "
                "the standard location. Please update the panel "
                "configuration manually."))
        sys.exit(1)

    if not os.path.exists("/usr/lib/fast-user-switch-applet/fast-user-switch-applet"):
        error(_("No fast-user-switching applet found"),
              _("The fusa applet can not be found or it is not in "
                "the standard location. Please update the panel "
                "configuration manually."))
        sys.exit(1)

    # search for the fusa applet
    applets = client.all_dirs("/apps/panel/applets")
    for d in applets:
        # move the fusa applet to new location
        if (client.get_string(os.path.join(d,"bonobo_iid")) == "OAFIID:GNOME_FastUserSwitchApplet"):
            client.set_int(os.path.join(d,"position"),0)
            client.set_bool(os.path.join(d,"panel_right_stick"), True)
            break
    else:
        # create a new one
        applet_name = "applet_fusa_auto_migrated"
        new_applet_name = os.path.join("/apps/panel/applets/",applet_name)
        associate_schemas_in_dir(client, engine, new_applet_name,
                                 "/schemas/apps/panel/objects")
        client.set_string(os.path.join(new_applet_name, "bonobo_iid"), 
                          "OAFIID:GNOME_FastUserSwitchApplet")
        client.set_string(os.path.join(new_applet_name, "toplevel_id"), 
                          logout_panel)
        client.set_string(os.path.join(new_applet_name, "object_type"), 
                          "bonobo-applet")
        client.set_bool(os.path.join(new_applet_name, "panel_right_stick"), True)
        l=client.get_list("/apps/panel/general/applet_id_list", gconf.VALUE_STRING)
        l.append(applet_name)
        client.set_list("/apps/panel/general/applet_id_list", gconf.VALUE_STRING, l)

    # remove the logout button (if its in the object_id_list)
    l=client.get_list("/apps/panel/general/object_id_list", gconf.VALUE_STRING)
    try:
        l.remove(logout)
        client.set_list("/apps/panel/general/object_id_list", gconf.VALUE_STRING, l)
    except ValueError, e:
        # print out message here so that it gets captured in .xsession-errors
        sys.stderr.write("ignoring logout object '%s' (not in object_id_list: %s)" % (logout, e))

    # show nice information
    info(_("Configuration updated"),
         _("Your panel configuration is updated. Please logout "
           "to complete the update."))

