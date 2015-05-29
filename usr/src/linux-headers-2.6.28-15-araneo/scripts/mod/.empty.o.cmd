cmd_scripts/mod/empty.o := gcc -Wp,-MD,scripts/mod/.empty.o.d  -nostdinc -isystem /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include -D__KERNEL__ -I/usr/src/linux-headers-lbm-2.6.28-15-araneo -Iinclude -Iinclude2 -I/build/buildd/linux-fsl-imx51-2.6.28/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include -include include/linux/autoconf.h -Iubuntu/include -I/build/buildd/linux-fsl-imx51-2.6.28/ubuntu/include -mlittle-endian -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/mach-mx51/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include -I/build/buildd/linux-fsl-imx51-2.6.28/scripts/mod -Iscripts/mod -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -fno-delete-null-pointer-checks -Os -marm -fno-omit-frame-pointer -mapcs -mno-sched-prolog -mabi=aapcs-linux -mno-thumb-interwork -D__LINUX_ARM_ARCH__=7 -march=armv7-a -msoft-float -Uarm -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-inline-functions-called-once -Wdeclaration-after-statement -Wno-pointer-sign -fwrapv  -D"KBUILD_STR(s)=\#s" -D"KBUILD_BASENAME=KBUILD_STR(empty)"  -D"KBUILD_MODNAME=KBUILD_STR(empty)"  -c -o scripts/mod/.tmp_empty.o scripts/mod/empty.c

deps_scripts/mod/empty.o := \
  scripts/mod/empty.c \

scripts/mod/empty.o: $(deps_scripts/mod/empty.o)

$(deps_scripts/mod/empty.o):
