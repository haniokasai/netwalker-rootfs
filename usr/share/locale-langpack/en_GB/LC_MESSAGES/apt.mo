��          �   %   �      P     Q     m  x   �  '   �  U   #  8   y  5   �  "   �  "     B   .  #   q  5   �  !   �  -   �  /     '   K  "   s  "   �     �  &  �  #   �  <   !  [   ^  <   �  <   �  �  4     �     �  x   �  '   m  Z   �  G   �  ;   8  &   t     �  F   �  +   �  9   *     d  ,   �  /   �  &   �  "     &   '      N    o  +   �  =   �  ^   �  @   P  <   �                                                              	   
                                                            Build command '%s' failed.
 Failed to resolve %s Hmm, seems like the AutoRemover destroyed something which really
shouldn't happen. Please file a bug report against apt. Internal Error, AutoRemover broke stuff Media change: please insert the disc labeled
 '%s'
in the drive '%s' and press enter
 Must specify at least one package to check builddeps for Must specify at least one package to fetch source for Note, selecting %s for regex '%s'
 Package extension list is too long Please provide a name for this Disc, such as 'Debian 2.1r1 Disk 1' Release '%s' for '%s' was not found Some files are missing in the package file group `%s' Source extension list is too long The following NEW packages will be installed: The following packages have unmet dependencies: The following packages will be REMOVED: Unable to minimize the upgrade set Unknown compression algorithm '%s' Unpack command '%s' failed.
 Usage: apt-ftparchive [options] command
Commands: packages binarypath [overridefile [pathprefix]]
          sources srcpath [overridefile [pathprefix]]
          contents path
          release path
          generate config [groups]
          clean config

apt-ftparchive generates index files for Debian archives. It supports
many styles of generation from fully automated to functional replacements
for dpkg-scanpackages and dpkg-scansources

apt-ftparchive generates Package files from a tree of .debs. The
Package file contains the contents of all the control fields from
each package as well as the MD5 hash and filesize. An override file
is supported to force the value of Priority and Section.

Similarly apt-ftparchive generates Sources files from a tree of .dscs.
The --source-override option can be used to specify a src override file

The 'packages' and 'sources' command should be run in the root of the
tree. BinaryPath should point to the base of the recursive search and 
override file should contain the override flags. Pathprefix is
appended to the filename fields if present. Example usage from the 
Debian archive:
   apt-ftparchive packages dists/potato/main/binary-i386/ > \
               dists/potato/main/binary-i386/Packages

Options:
  -h    This help text
  --md5 Control MD5 generation
  -s=?  Source override file
  -q    Quiet
  -d=?  Select the optional caching database
  --no-delink Enable delinking debug mode
  --contents  Control contents file generation
  -c=?  Read this configuration file
  -o=?  Set an arbitrary configuration option Version '%s' for '%s' was not found We are not supposed to delete stuff, can't start AutoRemover You are about to do something potentially harmful.
To continue type in the phrase '%s'
 ?]  You might want to run `apt-get -f install' to correct these. You might want to run `apt-get -f install' to correct these: Project-Id-Version: apt 0.7.18
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-03-31 02:50+0000
PO-Revision-Date: 2009-03-31 05:39+0000
Last-Translator: Neil Williams <Unknown>
Language-Team: en_GB <en_gb@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 01:06+0000
X-Generator: Launchpad (build Unknown)
 Build command ‘%s’ failed.
 Could not resolve ‘%s’ Hmm, seems like the AutoRemoved destroyed something which really
shouldn't happen. Please file a bug report against apt. Internal Error, AutoRemoved broke stuff Media Change: Please insert the disc labelled
 '%s'
in the drive ‘%s’ and press enter
 Must specify at least one package for which you want to check builddeps Must specify at least one package for which to fetch source Note, selecting %s for regex ‘%s’
 Option ‘%s’ is too long Please provide a name for this Disc, such as ‘Debian 2.1r1 Disk 1’ Release ‘%s’ for ‘%s’ was not found Some files are missing in the package file group ‘%s’ Option ‘%s’ is too long The following NEW packages will be installed The following packages have unmet dependencies. The following packages will be REMOVED Unable to minimise the upgrade set Unknown Compression Algorithm ‘%s’ Unpack command ‘%s’ failed.
 Usage: apt-ftparchive [options] command
Commands: packages binarypath [overridefile [pathprefix]]
          sources srcpath [overridefile [pathprefix]]
          contents path
          generate config [groups]
          clean config

apt-ftparchive generates index files for Debian archives. It supports
many styles of generation from fully automated to functional replacements
for dpkg-scanpackages and dpkg-scansources

apt-ftparchive generates Package files from a tree of .debs. The
Package file contains the contents of all the control fields from
each package as well as the MD5 hash and filesize. An override file
is supported to force the value of Priority and Section.

Similarly apt-ftparchive generates Sources files from a tree of .dscs.
The --source-override option can be used to specify a src override file

The ‘packages’ and ‘sources’ command should be run in the root of the
tree. BinaryPath should point to the base of the recursive search and 
override file should contain the override flags. Pathprefix is
appended to the filename fields if present. Example usage from the 
Debian archive:
   apt-ftparchive packages dists/potato/main/binary-i386/ > \
               dists/potato/main/binary-i386/Packages

Options:
  -h    This help text
  --md5 Control MD5 generation
  -s=?  Source override file
  -q    Quiet
  -d=?  Select the optional caching database
  --no-delink Enable delinking debug mode
  --contents  Control contents file generation
  -c=?  Read this configuration file
  -o=?  Set an arbitrary configuration option Version ‘%s’ for ‘%s’ was not found We are not supposed to delete stuff, cannot start AutoRemover You are about to do something potentially harmful
To continue type in the phrase ‘%s’
 ?]  You might want to run ‘apt-get -f install’ to correct these. You might want to run 'apt-get -f install' to correct these: 