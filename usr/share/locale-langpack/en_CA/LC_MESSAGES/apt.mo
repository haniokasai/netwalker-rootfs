��          �   %   �      `  u   a     �     �  .     #   <     `  x   x  *   �       '   9  8   a  5   �  3   �  1     B   6  $   y  ?   �  &   �  <       B  ;   R  R   �  (  �  '  
	  &  2
  H  Y  �  �  y   M     �     �  0     -   6     d  z   {  +   �     "  *   @  @   k  =   �  4   �  3     B   S  -   �  E   �  *   
  9   5    o  =   �  S   �  &    #  9    ]  D  y!            	                          
                                                                                      %s dependency for %s cannot be satisfied because no available versions of package %s can satisfy version requirements %s has no build depends.
 %s not a valid DEB package. Check if the 'dpkg-dev' package is installed.
 Couldn't determine free space in %s Failed to fetch %s  %s
 Hmm, seems like the AutoRemover destroyed something which really
shouldn't happen. Please file a bug report against apt. However the following packages replace it: IO to subprocess/file failed Internal Error, AutoRemover broke stuff Must specify at least one package to check builddeps for Must specify at least one package to fetch source for Packages need to be removed but remove is disabled. Please insert a Disc in the drive and press enter Please provide a name for this Disc, such as 'Debian 2.1r1 Disk 1' Problem during package list update.  Reinstallation of %s is not possible, it cannot be downloaded.
 Skipping already downloaded file '%s'
 The following information may help to resolve the situation: The package list update failed with a authentication failure. This usually happens behind a network proxy server. Please try to click on the "Run this action now" button to correct the problem or update the list manually by running Update Manager and clicking on "Check". Trivial Only specified but this is not a trivial operation. Unable to fetch some archives, maybe run apt-get update or try with --fix-missing? Usage: apt-config [options] command

apt-config is a simple tool to read the APT config file

Commands:
   shell - Shell mode
   dump - Show the configuration

Options:
  -h   This help text.
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
 Usage: apt-extracttemplates file1 [file2 ...]

apt-extracttemplates is a tool to extract config and template info
from debian packages

Options:
  -h   This help text
  -t   Set the temp dir
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
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
  -o=?  Set an arbitrary configuration option Usage: apt-sortpkgs [options] file1 [file2 ...]

apt-sortpkgs is a simple tool to sort package files. The -s option is used
to indicate what kind of file it is.

Options:
  -h   This help text
  -s   Use source file sorting
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
 Project-Id-Version: apt
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2009-03-31 02:50+0000
PO-Revision-Date: 2009-01-11 20:03+0000
Last-Translator: Joel Goguen <jgoguen@jgoguen.ca>
Language-Team: English (Canada) <en_CA@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 01:06+0000
X-Generator: Launchpad (build Unknown)
 %s dependency for %s cannot be satisfied because no available versions of package %s can satisfy the version requirements %s has no build dependencies.
 %s is not a valid DEB package. Check that the 'dpkg-dev' package is installed.
 Couldn't determine free space available in %s Failed to fetch %s %s
 An error has occurred: autoremove destroyed something which really
shouldn't happen. Please file a bug report against apt. However, the following packages replace it: I/O to subprocess/file failed Internal Error; autoremove broke something You must specify at least one package to check the builddeps for You must specify at least one package to fetch the source for Packages need to be removed, but remove is disabled. Please insert a Disk into the drive and press enter Please provide a name for this Disk, such as 'Debian 2.1r1 Disk 1' Problem occurred during package list update.  Reinstallation of %s is not possible, since it cannot be downloaded.
 Skipping the already downloaded file '%s'
 The following information may help resolve the situation: The package list update failed with an authentication failure. This usually happens behind a network proxy server. Please try to click on the "Run this action now" button to correct the problem or update the list manually by running Update Manager and clicking on "Check". `Trivial Only' specified but this is not a trivial operation. Unable to fetch some archives, try running apt-get update or apt-get --fix-missing. Usage: apt-config [options] command

apt-config is a simple tool to read the APT config file

Commands:
   shell - Shell mode
   dump - Show the configuration

Options:
  -h This help text.
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
 Usage: apt-extracttemplates file1 [file2 ...]

apt-extracttemplates is a tool to extract config and template info
from debian packages

Options:
  -h This help text
  -t Set the temp dir
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
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
  -h This help text
  --md5 Control MD5 generation
  -s=? Source override file
  -q Quiet
  -d=? Select the optional caching database
  --no-delink Enable delinking debug mode
  --contents Control contents file generation
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option Usage: apt-sortpkgs [options] file1 [file2 ...]

apt-sortpkgs is a simple tool to sort package files. The -s option is used
to indicate what kind of file it is.

Options:
  -h This help text
  -s Use source file sorting
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
 