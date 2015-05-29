/*
 * Copyright (C) 2005 Sigmatel Inc
 *
 * Copyright 2008-2009 Freescale Semiconductor, Inc. All Rights Reserved.
 * Copyright 2008 Embedded Alley Solutions, Inc All Rights Reserved.
 */

/*
 * The code contained herein is licensed under the GNU General Public
 * License. You may obtain a copy of the GNU General Public License
 * Version 2 or later at the following locations:
 *
 * http://www.opensource.org/licenses/gpl-license.html
 * http://www.gnu.org/copyleft/gpl.html
 */
#ifndef __ASM_ARCH_SYSTEM_H
#define __ASM_ARCH_SYSTEM_H

#include <asm/proc-fns.h>
#include <mach/regs-clkctrl.h>
#include <mach/regs-power.h>

static inline void arch_idle(void)
{
	/*
	 * This should do all the clock switching
	 * and wait for interrupt tricks
	 */

	cpu_do_idle();
}

static inline void arch_reset(char mode)
{
	/* Set BATTCHRG to default value */
	HW_POWER_CHARGE_WR(0x00010000);

	/* Set MINPWR to default value   */
	HW_POWER_MINPWR_WR(0);

	/* Reset digital side of chip (but not power or RTC) */
	HW_CLKCTRL_RESET_WR(BM_CLKCTRL_RESET_DIG);

	/* Should not return */
}

#endif
