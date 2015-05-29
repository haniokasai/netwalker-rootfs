cmd_scripts/genksyms/parse.o := gcc -Wp,-MD,scripts/genksyms/.parse.o.d -Iscripts/genksyms -Wall -Wstrict-prototypes -O2 -fomit-frame-pointer -Wno-uninitialized -I/build/buildd/linux-fsl-imx51-2.6.28/scripts/genksyms -Iscripts/genksyms -c -o scripts/genksyms/parse.o scripts/genksyms/parse.c

deps_scripts/genksyms/parse.o := \
  scripts/genksyms/parse.c \
  /usr/include/assert.h \
  /usr/include/features.h \
  /usr/include/sys/cdefs.h \
  /usr/include/bits/wordsize.h \
  /usr/include/gnu/stubs.h \
  /usr/include/malloc.h \
  /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include/stddef.h \
  scripts/genksyms/genksyms.h \
  /usr/include/stdio.h \
  /usr/include/bits/types.h \
  /usr/include/bits/typesizes.h \
  /usr/include/libio.h \
  /usr/include/_G_config.h \
  /usr/include/wchar.h \
  /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include/stdarg.h \
  /usr/include/bits/stdio_lim.h \
  /usr/include/bits/sys_errlist.h \
  /usr/include/bits/stdio.h \
  /usr/include/bits/stdio2.h \

scripts/genksyms/parse.o: $(deps_scripts/genksyms/parse.o)

$(deps_scripts/genksyms/parse.o):
