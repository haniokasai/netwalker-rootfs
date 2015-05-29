��          �      ,      �  �  �  c  *  �   �    b  �   w  �   U  �  �  �  �	  q  >  �  �    d     v     �    �  ;  �  3   �  �    �  �  d  �  �       �  �   �  �   �  �  X  �  	  q  �  �  ,    �      �!     "  
  "  <  (#  4   e$                            	                                              
    
By default, color is not used to distinguish types of files.  That is
equivalent to using --color=none.  Using the --color option without the
optional WHEN argument is equivalent to using --color=always.  With
--color=auto, color codes are output only if standard output is connected
to a terminal (tty).  The environment variable LS_COLORS can influence the
colors, and can be set easily by the dircolors command.
 
By default, sparse SOURCE files are detected by a crude heuristic and the
corresponding DEST file is made sparse as well.  That is the behavior
selected by --sparse=auto.  Specify --sparse=always to create a sparse DEST
file whenever the SOURCE file contains a long enough sequence of zero bytes.
Use --sparse=never to inhibit creation of sparse files.

 
FORMAT controls the output.  The only valid option for the second form
specifies Coordinated Universal Time.  Interpreted sequences are:

  %%   a literal %
  %a   locale's abbreviated weekday name (e.g., Sun)
 
Handle the tty line connected to standard input.  Without arguments,
prints baud rate, line discipline, and deviations from stty sane.  In
settings, CHAR is taken literally, or coded as in ^c, 0x37, 0177 or
127; special values ^- or undef used to disable special characters.
 
If FILE is specified, read it to determine which colors to use for which
file types and extensions.  Otherwise, a precompiled database is used.
For details on the format of these files, run `dircolors --print-database'.
 
NOTE: [ honors the --help and --version options, but test does not.
test treats each of those as it treats any other nonempty STRING.
   -C                         list entries by columns
      --color[=WHEN]         control whether color is used to distinguish file
                               types.  WHEN may be `never', `always', or `auto'
  -d, --directory            list directory entries instead of contents,
                               and do not dereference symbolic links
  -D, --dired                generate output designed for Emacs' dired mode
   -h HEADER, --header=HEADER
                    use a centered HEADER instead of filename in page header,
                    -h "" prints a blank line, don't use -h""
  -i[CHAR[WIDTH]], --output-tabs[=CHAR[WIDTH]]
                    replace spaces with CHARs (TABs) to tab WIDTH (8)
  -J, --join-lines  merge full lines, turns off -W line truncation, no column
                    alignment, --sep-string[=STRING] sets separators
   -n, --numeric-uid-gid      like -l, but list numeric user and group IDs
  -N, --literal              print raw entry names (don't treat e.g. control
                               characters specially)
  -o                         like -l, but do not list group information
  -p, --indicator-style=slash
                             append / indicator to directories
   -q, --hide-control-chars   print ? instead of non graphic characters
      --show-control-chars   show non graphic characters as-is (default
                             unless program is `ls' and output is a terminal)
  -Q, --quote-name           enclose entry names in double quotes
      --quoting-style=WORD   use quoting style WORD for entry names:
                               literal, locale, shell, shell-always, c, escape
 Output commands to set the LS_COLORS environment variable.

Determine format of output:
  -b, --sh, --bourne-shell    output Bourne shell code to set LS_COLORS
  -c, --csh, --c-shell        output C shell code to set LS_COLORS
  -p, --print-database        output defaults
 Request canceled Request not canceled Run COMMAND with an adjusted niceness, which affects process scheduling.
With no COMMAND, print the current niceness.  Nicenesses range from
%d (most favorable scheduling) to %d (least favorable).

  -n, --adjustment=N   add integer N to the niceness (default 10)
 This default behavior is not desirable when you really want to
track the actual name of the file, not the file descriptor (e.g., log
rotation).  Use --follow=name in that case.  That causes tail to track the
named file by reopening it periodically to see if it has been removed and
recreated by some other program.
 unparsable value for LS_COLORS environment variable Project-Id-Version: coreutils
Report-Msgid-Bugs-To: Abigail Brady <morwen@evilmagic.org>
POT-Creation-Date: 2008-01-09 11:29+0100
PO-Revision-Date: 2008-11-11 22:30+0000
Last-Translator: Joel Goguen <jgoguen@jgoguen.ca>
Language-Team: English (Canada) <en_CA@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Launchpad-Export-Date: 2009-04-14 22:35+0000
X-Generator: Launchpad (build Unknown)
 
By default, colour is not used to distinguish types of files.  That is
equivalent to using --colour=none.  Using the --colour option without the
optional WHEN argument is equivalent to using --colour=always.  With
--colour=auto, colour codes are output only if standard output is connected
to a terminal (tty).  The environment variable LSCOLOURS can influence the
colours, and can be set easily by the dircolors command.
 
By default, sparse SOURCE files are detected by a crude heuristic and the
corresponding DEST file is made sparse as well.  That is the behaviour
selected by --sparse=auto.  Specify --sparse=always to create a sparse DEST
file whenever the SOURCE file contains a long enough sequence of zero bytes.
Use --sparse=never to inhibit creation of sparse files.

 
FORMAT controls the output.  The only valid option for the second form
specifies Coordinated Universal Time.  Interpreted sequences are:

  %%   a litreal %
  %a   locale's abbreviated weekday name (e.g., Sun)
 
Handle the tty line connected to standard input.  Without arguments,
prints baud rate, line discipline, and deviations from stty sane.  In
settings, CHAR is taken litreally, or coded as in ^c, 0x37, 0177 or
127; special values ^- or undef used to disable special characters.
 
If FILE is specified, read it to determine which colours to use for which
file types and extensions.  Otherwise, a precompiled database is used.
For details on the format of these files, run `dircolors --print-database'.
 
NOTE: [ honours the --help and --version options, but test does not.
test treats each of those as it treats any other nonempty STRING.
   -C                         list entries by columns
      --colour[=WHEN]         control whether colour is used to distinguish file
                               types.  WHEN may be `never', `always', or `auto'
  -d, --directory            list directory entries instead of contents,
                               and do not dereference symbolic links
  -D, --dired                generate output designed for Emacs' dired mode
   -h HEADER, --header=HEADER
                    use a centred HEADER instead of filename in page header,
                    -h "" prints a blank line, don't use -h""
  -i[CHAR[WIDTH]], --output-tabs[=CHAR[WIDTH]]
                    replace spaces with CHARs (TABs) to tab WIDTH (8)
  -J, --join-lines  merge full lines, turns off -W line truncation, no column
                    alignment, --sep-string[=STRING] sets separators
   -n, --numeric-uid-gid      like -l, but list numeric user and group IDs
  -N, --litreal              print raw entry names (don't treat e.g. control
                               characters specially)
  -o                         like -l, but do not list group information
  -p, --indicator-style=slash
                             append / indicator to directories
   -q, --hide-control-chars   print ? instead of non graphic characters
      --show-control-chars   show non graphic characters as-is (default
                             unless program is `ls' and output is a terminal)
  -Q, --quote-name           enclose entry names in double quotes
      --quoting-style=WORD   use quoting style WORD for entry names:
                               litreal, locale, shell, shell-always, c, escape
 Output commands to set the LS_COLOURS environment variable.

Determine format of output:
  -b, --sh, --bourne-shell    output Bourne shell code to set LS_COLOURS
  -c, --csh, --c-shell        output C shell code to set LS_COLOURS
  -p, --print-database        output defaults
 Request cancelled Request not cancelled Run COMMAND with an adjusted niceness, which affects process scheduling.
With no COMMAND, print the current niceness.  Nicenesses range from
%d (most favourable scheduling) to %d (least favourable).

  -n, --adjustment=N   add integer N to the niceness (default 10)
 This default behaviour is not desirable when you really want to
track the actual name of the file, not the file descriptor (e.g., log
rotation).  Use --follow=name in that case.  That causes tail to track the
named file by reopening it periodically to see if it has been removed and
recreated by some other program.
 unparsable value for LS_COLOURS environment variable 