��          �      �       H    I  .   Q     �  )   �  (   �     �           #  h  A     �  !   �  %   �  "   
  �  -  
  �  .   �     -  *   D  (   o     �      �     �  i  �     [
  !   t
  %   �
  "   �
           	              
                                        
The @S could not be read or does not describe a correct ext2
@f.  If the @v is valid and it really contains an ext2
@f (and not swap or ufs or something else), then the @S
is corrupt, and you might try running e2fsck with an alternate @S:
    e2fsck -b %S <@v>

 %s: Filesystem byte order already normalized.
 %s: e2fsck canceled.
 @i %i has a extra size (%IS) which is @n
 Failed to optimize directory %q (%d): %m Optimizing directories:  Pass 3A: Optimizing directories
 Setting error behavior to %d
 Usage: %s [-c max_mounts_count] [-e errors_behavior] [-g group]
	[-i interval[d|m|w]] [-j] [-J journal_options] [-l]
	[-m reserved_blocks_percent] [-o [^]mount_options[,...]] 
	[-r reserved_blocks_count] [-u user] [-C mount_count] [-L volume_label]
	[-M last_mounted_dir] [-O [^]feature[,...]]
	[-E extended-option[,...]] [-T last_check_time] [-U UUID] device
 bad error behavior - %s while allocating zeroizing buffer while initializing journal superblock while trying to initialize program Project-Id-Version: e2fsprogs
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2008-06-17 22:16-0400
PO-Revision-Date: 2008-08-10 09:38+0000
Last-Translator: Jen Ockwell <jenfraggleubuntu@googlemail.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-13 23:28+0000
X-Generator: Launchpad (build Unknown)
 
The @S could not be read or does not describe a correct ext2
@f.  If the @v is valid and it really contains an ext2
@f (and not swap or ufs or something else), then the @S
is corrupt, and you might try running e2fsck with an alternate @S:
    e2fsck -b %S <@v&gt;

 %s: Filesystem byte order already normalised.
 %s: e2fsck cancelled.
 @i %i has an extra size (%IS) which is @n
 Failed to optimise directory %q (%d): %m Optimising directories:  Pass 3A: Optimising directories
 Setting error behaviour to %d
 Usage: %s [-c max_mounts_count] [-e errors_behaviour] [-g group]
	[-i interval[d|m|w]] [-j] [-J journal_options] [-l]
	[-m reserved_blocks_percent] [-o [^]mount_options[,...]] 
	[-r reserved_blocks_count] [-u user] [-C mount_count] [-L volume_label]
	[-M last_mounted_dir] [-O [^]feature[,...]]
	[-E extended-option[,...]] [-T last_check_time] [-U UUID] device
 bad error behaviour - %s while allocating zeroising buffer while initialising journal superblock while trying to initialise program 