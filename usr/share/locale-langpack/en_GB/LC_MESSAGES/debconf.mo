��            )   �      �  ?   �  �   �  .   h  #   �  '   �     �     �  -     Q   4  8   �  M   �  k     (   y  X   �  6   �  =   2  Y   p  �  �  7   �    �  �   �	  @   N
  &   �
  '   �
     �
  !   �
       a   5  �  �  >   T  �   �  .   )  $   X  (   }     �     �  4   �  W      ;   X  O   �  m   �  %   R  \   x  7   �  =     Y   K  �  �  8   j    �  s   �  A     +   _  (   �     �  !   �     �  a                                                                          
                                           	                        
  -o,  --owner=package		Set the package that owns the command.   -f,  --frontend		Specify debconf frontend to use.
  -p,  --priority		Specify minimum priority question to show.
       --terse			Enable terse mode.
 %s failed to preconfigure, with exit status %s %s is broken or not fully installed %s is fuzzy at byte %s: %s; dropping it %s is not installed %s is outdated Config database not specified in config file. Debconf was not configured to display this error message, so it mailed it to you. Dialog frontend is incompatible with emacs shell buffers Dialog frontend requires a screen at least 13 lines tall and 31 columns wide. Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal. Extracting templates from packages: %d%% No usable dialog-like program is installed, so the dialog based frontend cannot be used. TERM is not set, so the dialog frontend is not usable. Term::ReadLine::GNU is incompatable with emacs shell buffers. The Sigils and Smileys options in the config file are no longer used. Please remove them. The editor-based debconf frontend presents you with one or more text files to edit. This is one such text file. If you are familiar with standard unix configuration files, this file will look familiar to you -- it contains comments interspersed with configuration items. Edit the file, changing any items as necessary, and then save it and exit. At that point, debconf will read the edited file, and use the values you entered to configure the system. Unable to load Debconf::Element::%s. Failed because: %s Usage: dpkg-reconfigure [options] packages
  -a,  --all			Reconfigure all packages.
  -u,  --unseen-only		Show only not yet seen questions.
       --default-priority	Use default priority instead of low.
       --force			Force reconfiguration of broken packages. You are using the editor-based debconf frontend to configure your system. See the end of this document for detailed instructions. delaying package configuration, since apt-utils is not installed must specify some debs to preconfigure please specify a package to reconfigure template parse error: %s unable to initialize frontend: %s unable to re-open stdin: %s warning: possible database corruption. Will attempt to repair by adding back missing question %s. Project-Id-Version: debconf
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2009-03-24 05:30+0000
PO-Revision-Date: 2007-03-09 14:06+0000
Last-Translator: Bruce Cowan <lp@bcowan.fastmail.co.uk>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 20:59+0000
X-Generator: Launchpad (build Unknown)
 
  -o, --owner=package		Set the package that owns the command.   -f, --frontend		Specify debconf frontend to use.
  -p, --priority		Specify minimum priority question to show.
        --terse			Enable terse mode.
 %s failed to preconfigure with exit status %s. %s is broken or not fully installed. %s is fuzzy at byte %s: %s; dropping it. %s is not installed. %s is outdated. Configuration database not specified in config file. Debconf was not configured to display this error message, so it has been mailed to you. Dialogue frontend is incompatible with Emacs shell buffers. Dialogue frontend requires a screen at least 13 lines tall and 31 columns wide. Dialogue frontend will not work on a dumb terminal, an Emacs shell buffer, or without a controlling terminal. Extract templates from packages: %d%% No usable dialogue-like program is installed, so the dialogue based frontend cannot be used. TERM is not set so the dialogue frontend is not usable. Term::ReadLine::GNU is incompatible with Emacs shell buffers. The Sigils and Smilies options in the config file are no longer used. Please remove them. The editor-based debconf frontend presents you with one or more text files to edit. This is one such text file. If you are familiar with standard Unix configuration files, this file will look familiar to you  as it contains comments interspersed with configuration items. Edit the file, changing any items as necessary, and then save it and exit. At that point, debconf will read the edited file, and use the values you entered to configure the system. Unable to load Debconf::Element::%s. Failed because: %s. Usage: dpkg-reconfigure [options] packages
  -a, --all			Reconfigure all packages.
  -u, --unseen-only		Show only not yet seen questions.
        --default-priority	Use default priority instead of low.
        --force			Force reconfiguration of broken packages. You are using the editor-based debconf frontend to configure your system. See the end of this document for detailed Delaying package configuration, since apt-utils is not installed. You must specify some debs to preconfigure. Please specify a package to reconfigure. Template parse error: %s Unable to initialise frontend: %s Unable to re-open stdin: %s Warning: Possible database corruption; will attempt to repair by adding back missing question %s. 