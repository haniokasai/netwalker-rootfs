Þ            )         °  ¸  ±     j     }               ¦     µ  X  Ì  ³   %	     Ù	  2   í	  Ü   
  å   ý     ã     ö                    ´  ,   Ä  §   ñ  ±        K     g  ì  w  Í   d     2     ¹  *  Æ  Q   ñ  Å  C     	  1   ª     Ü     ï     ö          %  5  5  ß   k     K  G   ]    ¥  W  ½!  9   #     O#     h#     õ#  8   $     >$  >   Z$  ê   $    %  5   &     Á&    Ú&  F  g(  Ý   ®)     *    ¡*  Z   7,                                                     
                         	                                                          
Most providers send the needed login information per mail. Some providers describe it in odd ways, assuming the user to input the data in their "user-friendly" setup programs. But in fact, these applications generate usuall PPP user names and passwords from the entered data. You can find the real names too and input the correct data in the dialog box.

For example, this are methods used some german providers:

Sample username (alias "login" or "login name"): 11111111111

T-Online T-DSL:
  additional data:
    sample T-Onlinenummer: 222222222222
    sample Mitbenutzer: 0001

  complete username: 111111111111222222222222#0001@t-online.de

Telekom Business Online (DSL):

  complete username: t-online-com/111111111111@t-online-com.de

1und1 uses another scheme (using above example):

  complete username: 1und1/11111111111

Cyberfun:

  complete username: sdt/11111111111

Komtel:
  additional data:
    downstream speed class: 768

  complete username: 11111111111@FoniNet-768

Net Cologne:

  complete username: 11111111111@netcologne.de

Q-DSL:

  complete username: 11111111111@q-dsl.de

Versatel:

  complete username: 11111111111@VersaNet-1024k

Webnetix:

  complete username: sdt/11111111111
 ALL DEVICES FOUND? CONNECTION INITIATED DONE ENTER PASSWORD ENTER USERNAME ESTABLISH A CONNECTION I found $number ethernet device:
$list

Are all your ethernet interfaces listed above?
(If No, modconf will be started so you can load the card drivers manually).

$escmsg I found $number ethernet devices:
$list

Are all your ethernet interfaces listed above?
(If No, modconf will be started so you can load the card drivers manually).

$escmsg If you continue with this program, the configuration file $OPTSFILE will be modified. Please make sure that you have a backup copy before saying Yes.

Continue with configuration? LIMITED MSS PROBLEM Looking for PPPoE Access Concentrator on $iface... Many providers have routers that do not support TCP packets with a MSS higher than 1460. Usually, outgoing packets have this MSS when they go through one real Ethernet link with the default MTU size (1500). Unfortunately, if you are forwarding packets from other hosts (i.e. doing masquerading) the MSS may be increased depending on the packet size and the route to the client hosts, so your client machines won't be able to connect to some sites. There is a solution: the maximum MSS can be limited by pppoe. You can find more details about this issue in the pppoe documentation.

Should pppoe clamp MSS at 1452 bytes?

If unsure, say yes.

(If you still get problems described above, try setting to 1412 in the dsl-provider file.) Most people using popular dialup providers prefer the options 'noauth' and 'defaultroute' in their configuration and remove the 'nodetach' option. Should I check your configuration file and change these settings where neccessary? NO INTERFACE FOUND NOT CONNECTED Now, you can make a DSL connection with "pon dsl-provider" and terminate it with "poff". Would you like to start the connection now? OKAY TO MODIFY Or press ESC to abort here. POPULAR OPTIONS Please become root before running pppoeconf! Please enter the password which you usually need for the PPP login to your provider in the input box below.

NOTE: you can see the password in plain text while typing. Please enter the username which you usually need for the PPP login to your provider in the input box below. If you wish to see the help screen, delete the username and press OK. Press return to continue... SCANNING DEVICE Sorry, I scanned $number interface, but the Access Concentrator of your provider did not respond. Please check your network and modem cables. Another reason for the scan failure may also be another running pppoe process which controls the modem. Sorry, I scanned $number interfaces, but the Access Concentrator of your provider did not respond. Please check your network and modem cables. Another reason for the scan failure may also be another running pppoe process which controls the modem. Sorry, no working ethernet card could be found. If you do have an interface card which was not autodetected so far, you probably wish to load the driver manually using the modconf utility. Run modconf now? The DSL connection has been triggered. You can use the "plog" command to see the status or "ifconfig ppp0" for general interface info. USE PEER DNS You need at least one DNS IP address to resolve the normal host names. Normally your provider sends you addresses of useable servers when the connection is established. Would you like to add these addresses automatically to the list of nameservers in your local /etc/resolv.conf file? (recommended) Your PPPD is configured now. Would you like to start the connection at boot time? Project-Id-Version: pppoeconf
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2008-07-27 03:07+0200
PO-Revision-Date: 2008-09-02 12:11+0000
Last-Translator: Kenshi Muto <kmuto@debian.org>
Language-Team: Japanese <debian-japanese@lists.debian.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Launchpad-Export-Date: 2009-04-14 14:14+0000
X-Generator: Launchpad (build Unknown)
 
ã»ã¨ãã©ã®ãã­ãã¤ãã¯å¿è¦ã¨ãªãã­ã°ã¤ã³æå ±ãã¡ã¼ã«ã§éã£ã¦ãã¾ããããã¤ãã®ãã­ãã¤ãã¯ "ã¦ã¼ã¶ãã¬ã³ããª" ãªã»ããã¢ãããã­ã°ã©ã ã§ãã¼ã¿ãå¥åãããã¨ãä»®å®ãããé¢¨å¤ãããªæ¹æ³ã§æ¸ãã¦ãããã¨ãããã¾ããããããå®éã®ã¨ããããããã®ã¢ããªã±ã¼ã·ã§ã³ã¯ãå¥åããããã¼ã¿ããéå¸¸ã® PPP ã¦ã¼ã¶ã¼åã¨ãã¹ã¯ã¼ããçæããã ãã§ããããã§å®éã®ååãè¦ã¤ãã¦ãæ­£ãããã¼ã¿ããã¤ã¢ã­ã°ããã¯ã¹ã«å¥åãã¾ãã

ãã¨ãã°ãæ¬¡ã®ãã®ã¯ããã¤ãã®æ¥æ¬ã®ãã­ãã¤ãã§ä½¿ããã¦ããæ¹æ³ã§ã:

ãµã³ãã«ã¦ã¼ã¶å (å¥å "ã­ã°ã¤ã³" ã¾ãã¯ "ã­ã°ã¤ã³å"): 11111111111

NTTãã¬ãã
  å®å¨ãªã¦ã¼ã¶å: 11111111111@flets
Infosphere
  å®å¨ãªã¦ã¼ã¶å: 11111111111@zz.sphere.ne.jp
 ãã¹ã¦ã®ããã¤ã¹ãè¦ã¤ãã¾ããã? æ¥ç¶ã®åæå å®äº ãã¹ã¯ã¼ãã®å¥å ã¦ã¼ã¶åã®å¥å æ¥ç¶ã®ç¢ºç« $number åã®ã¤ã¼ãµãããããã¤ã¹ãçºè¦ãã¾ãã:
$list

ä¸è¨ã®ä¸­ã«ããªãã®ã¤ã¼ãµãããã¤ã³ã¿ã¼ãã§ã¤ã¹ãã¹ã¦ããªã¹ãããã¦ãã¾ãã?
(ããããããé¸ã¶ã¨ãæåã§ã«ã¼ããã©ã¤ããã­ã¼ããããã modconf ãèµ·åãã¾ã)

$escmsg ãã®ãã­ã°ã©ã ãç¶ããã¨ãè¨­å®ãã¡ã¤ã« $OPTSFILE ã¯å¤æ´ããã¾ãããã¯ããã¨ç­ããåã«ãããã¯ã¢ããã³ãã¼ããããã¨ãç¢ºèªãã¦ãã ããã
è¨­å®ãç¶ãã¾ãã? å¶é MSS åé¡ $iface ã§ã® PPPoE ã¢ã¯ã»ã¹ã³ã³ã»ã³ãã¬ã¼ã¿ã®æ¤ç´¢ä¸­... ã»ã¨ãã©ã®ãã­ãã¤ãã¯ 1460 ä»¥ä¸ã® MSS ã® IP ãã±ããããµãã¼ãããªãã«ã¼ã¿ãæã£ã¦ãã¾ããéå¸¸ããã®ãã·ã³ããå¤ã¸ã®ãã±ããã¯ãããã©ã«ãã® MTU ãµã¤ãº (1500) ã§å®ã¤ã¼ãµããããªã³ã¯ãéãã¾ããä¸éãªãã¨ã«ãããå¥ã®ãã¹ãããã®ãã±ãããè»¢é (ãã¹ã«ã¬ã¼ãã£ã³ã°ãªã©) ãã¦ããå ´åãMSS ã¯ãã±ããã®å¤§ããã¨ã¯ã©ã¤ã¢ã³ããã¹ãã¸ã®çµè·¯ã«å¿ãã¦å¢å ããããã¨ã«ãªãã¾ãããã®ãããããªãã®ã¯ã©ã¤ã¢ã³ããã·ã³ã¯ããã¤ãã®ãµã¤ãã«æ¥ç¶ã§ãã¾ãããè§£æ±ºæ¹æ³ã¯ããã¾ã: æå¤§ MSS ã pppoe ã§å¶éã§ãã¾ãããã®åé¡ã®è©³ç´°ã«ã¤ãã¦ã¯ pppoe ã®ãã­ã¥ã¡ã³ãã§åç§ã§ãã¾ãã

pppoe ã§ MSS ã 1452 ãã¤ãã«å¶éãã¾ãã?

ç¢ºä¿¡ããªããã°ãã¯ããã¨ç­ãã¦ãã ããã

(ä¸è¨ã®åé¡ãã¾ã åºãããã§ããã°ãdsl-provider ãã¡ã¤ã«ã® 1412 ã®è¨­å®ãè©¦ãã¦ã¿ã¦ãã ãã) ä¸è¬çãªãã¤ã¤ã«ã¢ãããã­ãã¤ããä½¿ã£ã¦ããã»ã¨ãã©ã®äººã¯ã'noauth' ãªãã·ã§ã³ã¨ 'defaultroute' ãªãã·ã§ã³ãè¨­å®ã«é¸ã³ã'nodetach' ãªãã·ã§ã³ãåé¤ããã®ãããã§ããããããªãã®è¨­å®ãã¡ã¤ã«ãç¢ºèªãã¦ããããã®è¨­å®ãå¿è¦ã«å¿ãã¦å¤æ´ãã¾ãã? ã¤ã³ã¿ã¼ãã§ã¤ã¹ãè¦ã¤ããã¾ããã§ãã æ¥ç¶ãããã¾ãã ããã§ã"pon dsl-provider" ã§ DSL æ¥ç¶ãè¡ãã"poff" ã§åæ­ã§ããããã«ãªãã¾ãããä»æ¥ç¶ãéå§ãã¾ãã? å¤æ´ã®ç¢ºèª ã¾ãã¯ããã§ ESC ãæ¼ãã¦ä¸­æ­¢ã§ãã¾ãã ä¸è¬çãªãªãã·ã§ã³ pppoeconf ãå®è¡ããåã« root ã«ãªã£ã¦ãã ãã! ä»¥ä¸ã®å¥åããã¯ã¹ã«ãããªãã®ãã­ãã¤ãã¸ã® PPP ã­ã°ã¤ã³ã«éå¸¸å¿è¦ã¨ãªããã¹ã¯ã¼ããå¥åãã¦ãã ããã

æ³¨æ: ãã¹ã¯ã¼ãã¯å¥åä¸­ã«ãã¬ã¤ã³ãã­ã¹ãã§è¦ãã¾ãã ä»¥ä¸ã®å¥åããã¯ã¹ã«ãããªãã®ãã­ãã¤ãã¸ã® PPP ã­ã°ã¤ã³ã«éå¸¸å¿è¦ã¨ãªãã¦ã¼ã¶åãå¥åãã¦ãã ããããããã«ãç»é¢ãè¦ããã®ã§ããã°ãã¦ã¼ã¶åãåé¤ãã¦ãOKããæ¼ãã¦ãã ããã ç¶ããããã« Return ãæ¼ãã¦ãã ãã... ããã¤ã¹ãæ¤æ»ä¸­ $number åã®ã¤ã³ã¿ã¼ãã§ã¤ã¹ãæ¤æ»ãã¾ããããããªãã®ãã­ãã¤ãã®ã¢ã¯ã»ã¹ã³ã³ã»ã³ãã¬ã¼ã¿ããã®åå¿ãããã¾ããã§ããããããã¯ã¼ã¯ã¨ã¢ãã ã±ã¼ãã«ãç¢ºèªãã¦ãã ãããæ¤æ»ã®å¤±æã®å¥ãªçç±ã¨ãã¦ã¯ãã¢ãã ãå¶å¾¡ããå¥ã® pppoe ãã­ã»ã¹ãå®è¡ä¸­ã§ããã¨ãããã¨ãããã¾ãã ç¨¼åãã¦ããã¤ã¼ãµãããã«ã¼ããè¦ã¤ããã¾ããã§ãããèªåæ¤åºã§ããªãã¤ã³ã¿ã¼ãã§ã¤ã¹ã«ã¼ããæã£ã¦ããã®ã§ããã°ãmodconf ã¦ã¼ãã£ãªãã£ãä½¿ã£ã¦ãããããã©ã¤ããæåã§ã­ã¼ããããã¨æãã§ããããmodconf ãä»å®è¡ãã¾ãã? DSL æ¥ç¶ãå¼ãèµ·ãããã¾ãããç¶æ³ãè¦ãã®ã« "plog" ã³ãã³ããä½¿ã£ãããä¸è¬çãªã¤ã³ã¿ã¼ãã§ã¤ã¹æå ±ãè¦ãã®ã« "ifconfig ppp0" ãä½¿ã£ãããããã¨ãã§ãã¾ãã ãã¢ DNS ã®å©ç¨ éå¸¸ã®ãã¹ãåãè§£æ±ºããããã«ã¯ãå°ãªãã¨ã 1 ã¤ã® DNS IP ã¢ãã¬ã¹ãå¿è¦ã§ããéå¸¸ãããªãã®ãã­ãã¤ãã¯ãæ¥ç¶ç¢ºç«æã«å©ç¨å¯è½ãªãµã¼ãã®ã¢ãã¬ã¹ãéã£ã¦ãã¦ããã¯ãã§ãããããã®ã¢ãã¬ã¹ãèªåçã«ã­ã¼ã«ã« /etc/resolv.conf ãã¡ã¤ã«ã®ãã¼ã ãµã¼ãã®ãªã¹ãã«è¿½å ãã¾ãã? (æ¨å¥¨ãã¾ã) PPPD ãè¨­å®ããã¾ããããã¼ãæã«æ¥ç¶ãéå§ããããã«ãã¾ãã? 