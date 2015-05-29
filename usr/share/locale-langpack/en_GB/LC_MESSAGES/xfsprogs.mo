��          �   %   �      0  �  1  �    �  �  �   �
  4   d  5   �  2   �  $     '   '     O  %   o     �  0   �  B   �      $  9   E  %     &   �     �     �  )   
  *   4  "   _  �  �  �  G  �  -  �  �  �   �  4   ~  5   �  2   �  $     '   A     i  %   �     �  0   �  C   �      ?  :   `  %   �  &   �     �       )   &  *   P  "   {                                                                         
         	                                             
 advise the page cache about access patterns expected for a mapping

 Modifies page cache behavior when operating on the current mapping.
 The range arguments are required by some advise commands ([*] below).
 With no arguments, the POSIX_MADV_NORMAL advice is implied.
 -d -- don't need these pages (POSIX_MADV_DONTNEED) [*]
 -r -- expect random page references (POSIX_MADV_RANDOM)
 -s -- expect sequential page references (POSIX_MADV_SEQUENTIAL)
 -w -- will need these pages (POSIX_MADV_WILLNEED) [*]
 Notes:
   NORMAL sets the default readahead setting on the file.
   RANDOM sets the readahead setting on the file to zero.
   SEQUENTIAL sets double the default readahead setting on the file.
   WILLNEED forces the maximum readahead.

 
 dirties a range of bytes in the current memory mapping

 Example:
 'mwrite 512 20 - writes 20 bytes at 512 bytes into the current mapping.

 Stores a byte into memory for a range within a mapping.
 The default stored value is 'X', repeated to fill the range specified.
 -S -- use an alternate seed character
 -r -- reverse order; start storing fom the end of range, moving backward
 The stores are performed sequentially from the start offset by default.

 
 reads a range of bytes in the current memory mapping

 Example:
 'mread -v 512 20' - dumps 20 bytes read from 512 bytes into the mapping

 Accesses a range of the current memory mapping, optionally dumping it to
 the standard output stream (with -v option) for subsequent inspection.
 -f -- verbose mode, dump bytes with offsets relative to start of file.
 -r -- reverse order; start accessing fom the end of range, moving backward
 -v -- verbose mode, dump bytes with offsets relative to start of mapping.
 The accesses are performed sequentially from the start offset by default.
 Notes:
   References to whole pages following the end of the backing file results
   in delivery of the SIGBUS signal.  SIGBUS signals may also be delivered
   on various filesystem conditions, including quota exceeded errors, and
   for physical device errors (such as unreadable disk blocks).  No attempt
   has been made to catch signals at this stage...

 
 report or modify prefered extent size (in bytes) for the current path

 -R -- recursively descend (useful when current path is a directory)
 -D -- recursively descend, only modifying extsize on directories

 %s %s filesystem failed to initialize
%s: Aborting.
 %s: %s filesystem failed to initialize
%s: Aborting.
 %s: couldn't initialize XFS library
%s: Aborting.
 %s: filesystem failed to initialize
 Couldn't initialize global thread mask
 Error initializing btree buf 1
 Error initializing the realtime space Error initializing wbuf 0
 This filesystem has uninitialized extent flags.
 bad directory/attribute forward block pointer, expected 0, saw %u
 couldn't initialize XFS library
 get/set prefered extent size (in bytes) for the open file reinitializing realtime bitmap inode
 reinitializing realtime summary inode
 reinitializing root directory
 summarize filesystem ownership would reinitialize realtime bitmap inode
 would reinitialize realtime summary inode
 would reinitialize root directory
 Project-Id-Version: xfsprogs
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2008-12-23 00:40+0000
PO-Revision-Date: 2007-11-19 11:41+0000
Last-Translator: Jen Ockwell <jenfraggleubuntu@googlemail.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 08:43+0000
X-Generator: Launchpad (build Unknown)
 
 advise the page cache about access patterns expected for a mapping

 Modifies page cache behaviour when operating on the current mapping.
 The range arguments are required by some advise commands ([*] below).
 With no arguments, the POSIX_MADV_NORMAL advice is implied.
 -d -- don't need these pages (POSIX_MADV_DONTNEED) [*]
 -r -- expect random page references (POSIX_MADV_RANDOM)
 -s -- expect sequential page references (POSIX_MADV_SEQUENTIAL)
 -w -- will need these pages (POSIX_MADV_WILLNEED) [*]
 Notes:
   NORMAL sets the default readahead setting on the file.
   RANDOM sets the readahead setting on the file to zero.
   SEQUENTIAL sets double the default readahead setting on the file.
   WILLNEED forces the maximum readahead.

 
 dirties a range of bytes in the current memory mapping

 Example:
 'mwrite 512 20 - writes 20 bytes at 512 bytes into the current mapping.

 Stores a byte into memory for a range within a mapping.
 The default stored value is 'X', repeated to fill the range specified.
 -S -- use an alternate seed character
 -r -- reverse order; start storing fom the end of range, moving backwards
 The stores are performed sequentially from the start offset by default.

 
 reads a range of bytes in the current memory mapping

 Example:
 'mread -v 512 20' - dumps 20 bytes read from 512 bytes into the mapping

 Accesses a range of the current memory mapping, optionally dumping it to
 the standard output stream (with -v option) for subsequent inspection.
 -f -- verbose mode, dump bytes with offsets relative to start of file.
 -r -- reverse order; start accessing fom the end of range, moving backwards
 -v -- verbose mode, dump bytes with offsets relative to start of mapping.
 The accesses are performed sequentially from the start offset by default.
 Notes:
   References to whole pages following the end of the backing file results
   in delivery of the SIGBUS signal.  SIGBUS signals may also be delivered
   on various filesystem conditions, including quota exceeded errors, and
   for physical device errors (such as unreadable disk blocks).  No attempt
   has been made to catch signals at this stage...

 
 report or modify preferred extent size (in bytes) for the current path

 -R -- recursively descend (useful when current path is a directory)
 -D -- recursively descend, only modifying extsize on directories

 %s %s filesystem failed to initialise
%s: Aborting.
 %s: %s filesystem failed to initialise
%s: Aborting.
 %s: couldn't initialise XFS library
%s: Aborting.
 %s: filesystem failed to initialise
 Couldn't initialise global thread mask
 Error initialising btree buf 1
 Error initialising the realtime space Error initialising wbuf 0
 This filesystem has uninitialised extent flags.
 bad directory/attribute forwards block pointer, expected 0, saw %u
 couldn't initialise XFS library
 get/set preferred extent size (in bytes) for the open file reinitialising realtime bitmap inode
 reinitialising realtime summary inode
 reinitialising root directory
 summarise filesystem ownership would reinitialise realtime bitmap inode
 would reinitialise realtime summary inode
 would reinitialise root directory
 