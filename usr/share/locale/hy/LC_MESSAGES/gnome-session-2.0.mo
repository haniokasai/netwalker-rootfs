��    h      \  �   �      �  K   �     	     5	  "   U	     x	     	     �	     �	     �	     �	  $   �	  !   
     ?
  &   N
     u
     }
  (   �
  �   �
     j     z     �      �     �     �    �  G      �   H     �     �     �     �            ?   3  D   s  C   �     �               :  6   A     x  .   ~     �  6   �     �  "   �               -     4     L  %   c     �     �     �     �     �     �  
   �     �       1   %  3   W     �  '   �     �     �     �     �  "        %  	   +  -   5  $   c  ;   �  +   �     �        #   1  �   U  &   �  �     �   �     p  	   v  "   �     �     �     �  %   �  .        1  ,   @     m     �     �     �     �     �  
   �     �     �  ^  �  �   N  =   �  $   '  8   L     �  4   �  $   �  7   �  /   2  h   b  K   �  ^     ,   v  e   �     	  K     >   d  +  �     �  3   �  B   #  a   f  4   �  *   �  C  (  �   l!     "     ##  >   3#     r#  ;   �#  9   �#  2   $  �   ;$  �   �$  �   ~%     "&  5   7&  -   m&     �&  r   �&     '  �   $'     �'  R   �'     (  \   3(     �(  #   �(     �(  0   �(  )   )  Y   1)  0   �)     �)  #   �)  4   �)  &   -*     T*     q*  O   �*  /   �*  V   +  e   X+  >   �+  N   �+     L,  #   a,  #   �,     �,  g   �,     &-     B-  \   S-  (   �-  e   �-  \   ?.  B   �.  A   �.  M   !/    o/  >   �0  �  �0  =  U2  
   �3     �3  i   �3     4  2   +4  e   ^4  L   �4  `   5  !   r5  g   �5  )   �5     &6  '   86  	   `6  2   j6  7   �6  5   �6  $   7     07     %   R   (       S   A       )       7               ]       ^   f   =   [   '   a      ?   \      9   -          *   U   _      8   e   I             @   F      b               +   $   K   O   Q   d             M   ;       ,         1       W   !       g           C           h   
   L   <                 D      #               `      Y   .   T         6          &   E       4                  "       P                            3   >   X   2           /   V       	   c   J   H   B   :          0      Z   G   N   5    

GNOME will still try to restart the Settings Daemon next time you log in. 

The last error message was:

 A normal member of the session. A session shutdown is in progress. Action Add Startup Program Add a new session Additional startup _programs: Allow TCP connections Always started on every login. Apply changes to the current session Are you sure you want to log out? As_k on logout Automatically save chan_ges to session Command Configure your sessions Could not connect to the session manager Could not look up internet address for %s.
This will prevent GNOME from operating correctly.
It may be possible to correct the problem by adding
%s to the file /etc/hosts. Current Session Currently running _programs: Desktop Settings Discarded on logout and can die. Edit Startup Program Edit session name For security reasons, on platforms which have _IceTcpTransNoListen() (XFree86 systems), gnome-session does not listen for connections on TCP ports. This option will allow connections from (authorized) remote hosts. gnome-session must be restarted for this to take effect. If enabled, gnome-session will prompt the user before ending a session. If enabled, gnome-session will save the session automatically. Otherwise, the logout dialog will have an option to save the session. Inactive Initialize session settings Kill session Log in Anyway Logout prompt Metacity Window Manager Millisecond period spent waiting for clients to die (0=forever) Millisecond period spent waiting for clients to register (0=forever) Millisecond period spent waiting for clients to respond (0=forever) Nautilus Never allowed to die. No response to the %s command. Normal Only read saved sessions from the default.session file Order Preferred Image to use for login splash screen Program Remove the currently selected client from the session. Restart Restart abandoned due to failures. Running Save sessions Saving Saving session details. Sawfish Window Manager Selected option in the log out dialog Session Manager Proxy Session Name Session Options Sessions Set the current session Settings Sh_ut down Show splash screen on _login Show the splash screen Show the splash screen when the session starts up Some changes are not saved.
Is it still OK to exit? Specify a session name to load Started but has not yet reported state. Starting Startup Command Startup Programs State State not reported within timeout. Style The Panel The Settings Daemon restarted too many times. The list of programs in the session. The order in which applications are started in the session. The program may be slow, stopped or broken. The session name already exists The session name cannot be empty The startup command cannot be empty There was an error starting the GNOME Settings Daemon.

Some things, such as themes, sounds, or background settings may not work correctly. There was an unknown activation error. This is a relative path value based off the $datadir/pixmaps/ directory. Sub-directories and image names are valid values. Changing this value will effect the next session login. This is the option that will be selected in the logout dialog, valid values are "logout" for logging out, "shutdown" for halting the system and "restart" for restarting the system. Trash Try Again Unaffected by logouts but can die. Unknown Use dialog boxes Wait abandoned due to conflict. Waiting to start or already finished. What happens to the application when it exits. Window Manager You may wait for it to respond or remove it. Your session has been saved _Edit _Log out _Order: _Restart the computer _Save current setup _Sessions: _Startup Command: _Style: Project-Id-Version: gnome-session.HEAD.hy
Report-Msgid-Bugs-To: norik@freenet.am
POT-Creation-Date: 2005-07-19 06:26+0000
PO-Revision-Date: 2005-08-25 13:59+0500
Last-Translator: Norayr Chilingaryan
Language-Team:  <norik@freenet.am>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: KBabel 1.9.1
 

Գնոմը միշտ կփորձի վերագործարկել Settings Daemon –ը, երբ հաջորդ անգամ դուք համակարգ մտնեք։ 

Վերջին սխալ հաղորդագրությունը:

 Սեանսի նորմալ անդամ Սեանսի անջատումը ընթացքի մեջ է Գործողություն Ավելացնել գործարկման ծրագիր Ավելացնել նոր սեանս Լրացուցիչ գործարկման -ծրագրեր Թույլատրել TCP միացումները Միշտ գործարկվում է յուրաքանչյուր անգամ համակարգ մտնելիս Կիրառել ընթացիկ սեանսի փոփոխությունները Համոզվա՞ծ եք, որ ցանկանում եք դուրս գալ համակարգից։ Սեանսի ավարտի հաստատում Ավտոմատ կերպով կատարել սեանսի փոփոխությունների պահում Հրահանգ Ձեր սեանսի կոնֆիգուրացիաները կարգավորել Անկարող է միանալ սեանսի մենեջերին Անկարող է փնտրել ինտերնետային հասցեն %s.
Դա կարող է Գնոմին հետ պահել ճիշտ շահագործումից 
Հնարավոր է, որ սխալը ուղղվի ավելացնելով 
%s ֆայլին /և այլն /գլխավոր հանգույցին Ընթացիկ սեանսներ Ընթացիկ գործարկվող _ծրագրեր Աշխատանքային էկրանի կարգադրվածքներ Համակարգից դուրս գալուց հրաժարում և կարող է ոչնչանալ Խմբագրել գործարկման ծրագիրը Խմբագրել սեանսի անունը Անվտանգության ապահովումից ելնելով, սարքահամալիրների վրա, որոնք ունեն _IcqTCPTransNoListen() (XFree86 համակարգեր), գնոմ–ենթահամակարգը չի կատարում TCP  պորտերի միացումները։ Այս տարբերակը թույլ է տալիս միացումների իրականացում (իրավասու) հեռավոր հանգույցներից։ Գնոմ ենթահամակարգը պետք է վերագործարկել այս արդյունքը ստանալու համար։ Միացնելու դեպքում գնոմ–ենթահամակարգը գործարկողին հուշում է սեանսի ավարտի մասին Միացնելու դեպքում գնոմ ենթահամակարգը սեանսը ավտոմատ կերպով պահում է, հակառակ դեպքում համակարգից դուրս գալու դիալոգը ներկայացնում է սեանսը պահելու տարբերակ Ոչ ակտիվ Գործարկել սեանսի կարգադրվածքները Սեանսը ոչնչացնել Միանալ համակարգին ցանկացած կերպ Համակարգից դուրս գալու հուշում Մետասիթի պատուհանի մենեջեր Միլիվայրկյանների ժամանակահատված, որն անցել է հաճախորդների ոչնչացմանը  սպասելով (0=հավերժ) Միլիվայրկյանների ժամանակահատված, որն անցել է հաճախորդների գրանցման ժամանակ (0=հավերժ) Միլիվայրկյանների ժամանակահատված, որն անցել է հաճախորդների արձագանքին սպասելով (0=հավերժ) Նաուտիլուս Երբեք չի թույլատրվի ոչնչանալ Պատասխան չկա %s հրահանգին Նորմալ Միայն կարդալ պահպանված սեանսները դեֆոլտ ենթահամակարգի ֆայլից Կարգ Նախընտրելի տարբերակ, որպես համակարգ մտնելու առկայծող էկրան օգտագործելու համար Ծրագիր Ընթացիկ ընտրված հաճախորդին սեանսից հեռացնել Վերագործարկում Վերագործարկումը դադարեցվում է սխալների պատճառով։ Գործարկում Պահպանել սեանսները Պահում Պահել սեանսի մանրամասները Sawfish պատուհանի մենեջեր Համակարգից դուրս գալու դիալոգի Ընտրված տարբերակ Սեանսի մենեջերի տվյալները Սեանսի անուն Սեանսի տարբերակներ Սեանսներ կամ ենթահամակարգեր Սկսել ընթացիկ սեանսը Կարգադրվածքներ _Անջատել Համակարգ մտնելից ցույց տալ առկայծող էկրանը Ցույց տալ առկայծող էկրանը Ցույց տալ առկայծող էկրանը, երբ սեանսը սկսվում է Որոշ փոփոխություններ չեն պահվել 
Համաձա՞յն եք հեռանալ։ Նշել սեանսի անունը բեռնելու համար Գործարկվել է, սակայն կարգավիճակը չի ֆիքսել Գործարկում Գործարկման հրահանգ Գործարկման ծրագրեր Կարգավիճակ Կարգավիճակ, որը ժամանակը սպառվելու ընթացքում չի ֆիքսվել Տեսքի ատրիբուտ Վահանակը Settings Daemon–ը վերագործարկվեց բավականին շատ անգամներ Սեանսի ծրագրերի ցանկը Կարգը, որով կիրառական ծրագրերը գործարկվում են սեանսում Ծրագիրը կարող է դանդաղ, կասեցված կամ կոտրված լինել Սեանսի անունը արդեն գոյություն ունի Սեանսի անունը դատարկ լինել չի կարող Գործարկման հրահանգը չի կարող դատարկ լինել GNOME Settings Daemon–ի գործարկման ժամանակ սխալ է կատարվել.

Այնպիսի բաներ, ինչպիսիք են թեմաները, ձայները կամ հետին պլանի կարգադրվածքները կարող են ճիշտ չաշխատել։ Կատարվել է ակտիվացման անհայտ սխալ Սա հարաբերական ուղու արժեք է՝ հիմնված $datadir/pixmaps/, տվյալների կատալոգից դուրս։ Ենթա–կատալոգները և պատկերների անունները համապատասխան արժեքներ են։ Այս արժեքները փոփոխելը կներգործի հաջորդ սեանսի համար համակարգ մտնելիս։ Սա այն տարբերակն է, որը պետք է ընտրել համակարգից դուրս գալու դիալոգում, համապատասխան արժեքներն են "logout" for logging out, "shutdown" for halting the system and "restart" , համակարգը վերագործարկելու համար։ Թափոն Կրին փորձել Համակարգից դուրս գալիս չի վնասվե, սակայն կարող է ոչնչանալ Անհայտ Օգտագործել դիալոգի արկղերը Սպասումը դադարեցված է կոնֆլիկտի առկայության պատճառով։ Սպասում է գործարկմանը կամ արդեն ավարտել է Ինչ է պատահում կիրառական ծրագրերին, երբ հեռանում են։ Պատուհանի մենեջեր Դուք կարող եք սպասել, որ այն արձագանքի, կամ հեռացնել այն։ Ձեր սեանսը պահպանվել է _Խմբագրել _Համակարգից դուրս գալ _կարգ _Համակարգիչը վերագործարկել _Պահպանել ընթացիկ պարամետրերը _Սեանսներ կամ ենթահամակարգեր _Գործարկման հրահանգ _Տեսքի ատրիբուտ 