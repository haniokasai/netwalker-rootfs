Þ    0        C         (  å  )  *     o   :  p   ª          8  )   O  	   y             ,   À  $   í     	  #   '	     K	      f	     	     §	  #   Æ	  !   ê	     
      
     9
     Y
  *   x
     £
     º
     Ñ
     ê
     
  &   )     P     o       â        ~          ¦  H   À  (   	  ø   2    +  -   Ë  F   ù  8   @  -   y     §  Ä  Æ  ú    F     Å   Í  ´     >   H  6     R   ¾            1   5  J   g  ;   ²  &   î  F     !   \  /   ~  &   ®  2   Õ  8     6   A     x  *     7   Â  -   ú  >   (     g  $     +   ¥  0   Ñ  %     3   (  $   \  .     ,   °    Ý  +   ô  #       %   D   \   j   7   Ç   |  ÿ     |"  m   &  F   t&  C   »&  I   ÿ&  #   I'                 "                    ,       -                   
                             %                 #      .              	   *                           !      0   &   +      $   '   /   )      (                                       killall -l, --list
       killall -V, --version

  -e,--exact          require exact match for very long names
  -I,--ignore-case    case insensitive process name match
  -g,--process-group  kill process group instead of process
  -i,--interactive    ask for confirmation before killing
  -l,--list           list all known signal names
  -q,--quiet          don't print complaints
  -r,--regexp         interpret NAME as an extended regular expression
  -s,--signal SIGNAL  send this signal instead of SIGTERM
  -u,--user USER      kill only process(es) running as USER
  -v,--verbose        report if the signal was successfully sent
  -V,--version        display version information
  -w,--wait           wait for processes to die
     -Z     show SELinux security contexts
     PID    start at this PID; default is 1 (init)
    USER   show only trees rooted at processes of this user

   -Z,--context REGEXP kill only process(es) having context
                      (must precede other arguments)
 %s is empty (not mounted ?)
 %s: no process killed
 %s: unknown signal; %s -l lists signals.
 (unknown) Bad regular expression: %s
 Can't get terminal capabilities
 Cannot allocate memory for matched proc: %s
 Cannot find socket's device number.
 Cannot find user %s
 Cannot get UID from process status
 Cannot open /etc/mtab: %s
 Cannot open /proc directory: %s
 Cannot open /proc/net/unix: %s
 Cannot open a network socket.
 Cannot open protocol file "%s": %s
 Cannot resolve local port %s: %s
 Cannot stat %s: %s
 Cannot stat file %s: %s
 Cannot stat mount point %s: %s
 Could not kill process %d: %s
 Internal error: MAX_DEPTH not big enough.
 Invalid namespace name Kill %s(%s%d) ? (y/N)  Kill process %d ? (y/N)  Killed %s(%s%d) with signal %d
 Maximum number of names is %d
 Namespace option requires an argument. No process specification given No processes found.
 No such user name: %s
 PSmisc comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under
the terms of the GNU General Public License.
For more information about these matters, see the files named COPYING.
 Press return to close
 TERM is not set
 Unknown local port AF %d
 Usage: killall [-Z CONTEXT] [-u USER] [ -eIgiqrvw ] [ -SIGNAL ] NAME...
 Usage: killall [OPTION]... [--] NAME...
 Usage: pidof [ -eg ] NAME...
       pidof -V

    -e      require exact match for very long names;
            skip if the command line is unavailable
    -g      show process group ID instead of process ID
    -V      display version information

 Usage: pstree [ -a ] [ -c ] [ -h | -H PID ] [ -l ] [ -n ] [ -p ] [ -u ]
              [ -A | -G | -U ] [ PID | USER ]
       pstree -V
Display a tree of processes.

    -a     show command line arguments
    -A     use ASCII line drawing characters
    -c     don't compact identical subtrees
    -h     highlight current process and its ancestors
    -H PID highlight this process and its ancestors
    -G     use VT100 line drawing characters
    -l     don't truncate long lines
    -n     sort output by PID
    -p     show PIDs; implies -c
    -u     show uid transitions
    -U     use UTF-8 (Unicode) line drawing characters
    -V     display version information
 You can only use files with mountpoint option You cannot search for only IPv4 and only IPv6 sockets at the same time You cannot use the mounted and mountpoint flags together all option cannot be used with silent option. skipping partial match %s(%d)
 Project-Id-Version: psmisc 22.2pre1
Report-Msgid-Bugs-To: csmall@small.dropbear.id.au
POT-Creation-Date: 2007-11-04 17:27+1100
PO-Revision-Date: 2008-01-15 12:38+0000
Last-Translator: GOTO Masanori <Unknown>
Language-Team: Japanese <translation-team-ja@lists.sourceforge.net>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 03:57+0000
X-Generator: Launchpad (build Unknown)
        killall -l, --list
       killall -V, --version

  -e,--exact            ã¨ã¦ãé·ãååã«å¯¾ãã¦å®å¨ä¸è´ãè¦æ±ãã
  -I,--ignore-case      ãã­ã»ã¹åã®ä¸è´ã¯å¤§æå­ã®å°æå­åºå¥ãªãè¡ã
  -g,--process-group    ãã­ã»ã¹ã®ä»£ãã«ãã­ã»ã¹ã°ã«ã¼ãã«ã·ã°ãã«ãéã
  -i,--interactive      kill ããåã«ç¢ºèªãæ±ãã
  -l,--list             æ¢ç¥ã®ã·ã°ãã«åããã¹ã¦è¡¨ç¤ºãã
  -q,--quiet            kill ãããã­ã»ã¹ããªãå ´åã«è¡¨ç¤ºãè¡ããªã
  -r,--regexp           æå®ããååãæ¡å¼µæ­£è¦è¡¨ç¾ã¨ãã¦è§£éãã
  -s,--signal ã·ã°ãã«  SIGTERMã®ä»£ãã«æå®ããã·ã°ãã«ãéã
  -u,--user ã¦ã¼ã¶      æå®ããã¦ã¼ã¶ã§èµ°è¡ãããã­ã»ã¹ã®ã¿killãã
  -v,--verbose          ã·ã°ãã«ã®éä¿¡ã«æåãããå ±åãã
  -V,--version          ãã¼ã¸ã§ã³æå ±ãè¡¨ç¤ºãã
  -w,--wait             killãããã­ã»ã¹ãçµäºããã¾ã§å¾ã¤
     -Z     SELinuxã»ã­ã¥ãªãã£ã³ã³ãã­ã¹ããè¡¨ç¤ºãã
     PID      æå®ããPIDããè¡¨ç¤ºéå§ãã¾ã; ããã©ã«ãã¯ 1 (init)
    ã¦ã¼ã¶å æå®ããã¦ã¼ã¶ã¨ãã¦åä½ãããã­ã»ã¹ããæ´¾çããããªã¼ã®ã¿è¡¨ç¤º

   -Z,--context æ­£è¦è¡¨ç¾ ã³ã³ãã­ã¹ããæã¤ãã­ã»ã¹ã®ã¿killãã
                        (ä»ã®å¼æ°ãããåã«æå®ããã¦ããªããã°ãªããªã)
 %s ã¯ç©ºãã£ã¬ã¯ããª (ãã¦ã³ãããã¦ããªã?)
 %s: ã©ã®ãã­ã»ã¹ãkillããã¾ããã§ãã
 %s: æªç¥ã®ã·ã°ãã«; %s -l ã«ãã£ã¦ã·ã°ãã«ãä¸è¦§è¡¨ç¤ºãã¾ã
 (ä¸æ) ä¸æ­£ãªæ­£è¦è¡¨ç¾: %s
 ç«¯æ«ã®æ©è½ãåå¾ã§ãã¾ããã§ãã
 ä¸è´ãããã­ã»ã¹ã«å¯¾ããã¡ã¢ãªãç²å¾ã§ãã¾ãã: %s
 ã½ã±ããã®ããã¤ã¹çªå·ãè¦ã¤ããã¾ãã.
 ã¦ã¼ã¶ %s ãçºè¦ã§ãã¾ãã
 ãã­ã»ã¹ã®ç¾å¨ç¶æããUIDãåå¾ã§ãã¾ããã§ãã
 /etc/mtab ãéãã¾ãã: %s
 /proc ãã£ã¬ã¯ããªãéãã¾ãã: %s
 /proc/net/unix ãéãã¾ãã: %s
 ãããã¯ã¼ã¯ã½ã±ãããéãã¾ãã.
 ãã­ãã³ã«ãã¡ã¤ã« "%s" ãéãã¾ãã: %s
 ã­ã¼ã«ã«ãã¼ã %s ãè§£æ±ºã§ãã¾ãã: %s
 %s ãstatã§ãã¾ãã: %s
 ãã¡ã¤ã«ãstatã§ãã¾ãã %s: %s
 ãã¦ã³ããã¤ã³ã %s ãstatã§ãã¾ãã: %s
 ãã­ã»ã¹ %d ã kill ã§ãã¾ãã: %s
 åé¨ã¨ã©ã¼: MAX_DEPTH ãååå¤§ããããã¾ãã.
 ä¸æ­£ãªååç©ºéå %s(%s%d) ãkillãã¾ãã? (y/N)  ãã­ã»ã¹ %d ãkillãã¾ãã? (y/N)  %s(%s%d) ãã·ã°ãã« %d ã§killãã¾ãã
 ååã®æå¤§æå®å¯è½æ°ã¯ %d
 ååç©ºéãªãã·ã§ã³ã¯å¼æ°ãå¿è¦ã§ã å¼æ°ãä¸ãããã¦ãã¾ãã ãã­ã»ã¹ã¯è¦ã¤ããã¾ããã§ãã
 æå®ã¦ã¼ã¶åã¯å­å¨ãã¾ãã: %s
 PSmiscã¯å®å¨ã«ç¡ä¿è¨¼ã§ã
ããã¯ããªã¼ã½ããã¦ã§ã¢ã§ããGNUä¸è¬å¬è¡å©ç¨è¨±è«¾å¥ç´æ¸ã®æ¡é ã«åºã¥ãã¦
åéå¸ãèªç±ã«è¡ã£ã¦ãã¾ãã¾ããã
ãããã«ã¤ãã¦ããè©³ç´°ãªæå ±ã¯COPYINGãã¡ã¤ã«ããè¦§ä¸ããã
 ãªã¿ã¼ã³ã­ã¼ãæ¼ãã¨éãã¾ã
 TERMãè¨­å®ããã¦ãã¾ãã
 æªç¥ã®ã­ã¼ã«ã«ãã¼ã AF %d
 ä½¿ç¨æ³: killall [-Z CONTEXT] [-u ã¦ã¼ã¶ã¼] [ -eIgiqrvw ] [ -ã·ã°ãã« ] åå...
 ä½¿ç¨æ³: killall [ãªãã·ã§ã³]... [--] åå...
 ä½¿ç¨æ³: pidof [ -eg ] ãã­ã»ã¹å...
        pidof -V

    -e      ã¨ã¦ãé·ããã­ã»ã¹åã«å¯¾ãã¦å®å¨ä¸è´ãè¦æ±ãã
            ã³ãã³ãã©ã¤ã³ãå©ç¨ã§ããªãå ´åã¯è©²å½ãã­ã»ã¹ã¯ã¹ã­ããããã
    -g      ãã­ã»ã¹IDã®ä»£ãã«ãã­ã»ã¹ã°ã«ã¼ãIDãè¡¨ç¤ºãã
    -V      ãã¼ã¸ã§ã³æå ±ãè¡¨ç¤ºãã

 ä½¿ç¨æ³: pstree [ -a ] [ -c ] [ -h | -H PID ] [ -l ] [ -n ] [ -p ] [ -u ]
              [ -A | -G | -U ] [ PID | ã¦ã¼ã¶å ]
        pstree -V
ãã­ã»ã¹ããªã¼ãè¡¨ç¤ºããã

    -a     ã³ãã³ãã©ã¤ã³å¼æ°ãè¡¨ç¤º
    -A     ASCII æå­ãç½«ç·è¡¨ç¤ºã«ä½¿ç¨
    -c     åãåå®¹ã®ãµãããªã¼ãã¾ã¨ãã¦ç­ãè¡¨ç¤ºããªã
    -h     ç¾å¨ã®ãã­ã»ã¹ã¨ãã®åç¥ã®ãã­ã»ã¹ãå¼·èª¿è¡¨ç¤ºãã
    -H PID æå®ãã­ã»ã¹PIDã¨ãã®åç¥ã®ãã­ã»ã¹ãå¼·èª¿è¡¨ç¤ºãã
    -G     VT100 ç½«ç·æå­ãè¡¨ç¤ºã«ä½¿ç¨
    -l     é·ãè¡ãè¡¨ç¤ºããéä¸­ã§æã¡åãã¾ãã
    -n     PIDã§ã½ã¼ããã¦è¡¨ç¤º
    -p     PIDãè¡¨ç¤º; -cãªãã·ã§ã³ãã¤ããå¹æãå«ã¿ã¾ã
    -u     UIDã®é·ç§»ç¶æ³ãè¡¨ç¤ºãã
    -U     UTF-8 (Unicode) æå­ãç½«ç·è¡¨ç¤ºã«ä½¿ç¨
    -V     ãã¼ã¸ã§ã³æå ±ãè¡¨ç¤º
 ãã¦ã³ããã¤ã³ããªãã·ã§ã³(-mã¾ãã¯-c)ã¨ä¸ç·ã«ä½¿ããã®ã¯fileååç©ºéã®ã¿ã§ã -4ãªãã·ã§ã³ã¨-6ãªãã·ã§ã³ã¯åæã«æå®ã§ãã¾ãã -mãªãã·ã§ã³ã¨-cãªãã·ã§ã³ã¯åæã«ã¯ä½¿ãã¾ãã -aãªãã·ã§ã³ã¯-sãªãã·ã§ã³ã¨ä¸ç·ã«ã¯ä½¿ç¨ã§ãã¾ãã é¨åä¸è´ãã¹ã­ãã %s(%d)
 