��    H      \  a   �         o   !  ?   �  �   �  .   h  #   �     �  '   �     �          '     ;  (   J     s  K   �     �     �     �  -   �     -	     <	     D	  Q   R	     �	  8   �	  M   �	  k   B
  8   �
  (   �
            u   4     �     �  X   �  @        N     d  ;   �  6   �  7   �  �   ,  /   �  4   �  =     Y   X  �  �  )   v  7   �     �  1   �  '   )  .   Q  C   �    �     �  �   �     e     k  n   �     �  @        T  &   q     �     �  '   �     �  !   �       a   ,     �  ^  �  �   �  y   �  l  ^  S   �  _     2     T   �       =   "  4   `  )   �  i   �  G   )  �   q     �  Q        b     s     �            �   &     �  �     �   �  �   1   T   !  I   ]!     �!  @   �!  �   �!     �"     �"  �   #  �   �#  $   `$  )   �$  �   �$  �   A%  Z   �%  �   1&  }   '  g   �'  w   �'  �   s(  �  +)  _   �,  _   &-  H   �-  Q   �-  '   !.  .   I.  C   x.  �  �.  6   �0  6  �0     2  *   '2  �   R2  <   L3  �   �3  &   4  \   ?4     �4  )   �4  ]   �4  2   +5  P   ^5  3   �5  �   �5     �6        5       (       C                    ?                       1      ,                !   @       +                  )   7   4   >   -   <                 9   0   =   H               .      F   /   D           :   B   2                               3   $          E             ;      &      8          "       %   #   *   
      G      	   6   A   '    
        --outdated		Merge in even outdated translations.
	--drop-old-templates	Drop entire outdated templates. 
  -o,  --owner=package		Set the package that owns the command.   -f,  --frontend		Specify debconf frontend to use.
  -p,  --priority		Specify minimum priority question to show.
       --terse			Enable terse mode.
 %s failed to preconfigure, with exit status %s %s is broken or not fully installed %s is fuzzy at byte %s: %s %s is fuzzy at byte %s: %s; dropping it %s is missing %s is missing; dropping %s %s is not installed %s is outdated %s is outdated; dropping whole template! %s must be run as root (Enter zero or more items separated by a comma followed by a space (', ').) Back Cannot read status file: %s Choices Config database not specified in config file. Configuring %s Debconf Debconf on %s Debconf was not configured to display this error message, so it mailed it to you. Debconf, running at %s Dialog frontend is incompatible with emacs shell buffers Dialog frontend requires a screen at least 13 lines tall and 31 columns wide. Dialog frontend will not work on a dumb terminal, an emacs shell buffer, or without a controlling terminal. Enter the items you want to select, separated by spaces. Extracting templates from packages: %d%% Help Ignoring invalid priority "%s" Input value, "%s" not found in C choices! This should never happen. Perhaps the templates were incorrectly localized. More Next No usable dialog-like program is installed, so the dialog based frontend cannot be used. Note: Debconf is running in web mode. Go to http://localhost:%i/ Package configuration Preconfiguring packages ...
 Problem setting up the database defined by stanza %s of %s. TERM is not set, so the dialog frontend is not usable. Template #%s in %s does not contain a 'Template:' line
 Template #%s in %s has a duplicate field "%s" with new value "%s". Probably two templates are not properly separated by a lone newline.
 Template database not specified in config file. Template parse error near `%s', in stanza #%s of %s
 Term::ReadLine::GNU is incompatable with emacs shell buffers. The Sigils and Smileys options in the config file are no longer used. Please remove them. The editor-based debconf frontend presents you with one or more text files to edit. This is one such text file. If you are familiar with standard unix configuration files, this file will look familiar to you -- it contains comments interspersed with configuration items. Edit the file, changing any items as necessary, and then save it and exit. At that point, debconf will read the edited file, and use the values you entered to configure the system. This frontend requires a controlling tty. Unable to load Debconf::Element::%s. Failed because: %s Unable to start a frontend: %s Unknown template field '%s', in stanza #%s of %s
 Usage: debconf [options] command [args] Usage: debconf-communicate [options] [package] Usage: debconf-mergetemplate [options] [templates.ll ...] templates Usage: dpkg-reconfigure [options] packages
  -a,  --all			Reconfigure all packages.
  -u,  --unseen-only		Show only not yet seen questions.
       --default-priority	Use default priority instead of low.
       --force			Force reconfiguration of broken packages. Valid priorities are: %s You are using the editor-based debconf frontend to configure your system. See the end of this document for detailed instructions. _Help apt-extracttemplates failed: %s debconf-mergetemplate: This utility is deprecated. You should switch to using po-debconf's po2debconf program. debconf: can't chmod: %s delaying package configuration, since apt-utils is not installed falling back to frontend: %s must specify some debs to preconfigure no none of the above please specify a package to reconfigure template parse error: %s unable to initialize frontend: %s unable to re-open stdin: %s warning: possible database corruption. Will attempt to repair by adding back missing question %s. yes Project-Id-Version: debconf_po_el
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2008-06-19 01:54+0000
PO-Revision-Date: 2008-08-24 17:53+0300
Last-Translator: 
Language-Team:  <en@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
org>
X-Generator: KBabel 1.11.4
Plural-Forms:  nplurals=2; plural=(n != 1);
 
        --outdated		Ενσωμάτωση ακόμα και των μη ενημερωμένων μεταφράσεων.
	--drop-old-templates	Απόρριψη ολόκληρων των ξεπερασμένων "προτύπων" (templates). 
  -o,  --owner=package		Προσδιορισμός του πακέτου στο οποίο ανήκει η εντολή.   -f,  --frontend		Προσδιορίστε το debconf frontend που θέλετε να χρησιμοποιήσετε.
  -p,  --priority		Προσδιορίστε την ερώτηση με την μικρότερη προτεραιότητα που θέλετε να εμφανιστεί.
       --terse			Ενεργοποίηση κατάστασης terse.
 Αδύνατη η προρύθμιση του %s, με κωδικό λάθους %s το %s είναι κατεστραμμένο ή όχι πλήρως εγκατεστημένο Το %s είναι ασαφές στο byte %s: %s Το %s είναι ασαφές στο byte %s: %s, και θα παραληφθεί το %s αγνοείται το %s αγνοείται, θα παραληφθεί το %s το %s δεν είναι εγκατεστημένο το %s είναι ξεπερασμένο το %s είναι ξεπερασμένο, παραλείπεται ολόκληρο το πρότυπο! Το %s πρέπει να εκτελεστεί ως χρήστης root (Εισάγετε καμία ή περισσότερες επιλογές χωρισμένες με κόμμα και κενό (', ').) Προηγούμενο Αδύνατη η ανάγνωση του αρχείου κατάστασης: %s Επιλογές Η βάση δεδομένων των ρυθμίσεων δεν έχει οριστεί στο αρχείο ρυθμίσεων. Ρύθμιση του %s Debconf Debconf στο %s Το debconf δεν έχει ρυθμιστεί να εμφανίζει αυτό το μήνυμα σφάλματος, οπότε σας την απέστειλε μέσω ηλ. ταχυδρομείου. Debconf, τρέχει στο %s Ο διαλογικός τρόπος αλληλεπίδρασης δεν είναι συμβατός με το κέλυφος του emacs. Το διαλογικό περιβάλλον απαιτεί οθόνη ύψους 13 γραμμών και 31 στηλών τουλάχιστον. Το διαλογικό περιβάλλον δε λειτουργεί σε απλοϊκό (dumb) τερματικό, περιβάλλον κέλυφος του emacs, ή χωρίς τυλέτυπο ελέγχου. Εισάγετε τις επιλογές σας, χωρισμένες με κενό. Εξαγωγή προτύπων (templates) από τα πακέτα:%d%% Βοήθεια Θα αγνοηθεί η μή έγκυρη ιδιότητα "%s" Η επιλογή που δώσατε, "%s" δε βρέθηκε σε C επιλογές! Αυτό δε θα έπρεπε να έχει συμβεί. Πιθανόν τα πρότυπα δε μεταφράστηκαν σωστά. Περισσότερα Επόμενο Δε βρέθηκε εγκατεστημένο λειτουργικό πρόγραμμα τύπου dialog, έτσι δε μπορεί να χρησιμοποιηθεί το διαλογικό περιβάλλον. Σημείωση: Το debconf τρέχει σε κατάσταση δικτυακού τόπου. Δείτε τη http://localhost:%i/ Ρύθμιση του πακέτου Προρύθμιση πακέτων ... 
 Σφάλμα κατά την ρύθμιση της βάσης δεδομένων όπως ορίστηκε κατά το τμήμα %s του %s. Η μεταβλητή TERM δεν είναι ορισμένη, έτσι ο διαλογικός τρόπος δεν είναι διαθέσιμος. Το πρότυπο #%s στο %s δεν περιέχει μια γραμμή 'Template:'
 Το πρότυπο #%s στο %s έχει διπλά ορισμένο πεδίο "%s" με νέα τιμή "%s". Πιθανόν δύο πρότυπα δεν είναι σωστά χωρισμένα με κενή γραμμή.
 Η βάση δεδομένων των προτύπων δεν έχει οριστεί στο αρχείο ρυθμίσεων. Σφάλμα ανάλυσης προτύπου κοντά στο `%s', στο τμήμα #%s του %s
 Το Term::ReadLine::GNU δεν είναι συμβατό με το περιβάλλον κελύφους του emacs. Οι χαρακτήρες Sigils και Smileys στο αρχείο ρυθμίσεων δε χρησιμοποιούνται πλέον. Παρακαλώ, αφαιρέστε τους. Η ρύθμιση μέσω κειμενογράφου σας παρουσιάζει μια λίστα με ένα ή περισσότερα αρχεία κειμένου προς επεξεργασία. Αυτό είναι ένα τέτοιο αρχείο. Αν έχετε εμπειρία με τυπικά αρχεία ρυθμίσεων του unix, η μορφή του αρχείου αυτού θα σας φανεί γνωστή -- περιέχει σχόλια εν μέσω ρυθμίσεων. Επεξεργαστείτε το αρχείο, αλλάζοντας όποιες ρυθμίσεις χρειάζονται, αποθηκεύστε το αρχείο και εξέλθετε από το πρόγραμμα. Στο σημείο αυτό, το debconf θα διαβάσει το επεξεργασμένο αρχείο και θα χρησιμοποιήσει τις ρυθμίσεις που δώσατε. Το περιβάλλον αυτό απαιτεί ένα τυλέτυπο (tty) ελέγχου. Αδύνατη η φόρτωση του Debconf::Element::%s. Αιτία αποτύχιας: %s Αδύνατη η εκκίνηση του περιβάλλοντος: %s Άγνωστο πεδίο προτύπου '%s', στο τμήμα #%s του %s
 Usage: debconf [options] command [args] Usage: debconf-communicate [options] [package] Usage: debconf-mergetemplate [options] [templates.ll ...] templates Χρήση: dpkg-reconfigure [options] packages
  -a,  --all			Επαναρύθμιση όλων των πακέτων.
  -u,  --unseen-only		Εμφάνιση μόνο των ερωτήσεων που δεν έχουν ήδη εμφανιστεί.
       --default-priority	Χρήση προκαθορισμένης αντί της χαμηλής προτεραιότητας.
       --force			Αναγκαστική επαναρύθμιση των "προβληματικών" πακέτων. Οι έγκυρες ιδιότητες είναι : %s Έχετε επιλέξει την βασισμένη σε επεξεργαστή κειμένου προθήκη του debconf για την ρύθμιση του συστήματός σας. Λεπτομερείς οδηγίες αναγράφονται στο τέλος αυτού του κειμένου. Βοήθεια η apt-extracttemplates απέτυχε: %s debconf-mergetemplate: Αυτό το βοηθητικό πρόγραμμα έχει πλέον εγκαταλειφθεί. Θα πρέπει να περάσετε στην χρήση του προγράμματος po2debconf από το po-debconf. debconf: αδύνατη η εκτέλεση της chmod: %s καθυστέρηση της ρύθμισης του πακέτου, εφόσον το apt-utils δεν είναι εγκατεστημένο επιστροφή στο frontend: %s πρέπει να δηλώσετε κάποια πακέτα deb για προρύθμιση όχι καμία από τις παραπάνω παρακαλώ προσδιορίστε το πακέτο προς επαναρύθμιση σφάλμα ανάλυσης προτύπου: %s αδύνατη η αρχικοποίηση του περιβάλλοντος: %s αδύνατο το άνοιγμα της stdin: %s προειδοποίηση: πιθανή καταστροφή της βάσης. Θα γίνει προσπάθεια επιδιόρθωσής της προσθέτοντας την εκλιπόμμενη ερώτηση %s. ναι 