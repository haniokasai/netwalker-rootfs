	.arch armv7-a
	.fpu softvfp
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 4
	.eabi_attribute 18, 4
	.file	"bounds.c"
@ GNU C (Ubuntu 4.3.3-5ubuntu4) version 4.3.3 (arm-linux-gnueabi)
@	compiled by GNU C version 4.3.3, GMP version 4.2.4, MPFR version 2.4.0.
@ GGC heuristics: --param ggc-min-expand=47 --param ggc-min-heapsize=32041
@ options passed:  -nostdinc -I/usr/src/linux-headers-lbm- -Iinclude
@ -Iinclude2 -I/build/buildd/linux-fsl-imx51-2.6.28/include
@ -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include -Iubuntu/include
@ -I/build/buildd/linux-fsl-imx51-2.6.28/ubuntu/include
@ -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/mach-mx51/include
@ -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include
@ -I/build/buildd/linux-fsl-imx51-2.6.28/. -I. -D__KERNEL__
@ -D__LINUX_ARM_ARCH__=7 -Uarm -DKBUILD_STR(s)=#s
@ -DKBUILD_BASENAME=KBUILD_STR(bounds) -DKBUILD_MODNAME=KBUILD_STR(bounds)
@ -isystem /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include -include
@ include/linux/autoconf.h -MD kernel/.bounds.s.d
@ /build/buildd/linux-fsl-imx51-2.6.28/kernel/bounds.c -D_FORTIFY_SOURCE=2
@ -mlittle-endian -marm -mapcs -mno-sched-prolog -mabi=aapcs-linux
@ -mno-thumb-interwork -march=armv7-a -msoft-float -mtune=cortex-a8
@ -auxbase-strip kernel/bounds.s -Os -Wall -Wundef -Wstrict-prototypes
@ -Wno-trigraphs -Werror-implicit-function-declaration
@ -Wdeclaration-after-statement -Wno-pointer-sign -fno-strict-aliasing
@ -fno-common -fno-delete-null-pointer-checks -fno-stack-protector
@ -fno-omit-frame-pointer -fno-optimize-sibling-calls
@ -fno-inline-functions-called-once -fwrapv -fverbose-asm
@ options enabled:  -falign-loops -fargument-alias -fauto-inc-dec
@ -fbranch-count-reg -fcaller-saves -fcprop-registers -fcrossjumping
@ -fcse-follow-jumps -fdefer-pop -fearly-inlining
@ -feliminate-unused-debug-types -fexpensive-optimizations
@ -fforward-propagate -ffunction-cse -fgcse -fgcse-lm
@ -fguess-branch-probability -fident -fif-conversion -fif-conversion2
@ -finline-functions -finline-small-functions -fipa-pure-const
@ -fipa-reference -fivopts -fkeep-static-consts -fleading-underscore
@ -fmath-errno -fmerge-constants -fmerge-debug-strings
@ -fmove-loop-invariants -foptimize-register-move -fpeephole -fpeephole2
@ -freg-struct-return -fregmove -freorder-functions -frerun-cse-after-loop
@ -fsched-interblock -fsched-spec -fsched-stalled-insns-dep
@ -fschedule-insns -fschedule-insns2 -fsigned-zeros -fsplit-ivs-in-unroller
@ -fsplit-wide-types -fstrict-overflow -fthread-jumps -ftoplevel-reorder
@ -ftrapping-math -ftree-ccp -ftree-copy-prop -ftree-copyrename
@ -ftree-cselim -ftree-dce -ftree-dominator-opts -ftree-dse -ftree-fre
@ -ftree-loop-im -ftree-loop-ivcanon -ftree-loop-optimize
@ -ftree-parallelize-loops= -ftree-reassoc -ftree-salias -ftree-scev-cprop
@ -ftree-sink -ftree-sra -ftree-store-ccp -ftree-ter
@ -ftree-vect-loop-version -ftree-vrp -funit-at-a-time -fverbose-asm
@ -fwrapv -fzero-initialized-in-bss -mapcs-frame -mglibc -mlittle-endian

@ Compiler executable checksum: 5b169929a9c648b8270b3cc05210e368

	.text
	.align	2
	.global	foo
	.type	foo, %function
foo:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	mov	ip, sp	@,
	stmfd	sp!, {fp, ip, lr, pc}	@,
	sub	fp, ip, #4	@,,
#APP
@ 16 "/build/buildd/linux-fsl-imx51-2.6.28/kernel/bounds.c" 1
	
->NR_PAGEFLAGS #22 __NR_PAGEFLAGS	@
@ 0 "" 2
@ 17 "/build/buildd/linux-fsl-imx51-2.6.28/kernel/bounds.c" 1
	
->MAX_NR_ZONES #3 __MAX_NR_ZONES	@
@ 0 "" 2
	ldmfd	sp, {fp, sp, pc}	@
	.size	foo, .-foo
	.ident	"GCC: (Ubuntu 4.3.3-5ubuntu4) 4.3.3"
	.section	.note.GNU-stack,"",%progbits
