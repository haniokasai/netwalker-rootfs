Þ    &      L  5   |      P  C  Q  (     ;   ¾     ú               (     D  n   ]     Ì     Ü  #   è  V        c  Ç   h  _   0               ®     Í     ì     ý     	          2  B   M  C        Ô     l	     	  O   	  p   â	  1   S
  ,   
     ²
  	   º
     Ä
  ¸  Ì
      H     K   Õ     !     7  !   V  *   x     £  º   Â  '   }     ¥  4   Á  R   ö     I  3  \  Þ     '   o  *     6   Â  3   ù  '   -     U     e       *      c   Ë  w   /  ½   §  '   e  (     F   ¶  û   ý  J   ù  F   D                    !                 &             %                                                                    
   	   #                      "                                        $       
%prog [options] find
%prog [options] cleanup [CRUFT]...
%prog [options] ignore [CRUFT]...
%prog [options] unignore [CRUFT]...

%prog finds and removes cruft from your system. 

Cruft is anything that shouldn't be on the system, but is. Stretching
the definition, it is also things that should be on the system, but
aren't. <big><b>Keep your system clean</b></big> Clean up a system so it's more like a freshly installed one Clean_up Computer Janitor Computer Janitor %s Could not clean up properly Do you want to continue? Essential package %s is missing. There may be problems with apt sources.list or Packages files may be missing? Finding plugins Ignored: %s Logging to syslog cannot be set up. Make the 'cleanup' command remove all packages, if none are given on the command line. Name Package is no longer supported: it is no longer in the package archive. (It may also have been installed from an unofficial archive that is no longer available. In that case you may want to keep it.) Package was installed because another package required it, but now nothing requires it anymore. Post-cleanup Post-cleanup: %s Pretending to post-cleanup: %s Pretending to remove cruft: %s Really clean up? Remove/fix? Removing cruft: %s Root access required. Running application, with: Store state of each piece of cruft in FILE. (Default is %default). The 'relatime' mount option is missing for filesystem mounted at %s This application helps you find and remove software packages you might not need anymore. It also suggests configuration changes that might benefit you. Unknown command: %s Unknown cruft: %s Verbose operation: make find show an explanation for each piece of cruft found. You are <b>removing %d .deb packages.</b> This may break your system, if you need them. Do you want to continue? You must run computer-janitor-gtk as root. Sorry. computer-janitor must be run as root, sorry. ignored removable updates Project-Id-Version: cruft-remover 1.10
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-04-03 18:42+0000
PO-Revision-Date: 2009-04-01 05:09+0000
Last-Translator: Hajime Mizuno <mizuno@as.airnet.ne.jp>
Language-Team: Ubuntu Japanese Team <ubuntu-jp@lists.ubuntu.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 21:17+0000
X-Generator: Launchpad (build Unknown)
 
%prog [options] find
%prog [options] cleanup [CRUFT]...
%prog [options] ignore [CRUFT]...
%prog [options] unignore [CRUFT]...

%prog ã¯ãã·ã¹ãã ä¸ã«ããä¸è¶³ãã¦ããããããã¯ä¸è¦ãªãã¼ã¿ (CRUFT) ã
çºè¦ã»åé¤ããã¢ããªã±ã¼ã·ã§ã³ã§ãã

ããã§è¨ãCRUFTã«ã¯ãã·ã¹ãã ä¸ã§å¿è¦ã¨ããã¦ããªãã«ãé¢ãããå­å¨ãããã¼ã¿ã¯
ãã¡ããã®ãã¨ãã·ã¹ãã ä¸ã§å¿è¦ã§ããã«ãé¢ãããå­å¨ããªããã¼ã¿ãå«ã¿ã¾ãã <big><b>ã·ã¹ãã ãæ´çæ´é ãããç¶æã«ãã¾ã</b></big> ã·ã¹ãã ãã¤ã³ã¹ãã¼ã«ç´å¾ã®ãããªç¶æã«æ´é ãã¾ã ã·ã¹ãã ãæ´é  ä¸è¦ããã±ã¼ã¸ã®ç®¡ç ä¸è¦ããã±ã¼ã¸ã®ç®¡ç %s æ­£ããæ´é ãè¡ãã¾ããã§ãã ä½æ¥­ãç¶è¡ãã¾ããï¼ å¿è¦ãªããã±ã¼ã¸ %s ãè¦ã¤ããã¾ãããsource.listãã¡ã¤ã«ã«åé¡ãããããããã±ã¼ã¸ãã¡ã¤ã«ãå­å¨ããªããªã£ã¦ããããããã¾ããã ãã©ã°ã¤ã³ãæ¤ç´¢ãã¦ãã¾ã ç¡è¦ããã¾ããï¼ %s syslog ã¸ã®ä¿å­ãè¨­å®ããã¦ãã¾ããã 'cleanup' ã³ãã³ãã§æå®ããå¨ã¦ã®ããã±ã¼ã¸ãåé¤ãã¾ãã ããã±ã¼ã¸å ãã®ããã±ã¼ã¸ã¯ãããµãã¼ãããã¦ãã¾ããï¼ ããã±ã¼ã¸ã¢ã¼ã«ã¤ãã«å­å¨ãã¾ãããï¼ç¾å¨å©ç¨ã§ããªããéå¬å¼ãªã¢ã¼ã«ã¤ãããã¤ã³ã¹ãã¼ã«ããå¯è½æ§ãããã¾ãããã®å ´åã¯ãæ®ãã¦ãããæ¹ãè¯ãããããã¾ããï¼ ãã®ããã±ã¼ã¸ã¯ãä»ã®ããã±ã¼ã¸ããã®ä¾å­é¢ä¿ã«ãã£ã¦ã¤ã³ã¹ãã¼ã«ããã¾ããããããç¾å¨ã¯ããã®ããã±ã¼ã¸ãå¿è¦ã¨ãã¦ããããã±ã¼ã¸ã¯å­å¨ãã¾ããã æ´é å¾ã®ä½æ¥­ãè¡ã£ã¦ãã¾ã æ´é å¾ã®ä½æ¥­ããã¦ãã¾ãï¼ %s æ´é å¾ã®ä½æ¥­ãæ¨¡æ¬å®è¡ãã¦ãã¾ãï¼ %s CRUFT ã®åé¤ãæ¨¡æ¬å®è¡ãã¦ãã¾ãï¼ %s æ´é ãè¡ã£ã¦ãããã§ããï¼ åé¤ããï¼ åé¤ãã¦ãã¾ãï¼ %s ç®¡çèæ¨©éãå¿è¦ã§ã ä»¥ä¸ã¨ä¸ç·ã«å®è¡ãã¦ãã¾ãï¼ CRUFT ã®ç¶æããFILE ã«ä¿å­ãã¾ãï¼åæè¨­å®ã§ã¯ %default ãä½¿ç¨ãã¾ãï¼ã %s ã§ãã¦ã³ãããããã¡ã¤ã«ã·ã¹ãã ã«ã¯ã'relatime' ãªãã·ã§ã³ãæå®ããã¦ãã¾ããã ãã®ã¢ããªã±ã¼ã·ã§ã³ã¯ãä¸è¦ãªã½ããã¦ã§ã¢ãè¦ã¤ãåé¤ãããã¨ãç°¡åã«è¡ããããã«ãã¾ããã¾ããããããæ§æå¤æ´ãææ¡ãã¾ãã å­å¨ããªãã³ãã³ãã§ãï¼ %s ãã® CRUFT ã¯å­å¨ãã¾ããï¼ %s ããããã® CRUFT ãã¨ã«ãè©³ç´°ãªèª¬æãè¡¨ç¤ºãã¾ãã <b>%d åã® .deb ããã±ã¼ã¸ã®åé¤ãé¸æãã¾ããã</b> ãããããã®ããã±ã¼ã¸ãå¿è¦ã¨ããã¦ãããªãã°ããã®æä½ã¯ã·ã¹ãã ãç ´å£ããå¯è½æ§ãããã¾ããç¶è¡ãã¦ãããããã§ããï¼ computer-janitor-gtkã¯ç®¡çèæ¨©éã§å®è¡ããå¿è¦ãããã¾ã computer-janitorã¯ç®¡çèæ¨©éã§å®è¡ããå¿è¦ãããã¾ã ç¡è¦ åé¤å¯è½ æ´æ° 