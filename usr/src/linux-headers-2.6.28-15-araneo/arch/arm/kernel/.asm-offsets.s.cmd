cmd_arch/arm/kernel/asm-offsets.s := gcc -Wp,-MD,arch/arm/kernel/.asm-offsets.s.d  -nostdinc -isystem /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include -D__KERNEL__ -I/usr/src/linux-headers-lbm- -Iinclude -Iinclude2 -I/build/buildd/linux-fsl-imx51-2.6.28/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include -include include/linux/autoconf.h -Iubuntu/include -I/build/buildd/linux-fsl-imx51-2.6.28/ubuntu/include -mlittle-endian -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/mach-mx51/include -I/build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include -I/build/buildd/linux-fsl-imx51-2.6.28/. -I. -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -Werror-implicit-function-declaration -fno-delete-null-pointer-checks -Os -marm -fno-omit-frame-pointer -mapcs -mno-sched-prolog -mabi=aapcs-linux -mno-thumb-interwork -D__LINUX_ARM_ARCH__=7 -march=armv7-a -msoft-float -Uarm -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-inline-functions-called-once -Wdeclaration-after-statement -Wno-pointer-sign -fwrapv  -D"KBUILD_STR(s)=\#s" -D"KBUILD_BASENAME=KBUILD_STR(asm_offsets)"  -D"KBUILD_MODNAME=KBUILD_STR(asm_offsets)"  -fverbose-asm -S -o arch/arm/kernel/asm-offsets.s /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/kernel/asm-offsets.c

deps_arch/arm/kernel/asm-offsets.s := \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/kernel/asm-offsets.c \
    $(wildcard include/config/arm/thumbee.h) \
    $(wildcard include/config/iwmmxt.h) \
    $(wildcard include/config/crunch.h) \
    $(wildcard include/config/cpu/has/asid.h) \
  include/linux/sched.h \
    $(wildcard include/config/sched/debug.h) \
    $(wildcard include/config/smp.h) \
    $(wildcard include/config/no/hz.h) \
    $(wildcard include/config/detect/softlockup.h) \
    $(wildcard include/config/core/dump/default/elf/headers.h) \
    $(wildcard include/config/keys.h) \
    $(wildcard include/config/bsd/process/acct.h) \
    $(wildcard include/config/taskstats.h) \
    $(wildcard include/config/audit.h) \
    $(wildcard include/config/inotify/user.h) \
    $(wildcard include/config/epoll.h) \
    $(wildcard include/config/posix/mqueue.h) \
    $(wildcard include/config/user/sched.h) \
    $(wildcard include/config/sysfs.h) \
    $(wildcard include/config/schedstats.h) \
    $(wildcard include/config/task/delay/acct.h) \
    $(wildcard include/config/fair/group/sched.h) \
    $(wildcard include/config/rt/group/sched.h) \
    $(wildcard include/config/preempt/notifiers.h) \
    $(wildcard include/config/blk/dev/io/trace.h) \
    $(wildcard include/config/preempt/rcu.h) \
    $(wildcard include/config/cc/stackprotector.h) \
    $(wildcard include/config/sysvipc.h) \
    $(wildcard include/config/security.h) \
    $(wildcard include/config/auditsyscall.h) \
    $(wildcard include/config/rt/mutexes.h) \
    $(wildcard include/config/debug/mutexes.h) \
    $(wildcard include/config/trace/irqflags.h) \
    $(wildcard include/config/lockdep.h) \
    $(wildcard include/config/task/xacct.h) \
    $(wildcard include/config/cpusets.h) \
    $(wildcard include/config/cgroups.h) \
    $(wildcard include/config/futex.h) \
    $(wildcard include/config/compat.h) \
    $(wildcard include/config/numa.h) \
    $(wildcard include/config/fault/injection.h) \
    $(wildcard include/config/latencytop.h) \
    $(wildcard include/config/have/unstable/sched/clock.h) \
    $(wildcard include/config/hotplug/cpu.h) \
    $(wildcard include/config/preempt/bkl.h) \
    $(wildcard include/config/preempt.h) \
    $(wildcard include/config/tracing.h) \
    $(wildcard include/config/group/sched.h) \
    $(wildcard include/config/mm/owner.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/param.h \
    $(wildcard include/config/hz.h) \
  include/linux/capability.h \
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
  include/linux/threads.h \
    $(wildcard include/config/nr/cpus.h) \
    $(wildcard include/config/base/small.h) \
  include/linux/kernel.h \
    $(wildcard include/config/preempt/voluntary.h) \
    $(wildcard include/config/debug/spinlock/sleep.h) \
    $(wildcard include/config/printk.h) \
    $(wildcard include/config/dynamic/printk/debug.h) \
    $(wildcard include/config/ftrace/mcount/record.h) \
  /usr/lib/gcc/arm-linux-gnueabi/4.3.3/include/stdarg.h \
  include/linux/linkage.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/linkage.h \
  include/linux/bitops.h \
    $(wildcard include/config/generic/find/first/bit.h) \
    $(wildcard include/config/generic/find/next/bit.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/bitops.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/system.h \
    $(wildcard include/config/cpu/xsc3.h) \
    $(wildcard include/config/cpu/sa1100.h) \
    $(wildcard include/config/cpu/sa110.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/memory.h \
    $(wildcard include/config/mmu.h) \
    $(wildcard include/config/page/offset.h) \
    $(wildcard include/config/dram/size.h) \
    $(wildcard include/config/dram/base.h) \
    $(wildcard include/config/zone/dma.h) \
    $(wildcard include/config/discontigmem.h) \
    $(wildcard include/config/sparsemem.h) \
  include/linux/const.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/memory.h \
    $(wildcard include/config/mach/mx35evb.h) \
    $(wildcard include/config/arch/mx51.h) \
    $(wildcard include/config/mach/mx27ads.h) \
    $(wildcard include/config/mach/mx37/3ds.h) \
    $(wildcard include/config/dma/zone/size.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/page.h \
    $(wildcard include/config/cpu/copy/v3.h) \
    $(wildcard include/config/cpu/copy/v4wt.h) \
    $(wildcard include/config/cpu/copy/v4wb.h) \
    $(wildcard include/config/cpu/copy/feroceon.h) \
    $(wildcard include/config/cpu/xscale.h) \
    $(wildcard include/config/cpu/copy/v6.h) \
    $(wildcard include/config/aeabi.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/glue.h \
    $(wildcard include/config/cpu/arm610.h) \
    $(wildcard include/config/cpu/arm710.h) \
    $(wildcard include/config/cpu/abrt/lv4t.h) \
    $(wildcard include/config/cpu/abrt/ev4.h) \
    $(wildcard include/config/cpu/abrt/ev4t.h) \
    $(wildcard include/config/cpu/abrt/ev5tj.h) \
    $(wildcard include/config/cpu/abrt/ev5t.h) \
    $(wildcard include/config/cpu/abrt/ev6.h) \
    $(wildcard include/config/cpu/abrt/ev7.h) \
    $(wildcard include/config/cpu/pabrt/ifar.h) \
    $(wildcard include/config/cpu/pabrt/noifar.h) \
  include/asm-generic/page.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/sizes.h \
  include/asm-generic/memory_model.h \
    $(wildcard include/config/flatmem.h) \
    $(wildcard include/config/sparsemem/vmemmap.h) \
    $(wildcard include/config/out/of/line/pfn/to/page.h) \
  include/linux/irqflags.h \
    $(wildcard include/config/irqsoff/tracer.h) \
    $(wildcard include/config/preempt/tracer.h) \
    $(wildcard include/config/trace/irqflags/support.h) \
    $(wildcard include/config/x86.h) \
  include/linux/typecheck.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/irqflags.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/ptrace.h \
    $(wildcard include/config/arm/thumb.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/hwcap.h \
  include/asm-generic/cmpxchg-local.h \
  include/asm-generic/cmpxchg.h \
  include/asm-generic/bitops/non-atomic.h \
  include/asm-generic/bitops/fls64.h \
  include/asm-generic/bitops/sched.h \
  include/asm-generic/bitops/hweight.h \
  include/asm-generic/bitops/lock.h \
  include/linux/log2.h \
    $(wildcard include/config/arch/has/ilog2/u32.h) \
    $(wildcard include/config/arch/has/ilog2/u64.h) \
  include/linux/ratelimit.h \
  include/linux/param.h \
  include/linux/dynamic_printk.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/byteorder.h \
  include/linux/byteorder/little_endian.h \
  include/linux/byteorder/swab.h \
  include/linux/byteorder/swabb.h \
  include/linux/byteorder/generic.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/bug.h \
    $(wildcard include/config/bug.h) \
    $(wildcard include/config/debug/bugverbose.h) \
  include/asm-generic/bug.h \
    $(wildcard include/config/generic/bug.h) \
  include/linux/timex.h \
  include/linux/time.h \
  include/linux/cache.h \
    $(wildcard include/config/arch/has/cache/line/size.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/cache.h \
  include/linux/seqlock.h \
  include/linux/spinlock.h \
    $(wildcard include/config/debug/spinlock.h) \
    $(wildcard include/config/generic/lockbreak.h) \
    $(wildcard include/config/debug/lock/alloc.h) \
  include/linux/preempt.h \
    $(wildcard include/config/debug/preempt.h) \
  include/linux/thread_info.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/thread_info.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/fpstate.h \
    $(wildcard include/config/vfpv3.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/domain.h \
    $(wildcard include/config/io/36.h) \
  include/linux/list.h \
    $(wildcard include/config/debug/list.h) \
  include/linux/poison.h \
  include/linux/prefetch.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/processor.h \
  include/linux/stringify.h \
  include/linux/bottom_half.h \
  include/linux/spinlock_types.h \
  include/linux/spinlock_types_up.h \
  include/linux/lockdep.h \
    $(wildcard include/config/lock/stat.h) \
    $(wildcard include/config/generic/hardirqs.h) \
    $(wildcard include/config/prove/locking.h) \
  include/linux/spinlock_up.h \
  include/linux/spinlock_api_up.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/atomic.h \
  include/asm-generic/atomic.h \
  include/linux/math64.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/div64.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/timex.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/timex.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/hardware.h \
    $(wildcard include/config/arch/mx3.h) \
    $(wildcard include/config/arch/mx35.h) \
    $(wildcard include/config/arch/mx37.h) \
    $(wildcard include/config/arch/mx21.h) \
    $(wildcard include/config/arch/mx25.h) \
    $(wildcard include/config/arch/mx27.h) \
    $(wildcard include/config/mxc/pseudo/irqs.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/mx51.h \
    $(wildcard include/config/mxc/security/scc2.h) \
    $(wildcard include/config/sdma/iram.h) \
    $(wildcard include/config/sdma/iram/size.h) \
    $(wildcard include/config/snd/mxc/soc/iram.h) \
    $(wildcard include/config/mxc/vpu/iram.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/mxc.h \
  include/linux/jiffies.h \
  include/linux/rbtree.h \
  include/linux/cpumask.h \
    $(wildcard include/config/debug/per/cpu/maps.h) \
    $(wildcard include/config/cpumask/offstack.h) \
  include/linux/bitmap.h \
  include/linux/string.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/string.h \
  include/linux/errno.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/errno.h \
  include/asm-generic/errno.h \
  include/asm-generic/errno-base.h \
  include/linux/nodemask.h \
    $(wildcard include/config/highmem.h) \
  include/linux/numa.h \
    $(wildcard include/config/nodes/shift.h) \
  include/linux/mm_types.h \
    $(wildcard include/config/split/ptlock/cpus.h) \
    $(wildcard include/config/proc/fs.h) \
    $(wildcard include/config/mmu/notifier.h) \
  include/linux/auxvec.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/auxvec.h \
  include/linux/prio_tree.h \
  include/linux/rwsem.h \
    $(wildcard include/config/rwsem/generic/spinlock.h) \
  include/linux/rwsem-spinlock.h \
  include/linux/completion.h \
  include/linux/wait.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/current.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/mmu.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/cputime.h \
  include/asm-generic/cputime.h \
  include/linux/smp.h \
    $(wildcard include/config/use/generic/smp/helpers.h) \
  include/linux/sem.h \
  include/linux/ipc.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/ipcbuf.h \
  include/linux/kref.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/sembuf.h \
  include/linux/rcupdate.h \
    $(wildcard include/config/classic/rcu.h) \
  include/linux/percpu.h \
    $(wildcard include/config/modules.h) \
  include/linux/slab.h \
    $(wildcard include/config/slab/debug.h) \
    $(wildcard include/config/debug/objects.h) \
    $(wildcard include/config/slub.h) \
    $(wildcard include/config/slob.h) \
    $(wildcard include/config/debug/slab.h) \
  include/linux/gfp.h \
    $(wildcard include/config/zone/dma32.h) \
  include/linux/mmzone.h \
    $(wildcard include/config/force/max/zoneorder.h) \
    $(wildcard include/config/unevictable/lru.h) \
    $(wildcard include/config/memory/hotplug.h) \
    $(wildcard include/config/arch/populates/node/map.h) \
    $(wildcard include/config/flat/node/mem/map.h) \
    $(wildcard include/config/cgroup/mem/res/ctlr.h) \
    $(wildcard include/config/have/memory/present.h) \
    $(wildcard include/config/need/node/memmap/size.h) \
    $(wildcard include/config/need/multiple/nodes.h) \
    $(wildcard include/config/have/arch/early/pfn/to/nid.h) \
    $(wildcard include/config/sparsemem/extreme.h) \
    $(wildcard include/config/nodes/span/other/nodes.h) \
    $(wildcard include/config/holes/in/zone.h) \
  include/linux/init.h \
    $(wildcard include/config/hotplug.h) \
  include/linux/pageblock-flags.h \
    $(wildcard include/config/hugetlb/page.h) \
    $(wildcard include/config/hugetlb/page/size/variable.h) \
  include/linux/bounds.h \
  include/linux/memory_hotplug.h \
    $(wildcard include/config/have/arch/nodedata/extension.h) \
    $(wildcard include/config/memory/hotremove.h) \
  include/linux/notifier.h \
  include/linux/mutex.h \
  include/linux/srcu.h \
  include/linux/topology.h \
    $(wildcard include/config/sched/smt.h) \
    $(wildcard include/config/sched/mc.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/topology.h \
  include/asm-generic/topology.h \
  include/linux/slub_def.h \
    $(wildcard include/config/slub/stats.h) \
    $(wildcard include/config/slub/debug.h) \
  include/linux/workqueue.h \
  include/linux/timer.h \
    $(wildcard include/config/timer/stats.h) \
    $(wildcard include/config/debug/objects/timers.h) \
  include/linux/ktime.h \
    $(wildcard include/config/ktime/scalar.h) \
  include/linux/debugobjects.h \
    $(wildcard include/config/debug/objects/free.h) \
  include/linux/kobject.h \
  include/linux/sysfs.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/percpu.h \
  include/asm-generic/percpu.h \
    $(wildcard include/config/have/setup/per/cpu/area.h) \
  include/linux/rcuclassic.h \
    $(wildcard include/config/rcu/cpu/stall/detector.h) \
  include/linux/signal.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/signal.h \
  include/asm-generic/signal.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/sigcontext.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/siginfo.h \
  include/asm-generic/siginfo.h \
  include/linux/fs_struct.h \
  include/linux/path.h \
  include/linux/pid.h \
  include/linux/proportions.h \
  include/linux/percpu_counter.h \
  include/linux/seccomp.h \
    $(wildcard include/config/seccomp.h) \
  include/linux/rtmutex.h \
    $(wildcard include/config/debug/rt/mutexes.h) \
  include/linux/plist.h \
    $(wildcard include/config/debug/pi/list.h) \
  include/linux/resource.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/resource.h \
  include/asm-generic/resource.h \
  include/linux/hrtimer.h \
    $(wildcard include/config/high/res/timers.h) \
  include/linux/task_io_accounting.h \
    $(wildcard include/config/task/io/accounting.h) \
  include/linux/latencytop.h \
  include/linux/cred.h \
  include/linux/aio.h \
    $(wildcard include/config/aio.h) \
  include/linux/aio_abi.h \
  include/linux/uio.h \
  include/linux/mm.h \
    $(wildcard include/config/sysctl.h) \
    $(wildcard include/config/stack/growsup.h) \
    $(wildcard include/config/swap.h) \
    $(wildcard include/config/shmem.h) \
    $(wildcard include/config/ia64.h) \
    $(wildcard include/config/debug/pagealloc.h) \
    $(wildcard include/config/hibernation.h) \
  include/linux/mmdebug.h \
    $(wildcard include/config/debug/vm.h) \
    $(wildcard include/config/debug/virtual.h) \
  include/linux/debug_locks.h \
    $(wildcard include/config/debug/locking/api/selftests.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/pgtable.h \
  include/asm-generic/4level-fixup.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/proc-fns.h \
    $(wildcard include/config/cpu/32.h) \
    $(wildcard include/config/cpu/arm7tdmi.h) \
    $(wildcard include/config/cpu/arm720t.h) \
    $(wildcard include/config/cpu/arm740t.h) \
    $(wildcard include/config/cpu/arm9tdmi.h) \
    $(wildcard include/config/cpu/arm920t.h) \
    $(wildcard include/config/cpu/arm922t.h) \
    $(wildcard include/config/cpu/arm925t.h) \
    $(wildcard include/config/cpu/arm926t.h) \
    $(wildcard include/config/cpu/arm940t.h) \
    $(wildcard include/config/cpu/arm946e.h) \
    $(wildcard include/config/cpu/arm1020.h) \
    $(wildcard include/config/cpu/arm1020e.h) \
    $(wildcard include/config/cpu/arm1022.h) \
    $(wildcard include/config/cpu/arm1026.h) \
    $(wildcard include/config/cpu/feroceon.h) \
    $(wildcard include/config/cpu/v6.h) \
    $(wildcard include/config/cpu/v7.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/cpu-single.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/plat-mxc/include/mach/vmalloc.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/pgtable-hwdef.h \
  include/asm-generic/pgtable.h \
  include/linux/page-flags.h \
    $(wildcard include/config/pageflags/extended.h) \
    $(wildcard include/config/ia64/uncached/allocator.h) \
    $(wildcard include/config/s390.h) \
  include/linux/vmstat.h \
    $(wildcard include/config/vm/event/counters.h) \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/mach/arch.h \
  /build/buildd/linux-fsl-imx51-2.6.28/arch/arm/include/asm/procinfo.h \
  include/linux/kbuild.h \

arch/arm/kernel/asm-offsets.s: $(deps_arch/arm/kernel/asm-offsets.s)

$(deps_arch/arm/kernel/asm-offsets.s):
