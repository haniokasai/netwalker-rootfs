��    3      �  G   L      h  �   i    V  �  [  c  �  �   `	  �   
  �   �
  �   �  �  B  �     �   �  �   Y  �    �  �  J   h  �  �  <   h  �  �  *   R  '   }  	   �     �     �     �     �  ;    �   W  �   �     p     �    �  A   �  ;  �  ;     3   Y  /   �  +   �  '   �  #        5     U  0   q  *   �  ]   �     +     C     ^  3   v  7   �  "   �  �     �   �!    �"  �  �#  d  �%  �   �&  �   �'  �   �(  �   P)  �  �)  �   �+  �   O,  �   �,  �  �-  �  >/  I   �0  �  81  $   �2  �  3  *   �4  "   �4  	   5     5     #5     C5     c5  <  �5  �   �6  �   F7     �7     �7  
  8  A   9  <  N9  :   �:  2   �:  .   �:  *   (;  &   S;  "   z;     �;     �;  1   �;  *   	<  ]   4<     �<     �<     �<  3   �<  7   =  "   I=        ,   $   #              2   %   "                            3                    &   *             1   !                               '                    -   )                0       .   +             /      
                	           (          
BLOCKS and BYTES may be followed by the following multiplicative suffixes:
xM M, c 1, w 2, b 512, kB 1000, K 1024, MB 1000*1000, M 1024*1024,
GB 1000*1000*1000, G 1024*1024*1024, and so on for T, P, E, Z, Y.

Each CONV symbol may be:

 
Both MAJOR and MINOR must be specified when TYPE is b, c, or u, and they
must be omitted when TYPE is p.  If MAJOR or MINOR begins with 0x or 0X,
it is interpreted as hexadecimal; otherwise, if it begins with 0, as octal;
otherwise, as decimal.  TYPE may be:
 
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
If -e is in effect, the following sequences are recognized:

  \0NNN   the character whose ASCII code is NNN (octal)
  \\     backslash
  \a     alert (BEL)
  \b     backspace
 
If FILE is specified, read it to determine which colors to use for which
file types and extensions.  Otherwise, a precompiled database is used.
For details on the format of these files, run `dircolors --print-database'.
 
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

 
NOTE: [ honors the --help and --version options, but test does not.
test treats each of those as it treats any other nonempty STRING.
 
POS is F[.C][OPTS], where F is the field number and C the character position
in the field; both are origin 1.  If neither -t nor -b is in effect, characters
in a field are counted from the beginning of the preceding whitespace.  OPTS is
one or more single-letter ordering options, which override global ordering
options for that key.  If no key is given, use the entire line as the key.

SIZE may be followed by the following multiplicative suffixes:
 
Special settings:
  N             set the input and output speeds to N bauds
 * cols N        tell the kernel that the terminal has N columns
 * columns N     same as cols N
 
TYPE is made up of one or more of these specifications:

  a          named character, ignoring high-order bit
  c          ASCII character or backslash escape
 
With no options, produce three-column output.  Column one contains
lines unique to FILE1, column two contains lines unique to FILE2,
and column three contains lines common to both files.
       --files0-from=F   summarize disk usage of the NUL-terminated file
                          names specified in file F
  -H                    like --si, but also evokes a warning; will soon
                          change to be equivalent to --dereference-args (-D)
  -h, --human-readable  print sizes in human readable format (e.g., 1K 234M 2G)
      --si              like -h, but use powers of 1000 not 1024
   -C                         list entries by columns
      --color[=WHEN]         control whether color is used to distinguish file
                               types.  WHEN may be `never', `always', or `auto'
  -d, --directory            list directory entries instead of contents,
                               and do not dereference symbolic links
  -D, --dired                generate output designed for Emacs' dired mode
   -Z, --context=CTX  set the SELinux security context of each NAME to CTX
   -f, --canonicalize            canonicalize by following every symlink in
                                every component of the given name recursively;
                                all but the last component must exist
  -e, --canonicalize-existing   canonicalize by following every symlink in
                                every component of the given name recursively,
                                all components must exist
   -g                         like -l, but do not list owner
   -m, --canonicalize-missing    canonicalize by following every symlink in
                                every component of the given name recursively,
                                without requirements on components existence
  -n, --no-newline              do not output the trailing newline
  -q, --quiet,
  -s, --silent                  suppress most error messages
  -v, --verbose                 report error messages
   dsync     use synchronized I/O for data
  %s-blocks      Used Available Capacity %b %e  %Y %b %e %H:%M %s: unrecognized option `%c%s'
 %s: unrecognized option `--%s'
 %s:%lu: unrecognized keyword %s * log-structured or journaled file systems, such as those supplied with
AIX and Solaris (and JFS, ReiserFS, XFS, Ext3, etc.)

* file systems that write redundant data and carry on even if some writes
fail, such as RAID-based file systems

* file systems that make snapshots, such as Network Appliance's NFS server

 Output pieces of FILE separated by PATTERN(s) to files `xx00', `xx01', ...,
and output byte counts of each piece to standard output.

 Remove (unlink) the FILE(s).

  -f, --force           ignore nonexistent files, never prompt
  -i                    prompt before every removal
 Request canceled Request not canceled Run COMMAND with an adjusted niceness, which affects process scheduling.
With no COMMAND, print the current niceness.  Nicenesses range from
%d (most favorable scheduling) to %d (least favorable).

  -n, --adjustment=N   add integer N to the niceness (default 10)
 Summarize disk usage of each FILE, recursively for directories.

 This default behavior is not desirable when you really want to
track the actual name of the file, not the file descriptor (e.g., log
rotation).  Use --follow=name in that case.  That causes tail to track the
named file by reopening it periodically to see if it has been removed and
recreated by some other program.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s, %s, and others.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s, and %s.
 Written by %s, %s, %s,
%s, %s, %s, %s,
and %s.
 Written by %s, %s, %s,
%s, %s, %s, and %s.
 Written by %s, %s, %s,
%s, %s, and %s.
 Written by %s, %s, %s,
%s, and %s.
 Written by %s, %s, %s,
and %s.
 Written by %s, %s, and %s.
 can't apply partial context to unlabeled file %s cannot both summarize and show all entries invalid option -- %c; -WIDTH is recognized only when it is the first
option; use -w N instead unrecognized operand %s unrecognized operand %s=%s unrecognized prefix: %s warning: summarizing conflicts with --max-depth=%lu warning: summarizing is the same as using --max-depth=0 warning: unrecognized escape `\%c' Project-Id-Version: coreutils
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2008-01-09 11:29+0100
PO-Revision-Date: 2008-07-20 10:10+0000
Last-Translator: Jen Ockwell <jenfraggleubuntu@googlemail.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Launchpad-Export-Date: 2009-04-14 22:34+0000
X-Generator: Launchpad (build Unknown)
 
BLOCKS and BYTES may be followed by the following multiplicative suffixes:
xM M, c 1, w 2, b 512, kB 1000, K 1024, MB 1000*1000, M 1024*1024,
GB 1000*1000*1000, G 1024*1024*1024 and so on for T, P, E, Z, Y.

Each CONV symbol may be:

 
Both MAJOR and MINOR must be specified when TYPE is b, c, or u, and they
must be omitted when TYPE is p.  If MAJOR or MINOR begins with 0x or 0X,
it is interpreted as hexadecimal; if it begins with 0, as octal;
otherwise, it is interpreted as decimal.  TYPE may be:
 
By default, colour is not used to distinguish types of files.  That is
equivalent to using --color=none.  Using the --color option without the
optional WHEN argument is equivalent to using --color=always.  With
--color=auto, colour codes are output only if standard output is connected
to a terminal (tty).  The environment variable LS_COLORS can influence the
colours, and can be set easily by the dircolors command.
 
By default, sparse SOURCE files are detected by a crude heuristic and the
corresponding DEST file is made sparse as well.  That is the behaviour
selected by --sparse=auto.  Specify --sparse=always to create a sparse DEST
file whenever the SOURCE file contains a long enough sequence of zero bytes.
Use --sparse=never to inhibit creation of sparse files.

 
If -e is in effect, the following sequences are recognised:

  \0NNN   the character whose ASCII code is NNN (octal)
  \\     backslash
  \a     alert (BEL)
  \b     backspace
 
If FILE is specified, read it to determine which colours to use for which
file types and extensions.  Otherwise, a precompiled database is used.
For details on the format of these files, run `dircolors --print-database'.
 
Licence GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

 
NOTE: [ honours the --help and --version options, but test does not.
test treats each of those as it treats any other non-empty STRING.
 
POS is F[.C][OPTS], where F is the field number and C the character position
in the field; both are origin 1.  If neither -t nor -b is in effect, characters
in a field are counted from the beginning of the preceding white space.  OPTS is
one or more single-letter ordering options, which override global ordering
options for that key.  If no key is given, use the entire line as the key.

SIZE may be followed by the following multiplicative suffixes:
 
Special settings:
  N             set the input and output speeds to N baud
 * cols N        tell the kernel that the terminal has N columns
 * columns N     same as cols N
 
TYPE is made up of one or more of these specifications:

  a named character, ignoring high-order bit
  c ASCII character or backslash escape
 
With no options, produce three-column output.  Column one contains
lines unique to FILE1, column two contains lines unique to FILE2
and column three contains lines common to both files.
       --files0-from=F   summarise disk usage of the NUL-terminated file
                          names specified in file F
  -H                    like --si, but also evokes a warning; will soon
                          change to be equivalent to --dereference-args (-D)
  -h, --human-readable  print sizes in human readable format (e.g., 1K 234M 2G)
      --si              like -h, but use powers of 1000 not 1024
   -C                         list entries by columns
      --color[=WHEN]         control whether colour is used to distinguish file
                               types.  WHEN may be `never', `always', or `auto'
  -d, --directory            list directory entries instead of contents,
                               and do not dereference symbolic links
  -D, --dired                generate output designed for Emacs' dired mode
   -Z, --context=CTX set the SELinux security context of each NAME to CTX
   -f, --canonicalize            canonicalise by following every symlink in
                                every component of the given name recursively;
                                all but the last component must exist
  -e, --canonicalize-existing   canonicalise by following every symlink in
                                every component of the given name recursively,
                                all components must exist
   -g like -l, but do not list owner
   -m, --canonicalize-missing    canonicalise by following every symlink in
                                every component of the given name recursively,
                                without requirements on components existence
  -n, --no-newline              do not output the trailing newline
  -q, --quiet,
  -s, --silent                  suppress most error messages
  -v, --verbose                 report error messages
   dsync     use synchronised I/O for data
  %s-blocks Used Available Capacity %e %b  %Y %e %b %H:%M %s: unrecognised option `%c%s'
 %s: unrecognised option `--%s'
 %s:%lu: unrecognised keyword %s * log-structured or journalled file systems, such as those supplied with
AIX and Solaris (and JFS, ReiserFS, XFS, Ext3, etc.)

* file systems that write redundant data and carry on even if some writes
fail, such as RAID-based file systems

* file systems that make snapshots, such as Network Appliance's NFS server

 Output pieces of FILE separated by PATTERN(s) to files `xx00', `xx01', ...
and output byte counts of each piece to standard output.

 Remove (unlink) the FILE(s).

  -f, --force           ignore non-existent files, never prompt
  -i                    prompt before every removal
 Request cancelled Request not cancelled Run COMMAND with an adjusted niceness, which affects process scheduling.
With no COMMAND, print the current niceness.  Nicenesses range from
%d (most favourable scheduling) to %d (least favourable).

  -n, --adjustment=N   add integer N to the niceness (default 10)
 Summarise disk usage of each FILE, recursively for directories.

 This default behaviour is not desirable when you really want to
track the actual name of the file, not the file descriptor (e.g., log
rotation).  Use --follow=name in that case.  That causes tail to track the
named file by reopening it periodically to see if it has been removed and
recreated by some other program.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s, %s and others.
 Written by %s, %s, %s,
%s, %s, %s, %s,
%s and %s.
 Written by %s, %s, %s,
%s, %s, %s, %s
and %s.
 Written by %s, %s, %s,
%s, %s, %s and %s.
 Written by %s, %s, %s,
%s, %s and %s.
 Written by %s, %s, %s,
%s and %s.
 Written by %s, %s, %s
and %s.
 Written by %s, %s and %s.
 can't apply partial context to unlabelled file %s cannot both summarise and show all entries invalid option -- %c; -WIDTH is recognised only when it is the first
option; use -w N instead unrecognised operand %s unrecognised operand %s=%s unrecognised prefix: %s warning: summarising conflicts with --max-depth=%lu warning: summarising is the same as using --max-depth=0 warning: unrecognised escape `\%c' 