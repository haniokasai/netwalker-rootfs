Þ    R      ¬  m   <      ð  ú   ñ  ,   ì  5     7   O  \     `   ä  u   E	  l   »	  b   (
  V   
  Y   â
  ~   <     »  º   K  %        ,     C     ]  d   z     ß     ó     
     '     C  $   [               ­     ¾     Ç  #   æ     
     %     -     @     R     d     v  H        Ì     æ       !   #     E     Z  (   o       #   ¶     Ú  $   ú       #   9  B   ]  2         Ó      ç          &  *   E  *   p          »     Ë  #   Ù  #   ý  &   !     H     W  ,   v     £     ¼  -   Ñ     ÿ          $     3     I     _     m            Ï  º  2    3   ½  <   ñ  7   .  _   f  ~   Æ  ®   E     ô  [     ]   â  Z   @  _     ¦   û    ¢  &   ´  #   Û     ÿ          ?     Ñ     à     ó           %      =      Y      r            §   *   º      å      !      !     '!     C!     _!     x!     !  b   ¬!  :   "  %   J"     p"  >   "     Å"  '   ä"  9   #  4   F#  3   {#  4   ¯#  L   ä#  -   1$  5   _$  >   $  <   Ô$     %  4   -%     b%  6   ~%  4   µ%  :   ê%  %   %&     K&     j&  5   &  5   ·&  4   í&  $   "'  *   G'  I   r'  =   ¼'     ú'  =   (     T(     e(     (  %   (  +   ¿(     ë(  .   )  .   :)  ,   i)           $           E       R       "          !   @   =   F       M   B      5          ?      4   3                .               O               ;           2   (   :       9   %           <   	   /       C       Q   '   ,   L                 N                
          #   6   +   0       1       7   G         D   I   *      -   >   K         P   8       &          J   )                 H      A    
If no -e, --expression, -f, or --file option is given, then the first
non-option argument is taken as the sed script to interpret.  All
remaining arguments are names of input files; if no input files are
specified, then the standard input is read.

       --help     display this help and exit
       --version  output version information and exit
   --posix
                 disable all GNU extensions.
   -R, --regexp-perl
                 use Perl 5's regular expressions syntax in the script.
   -e script, --expression=script
                 add the script to the commands to be executed
   -f script-file, --file=script-file
                 add the contents of script-file to the commands to be executed
   -i[SUFFIX], --in-place[=SUFFIX]
                 edit files in place (makes backup if extension supplied)
   -l N, --line-length=N
                 specify the desired line-wrap length for the `l' command
   -n, --quiet, --silent
                 suppress automatic printing of pattern space
   -r, --regexp-extended
                 use extended regular expressions in the script.
   -s, --separate
                 consider files as separate rather than as a single continuous
                 long stream.
   -u, --unbuffered
                 load minimal amounts of data from the input files and flush
                 the output buffers more often
 %s
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,
to the extent permitted by law.
 %s: -e expression #%lu, char %lu: %s
 %s: can't read %s: %s
 %s: file %s line %lu: %s
 : doesn't want any addresses E-mail bug reports to: %s .
Be sure to include the word ``%s'' somewhere in the ``Subject:'' field.
 GNU sed version %s
 Invalid back reference Invalid character class name Invalid collation character Invalid content of \{\} Invalid preceding regular expression Invalid range end Invalid regular expression Memory exhausted No match No previous regular expression Premature end of regular expression Regular expression too big Success Trailing backslash Unmatched ( or \( Unmatched ) or \) Unmatched [ or [^ Unmatched \{ Usage: %s [OPTION]... {script-only-if-no-other-script} [input-file]...

 `e' command not supported `}' doesn't want any addresses based on GNU sed version %s

 can't find label for jump to `%s' cannot remove %s: %s cannot rename %s: %s cannot specify modifiers on empty regexp command only uses one address comments don't accept any addresses couldn't edit %s: is a terminal couldn't edit %s: not a regular file couldn't open file %s: %s couldn't open temporary file %s: %s couldn't write %d item to %s: %s couldn't write %d items to %s: %s delimiter character is not a single-byte character error in subprocess expected \ after `a', `c' or `i' expected newer version of sed extra characters after command invalid reference \%d on `s' command's RHS invalid usage of +N or ~N as first address invalid usage of line address 0 missing command multiple `!'s multiple `g' options to `s' command multiple `p' options to `s' command multiple number options to `s' command no input files no previous regular expression number option to `s' command may not be zero option `e' not supported read error on %s: %s strings for `y' command are different lengths super-sed version %s
 unexpected `,' unexpected `}' unknown command: `%c' unknown option to `s' unmatched `{' unterminated `s' command unterminated `y' command unterminated address regex Project-Id-Version: GNU sed 4.1.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2006-02-03 10:26+0100
PO-Revision-Date: 2008-11-17 07:28+0000
Last-Translator: IIDA Yosiaki <iida@gnu.org>
Language-Team: Japanese <translation-team-ja@lists.sourceforge.net>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Launchpad-Export-Date: 2009-04-14 08:45+0000
X-Generator: Launchpad (build Unknown)
 
-eã--expressionã-fã--fileãªãã·ã§ã³ã®ã©ãããªãã¨ããªãã·ã§ã³ä»¥å¤ã®
æåã®å¼æ°ãsedã¹ã¯ãªããã¨ãã¦è§£éãã¾ããæ®ãã®å¼æ°ã¯å¨é¨ãå¥åãã¡
ã¤ã«åã¨ãªãã¾ããå¥åãã¡ã¤ã«ã®æå®ããªãã¨ãæ¨æºå¥åãèª­ã¿è¾¼ã¿ã¾ãã

       --help     ãã®èª¬æãè¡¨ç¤ºãã¦çµäº
       --version  ãã¼ã¸ã§ã³æå ±ãè¡¨ç¤ºãã¦çµäº
   --posix
                 GNUæ¡å¼µãå¨é¨ç¦æ­¢ã
   -R, --regexp-perl
                 ã¹ã¯ãªããã§Perl 5ã®æ­£è¦è¡¨ç¾æ§æãä½¿ãã
   -e ã¹ã¯ãªãã, --expression=ã¹ã¯ãªãã
                 å®è¡ããã³ãã³ãã¨ãã¦ã¹ã¯ãªãããè¿½å 
   -f ã¹ã¯ãªããã»ãã¡ã¤ã«, --file=ã¹ã¯ãªããã»ãã¡ã¤ã«
                 å®è¡ããã³ãã³ãã¨ãã¦ã¹ã¯ãªããã»ãã¡ã¤ã«ã®åå®¹ãè¿½å 
   -i[æ¥å°¾è¾], --in-place[=æ¥å°¾è¾]
                 ãã¡ã¤ã«ããã®å ´ã§ç·¨é (æ¡å¼µå­ãããã°ãããã¯ã¢ãããä½æ)
   -l N, --line-length=N
                 ãlãã³ãã³ãç¨ã®è¡æè¿ãé·ãæå®
   -n, --quiet, --silent
                 ãã¿ã¼ã³ã»ã¹ãã¼ã¹ã®èªååºåãæå¶
   -r, --regexp-extended
                 ã¹ã¯ãªããã§æ¡å¼µæ­£è¦è¡¨ç¾ãä½¿ç¨ã
   -s, --separate
                 ãã¡ã¤ã«ãä¸é£ã®å¥åã«ãããå¥ãã«å¦çã
   -u, --unbuffered
                 å¥åãã¡ã¤ã«ããæ¥µå°ã®ãã¼ã¿ãåãè¾¼ã¿ã
                 ã¡ããã¡ããåºåãããã¡ã¼ã«æåºã
 %s
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,
to the extent permitted by law.

è¨³æ³¨: éå¸¸ã«éè¦ãªæç« ã®ãããåæãæ®ãã¦ãã¾ãã
  -- åèè¨³
ããã¯ããªã¼ã»ã½ããã¦ã§ã¢ã§ããè¤è£½ã®æ¡ä»¶ã«é¢ãã¦ã¯ãã½ã¼ã¹ããè¦§ãã ã
ããä¿è¨¼ã¯ä¸åããã¾ãããå¶å©ç®çãæ³ã§å®ããããç¯å²ã§ã®ç¹å®ç®çã®ãã
ã®é©åæ§ãããã¾ããã
 %s: -e è¡¨ç¾ #%lu, æå­æ° %lu: %s
 %s: %sãèª­ã¿è¾¼ãã¾ãã: %s
 %s: ãã¡ã¤ã« %s %luè¡: %s
 :ã«ã¢ãã¬ã¹ã¯ä¸è¦ã§ã é»å­ã¡ã¼ã«ã«ãããã°å ±åã®å®å: %s
å ±åã®éãâSubject:âãã£ã¼ã«ãã®ã©ããã«â%sâãå¥ãã¦ãã ããã
 GNU sed %sç
 ç¡å¹ãªéåç§ ç¡å¹ãªæå­ã¯ã©ã¹å ç¡å¹ãªæ ¡åæå­ ç¡å¹ãª\{\}ã®åå®¹" ç¡å¹ãªåè¡æ­£è¦è¡¨ç¾ ç¡å¹ãªç¯å²ã®çµç«¯ ç¡å¹ãªæ­£è¦è¡¨ç¾ ã¡ã¢ãªã¼ãè¶³ãã¾ãã ç§åãã¾ãã ç´åã®æ­£è¦è¡¨ç¾ããããã¾ãã æ©éããæ­£è¦è¡¨ç¾çµç«¯ å¤§ãéããæ­£è¦è¡¨ç¾ æå å¾ç¶ã®éã¹ã©ãã·ã¥ (ã\(ãé£åãã¾ãã é£ãåããªã)ã\) [ã[^ãé£åãã¾ãã \{ãé£åãã¾ãã ä½¿ç¨æ³: %s [ãªãã·ã§ã³]... {ã¹ã¯ãªãã(ä»ã«ãªããã°)} [å¥åãã¡ã¤ã«]...

 ãeãã³ãã³ãã¯ããµãã¼ãããã¦ãã¾ãã ã}ãã«ã¢ãã¬ã¹ã¯ä¸è¦ã§ã åä½GNU sed %sç

 ã%sãã¸ã®ã¸ã£ã³ãã®ã©ãã«ãè¦ã¤ããã¾ãã %sãåé¤ã§ãã¾ãã: %s %sã®ååãå¤æ´ã§ãã¾ãã: %s ä¿®é£¾å­ã¯ãç©ºã®æ­£è¦è¡¨ç¾ã«æå®ã§ãã¾ãã ã³ãã³ãã¯ã¢ãã¬ã¹ã1ã¤ã ãä½¿ãã¾ã ã³ã¡ã³ãã¯ã¢ãã¬ã¹ãåãä»ãã¾ãã %sã¯ãç·¨éã§ãã¾ããã§ãã: ç«¯æ«ã§ã %sã¯ãç·¨éã§ãã¾ããã§ãã: éå¸¸ãã¡ã¤ã«ã§ããã¾ãã ãã¡ã¤ã«%sãéãã¾ããã§ãã: %s ä¸æãã¡ã¤ã«ãéãã¾ããã§ãã: %s: %s %dåã®ã¢ã¤ãã ã%sã¸æ¸ãè¾¼ãã¾ããã§ãã: %s åºåãæå­ããåä¸ãã¤ãæå­ã§ããã¾ãã å­ãã­ã»ã¹ã®ã¨ã©ã¼ \ããaããcããiãã®å¾ã«äºæããã¾ã sedã®æ°çãåæã§ã ã³ãã³ãã®å¾ãã«ä½è¨ãªæå­ãããã¾ã ãsãã³ãã³ãã®å³å´ã«ç¡å¹ãª\%dã®åç§ æåã®ã¢ãã¬ã¹ã¸ã®+Nã~Nã®æå®ã¯ç¡å¹ã§ã ç¡å¹ãªè¡ã¢ãã¬ã¹0ã®ä½¿ç¨æ³ ã³ãã³ããè¶³ãã¾ãã è¤æ°ã®ã!ãã§ã ãsãã³ãã³ãã«è¤æ°ã®ãgããªãã·ã§ã³ ãsãã³ãã³ãã«è¤æ°ã®ãpããªãã·ã§ã³ ãsãã³ãã³ãã«è¤æ°ã®æ°å¤ãªãã·ã§ã³ å¥åãã¡ã¤ã«ãããã¾ãã ç´åã®æ­£è¦è¡¨ç¾ããããã¾ãã ãsãã³ãã³ãã¸ã®æ°å¤ãªãã·ã§ã³ã¯é¶ã§ã¯ããã¾ãã ãeããªãã·ã§ã³ã¯ããµãã¼ãããã¦ãã¾ãã %sã®èª­è¾¼ã¿ã¨ã©ã¼: %s ãyãã³ãã³ãã¸ã®æå­åã®é·ãããéãã¾ã super-sed %sç
 äºæãã¬ã,ãã§ã äºæãã¬ã}ãã§ã æªç¥ã®ã³ãã³ãã§ã: ã%cã ãsãã¸ã®ãªãã·ã§ã³ãæªç¥ã§ã é£ãåããªãã{ãã§ã ãsãã³ãã³ããçµäºãã¦ãã¾ãã ãyãã³ãã³ããçµäºãã¦ãã¾ãã ã¢ãã¬ã¹regexãçµäºãã¦ãã¾ãã 