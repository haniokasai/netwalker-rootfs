Þ    *      l  ;   ¼      ¨  )   ©  )   Ó  Ë   ý  Z   É  7  $  B   \       '   $  '   L     t  $        ·  &   Î  /   õ  /   %  =   U       %   ®  2   Ô     	  $   	  &   D	  +   k	  '   	  ,   ¿	  &   ì	  '   
  *   ;
  +   f
     
     ©
     Á
     Ó
     æ
     ý
  &        B     J     X     r       ¢  «  ,   N  ,   {  ý   ¨  T   ¦  «  û  W   §     ÿ  V     O   å  #   5  %   Y       8     X   Ñ  T   *  c     8   ã  +     2   H     {  /     =   Â  H      @   I  K     <   Ö  ?     A   S  A     '   ×  %   ÿ     %  !   8  '   Z  $     9   §     á     í     ÿ          7                               !                     '      )   %      $                        *                                            	          
   "   &                    #   (                        	%s -l pathname...	[not IRIX compatible]
 	%s -r pathname...	[not IRIX compatible]
       --set=acl           set the ACL of file(s), replacing the current ACL
      --set-file=file     read ACL entries to set from file
      --mask              do recalculate the effective rights mask
       --version           print version and exit
      --help              this help text
   -R, --recursive         recurse into subdirectories
  -L, --logical           logical walk, follow symbolic links
  -P, --physical          physical walk, do not follow symbolic links
      --restore=file      restore ACLs (inverse of `getfacl -R')
      --test              test mode (ACLs are not modified)
   -d, --default           display the default access control list
   -n, --no-mask           don't recalculate the effective rights mask
  -d, --default           operations apply to the default ACL
 %s %s -- get file access control lists
 %s %s -- set file access control lists
 %s: %s in line %d of file %s
 %s: %s in line %d of standard input
 %s: %s: %s in line %d
 %s: %s: Cannot change owner/group: %s
 %s: %s: No filename found in line %d, aborting
 %s: %s: Only directories can have default ACLs
 %s: No filename found in line %d of standard input, aborting
 %s: Option -%c incomplete
 %s: Option -%c: %s near character %d
 %s: Removing leading '/' from absolute path names
 %s: Standard input: %s
 %s: access ACL '%s': %s at entry %d
 %s: cannot get access ACL on '%s': %s
 %s: cannot get access ACL text on '%s': %s
 %s: cannot get default ACL on '%s': %s
 %s: cannot get default ACL text on '%s': %s
 %s: cannot set access acl on "%s": %s
 %s: cannot set default acl on "%s": %s
 %s: error removing access acl on "%s": %s
 %s: error removing default acl on "%s": %s
 %s: malloc failed: %s
 %s: opendir failed: %s
 Duplicate entries Invalid entry type Missing or wrong entry Multiple entries of same type Try `%s --help' for more information.
 Usage:
 Usage: %s %s
 Usage: %s [-%s] file ...
 preserving permissions for %s setting permissions for %s Project-Id-Version: acl
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2008-11-13 17:22+0000
PO-Revision-Date: 2007-04-01 05:09+0000
Last-Translator: Fumihito YOSHIDA <hito@kugutsu.org>
Language-Team: Japanese <ja@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-13 22:26+0000
X-Generator: Launchpad (build Unknown)
 	%s -l pathname...	[IRIXã¨ã¯éäºæ]âµ
 	%s -r pathname...	[IRIXã¨ã¯éäºæ]âµ
       --set=acl           ACLãè¨­å®ãã¾ããç¾å¨ã®è¨­å®ãä¸æ¸ãããã¾ãã
      --set-file=file     ãã¡ã¤ã«ã«æ¸ãããè¨­å®ããã¨ã«ACLãè¨­å®ããã
      --mask              é©åãªmaskè¨­å®ãåçæããã
       --version ãã¼ã¸ã§ã³ãå°å·ãã¦çµäº

      --help ãã®ãã«ã

   -R, --recursive         ãµããã£ã¬ã¯ããªã«ãåå¸°çã«é©ç¨ããã
  -L, --logical           è«ççã«è¾¿ããã·ã³ããªãã¯ãªã³ã¯ãè¾¿ãã¾ãã
  -P, --physical          ç©ççã«è¾¿ããã·ã³ããªãã¯ãªã³ã¯ãè¾¿ãã¾ããã
      --restore=file      ACLãåã«æ»ãã¾ã(`getfacl -R'ã®é)ã
      --test              ãã¹ãã¢ã¼ã(ACLè¨­å®ãå¤æ´ãã¾ãã)ã
   -d, --default æ¢å®ã®ã¢ã¯ã»ã¹ã»ã³ã³ãã­ã¼ã«ã»ãªã¹ããè¡¨ç¤ºãã

   -n, --no-mask           æå¹ãªmaskè¨­å®ãåçæããªãã
  -d, --default           ããã©ã«ãã®ACLè¨­å®ãé©ç¨ããã
 %s %s -- ãã¡ã¤ã«ã®ã¢ã¯ã»ã¹ã»ã³ã³ãã­ã¼ã«ã»ãªã¹ããåå¾ãã

 %s %s -- ãã¡ã¤ã«ã»ã¢ã¯ã»ã¹ã»ã³ã³ãã­ã¼ã«ã®ãªã¹ããè¨­å®
 %s: %s è¡æ°: %d ãã¡ã¤ã«: %s
 %s: %s æ¨æºå¥åã®ã©ã¤ã³ %d 

 %s: %s: %s ã©ã¤ã³ %d
 %s: %s: ownerã¾ãã¯groupãå¤æ´ã§ãã¾ãã: %s
 %s: %s: ãã¡ã¤ã«åã %d ã®ã©ã¤ã³ã«è¦ã¤ãããªãã®ã§ä¸­æ­ãã¾ãã
 %s: %s: ãã£ã¬ã¯ããªã ããããã©ã«ãACLãæã¤ãã¨ãã§ãã¾ã
 %s: ãã¡ã¤ã«åãæ¨æºå¥åã® %d ã®ã©ã¤ã³ã«è¦ã¤ãããªãã®ã§ä¸­æ­ãã¾ãã
 %s: ãªãã·ã§ã³ -%c ä»¥éãä¸è¶³ãã¦ãã¾ã

 %s: ãªãã·ã§ã³ -%c: %s  %d ã®è¿ã

 %s: çµ¶å¯¾ãã¹åããåé ­ã® '/' ãåé¤

 %s: æ¨æºå¥å: %s

 %s: ã¢ã¯ã»ã¹ACL '%s': %sãã¨ã³ããª %d
 %s: ã¢ã¯ã»ã¹ACLã '%s' ä¸ã§åå¾ã§ãã¾ãã : %s
 %s: ã¢ã¯ã»ã¹ACLãã­ã¹ãã '%s' ä¸ã§åå¾ã§ãã¾ãã: %s
 %s: ããã©ã«ãACLã  '%s' ä¸ã§åå¾ã§ãã¾ãã: %s
 %s: ããã©ã«ãACLãã­ã¹ãã '%s' ä¸ã§åå¾ã§ãã¾ãã: %s
 %s: ã¢ã¯ã»ã¹aclã "%s" ä¸ã§è¨­å®ã§ãã¾ãã: %s
 %s: ããã©ã«ãaclã "%s" ä¸ã§è¨­å®ã§ãã¾ãã: %s
 %s:  "%s"ã®ã¢ã¯ã»ã¹aclãåé¤ããã¨ãã®ã¨ã©ã¼: %s
 %s:"%s"ã®ããã©ã«ãaclãåé¤ããã¨ãã®ã¨ã©ã¼:%s
 %s: mallocã«å¤±æãã¾ãã: %sâµ
 %s: opendirã«å¤±æãã¾ãã: %s
 éè¤ã¨ã³ããª ä¸æ­£ãªã¨ã³ããªã»ã¿ã¤ã ä¸è¶³ã¾ãã¯ééã£ãã¨ã³ããª è¤æ°ã®åã¿ã¤ãã®ã¨ã³ããª è©³ããã¯ `%s --help' ãå®è¡ãã¦ãã ããã

 ä½¿ãæ¹:
 ä½¿ãæ¹: %s %s
 ä½¿ãæ¹: %s [-%s] file ...

 %s ã¸ã®æ¨©éã®ä¿å­ %s ã¸ã®æ¨©éã®è¨­å® 