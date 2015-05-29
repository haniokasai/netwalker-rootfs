import warnings
warnings.warn("Module gnome.applet is deprecated; "
              "please import gnomeapplet instead",
              DeprecationWarning)
del warnings

from gnomeapplet import *
