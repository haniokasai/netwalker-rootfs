// This is the Debian specific preferences file for Mozilla sunbird
// You can make any change in here, it is the purpose of this file.
// You can, with this file and all files present in the
// /etc/sunbird/pref directory, override any preference that is
// present in /usr/lib/sunbird/defaults/pref directory.
// While your changes will be kept on upgrade if you modify files in
// /etc/sunbird/pref, please note that they won't be kept if you
// do them in /usr/lib/sunbird/defaults/pref.

pref("extensions.update.enabled", true);

// Use LANG environment variable to choose locale
pref("intl.locale.matchOS", true);

// Disable default browser checking.
pref("browser.shell.checkDefaultBrowser", false);
