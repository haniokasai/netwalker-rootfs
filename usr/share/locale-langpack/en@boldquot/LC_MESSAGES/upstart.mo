Þ    
      l      ¼       ð   2   ñ   0   $  &   U  <   |     ¹  /  Ï  Û  ÿ  &   Û  !     ³  $  J   Ø	  H   #
  2   l
  H   
  !   è
  w  
  ç    2   j  -                  
      	                        %s: 'pid binary' ignored unless 'daemon' specified %s: 'pid file' ignored unless 'daemon' specified For a list of commands, try `%s help'. For more information on a command, try `%s COMMAND --help'.
 No jobs matching `%s' PRIORITY may be one of `debug' (messages useful for debugging upstart are logged, equivalent to --debug on kernel command-line); `info' (messages about job goal and state changes, as well as event emissions are logged, equivalent to --verbose on the kernel command-line); `message' (informational and debugging messages are suppressed, the default); `warn' (ordinary messages are suppressed whilst still logging warnings and errors); `error' (only errors are logged, equivalent to --quiet on the kernel command-line) or `fatal' (only fatal errors are logged). TIME may have different formats, the most common is simply the word 'now' which will bring the system down immediately.  Other valid formats are +m, where m is the number of minutes to wait until shutting down and hh:mm which specifies the time on the 24hr clock.

Logged in users are warned by a message sent to their terminal, you may include an optional MESSAGE included with this.  Messages can be sent without actually bringing the system down by using the -k option.

If TIME is given, the command will remain in the foreground until the shutdown occurs.  It can be cancelled by Control-C, or by another user using the -c option.

The system is brought down into maintenance (single-user) mode by default, you can change this with either the -r or -h option which specify a reboot or system halt respectively.  The -h option can be further modified with -H or -P to specify whether to halt the system, or to power it off afterwards.  The default is left up to the shutdown scripts. Try `%s --help' for more information.
 Unable to execute "%s" for %s: %s Project-Id-Version: upstart 0.3.9
Report-Msgid-Bugs-To: new@bugs.launchpad.net
POT-Creation-Date: 2007-10-11 22:13+0100
PO-Revision-Date: 2008-04-16 19:29+0000
Last-Translator: Launchpad Translations Administrators <rosetta@launchpad.net>
Language-Team: none
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 12:22+0000
X-Generator: Launchpad (build Unknown)
 %s: â[1mpid binary[0mâ ignored unless â[1mdaemon[0mâ specified %s: â[1mpid file[0mâ ignored unless â[1mdaemon[0mâ specified For a list of commands, try â[1m%s help[0mâ. For more information on a command, try â[1m%s COMMAND --help[0mâ.
 No jobs matching â[1m%s[0mâ PRIORITY may be one of â[1mdebug[0mâ (messages useful for debugging upstart are logged, equivalent to --debug on kernel command-line); â[1minfo[0mâ (messages about job goal and state changes, as well as event emissions are logged, equivalent to --verbose on the kernel command-line); â[1mmessage[0mâ (informational and debugging messages are suppressed, the default); â[1mwarn[0mâ (ordinary messages are suppressed whilst still logging warnings and errors); â[1merror[0mâ (only errors are logged, equivalent to --quiet on the kernel command-line) or â[1mfatal[0mâ (only fatal errors are logged). TIME may have different formats, the most common is simply the word â[1mnow[0mâ which will bring the system down immediately.  Other valid formats are +m, where m is the number of minutes to wait until shutting down and hh:mm which specifies the time on the 24hr clock.

Logged in users are warned by a message sent to their terminal, you may include an optional MESSAGE included with this.  Messages can be sent without actually bringing the system down by using the -k option.

If TIME is given, the command will remain in the foreground until the shutdown occurs.  It can be cancelled by Control-C, or by another user using the -c option.

The system is brought down into maintenance (single-user) mode by default, you can change this with either the -r or -h option which specify a reboot or system halt respectively.  The -h option can be further modified with -H or -P to specify whether to halt the system, or to power it off afterwards.  The default is left up to the shutdown scripts. Try â[1m%s --help[0mâ for more information.
 Unable to execute â[1m%s[0mâ for %s: %s 