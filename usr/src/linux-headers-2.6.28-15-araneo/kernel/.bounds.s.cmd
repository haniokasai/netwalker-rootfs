cmd_kernel/bounds.s := gcc -Wp,-MD,kernel/.bounds.s.d  -nostdinc -isystem /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include -D__KERNEL__ -I/usr/src/linux-headers-lbm- -Iinclude -Iinclude2 -I/build/buildd/linux-fsl-imx51-2.6.28/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include -include include/linux/autoconf.h -Iubuntu/include -I/build/buildd/linux-fsl-imx51-2.6.28/ubuntu/include -mlittle-endian -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/mach-mx51/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include -I/build/buildd/linux-fsl-imx51-2.6.28/. -I. -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -fno-delete-null-pointer-checks -Os -marm -fno-omit-frame-pointer -mapcs -mno-sched-prolog -mabi=aapcs-linux -mno-thumb-interwork -D__LINUX_ARM_ARCH__=7 -march=armv7-a -msoft-float -Uarm -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-inline-functions-called-once -Wdeclaration-after-statement -Wno-pointer-sign -fwrapv  -D"KBUILD_STR(s)=\#s" -D"KBUILD_BASENAME=KBUILD_STR(bounds)"  -D"KBUILD_MODNAME=KBUILD_STR(bounds)"  -fverbose-asm -S -o kernel/bounds.s /build/buildd/linux-fsl-imx51-2.6.28/kernel/bounds.c

deps_kernel/bounds.s := \
  /build/buildd/linux-fsl-imx51-2.6.28/kernel/bounds.c \
  include/linux/page-flags.h \
    $(wildcard include/config/pageflags/extended.h) \
    $(wildcard include/config/unevictable/lru.h) \
    $(wildcard include/config/ia64/uncached/allocator.h) \
    $(wildcard include/config/highmem.h) \
    $(wildcard include/config/swap.h) \
    $(wildcard include/config/s390.h) \
  include/linux/types.h \
    $(wildcard include/config/uid16.h) \
    $(wildcard include/config/lbd.h) \
    $(wildcard include/config/lsf.h) \
    $(wildcard include/config/phys/addr/t/64bit.h) \
  include/linux/posix_types.h \
  include/linux/stddef.h \
  include/linux/compiler.h \
    $(wildcard include/config/enable/must/check.h) \
    $(wildcard include/config/enable/warn/deprecated.h) \
  include/linux/compiler-gcc4.h \
  include/linux/compiler-gcc.h \
    $(wildcard include/config/arch/supports/optimized/inlining.h) \
    $(wildcard include/config/optimize/inlining.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/posix_types.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/types.h \
  include/asm-generic/int-ll64.h \
  include/linux/mmzone.h \
    $(wildcard include/config/force/max/zoneorder.h) \
    $(wildcard include/config/smp.h) \
    $(wildcard include/config/numa.h) \
    $(wildcard include/config/zone/dma.h) \
    $(wildcard include/config/zone/dma32.h) \
    $(wildcard include/config/memory/hotplug.h) \
    $(wildcard include/config/sparsemem.h) \
    $(wildcard include/config/arch/populates/node/map.h) \
    $(wildcard include/config/discontigmem.h) \
    $(wildcard include/config/flat/node/mem/map.h) \
    $(wildcard include/config/cgroup/mem/res/ctlr.h) \
    $(wildcard include/config/have/memory/present.h) \
    $(wildcard include/config/need/node/memmap/size.h) \
    $(wildcard include/config/need/multiple/nodes.h) \
    $(wildcard include/config/have/arch/early/pfn/to/nid.h) \
    $(wildcard include/config/flatmem.h) \
    $(wildcard include/config/sparsemem/extreme.h) \
    $(wildcard include/config/nodes/span/other/nodes.h) \
    $(wildcard include/config/holes/in/zone.h) \
  include/linux/kbuild.h \

kernel/bounds.s: $(deps_kernel/bounds.s)

$(deps_kernel/bounds.s):
