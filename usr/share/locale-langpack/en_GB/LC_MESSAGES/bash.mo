��          T      �       �   �  �   [  H  <   �	  *   �	  B   
  E   O
  �  �
  �    ^    4   m  %   �  A   �  D   
                                        Getopts is used by shell procedures to parse positional parameters.
    
    OPTSTRING contains the option letters to be recognized; if a letter
    is followed by a colon, the option is expected to have an argument,
    which should be separated from it by white space.
    
    Each time it is invoked, getopts will place the next option in the
    shell variable $name, initializing name if it does not exist, and
    the index of the next argument to be processed into the shell
    variable OPTIND.  OPTIND is initialized to 1 each time the shell or
    a shell script is invoked.  When an option requires an argument,
    getopts places that argument into the shell variable OPTARG.
    
    getopts reports errors in one of two ways.  If the first character
    of OPTSTRING is a colon, getopts uses silent error reporting.  In
    this mode, no error messages are printed.  If an invalid option is
    seen, getopts places the option character found into OPTARG.  If a
    required argument is not found, getopts places a ':' into NAME and
    sets OPTARG to the option character found.  If getopts is not in
    silent mode, and an invalid option is seen, getopts places '?' into
    NAME and unsets OPTARG.  If a required argument is not found, a '?'
    is placed in NAME, OPTARG is unset, and a diagnostic message is
    printed.
    
    If the shell variable OPTERR has the value 0, getopts disables the
    printing of error messages, even if the first character of
    OPTSTRING is not a colon.  OPTERR has the value 1 by default.
    
    Getopts normally parses the positional parameters ($0 - $9), but if
    more arguments are given, they are parsed instead. Output the ARGs.  If -n is specified, the trailing newline is
    suppressed.  If the -e option is given, interpretation of the
    following backslash-escaped characters is turned on:
    	\a	alert (bell)
    	\b	backspace
    	\c	suppress trailing newline
    	\E	escape character
    	\f	form feed
    	\n	new line
    	\r	carriage return
    	\t	horizontal tab
    	\v	vertical tab
    	\\	backslash
    	\0nnn	the character whose ASCII code is NNN (octal).  NNN can be
    		0 to 3 octal digits
    
    You can explicitly turn off the interpretation of the above characters
    with the -E option. Without EXPR, returns returns "$line $filename".  With EXPR, can be used used to provide a stack trace. flag does the same thing, but the stack position is not prepended. prepending the directory name with its position in the stack.  The -p Project-Id-Version: bash
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2006-10-23 17:20-0400
PO-Revision-Date: 2008-08-10 10:58+0000
Last-Translator: Jen Ockwell <jenfraggleubuntu@googlemail.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Launchpad-Export-Date: 2009-04-14 21:34+0000
X-Generator: Launchpad (build Unknown)
 Getopts is used by shell procedures to parse positional parameters.
    
    OPTSTRING contains the option letters to be recognised; if a letter
    is followed by a colon, the option is expected to have an argument,
    which should be separated from it by white space.
    
    Each time it is invoked, getopts will place the next option in the
    shell variable $name, initialising name if it does not exist, and
    the index of the next argument to be processed into the shell
    variable OPTIND.  OPTIND is initialised to 1 each time the shell or
    a shell script is invoked.  When an option requires an argument,
    getopts places that argument into the shell variable OPTARG.
    
    getopts reports errors in one of two ways.  If the first character
    of OPTSTRING is a colon, getopts uses silent error reporting.  In
    this mode, no error messages are printed.  If an invalid option is
    seen, getopts places the option character found into OPTARG.  If a
    required argument is not found, getopts places a ':' into NAME and
    sets OPTARG to the option character found.  If getopts is not in
    silent mode, and an invalid option is seen, getopts places '?' into
    NAME and unsets OPTARG.  If a required argument is not found, a '?'
    is placed in NAME, OPTARG is unset, and a diagnostic message is
    printed.
    
    If the shell variable OPTERR has the value 0, getopts disables the
    printing of error messages, even if the first character of
    OPTSTRING is not a colon.  OPTERR has the value 1 by default.
    
    Getopts normally parses the positional parameters ($0 - $9), but if
    more arguments are given, they are parsed instead. Output the ARGs.  If -n is specified, the trailing newline is
    suppressed.  If the -e option is given, interpretation of the
    following backslash-escaped characters is turned on:
    	\a	alert (bell)
    	\b	backspace
    	\c	suppress trailing newline
    	\E	escape character
    	\f	form feed
    	\n	new line
    	\r	carriage return
    	\t	horizontal tab
    	\v	vertical tab
    	\[tab]backslash
    	\0nnn	the character whose ASCII code is NNN (octal).  NNN can be
    		0 to 3 octal digits
    
    You can explicitly turn off the interpretation of the above characters
    with the -E option. Without EXPR, returns "$line $filename".  With EXPR, can be used to provide a stack trace. flag does the same thing, but the stack position is not prefixed. prefixing the directory name with its position in the stack.  The -p 