��    k      t  �   �       	  K   !	     m	     �	     �	     �	  "   �	     
     
     !
     3
     Q
     g
  $   �
  !   �
     �
  &   �
            (   #  �   L     �          %     +     <      D     e     z     �    �  G   �  �   �     p     y     �     �     �  ?   �  D   �  C   ?     �     �     �     �     �  6   �       .   
     9  6   A     x  "   �     �     �     �     �     �  %   �          "     2     ;     X  
   a     l     �  1   �  3   �       '   %     M     V     f     w  "   }     �  	   �  -   �  $   �  ;     +   ?     k      �  #   �  �   �  �   \  �        �  	   �  "   �     �     �       %   0  .   V     �  ,   �     �     �     �     �     �     
  
        )     ;  _  C  �   �  D   s  =   �  G   �  F   >  Q   �  	   �  _   �  0   A  i   r  E   �  G   "  d   j  f   �  G   6  �   ~        ?     k   S  f  �  "   &   V   I      �   (   �      �   v   �   n   i!  B   �!     "  v  ."  �   �$  G  a%     �&  &   �&  '   �&  &   '  G   9'  �   �'  �   2(  �   �(  	   �)     �)  7   �)  U   �)     I*  v   \*     �*  v   �*     W+  �   s+     
,  m   *,     �,  ;   �,  %   �,  a   -  E   i-  O   �-     �-  ,   .     I.  O   c.     �.      �.  c   �.  >   K/  d   �/  �   �/  Z   �0  o   �0     P1  ?   m1  K   �1     �1  o   2  	   |2     �2  �   �2  D   13  �   v3  �   �3  i   �4  J   5  j   W5  \  �5  �  7  �  �8     p:  ,   �:  j   �:     ;  E   1;  k   w;  l   �;  f   P<  .   �<  �   �<  L   �=     �=      >     >  O   ,>  R   |>  !   �>  G   �>     9?            E   M          T          I   h   N   =              a   c       
   j                  :   Z   8   ?   !       A       b   )       L   K   2      e   H   C   g   P         /      i               k   .      _   <       B   U   7              \                           *      O      3          4   (      "          F       R       +       #         -       @   `                     S   	           d       V   $   '   9       ^              Y       D   >   &       ,           1   [       6   J      X   ;      ]      %   W   5   Q   G       f   0        

GNOME will still try to restart the Settings Daemon next time you log in. 

The last error message was:

 - Manage the GNOME session - Save the current session A normal member of the session. A session shutdown is in progress. Action Add Startup Program Add a new session Additional startup _programs: Allow TCP connections Always started on every login. Apply changes to the current session Are you sure you want to log out? As_k on logout Automatically save chan_ges to session Command Configure your sessions Could not connect to the session manager Could not look up internet address for %s.
This will prevent GNOME from operating correctly.
It may be possible to correct the problem by adding
%s to the file /etc/hosts. Current Session Currently running _programs: DELAY Desktop Settings Disable Discarded on logout and can die. Edit Startup Program Edit session name Enable For security reasons, on platforms which have _IceTcpTransNoListen() (XFree86 systems), gnome-session does not listen for connections on TCP ports. This option will allow connections from (authorized) remote hosts. gnome-session must be restarted for this to take effect. If enabled, gnome-session will prompt the user before ending a session. If enabled, gnome-session will save the session automatically. Otherwise, the logout dialog will have an option to save the session. Inactive Kill session Log in Anyway Logout prompt Metacity Window Manager Millisecond period spent waiting for clients to die (0=forever) Millisecond period spent waiting for clients to register (0=forever) Millisecond period spent waiting for clients to respond (0=forever) NAME Nautilus Never allowed to die. No response to the %s command. Normal Only read saved sessions from the default.session file Order Preferred Image to use for login splash screen Program Remove the currently selected client from the session. Restart Restart abandoned due to failures. Running Save sessions Saving Saving session details. Sawfish Window Manager Selected option in the log out dialog Session Name Session Options Sessions Set the current session name Settings Sh_ut down Show splash screen on _login Show the splash screen Show the splash screen when the session starts up Some changes are not saved.
Is it still OK to exit? Specify a session name to load Started but has not yet reported state. Starting Startup Command Startup Programs State State not reported within timeout. Style The Panel The Settings Daemon restarted too many times. The list of programs in the session. The order in which applications are started in the session. The program may be slow, stopped or broken. The session name already exists The session name cannot be empty The startup command cannot be empty There was an error starting the GNOME Settings Daemon.

Some things, such as themes, sounds, or background settings may not work correctly. This is a relative path value based off the $datadir/pixmaps/ directory. Sub-directories and image names are valid values. Changing this value will effect the next session login. This is the option that will be selected in the logout dialog, valid values are "logout" for logging out, "shutdown" for halting the system and "restart" for restarting the system. Trash Try Again Unaffected by logouts but can die. Unknown Use dialog boxes Wait abandoned due to conflict. Waiting to start or already finished. What happens to the application when it exits. Window Manager You may wait for it to respond or remove it. Your session has been saved _Edit _Log out _Order: _Restart the computer _Save current setup _Sessions: _Startup Command: _Style: Project-Id-Version: gnome-session
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2006-08-07 16:17+0200
PO-Revision-Date: 2006-08-08 01:29+0600
Last-Translator: Khandakar Mujahidul Islam <suzan@bengalinux.org>
Language-Team: Bangla <gnome-translation@bengalinux.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 

আপনি যখন পরের বার লগ-ইন করবেন তখনও গ‌নোম সেটিংস ডিমন(Daemon) চালু করার চেষ্টা করবে। 

শেষ ত্রুটি বার্তাটি ছিল:

 - গনোম সেশন ব্যবস্থাপনা - বর্তমান সেশন কার্যকর করুন সেশনের এক জন সাধারণ সদস্য। সেশন বন্ধ হওয়ার প্রক্রিয়াধীন। কাজ প্রথমে চালু করার প্রোগ্রাম যোগ করুন নতুন সেশন যোগ করুন প্রথমে চালু হওয়ার সংযোজিত প্রোগ্রাম (_গ): টিসিপি সংযোগ অনুমোদন করুন প্রতি বার লগ-ইনের সময় চালু। বর্তমান সেশনের পরিবর্তন কার্যকর করুন আপনি কি নিশ্চিত যে আপনি লগ-আউট করতে চান? লগ-আউটের সময় জিজ্ঞাসা কর (_স) স্বয়ংক্রিয় সেশনের পরিবর্তন সমূহ সংরক্ষন করুন (_র) কমান্ড আপনার সেশন কনফিগার করুন সেশন ম্যানেজারের সাথে যোগাযোগ করা যায়নি %s এর জন্য ইন্টারনেট ঠিকানা খুঁজে পওয়া যায়নি।
এটি গ‌নোমকে ঠিকমত চলতে দেবে না।
%s কে /etc/hosts ফাইলের মধ্যে যোগ করে এই সমস্যাটি হয়তো ঠিক
করা যাবে। বর্তমান সেশন বর্তমানে যেসব প্রোগ্রাম চলছে (_ম): দেরী ডেস্কটপ সেটিংস নিষ্ক্রিয় লগ-আউটের সময় প্রত্যাখ্যাত হবে এবং ধ্বংস হবে। প্রথমে চালু করার প্রোগ্রাম পরিবর্তন করুন সেশনের নাম পরিবর্তন করুন সক্রিয় নিরাপত্তাজনিত কারনে, যেসব প্লাটফর্মের _IceTcpTransNoListen() (XFree86 systems) আছে সেখানে gnome-session টিসিপি পোর্টে সংযোগের জন্য অপেক্ষা করে না। এই অপশন (অনুমোদিত) দূরবর্তী হোস্টের কাছ থেকে সংযোগের অনুমতি দেবে। এই কাজের ফলাফল পেতে হলে gnome-session অবশ্যই পুনরায় চালু করে হবে।  যদি কার্যকর করা হয়, সেশন শেষ করার আগে gnome-session ব্যবহারকারীকে জিজ্ঞেস করবে। যদি কার্যকর করা হয়, gnome-session স্বয়ংক্রিয় ভাবে সেশন সংরক্ষণ করবে। তা না হলে লগ-আউট ডায়ালগে সেশন সংরক্ষণ করার জন্য একটি অপশন থাকবে। সক্রিয় নয় সেশন বন্ধ করুন তবুও লগ-ইন করুন লগ-আউট প্রম্পট মেটাসিটি উইন্ডো ম্যানেজার ক্লায়েন্টটি শেষ হওয়ার জন্য মিলিসেকেন্ড সময় অপেক্ষা করা হয়েছে (0=forever) ক্লায়েন্টটি রেজিস্টার হওয়ার জন্য মিলিসেকেন্ড সময় অপেক্ষা করেছে (0=forever) ক্লায়েন্টটির জবাবের জন্য মিলিসেকেন্ড সময় অপেক্ষা করা হয়েছে (0=forever) নাম নটিল্যাস কখনো শেষ হতে দিবে না। %s কমান্ডের কোন জবাব পাওয়া যায়নি। সাধারণ default.session ফাইল থেকে শুধু সংরক্ষিত সেশন সমূহ পড়ুন ধারা লগ-ইনের প্রাথমিক স্ক্রীনে যে ছবিটি দেখতে চান প্রোগ্রাম বর্তমানে উল্লেখিত ক্লায়েন্টটিকে সেশন থেকে সরিয়ে ফেলুন। পুনরায় চালু কিছু ভুলের জন্য পুনরায় শুরু করা হচ্ছে না। চলছে সেশনসমূহ সংরক্ষণ করুন সংরক্ষণ হচ্ছে সেশনের বিস্তারিত সংরক্ষণ করা হচ্ছে। স্যা-ফিস উইন্ডো ম্যানেজার লগ আউট ডায়ালগে নির্বাচিত অপশন সেশনের নাম সেশনের অপশন সমুহ সেশন সমূহ বর্তমান সেশন নাম কার্যকর করুন সেটিংস বন্ধ করুন (_ব) লগ-ইনের সময় প্রাথমিক স্ক্রীন দেখাও (_ল) প্রাথমিক স্ক্রিন দেখাও সেশনের শুরুতে প্রাথমিক স্ক্রিন দেখাও কিছু কিছু পরিবর্তন সংরক্ষিত নয়।
তবুও কি বের হওয়া ঠিক আছে? চালু করার জন্য একটি সেশনের নাম দিন শুরু করা হয়েছে কিন্তু অবস্থা জানানো হয়নি। শুরু হচ্ছে প্রথমে চালু করার কমান্ড প্রথমে চালু হওয়ার প্রোগ্রাম অবস্থা নির্ধারিত সময় এর মধ্যে অবস্থা জানান হয়নি। ধরণ প্যানেল মানসমূহের ডিমন অতিরিক্ত অনেকবার পুনরায় চালু করা হয়েছে। সেশনের প্রোগ্রাম তালিকা। যেই ধারা অনুযায়ী সেশনে অ্যাপ্লিকেশন চালু হয়েছে। প্রোগ্রামটি হয়তো ধীরে চলছে, বন্ধ হয়ে গিয়েছে অথবা ভেঙ্গে গিয়েছে। এই সেশন নামটি ইতিমধ্যেই অন্য একটি রয়েছে সেশন নাম খালি থাকতে পারবে না প্রথমে চালু করার কমান্ড খালি হতে পারে না গ‌নোম বৈশিষ্ট্যের ডিমন(Daemon) চালু করার সময় একটি ভুল হয়েছে।

কিছু জিনিস, যেমন থিম, শব্দ, অথবা পটভূমির মানসমূহ সঠিকভাবে কাজ নাও করতে পারে। $datadir/pixmaps/ ডিরেক্টরির সাপেক্ষে এটি একটি আপেক্ষিক পাথ মান। সাব-ডিরেক্টরিসমূহএবং ছবির নামসমূহ সঠিক মান। এই মান পরিবর্তন করলে পরবর্তী সেশন লগিনে প্রভাব ফেলবে। এটি হচ্ছে সেই অপশন যেটি লগ আউট ডায়ালগে নির্বাচিত হবে, সঠিক মানগুলো হচ্ছে লগ আউটের জন্য "লগ আউট", সিস্টেম বন্ধের জন্য "বন্ধ" এবং সিস্টেম পুনরায় চালু করতে "পুনরায় চালু করো"। আবর্জনা আবার চেষ্টা করুন লগ-আউটে প্রভাবিত না হলেও ধ্বংস হতে পারে। অজ্ঞাত ডায়ালগ বাক্স ব্যবহার করুন গোলযোগের কারণে অপেক্ষা করা বাতিল হয়েছে। শুরু হওয়ার অপেক্ষায় অথবা শেষ হয়ে গিয়েছে। অ্যাপ্লিকেশনটির কি হয় যখন সেটি শেষ হয়। উইন্ডো ম্যানেজার আপনি এটির জবাবের অপেক্ষা করতে পারেন অথবা পুনরায় চালু করতে পারেন। আপনার সেশন সংরক্ষণ করা হয়েছে সম্পাদনা (_প) লগআউট (_ল) ধারা (_ধ): কম্পিউটার পুনরায় চালু করুন (_চ) বর্তমান অবস্থা সংরক্ষণ করুন (_স) সেশন সমূহ (_শ): প্রথমে শুরু করার কমান্ড (_থ): ধরণ (_র): 