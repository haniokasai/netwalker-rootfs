;; File: debian-ispell.el
;; -----------------------------------------------------------------------
;; Description: Emacsen support for Debian package dictionaries-common
;; Authors: Rafael Laboissi�re <rafael@debian.org>
;;          Agustin Martin     <agmartin@debian.org>
;; Created on: Tue Oct 26 10:16:12 CEST 1999
;; -----------------------------------------------------------------------

(defcustom debian-dict-common-debug nil
  "A lot of debugging info will be shown if non nil."
  :type 'boolean
  :group 'ispell)

(defvar debian-ispell-only-dictionary-alist nil
  "Alist of Debian installed ispell dicts and properties.
Its value will be used to set `ispell-dictionary-alist' after
ispell.el is loaded when ispell is in use.
Do not change this variable directly. It is autogenerated
from data supplied by ispell dictionaries maintainers.")

(defvar debian-aspell-only-dictionary-alist nil
  "Alist of Debian installed aspell dicts and properties.
Its value will be used to set `ispell-dictionary-alist' after
ispell.el is loaded when aspell is in use.
Do not change this variable directly. It is autogenerated
from data supplied by aspell dictionaries maintainers.")

(defvar debian-hunspell-only-dictionary-alist nil
  "Alist of Debian installed hunspell dicts and properties.
Its value will be used to set `ispell-dictionary-alist' after
ispell.el is loaded when hunspell is in use.
Do not change this variable directly. It is autogenerated
from data supplied by hunspell dictionaries maintainers.")

(defvar debian-ispell-valid-dictionary-list nil
  "List of registered ispell, aspell or hunspell dicts.
Will be used to set the dictionaries pop-up menu.")

(defun debian-ispell-add-dictionary-entry (entry &optional name)
  "Obsolete function!!. Entries in ~/.emacs must be adapted to
modify `ispell-local-dictionary-alist'"
  (message "`debian-ispell-add-dictionary-entry': Obsolete function!!.
Entries in ~/.emacs must be adapted to modify `ispell-local-dictionary-alist'.
See dictionaries-common README.emacs")
  )

;;; ----------------------------------------------------------------------
;;;  Handle ispell.el load at startup
;;; ----------------------------------------------------------------------

(defun debian-ispell-build-startup-menu (mylist)
;;; ----------------------------------------------------------------------
;;; Extracted from ispell.el, by Ken Stevens, part of GNU emacs.
;;; Original code released under the GNU GPL license
;;; ----------------------------------------------------------------------
  "Build startup menu, trying to not explicitely load ispell.el"
  (if ispell-menu-map-needed
      (let ((dicts (reverse mylist)))
	(setq ispell-menu-map (make-sparse-keymap "Spell"))
	;; add the dictionaries to the bottom of the list.
	(dolist (name dicts)
	  (if (string-equal "default" name)
	      (define-key ispell-menu-map (vector 'default)
		(cons "Select Default Dict"
		      (cons "Dictionary for which Ispell was configured"
			    (list 'lambda () '(interactive)
				  (list
				   'ispell-change-dictionary "default")))))
	    (define-key ispell-menu-map (vector (intern name))
	      (cons (concat "Select " (capitalize name) " Dict")
		    (list 'lambda () '(interactive)
			  (list 'ispell-change-dictionary name))))))))

  (if ispell-menu-map-needed
      (progn
	(define-key ispell-menu-map [ispell-change-dictionary]
	  '(menu-item "Change Dictionary..." ispell-change-dictionary
		      :help "Supply explicit dictionary file name"))
	;; --
	(define-key ispell-menu-map [ispell-kill-ispell]
	  '(menu-item "Kill Process" ispell-kill-ispell
		      :enable (and (boundp 'ispell-process) ispell-process
	 			   (eq (ispell-process-status) 'run))
		      :visible (featurep 'ispell)
		      :help "Terminate Ispell subprocess"))
	;; --
	(define-key ispell-menu-map [ispell-pdict-save]
	  '(menu-item "Save Dictionary"
	 	      (lambda () (interactive) (ispell-pdict-save t t))
		      :visible (featurep 'ispell)
	 	      :help "Save personal dictionary"))
	;; --
	(define-key ispell-menu-map [ispell-customize]
	  '(menu-item "Customize..."
		      (lambda () (interactive) (customize-group 'ispell))
		      :help "Customize spell checking options"))
	;; --
	(define-key ispell-menu-map [ispell-help]
	  ;; use (x-popup-menu last-nonmenu-event(list "" ispell-help-list)) ?
	  '(menu-item "Help"
		      (lambda () (interactive) (describe-function 'ispell-help))
		      :help "Show standard Ispell keybindings and commands"))
	;; --
	(define-key ispell-menu-map [flyspell-mode]
	  '(menu-item "Automatic spell checking (Flyspell)"
		      flyspell-mode
		      :help "Check spelling while you edit the text"
		      :button (:toggle . (and (boundp 'flyspell-mode)
					      flyspell-mode))))
	;; --
	(define-key ispell-menu-map [ispell-complete-word]
	  '(menu-item "Complete Word" ispell-complete-word
		      :help "Complete word at cursor using dictionary"))
	;; --
	(define-key ispell-menu-map [ispell-complete-word-interior-frag]
	  '(menu-item "Complete Word Fragment" ispell-complete-word-interior-frag
		      :help "Complete word fragment at cursor"))))

  (if ispell-menu-map-needed
      (progn
	(define-key ispell-menu-map [ispell-continue]
	  '(menu-item "Continue Spell-Checking" ispell-continue
	 	      :enable (and (boundp 'ispell-region-end)
				   (marker-position ispell-region-end)
				   (equal (marker-buffer ispell-region-end)
					  (current-buffer)))
		      :visible (featurep 'ispell)
	 	      :help "Continue spell checking last region"))
	;; --
	(define-key ispell-menu-map [ispell-word]
	  '(menu-item "Spell-Check Word" ispell-word
		      :help "Spell-check word at cursor"))
	;; --
	(define-key ispell-menu-map [ispell-comments-and-strings]
	  '(menu-item "Spell-Check Comments" ispell-comments-and-strings
		      :help "Spell-check only comments and strings"))))


  (if ispell-menu-map-needed
      (progn
	(define-key ispell-menu-map [ispell-region]
	  '(menu-item "Spell-Check Region" ispell-region
		      :enable mark-active
		      :help "Spell-check text in marked region"))
	(define-key ispell-menu-map [ispell-message]
	  '(menu-item "Spell-Check Message" ispell-message
		      :visible (eq major-mode 'mail-mode)
		      :help "Skip headers and included message text"))
	(define-key ispell-menu-map [ispell-buffer]
	  '(menu-item "Spell-Check Buffer" ispell-buffer
		      :help "Check spelling of selected buffer"))
	;;(put 'ispell-region 'menu-enable 'mark-active)
	(fset 'ispell-menu-map (symbol-value 'ispell-menu-map))))

  (if (and (featurep 'xemacs)
	   (featurep 'menubar)
	   ;;(null ispell-menu-xemacs)
	   (not (and (boundp 'infodock-version) infodock-version)))
      (let ((dicts mylist)
	    (current-menubar (or current-menubar default-menubar))
	    (menu
	     '(["Help"		(describe-function 'ispell-help) t]
		;;["Help"		(popup-menu ispell-help-list)	t]
		["Check Message"       ispell-message (eq major-mode 'mail-mode)]
		["Check Buffer"	       ispell-buffer			    t]
		["Check Comments"      ispell-comments-and-strings	    t]
		["Check Word"	       ispell-word			    t]
		["Check Region"	       ispell-region  (or (not zmacs-regions) (mark))]
		["Continue Check"      ispell-continue	      (featurep 'ispell)]
		["Complete Word Frag"  ispell-complete-word-interior-frag   t]
		["Complete Word"       ispell-complete-word		    t]
		["Kill Process"	       ispell-kill-ispell     (featurep 'ispell)]
		["Customize..."	       (customize-group 'ispell)	    t]
		;; flyspell-mode may not be bound...
		["flyspell"	       flyspell-mode
		:style toggle :selected flyspell-mode ]
		"-"
		["Save Personal Dict"  (ispell-pdict-save t t)(featurep 'ispell)]
		["Change Dictionary"   ispell-change-dictionary	t])))
	(if (null dicts)
	    (setq dicts (cons "default" nil)))
	(dolist (name dicts)
	  (setq menu (append menu
			     (list
			      (vector
			       (concat "Select " (capitalize name))
			       (list 'ispell-change-dictionary name)
			       t)))))
	(setq ispell-menu-xemacs menu)
	(if current-menubar
	    (progn
	      (if (car (find-menu-item current-menubar '("Cmds")))
		  (progn
		    ;; XEmacs 21.2
		    (delete-menu-item '("Cmds" "Spell-Check"))
		    (add-menu '("Cmds") "Spell-Check" ispell-menu-xemacs))
		;; previous
		(delete-menu-item '("Edit" "Spell")) ; in case already defined
		(add-menu '("Edit") "Spell" ispell-menu-xemacs))))))

  )

(defun debian-ispell-set-startup-menu (&optional force)
  "Make sure ispell startup menu is ready after startup.
To be run at `after-init-hook' or at any time if FORCE is given."
  ;; I know let* is cleaner, but this helps debugging
  (let (really-aspell
	really hunspell
	debian-valid-dictionary-list
	dicts-list)

    ;; Check for spellchecker engine
    (or (setq really-aspell
	      (if (boundp 'ispell-really-aspell)
		  ispell-really-aspell
		(and (boundp 'ispell-program-name)
		     (string-match "aspell" ispell-program-name)
		     t)))
	(setq really-hunspell
	      (if (boundp 'ispell-really-hunspell)
		  ispell-really-hunspell
		(and (boundp 'ispell-program-name)
		     (string-match "hunspell" ispell-program-name)
		     t))))

    ;; Get list of registered for given spellchecker
    (setq debian-valid-dictionary-list
	  (if really-aspell
	      (mapcar 'car debian-aspell-only-dictionary-alist)
	    (if really-hunspell
		(mapcar 'car debian-hunspell-only-dictionary-alist)
	      (mapcar 'car debian-ispell-only-dictionary-alist))))

    ;; Get full list of dicts to be displayed in the menu
    (setq dicts-list
	  (if (boundp 'ispell-local-dictionary-alist)
	      (append (mapcar 'car ispell-local-dictionary-alist)
		      debian-valid-dictionary-list)
	    debian-valid-dictionary-list))

    (if (and (featurep 'ispell)
	     (not force))
	(message "ispell.el is already loaded")
      (when (fboundp 'debian-ispell-build-startup-menu)
	(debian-ispell-build-startup-menu dicts-list)
	;; (fmakunbound 'debian-ispell-build-startup-menu)
	))))

;; Make sure updated Debian menu is available after emacs is started
(add-hook 'after-init-hook 'debian-ispell-set-startup-menu)

;; Make sure updated Debian menu is not overriden by ispell.el one
(eval-after-load "ispell" '(debian-ispell-set-startup-menu))

;;; -----------------------------------------------------------------------
;;;  Guess default ispell dictionary under emacs and make ispell.el use it
;;; -----------------------------------------------------------------------

(defvar debian-ispell-dictionary
  nil
  "The name of the ispell dictionary that will become the default after
loading of ispell.el.")

;; ---------------------------------------------------------------------------
;; Load the file containing the default value for debian-ispell-dictionary
;; ---------------------------------------------------------------------------

(if (file-exists-p "/var/cache/dictionaries-common/emacsen-ispell-default.el")
    (load "/var/cache/dictionaries-common/emacsen-ispell-default.el"))

;;; ----------------

(defvar debian-aspell-dictionary
  nil
  "The name of the aspell dictionary that will become the default after
loading of ispell.el.")

(defvar debian-hunspell-dictionary
  nil
  "The name of the hunspell dictionary that will become the default after
loading of ispell.el.")

(defvar debian-aspell-equivs-alist
  '((nil . nil))
  "Alist of equivalences between locales and aspell dictionaries,
used internally by the debian ispell.el initialization scheme.
Do not change this variable directly. It is autogenerated
from data supplied by aspell dictionaries maintainers.")

(defvar debian-hunspell-equivs-alist
  '((nil . nil))
  "Alist of equivalences between locales and hunspell dictionaries,
used internally by the debian ispell.el initialization scheme.
Do not change this variable directly. It is autogenerated
from data supplied by hunspell dictionaries maintainers.")

;; ---------------------------------------------------------------------------
;; Guess emacsen entry for aspell and hunspell after locale provided by aspell
;; or after environment variables LC_ALL and LANG for hunspell
;; Intended to be called from /var/cache/emacsen-ispell-dicts.el
;; to set debian-{a,huns}spell-dictionary if possible
;; ---------------------------------------------------------------------------

(defun debian-ispell-try-lang-equiv (langstring equivs-alist)
  "Try finding a LANGSTRING match in EQUIVS-ALIST.
EQUIVS-ALIST is an assoc list of locales vs dict names."
  (let ((prefixes  '("" "1:"))
	(suffixes  '("^" "@" "." "_"))
	(langmatch '(nil nil)))

    (if langstring
	(catch 'tag
	  (dolist (lang (split-string langstring ":"))
	    (dolist (suffix suffixes)
	      (dolist (prefix prefixes)
		(if (setq langmatch
			  (cdr (assoc (concat prefix
					      (car (split-string lang suffix)))
				      equivs-alist)))
		    (throw 'tag (car langmatch))))))))))


(defun debian-ispell-get-aspell-default ()
  "Get default dictionary for aspell.
Ask aspell about the default dictionary it will use, and
try finding a match for it in `debian-aspell-equivs-alist'
alist provided by registered dicts."
  (let ((lang (condition-case ()
		  (with-temp-buffer
		    (call-process "aspell" nil t nil "config" "lang")
		    (car (split-string (buffer-string))))
		(error nil))))

    (debian-ispell-try-lang-equiv lang debian-aspell-equivs-alist)))

(defun debian-ispell-get-hunspell-default ()
  "Get default dictionary for hunspell.
Look at the `debian-aspell-equivs-alist' alist provided by registered
dicts to try finding a match for \"LC_ALL\" or \"LANG\"."
  (or (debian-ispell-try-lang-equiv (getenv "LC_ALL") debian-hunspell-equivs-alist)
      (debian-ispell-try-lang-equiv (getenv "LANG")   debian-hunspell-equivs-alist)))

;; ---------------------------------------------------------------------------
;; Make sure the correct installed dicts alist is used for each spellchecker
;; This hook will be run after each change in `ispell-program-name'
;; ---------------------------------------------------------------------------

(defun debian-ispell-initialize-dicts-alist ()
  (setq ispell-base-dicts-override-alist
	(if (and (boundp 'ispell-really-aspell)
		 ispell-really-aspell)
	    debian-aspell-only-dictionary-alist
	  (if (and (boundp 'ispell-really-hunspell)
		   ispell-really-hunspell)
	      debian-hunspell-only-dictionary-alist
	    debian-ispell-only-dictionary-alist)))
  (setq debian-ispell-valid-dictionary-list
	(mapcar 'car ispell-base-dicts-override-alist))
  (debian-ispell-set-startup-menu 'force)
  (if debian-dict-common-debug
      (message "- (ispell-set-spellchecker-params) old: %s new:%s"
	       ispell-last-program-name ispell-program-name))
  )

(add-hook 'ispell-initialize-spellchecker-hook 'debian-ispell-initialize-dicts-alist)

;;; --------------

(defun debian-ispell-set-default-dictionary ()
  "Set ispell default to the debconf selected one if ispell-program-name is
ispell or, when ispell-program-name is aspell, to the value guessed after
LANG if any."
  (let ((really-aspell
	 (if (boundp 'ispell-really-aspell)
	     ispell-really-aspell
	   (and (boundp 'ispell-program-name)
		(string-match "aspell" ispell-program-name)
		t)))
	(really-hunspell
	 (if (boundp 'ispell-really-hunspell)
	     ispell-really-hunspell
	   (and (boundp 'ispell-program-name)
		(string-match "hunspell" ispell-program-name)
		t))))

    ;; Set local dictionary if known
    (unless (and (boundp 'ispell-local-dictionary)
		 ispell-local-dictionary)
      (setq ispell-local-dictionary
	    (if really-aspell
		debian-aspell-dictionary
	      (if really-hunspell
		  debian-hunspell-dictionary
		debian-ispell-dictionary))))

    ;; The debugging output if required

    (if debian-dict-common-debug
	(message "- dictionaries DID:%s, DAD:%s, DHD: %s, RA:%s, RH: %s, ILD:%s, IPN:%s"
		 debian-ispell-dictionary
		 debian-aspell-dictionary
		 debian-hunspell-dictionary
		 really-aspell
		 really-hunspell
		 ispell-local-dictionary
		 ispell-program-name))
    )) ;; let and defun ends

(add-hook 'after-init-hook 'debian-ispell-set-default-dictionary)

;; ---------------------------------------------------------------------------
;; Make sure patched ispell.el is first in the loadpath if not already there
;; ---------------------------------------------------------------------------

(let ((mypath (concat "/usr/share/"
		      (symbol-name debian-emacs-flavor)
		      "/site-lisp/dictionaries-common")))
  (unless (member mypath load-path)
    (debian-pkg-add-load-path-item mypath)))

;; --------------------------------------------------------------------------
;; Set ispell-program-name consistently for all emacsen flavours, preferring
;; ispell over aspell for backwards compatibility
;; --------------------------------------------------------------------------

(setq ispell-program-name
      (or (and (executable-find "aspell")
	       (not (executable-find "ispell"))
	       "aspell")
	  (and (executable-find "hunspell")
	       (not (executable-find "ispell"))
	       "hunspell")
	  "ispell"))

;;; -----------------------------------------------------------------------

;; Local Variables:
;; mode: lisp
;; End: