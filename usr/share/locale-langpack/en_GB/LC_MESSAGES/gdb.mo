��    P      �  k         �  �  �  ;   x	  -   �	  %   �	     
     '
  "   =
  $   `
  4   �
  .   �
  \   �
  X   F  '   �     �  -   �  %     9   8  4  r  -   �     �  '   �           6  =   W  (   �    �    �     �  M   �  #   J  $   n  $   �     �     �     �          7  $   W  6   |      �      �      �        7   7  \  o  '  �  +   �  #      )   D  �   n  '   ,  �   T  �   �  (   �  $   �  )     &   5  3   \  ,   �  *   �  !   �  &   
     1      P  %   q  �   �     r  1   {  2   �     �     �  .   �  *   )      T   !   t      �   &   �      �      �   �  !  �  �"  ;   %  -   �%  %   �%     &     .&  "   D&  $   g&  4   �&  .   �&  ]   �&  Y   N'  '   �'     �'  -   �'  %   (  :   A(  4  |(  -   �)     �)  '   �)     #*      @*  =   a*  '   �*    �*    �+     �,  K   -  #   Q-  %   u-  %   �-     �-     �-      .      .     @.  $   `.  7   �.      �.      �.      �.       /  8   A/  \  z/  '  �2  +   �5  #   +6  )   O6  �   y6  /   77  �   g7  �   �7  (   �8  $   �8  )   9  &   H9  3   o9  ,   �9  *   �9  !   �9  &   :     D:      c:  %   �:  �   �:  	   �;  1   �;  2   �;     �;     <  .   <  *   ><     i<  !   �<     �<  &   �<     �<     =                    7   A         ?          9         @   &      N       3      
   !   F          :         I   .   J             0   "       /          )         -       ;   D   =       G       4          H   #   E         C      6              P   	                  ,       '           L   +      $               2   M       8   <   1   5       B      O                    *      (   >   %   K      -b BAUDRATE        Set serial port baud rate used for remote debugging.
  --batch            Exit after processing options.
  --batch-silent     As for --batch, but suppress all gdb stdout output.
  --return-child-result
                     GDB exit code will be the child's exit code.
  --cd=DIR           Change current directory to DIR.
  --command=FILE, -x Execute GDB commands from FILE.
  --eval-command=COMMAND, -ex
                     Execute a single GDB command.
                     May be used multiple times and in conjunction
                     with --command.
  --core=COREFILE    Analyze the core dump COREFILE.
  --pid=PID          Attach to running process PID.
 "%s": no core file handler recognizes format, using default %s is optimized away and cannot be collected. '%s' is not a recognized file format. <optimized out or zero length> <value optimized out> Architecture `%s' not recognized.
 Architecture of file not recognized. Attempt to assign to a value that was optimized out. Cannot initialize thread debugging library: %s Cannot perform pointer math on incomplete type "%s", try casting to a known type, or void *. Cannot perform pointer math on incomplete types, try casting to a known type, or void *. Canonicalized file name given to execve Couldn't initialize WINSOCK. Couldn't recognize %s registers in core file. Couldn't recognize signal trampoline. Debugger's behavior regarding pending breakpoints is %s.
 Deprecate a command.  Note that this is just in here so the 
testsuite can check the comamnd deprecator. You probably shouldn't use this,
rather you should use the C function deprecate_cmd().  If you decide you 
want to use it: maintenance deprecate 'commandname' "replacement". The 
replacement is optional. Enabled packet %s (%s) not recognized by stub Event type not recognized.
 Failed to initialize new interp "%s" %s Garbage %s follows condition Garbage after "%s" command: `%s' Garbage after "show remote system-call-allowed" command: `%s' Hardware breakpoints used exceeds limit. If on, an unrecognized breakpoint location will cause gdb to create a
pending breakpoint.  If off, an unrecognized breakpoint location results in
an error.  If auto, an unrecognized breakpoint location results in a
user-query to see if a pending breakpoint should be created. Initialize a convenience variable if necessary.
init-if-undefined VARIABLE = EXPRESSION
Set an internal VARIABLE to the result of the EXPRESSION if it does not
exist or does not contain a value.  The EXPRESSION is not evaluated if the
VARIABLE is already initialized. Interpreter `%s' unrecognized One or more sections of the remote executable does not match
the loaded file
 Reinitialize source path to empty?  Scroll the register window backward
 Scroll the registers window forward
 Section index is uninitialized Set COM1 base i/o port address. Set COM2 base i/o port address. Set COM3 base i/o port address. Set COM4 base i/o port address. Set current context from pcb address Set debugger's behavior regarding pending breakpoints. Show COM1 base i/o port address. Show COM2 base i/o port address. Show COM3 base i/o port address. Show COM4 base i/o port address. Show debugger's behavior regarding pending breakpoints. Specify how to handle a signal.
Args are signals and actions to apply to those signals.
Symbolic signals (e.g. SIGSEGV) are recommended but numeric signals
from 1-15 are allowed for compatibility with old versions of GDB.
Numeric ranges may be specified with the form LOW-HIGH (e.g. 1-5).
The special arg "all" is recognized to mean all signals except those
used by the debugger, typically SIGTRAP and SIGINT.
Recognized actions include "s" (toggles between stop and nostop), 
"r" (toggles between print and noprint), "i" (toggles between pass and nopass), "Q" (noprint)
Stop means reenter debugger if this signal happens (implies print).
Print means print a message if this signal happens.
Pass means let program see this signal; otherwise program doesn't know.
Ignore is a synonym for nopass and noignore is a synonym for pass.
Pass and Stop may be combined. Specify how to handle a signal.
Args are signals and actions to apply to those signals.
Symbolic signals (e.g. SIGSEGV) are recommended but numeric signals
from 1-15 are allowed for compatibility with old versions of GDB.
Numeric ranges may be specified with the form LOW-HIGH (e.g. 1-5).
The special arg "all" is recognized to mean all signals except those
used by the debugger, typically SIGTRAP and SIGINT.
Recognized actions include "stop", "nostop", "print", "noprint",
"pass", "nopass", "ignore", or "noignore".
Stop means reenter debugger if this signal happens (implies print).
Print means print a message if this signal happens.
Pass means let program see this signal; otherwise program doesn't know.
Ignore is a synonym for nopass and noignore is a synonym for pass.
Pass and Stop may be combined. Storage class %d not recognized during scan Symbol "%s" has been optimized out. The variable `%s' has been optimized out. This variable controls the border of TUI windows:
space           use a white space
ascii           use ascii characters + - | for the border
acs             use the Alternate Character Set Type required within braces in coercion Unable to find dynamic linker breakpoint function.
GDB will be unable to debug shared library initializers
and track explicitly loaded dynamic code. Undeprecate a command.  Note that this is just in here so the 
testsuite can check the comamnd deprecator. You probably shouldn't use this,
If you decide you want to use it: maintenance undeprecate 'commandname' Unrecognized %d-bit floating-point type. Unrecognized case-sensitive setting. Unrecognized case-sensitive setting: "%s" Unrecognized cross-reference type `%c' Unrecognized escape character \%c in format string. Unrecognized format specifier '%c' in printf Unrecognized or ambiguous flag word: "%s". Unrecognized range check setting. Unrecognized range check setting: "%s" Unrecognized storage class %d. Unrecognized type check setting. Unrecognized type check setting: "%s" When non-zero, this timeout is used instead of waiting forever for a target
to finish a low-level step or continue operation.  If the specified amount
of time passes without a response from the target, an error occurs. canceled mi_cmd_break_insert: Garbage following <location> mi_cmd_break_watch: Garbage following <expression> optimized out pcb address print_bp_stop_message: unrecognized enum value print_stop_reason: unrecognized enum value sect_index_data not initialized sect_index_rodata not initialized sect_index_text not initialized static field %s has been optimized out too many initializers unrecognized attribute: `%s' Project-Id-Version: gdb
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2008-03-27 18:27+0000
PO-Revision-Date: 2008-03-11 03:35+0000
Last-Translator: Andrew Barber <andrew-alex-barber@ubuntu.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 07:16+0000
X-Generator: Launchpad (build Unknown)
   -b BAUDRATE        Set serial port baud rate used for remote debugging.
  --batch            Exit after processing options.
  --batch-silent     As for --batch, but suppress all gdb stdout output.
  --return-child-result
                     GDB exit code will be the child's exit code.
  --cd=DIR           Change current directory to DIR.
  --command=FILE, -x Execute GDB commands from FILE.
  --eval-command=COMMAND, -ex
                     Execute a single GDB command.
                     May be used multiple times and in conjunction
                     with --command.
  --core=COREFILE    Analyse the core dump COREFILE.
  --pid=PID          Attach to running process PID.
 "%s": no core file handler recognises format, using default %s is optimised away and cannot be collected. '%s' is not a recognised file format. <optimised out or zero length> <value optimised out> Architecture `%s' not recognised.
 Architecture of file not recognised. Attempt to assign to a value that was optimised out. Cannot initialise thread debugging library: %s Cannot perform pointer maths on incomplete type "%s", try casting to a known type, or void *. Cannot perform pointer maths on incomplete types, try casting to a known type, or void *. Canonicalised file name given to execve Couldn't initialise WINSOCK. Couldn't recognise %s registers in core file. Couldn't recognise signal trampoline. Debugger's behaviour regarding pending breakpoints is %s.
 Deprecate a command.  Note that this is just in here so the 
testsuite can check the command deprecator. You probably shouldn't use this,
rather you should use the C function deprecate_cmd().  If you decide you 
want to use it: maintenance deprecate 'commandname' "replacement". The 
replacement is optional. Enabled packet %s (%s) not recognised by stub Event type not recognised.
 Failed to initialise new interp "%s" %s Rubbish %s follows condition Rubbish after "%s" command: `%s' Rubbish after "show remote system-call-allowed" command: `%s' Hardware breakpoints used exceed limit. If on, an unrecognised breakpoint location will cause gdb to create a
pending breakpoint.  If off, an unrecognised breakpoint location results in
an error.  If auto, an unrecognised breakpoint location results in a
user-query to see if a pending breakpoint should be created. Initialise a convenience variable if necessary.
init-if-undefined VARIABLE = EXPRESSION
Set an internal VARIABLE to the result of the EXPRESSION if it does not
exist or does not contain a value.  The EXPRESSION is not evaluated if the
VARIABLE is already initialized. Interpreter `%s' unrecognised One or more sections of the remote executable do not match
the loaded file
 Reinitialise source path to empty?  Scroll the register window backwards
 Scroll the registers window forwards
 Section index is uninitialised Set COM1 base I/O port address. Set COM2 base I/O port address. Set COM3 base I/O port address. Set COM4 base I/O port address. Set current context from PCB address Set debugger's behaviour regarding pending breakpoints. Show COM1 base I/O port address. Show COM2 base I/O port address. Show COM3 base I/O port address. Show COM4 base I/O port address. Show debugger's behaviour regarding pending breakpoints. Specify how to handle a signal.
Args are signals and actions to apply to those signals.
Symbolic signals (e.g. SIGSEGV) are recommended but numeric signals
from 1-15 are allowed for compatibility with old versions of GDB.
Numeric ranges may be specified with the form LOW-HIGH (e.g. 1-5).
The special arg "all" is recognised to mean all signals except those
used by the debugger, typically SIGTRAP and SIGINT.
Recognised actions include "s" (toggles between stop and nostop), 
"r" (toggles between print and noprint), "i" (toggles between pass and nopass), "Q" (noprint)
Stop means reenter debugger if this signal happens (implies print).
Print means print a message if this signal happens.
Pass means let program see this signal; otherwise program doesn't know.
Ignore is a synonym for nopass and noignore is a synonym for pass.
Pass and Stop may be combined. Specify how to handle a signal.
Args are signals and actions to apply to those signals.
Symbolic signals (e.g. SIGSEGV) are recommended but numeric signals
from 1-15 are allowed for compatibility with old versions of GDB.
Numeric ranges may be specified with the form LOW-HIGH (e.g. 1-5).
The special arg "all" is recognised to mean all signals except those
used by the debugger, typically SIGTRAP and SIGINT.
Recognised actions include "stop", "nostop", "print", "noprint",
"pass", "nopass", "ignore", or "noignore".
Stop means reenter debugger if this signal happens (implies print).
Print means print a message if this signal happens.
Pass means let program see this signal; otherwise program doesn't know.
Ignore is a synonym for nopass and noignore is a synonym for pass.
Pass and Stop may be combined. Storage class %d not recognised during scan Symbol "%s" has been optimised out. The variable `%s' has been optimised out. This variable controls the border of TUI windows:
space           use a white space
ascii           use ASCII characters + - | for the border
acs             use the Alternate Character Set Type required within curly brackets in coercion Unable to find dynamic linker breakpoint function.
GDB will be unable to debug shared library initialisers
and track explicitly loaded dynamic code. Undeprecate a command.  Note that this is just in here so the 
testsuite can check the command deprecator. You probably shouldn't use this,
If you decide you want to use it: maintenance undeprecate 'commandname' Unrecognised %d-bit floating-point type. Unrecognised case-sensitive setting. Unrecognised case-sensitive setting: "%s" Unrecognised cross-reference type `%c' Unrecognised escape character \%c in format string. Unrecognised format specifier '%c' in printf Unrecognised or ambiguous flag word: "%s". Unrecognised range check setting. Unrecognised range check setting: "%s" Unrecognised storage class %d. Unrecognised type check setting. Unrecognised type check setting: "%s" When non-zero, this timeout is used instead of waiting for ever for a target
to finish a low-level step or continue operation.  If the specified amount
of time passes without a response from the target, an error occurs. cancelled mi_cmd_break_insert: Rubbish following <location> mi_cmd_break_watch: Rubbish following <expression> optimised out PCB address print_bp_stop_message: unrecognised enum value print_stop_reason: unrecognised enum value sect_index_data not initialised sect_index_rodata not initialised sect_index_text not initialised static field %s has been optimised out too many initialisers unrecognised attribute: `%s' 