const Cc = Components.classes;
const Ci = Components.interfaces;

// This is copied from toolkit/components/content/js/lang.js.
// It seems cleaner to copy this rather than #include from so far away.
Function.prototype.inherits = function(parentCtor) {
  var tempCtor = function(){};
  tempCtor.prototype = parentCtor.prototype;
  this.superClass_ = parentCtor.prototype;
  this.prototype = new tempCtor();
}  

/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is Google Safe Browsing.
 *
 * The Initial Developer of the Original Code is Google Inc.
 * Portions created by the Initial Developer are Copyright (C) 2006
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Fritz Schneider <fritz@google.com> (original author)
 *   Scott MacGregor <mscott@mozilla.org>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */

// We instantiate this variable when we create the application.
var gDataProvider = null;

// An instance of our application is a PROT_Application object. It
// basically just populates a few globals and instantiates wardens and
// the listmanager.

/**
 * An instance of our application. There should be exactly one of these.
 * 
 * Note: This object should instantiated only at profile-after-change
 * or later because the listmanager and the cryptokeymanager need to
 * read and write data files. Additionally, NSS isn't loaded until
 * some time around then (Moz bug #321024).
 *
 * @constructor
 */
function PROT_Application() {
  this.debugZone= "application";
  
  this.PROT_PhishingWarden = PROT_PhishingWarden;

  // Load data provider pref values
  gDataProvider = new PROT_DataProvider();

  // expose the object
  this.wrappedJSObject = this;
}

/**
 * @return String the report phishing URL (localized).
 */
PROT_Application.prototype.getReportPhishingURL = function() {
  return gDataProvider.getReportPhishURL();
}
/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is Google Safe Browsing.
 *
 * The Initial Developer of the Original Code is Google Inc.
 * Portions created by the Initial Developer are Copyright (C) 2006
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Fritz Schneider <fritz@google.com> (original author)
 *   J. Paul Reed <preed@mozilla.com>
 *   Scott MacGregor <mscott@mozilla.org>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */


// A class that encapsulates data provider specific values.  The
// root of the provider pref tree is browser.safebrowsing.provider.
// followed by a number, followed by specific properties.  The properties
// that a data provider can supply are:
//
// name: The name of the provider
// lookupURL: The URL to send requests to in enhanced mode
// keyURL: Before we send URLs in enhanced mode, we need to encrypt them
// reportURL: When shown a warning bubble, we send back the user decision
//            (get me out of here/ignore warning) to this URL (strip cookies
//            first).  This is optional.
// reportGenericURL: HTML page for general user feedback
// reportPhishURL: HTML page for notifying the provider of a new phishing page
// reportErrorURL: HTML page for notifying the provider of a false positive

const kDataProviderIdPref = 'browser.safebrowsing.dataProvider';
const kProviderBasePref = 'browser.safebrowsing.provider.';

const MOZ_PARAM_LOCALE = /\{moz:locale\}/g;
const MOZ_PARAM_CLIENT = /\{moz:client\}/g;
const MOZ_PARAM_BUILDID = /\{moz:buildid\}/g;
const MOZ_PARAM_VERSION = /\{moz:version\}/g;

/**
 * Information regarding the data provider.
 */
function PROT_DataProvider() {
  this.prefs_ = new G_Preferences();

  this.loadDataProviderPrefs_();
  
  // Watch for changes in the data provider and update accordingly.
  this.prefs_.addObserver(kDataProviderIdPref,
                          BindToObject(this.loadDataProviderPrefs_, this));

  // Watch for when anti-phishing is toggled on or off.
  this.prefs_.addObserver(kPhishWardenEnabledPref,
                          BindToObject(this.loadDataProviderPrefs_, this));
}

/**
 * Populate all the provider variables.  We also call this when whenever
 * the provider id changes.
 */
PROT_DataProvider.prototype.loadDataProviderPrefs_ = function() {
  // Currently, there's no UI for changing local list provider so we
  // hard code the value for provider 0.
  this.updateURL_ = this.getUrlPref_(
        'browser.safebrowsing.provider.0.updateURL');

  var id = this.prefs_.getPref(kDataProviderIdPref, null);

  // default to 0
  if (null == id)
    id = 0;
  
  var basePref = kProviderBasePref + id + '.';

  this.name_ = this.prefs_.getPref(basePref + "name", "");

  // Urls used to get data from a provider
  this.lookupURL_ = this.getUrlPref_(basePref + "lookupURL");
  this.keyURL_ = this.getUrlPref_(basePref + "keyURL");
  this.reportURL_ = this.getUrlPref_(basePref + "reportURL");

  // Urls to HTML report pages
  this.reportGenericURL_ = this.getUrlPref_(basePref + "reportGenericURL");
  this.reportErrorURL_ = this.getUrlPref_(basePref + "reportErrorURL");
  this.reportPhishURL_ = this.getUrlPref_(basePref + "reportPhishURL");

  // Propogate the changes to the list-manager.
  this.updateListManager_();
}

/**
 * The list manager needs urls to operate.  It needs a url to know where the
 * table updates are, and it needs a url for decrypting enchash style tables.
 */
PROT_DataProvider.prototype.updateListManager_ = function() {
  var listManager = Cc["@mozilla.org/url-classifier/listmanager;1"]
                      .getService(Ci.nsIUrlListManager);

  // If we add support for changing local data providers, we need to add a
  // pref observer that sets the update url accordingly.
  listManager.setUpdateUrl(this.getUpdateURL());

  // setKeyUrl has the side effect of fetching a key from the server.
  // This shouldn't happen if anti-phishing is disabled, so we need to
  // check for that.
  var isEnabled = this.prefs_.getPref(kPhishWardenEnabledPref, false);
  if (isEnabled) {
    listManager.setKeyUrl(this.getKeyURL());
  }
}

/**
 * Lookup the value of a URL from prefs file and do parameter substitution.
 */
PROT_DataProvider.prototype.getUrlPref_ = function(prefName) {
  var url = this.prefs_.getPref(prefName);

  var appInfo = Components.classes["@mozilla.org/xre/app-info;1"]
                          .getService(Components.interfaces.nsIXULAppInfo);

  // What value should we use here for Thunderbird??
  var mozClientStr = appInfo.name;

  // Parameter substitution
  url = url.replace(MOZ_PARAM_LOCALE, this.getLocale_());
  url = url.replace(MOZ_PARAM_CLIENT, mozClientStr + appInfo.version);
  url = url.replace(MOZ_PARAM_BUILDID, appInfo.appBuildID);
  url = url.replace(MOZ_PARAM_VERSION, appInfo.platformVersion);
  return url;
}

/**
 * @return String the user locale (similar code is in nsSearchService.js)
 */
PROT_DataProvider.prototype.getLocale_ = function() {
  const localePref = "general.useragent.locale";
  var locale = this.getLocalizedPref_(localePref);
  if (locale)
    return locale;

  // Not localized
  var prefs = new G_Preferences();
  return prefs.getPref(localePref, "");
}

/**
 * @return String name of the localized pref, null if none exists.
 */
PROT_DataProvider.prototype.getLocalizedPref_ = function(aPrefName) {
  // G_Preferences doesn't know about complex values, so we use the
  // xpcom object directly.
  var prefs = Cc["@mozilla.org/preferences-service;1"]
              .getService(Ci.nsIPrefBranch);
  try {
    return prefs.getComplexValue(aPrefName, Ci.nsIPrefLocalizedString).data;
  } catch (ex) {
  }
  return "";
}

//////////////////////////////////////////////////////////////////////////////
// Getters for the remote provider pref values mentioned above.
PROT_DataProvider.prototype.getName = function() {
  return this.name_;
}

PROT_DataProvider.prototype.getUpdateURL = function() {
  return this.updateURL_;
}

PROT_DataProvider.prototype.getLookupURL = function() {
  return this.lookupURL_;
}
PROT_DataProvider.prototype.getKeyURL = function() {
  return this.keyURL_;
}
PROT_DataProvider.prototype.getReportURL = function() {
  return this.reportURL_;
}

PROT_DataProvider.prototype.getReportGenericURL = function() {
  return this.reportGenericURL_;
}
PROT_DataProvider.prototype.getReportErrorURL = function() {
  return this.reportErrorURL_;
}
PROT_DataProvider.prototype.getReportPhishURL = function() {
  return this.reportPhishURL_;
}
/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is Google Safe Browsing.
 *
 * The Initial Developer of the Original Code is Google Inc.
 * Portions created by the Initial Developer are Copyright (C) 2006
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Niels Provos <niels@google.com> (original author)
 *   Fritz Schneider <fritz@google.com>
 *   Scott MacGregor <mscott@mozilla.org>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */

// A warden that knows how to register lists with a listmanager and keep them
// updated if necessary.  The ListWarden also provides a simple interface to
// check if a URL is evil or not.  Specialized wardens like the PhishingWarden
// inherit from it.
//
// Classes that inherit from ListWarden are responsible for calling
// enableTableUpdates or disableTableUpdates.  This usually entails
// registering prefObservers and calling enable or disable in the base
// class as appropriate.
//

/**
 * Abtracts the checking of user/browser actions for signs of
 * phishing. 
 *
 * @constructor
 */
function PROT_ListWarden() {
  this.debugZone = "listwarden";
  var listManager = Cc["@mozilla.org/url-classifier/listmanager;1"]
                      .getService(Ci.nsIUrlListManager);
  this.listManager_ = listManager;

  // Once we register tables, their respective names will be listed here.
  this.blackTables_ = [];
  this.whiteTables_ = [];
}

PROT_ListWarden.IN_BLACKLIST = 0
PROT_ListWarden.IN_WHITELIST = 1
PROT_ListWarden.NOT_FOUND = 2

/**
 * Tell the ListManger to keep all of our tables updated
 */

PROT_ListWarden.prototype.enableBlacklistTableUpdates = function() {
  for (var i = 0; i < this.blackTables_.length; ++i) {
    this.listManager_.enableUpdate(this.blackTables_[i]);
  }
}

/**
 * Tell the ListManager to stop updating our tables
 */

PROT_ListWarden.prototype.disableBlacklistTableUpdates = function() {
  for (var i = 0; i < this.blackTables_.length; ++i) {
    this.listManager_.disableUpdate(this.blackTables_[i]);
  }
}

/**
 * Tell the ListManager to update whitelist tables.  They may be enabled even
 * when other updates aren't, for performance reasons.
 */
PROT_ListWarden.prototype.enableWhitelistTableUpdates = function() {
  for (var i = 0; i < this.whiteTables_.length; ++i) {
    this.listManager_.enableUpdate(this.whiteTables_[i]);
  }
}

/**
 * Tell the ListManager to stop updating whitelist tables.
 */
PROT_ListWarden.prototype.disableWhitelistTableUpdates = function() {
  for (var i = 0; i < this.whiteTables_.length; ++i) {
    this.listManager_.disableUpdate(this.whiteTables_[i]);
  }
}

/**
 * Register a new black list table with the list manager
 * @param tableName - name of the table to register
 * @returns true if the table could be registered, false otherwise
 */

PROT_ListWarden.prototype.registerBlackTable = function(tableName) {
  var result = this.listManager_.registerTable(tableName, false);
  if (result) {
    this.blackTables_.push(tableName);
  }
  return result;
}

/**
 * Register a new white list table with the list manager
 * @param tableName - name of the table to register
 * @returns true if the table could be registered, false otherwise
 */

PROT_ListWarden.prototype.registerWhiteTable = function(tableName) {
  var result = this.listManager_.registerTable(tableName, false);
  if (result) {
    this.whiteTables_.push(tableName);
  }
  return result;
}

/**
 * Method that looks up a url on the whitelist.
 *
 * @param url The URL to check
 * @param callback Function with a single param:
 *       PROT_ListWarden.IN_BLACKLIST, PROT_ListWarden.IN_WHITELIST,
 *       or PROT_ListWarden.NOT_FOUND
 */
PROT_ListWarden.prototype.isWhiteURL = function(url, callback) {
  (new MultiTableQuerier(url,
                         this.whiteTables_,
                         [] /* no blacklists */,
                         callback)).run();
}

/**
 * Method that looks up a url in both the white and black lists.
 *
 * If there is conflict, the white list has precedence over the black list.
 *
 * This is tricky because all database queries are asynchronous.  So we need
 * to chain together our checks against white and black tables.  We use
 * MultiTableQuerier (see below) to manage this.
 *
 * @param msgURI uri corresponding to the message the url came from
 * @param aFailsStaticTests boolean result for whether the url failed our static tests
 * @param url URL to look up
 * @param callback Function with a single param:
 *       PROT_ListWarden.IN_BLACKLIST, PROT_ListWarden.IN_WHITELIST,
 *       or PROT_ListWarden.NOT_FOUND
 */
PROT_ListWarden.prototype.isEvilURL = function(msgURI, aFailsStaticTests, url, callback) {
  var evilCallback = BindToObject(callback,
                                  null,
                                  msgURI,
                                  aFailsStaticTests,
                                  url);

  (new MultiTableQuerier(url,
                         this.whiteTables_,
                         this.blackTables_,
                         evilCallback)).run();
}

/**
 * This class helps us query multiple tables even though each table check
 * is asynchronous.  It provides callbacks for each listManager lookup
 * and decides whether we need to continue querying or not.  After
 * instantiating the method, use run() to invoke.
 *
 * @param url String The url to check
 * @param whiteTables Array of strings with each white table name
 * @param blackTables Array of strings with each black table name
 * @param callback Function to call with result 
 *       PROT_ListWarden.IN_BLACKLIST, PROT_ListWarden.IN_WHITELIST,
 *       or PROT_ListWarden.NOT_FOUND
 */
function MultiTableQuerier(url, whiteTables, blackTables, callback) {
  this.debugZone = "multitablequerier";
  this.url_ = url;

  this.whiteTables_ = whiteTables;
  this.blackTables_ = blackTables;
  this.whiteIdx_ = 0;
  this.blackIdx_ = 0;

  this.callback_ = callback;
  this.listManager_ = Cc["@mozilla.org/url-classifier/listmanager;1"]
                      .getService(Ci.nsIUrlListManager);
}

/**
 * We first query the white tables in succession.  If any contain
 * the url, we stop.  If none contain the url, we query the black tables
 * in succession.  If any contain the url, we call callback and
 * stop.  If none of the black tables contain the url, then we just stop
 * (i.e., it's not black url).
 */
MultiTableQuerier.prototype.run = function() {
  var whiteTable = this.whiteTables_[this.whiteIdx_];
  var blackTable = this.blackTables_[this.blackIdx_];
  if (whiteTable) {
    //G_Debug(this, "Looking in whitetable: " + whiteTable);
    ++this.whiteIdx_;
    this.listManager_.safeExists(whiteTable, this.url_,
                                 BindToObject(this.whiteTableCallback_,
                                              this));
  } else if (blackTable) {
    //G_Debug(this, "Looking in blacktable: " + blackTable);
    ++this.blackIdx_;
    this.listManager_.safeExists(blackTable, this.url_,
                                 BindToObject(this.blackTableCallback_,
                                              this));
  } else {
    // No tables left to check, so we quit.
    G_Debug(this, "Not found in any tables: " + this.url_);
    this.callback_(PROT_ListWarden.NOT_FOUND);

    // Break circular ref to callback.
    this.callback_ = null;
    this.listManager_ = null;
  }
}

/**
 * After checking a white table, we return here.  If the url is found,
 * we can stop.  Otherwise, we call run again.
 */
MultiTableQuerier.prototype.whiteTableCallback_ = function(isFound) {
  //G_Debug(this, "whiteTableCallback_: " + isFound);
  if (!isFound)
    this.run();
  else {
    G_Debug(this, "Found in whitelist: " + this.url_)
    this.callback_(PROT_ListWarden.IN_WHITELIST);

    // Break circular ref to callback.
    this.callback_ = null;
    this.listManager_ = null;
  }
}

/**
 * After checking a black table, we return here.  If the url is found,
 * we can call the callback and stop.  Otherwise, we call run again.
 */
MultiTableQuerier.prototype.blackTableCallback_ = function(isFound) {
  //G_Debug(this, "blackTableCallback_: " + isFound);
  if (!isFound) {
    this.run();
  } else {
    // In the blacklist, must be an evil url.
    G_Debug(this, "Found in blacklist: " + this.url_)
    this.callback_(PROT_ListWarden.IN_BLACKLIST);

    // Break circular ref to callback.
    this.callback_ = null;
    this.listManager_ = null;
  }
}
/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is Google Safe Browsing.
 *
 * The Initial Developer of the Original Code is Google Inc.
 * Portions created by the Initial Developer are Copyright (C) 2006
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Fritz Schneider <fritz@google.com> (original author)
 *   Scott MacGregor <mscott@mozilla.org>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */


// The warden checks URLs to see if they are phishing URLs. It
// does so by querying our locally stored blacklists (privacy
// mode).
//
// Note: There is a single warden for the whole application.

const kPhishWardenEnabledPref = "browser.safebrowsing.enabled";

// We have hardcoded URLs that let people navigate to in order to 
// check out the warning.
const kTestUrls = {
  "http://www.google.com/tools/firefox/safebrowsing/phish-o-rama.html": true,
  "http://www.mozilla.org/projects/bonecho/anti-phishing/its-a-trap.html": true,
  "http://www.mozilla.com/firefox/its-a-trap.html": true,
}

/**
 * Abtracts the checking of user/browser actions for signs of
 * phishing. 
 *
 * @param progressListener nsIDocNavStartProgressListener
 * @constructor
 */
function PROT_PhishingWarden(progressListener) {
  PROT_ListWarden.call(this);

  this.debugZone = "phishwarden";
  this.testing_ = false;

  // Use this to query preferences
  this.prefs_ = new G_Preferences();
  
  // Global preference to enable the phishing warden
  this.phishWardenEnabled_ = this.prefs_.getPref(kPhishWardenEnabledPref, null);

  // Get notifications when the phishing warden enabled pref changes
  var phishWardenPrefObserver = 
    BindToObject(this.onPhishWardenEnabledPrefChanged, this);
  this.prefs_.addObserver(kPhishWardenEnabledPref, phishWardenPrefObserver);
  
  // Get notifications when the data provider pref changes
  var dataProviderPrefObserver =
    BindToObject(this.onDataProviderPrefChanged, this);
  this.prefs_.addObserver(kDataProviderIdPref, dataProviderPrefObserver);

  G_Debug(this, "phishWarden initialized");
}

PROT_PhishingWarden.inherits(PROT_ListWarden);

/**
 * We implement nsIWebProgressListener
 */
PROT_PhishingWarden.prototype.QueryInterface = function(iid) {
  if (iid.equals(Ci.nsISupports) || 
      iid.equals(Ci.nsISupportsWeakReference))
    return this;
  throw Components.results.NS_ERROR_NO_INTERFACE;
}

/**
 * Cleanup on shutdown.
 */
PROT_PhishingWarden.prototype.shutdown = function() {
}

/**
 * When a preference (either advanced features or the phishwarden
 * enabled) changes, we might have to start or stop asking for updates. 
 * 
 * This is a little tricky; we start or stop management only when we
 * have complete information we can use to determine whether we
 * should.  It could be the case that one pref or the other isn't set
 * yet (e.g., they haven't opted in/out of advanced features). So do
 * nothing unless we have both pref values -- we get notifications for
 * both, so eventually we will start correctly.
 */ 
PROT_PhishingWarden.prototype.maybeToggleUpdateChecking = function() {
  if (this.testing_)
    return;

  var phishWardenEnabled = this.prefs_.getPref(kPhishWardenEnabledPref, null);

  // Do nothing unless the phishing warden pref is set.  It can be null (unset), true, or
  // false.
  if (phishWardenEnabled === null)
    return;

  // We update and save to disk all tables if we don't have remote checking
  // enabled.
  if (phishWardenEnabled === true) {
    // If anti-phishing is enabled, we always download the local files to
    // use in case remote lookups fail.
    this.enableBlacklistTableUpdates();
    this.enableWhitelistTableUpdates();
  } else {
    // Anti-phishing is off, disable table updates
    this.disableBlacklistTableUpdates();
    this.disableWhitelistTableUpdates();
  }
}

/**
 * Deal with a user changing the pref that says whether we should 
 * enable the phishing warden (i.e., that SafeBrowsing is active)
 *
 * @param prefName Name of the pref holding the value indicating whether
 *                 we should enable the phishing warden
 */
PROT_PhishingWarden.prototype.onPhishWardenEnabledPrefChanged = function(
                                                                    prefName) {
  this.phishWardenEnabled_ = this.prefs_.getBoolPrefOrDefault(prefName, this.phishWardenEnabled_);
  this.maybeToggleUpdateChecking();
}

/**
 * Event fired when the user changes data providers.
 */
PROT_PhishingWarden.prototype.onDataProviderPrefChanged = function(prefName) {
}

/**
 * Indicates if this URL is one of the possible blacklist test URLs.
 * These test URLs should always be considered as phishy.
 *
 * @param url URL to check 
 * @return A boolean indicating whether this is one of our blacklist
 *         test URLs
 */
PROT_PhishingWarden.prototype.isBlacklistTestURL = function(url) {
  // Explicitly check for URL so we don't get JS warnings in strict mode.
  if (kTestUrls[url])
    return true;
  return false;
}

/**
 * Callback for found local blacklist match.  First we report that we have
 * a blacklist hit, then we bring up the warning dialog.
 * @param status Number enum from callback (PROT_ListWarden.IN_BLACKLIST,
 *    PROT_ListWarden.IN_WHITELIST, PROT_ListWarden.NOT_FOUND)
 */
PROT_PhishingWarden.prototype.localListMatch_ = function(url, request, status) {
  if (PROT_ListWarden.IN_BLACKLIST != status)
    return;
}
//@line 17 "/build/buildd/thunderbird-2.0.0.22+build1+nobinonly/build-tree/mozilla/mail/components/phishing/nsPhishingProtectionApplication.js"

var modScope = this;
function Init() {
  var jslib = Cc["@mozilla.org/url-classifier/jslib;1"]
              .getService().wrappedJSObject;
  modScope.String.prototype.startsWith = jslib.String.prototype.startsWith;
  modScope.G_Debug = jslib.G_Debug;
  modScope.G_Assert = jslib.G_Assert;
  modScope.G_Alarm = jslib.G_Alarm;
  modScope.G_ConditionalAlarm = jslib.G_ConditionalAlarm;
  modScope.G_ObserverWrapper = jslib.G_ObserverWrapper;
  modScope.G_Preferences = jslib.G_Preferences;
  modScope.PROT_XMLFetcher = jslib.PROT_XMLFetcher;
  modScope.BindToObject = jslib.BindToObject;
  modScope.G_Protocol4Parser = jslib.G_Protocol4Parser;
  modScope.G_ObjectSafeMap = jslib.G_ObjectSafeMap;
  modScope.PROT_UrlCrypto = jslib.PROT_UrlCrypto;
  modScope.RequestBackoff = jslib.RequestBackoff;
  
  // We only need to call Init once
  modScope.Init = function() {};
}

// Module object
function PhishingProtectionApplicationMod() {
  this.firstTime = true;
  this.cid = Components.ID("{C46D1931-4B6A-4e52-99B0-7877F70634DE}");
  this.progid = "@mozilla.org/phishingprotection/application;1";
}

PhishingProtectionApplicationMod.prototype.registerSelf = function(compMgr, fileSpec, loc, type) {
  if (this.firstTime) {
    this.firstTime = false;
    throw Components.results.NS_ERROR_FACTORY_REGISTER_AGAIN;
  }
  compMgr = compMgr.QueryInterface(Ci.nsIComponentRegistrar);
  compMgr.registerFactoryLocation(this.cid,
                                  "Phishing Protection Application Module",
                                  this.progid,
                                  fileSpec,
                                  loc,
                                  type);
};

PhishingProtectionApplicationMod.prototype.getClassObject = function(compMgr, cid, iid) {  
  if (!cid.equals(this.cid))
    throw Components.results.NS_ERROR_NO_INTERFACE;
  if (!iid.equals(Ci.nsIFactory))
    throw Components.results.NS_ERROR_NOT_IMPLEMENTED;

  return this.factory;
}

PhishingProtectionApplicationMod.prototype.canUnload = function(compMgr) {
  return true;
}

PhishingProtectionApplicationMod.prototype.factory = {
  createInstance: function(outer, iid) {
    if (outer != null)
      throw Components.results.NS_ERROR_NO_AGGREGATION;
    Init();
    return new PROT_Application();
  }
};

var ApplicationModInst = new PhishingProtectionApplicationMod();

function NSGetModule(compMgr, fileSpec) {
  return ApplicationModInst;
}
