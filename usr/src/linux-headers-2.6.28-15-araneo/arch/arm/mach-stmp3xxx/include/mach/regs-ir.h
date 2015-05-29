/*
 * STMP IR Register Definitions
 *
 * Copyright 2008-2009 Freescale Semiconductor
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
 */

#ifndef __ARCH_ARM___IR_H
#define __ARCH_ARM___IR_H  1

#include <mach/stmp3xxx_regs.h>

#define REGS_IR_BASE (REGS_BASE + 0x78000)
#define REGS_IR_BASE_PHYS (0x80078000)
#define REGS_IR_SIZE 0x00002000
HW_REGISTER(HW_IR_CTRL, REGS_IR_BASE, 0x00000000)
#define HW_IR_CTRL_ADDR (REGS_IR_BASE + 0x00000000)
#define BM_IR_CTRL_SFTRST 0x80000000
#define BV_IR_CTRL_SFTRST__RUN   0x0
#define BV_IR_CTRL_SFTRST__RESET 0x1
#define BM_IR_CTRL_CLKGATE 0x40000000
#define BP_IR_CTRL_MTA      24
#define BM_IR_CTRL_MTA 0x07000000
#define BF_IR_CTRL_MTA(v)  \
	(((v) << 24) & BM_IR_CTRL_MTA)
#define BV_IR_CTRL_MTA__MTA_10MS  0x0
#define BV_IR_CTRL_MTA__MTA_5MS   0x1
#define BV_IR_CTRL_MTA__MTA_1MS   0x2
#define BV_IR_CTRL_MTA__MTA_500US 0x3
#define BV_IR_CTRL_MTA__MTA_100US 0x4
#define BV_IR_CTRL_MTA__MTA_50US  0x5
#define BV_IR_CTRL_MTA__MTA_10US  0x6
#define BV_IR_CTRL_MTA__MTA_0     0x7
#define BP_IR_CTRL_MODE      22
#define BM_IR_CTRL_MODE 0x00C00000
#define BF_IR_CTRL_MODE(v)  \
	(((v) << 22) & BM_IR_CTRL_MODE)
#define BV_IR_CTRL_MODE__SIR  0x0
#define BV_IR_CTRL_MODE__MIR  0x1
#define BV_IR_CTRL_MODE__FIR  0x2
#define BV_IR_CTRL_MODE__VFIR 0x3
#define BP_IR_CTRL_SPEED      19
#define BM_IR_CTRL_SPEED 0x00380000
#define BF_IR_CTRL_SPEED(v)  \
	(((v) << 19) & BM_IR_CTRL_SPEED)
#define BV_IR_CTRL_SPEED__SPD000 0x0
#define BV_IR_CTRL_SPEED__SPD001 0x1
#define BV_IR_CTRL_SPEED__SPD010 0x2
#define BV_IR_CTRL_SPEED__SPD011 0x3
#define BV_IR_CTRL_SPEED__SPD100 0x4
#define BV_IR_CTRL_SPEED__SPD101 0x5
#define BP_IR_CTRL_TC_TIME_DIV      8
#define BM_IR_CTRL_TC_TIME_DIV 0x00003F00
#define BF_IR_CTRL_TC_TIME_DIV(v)  \
	(((v) << 8) & BM_IR_CTRL_TC_TIME_DIV)
#define BM_IR_CTRL_TC_TYPE 0x00000080
#define BP_IR_CTRL_SIR_GAP      4
#define BM_IR_CTRL_SIR_GAP 0x00000070
#define BF_IR_CTRL_SIR_GAP(v)  \
	(((v) << 4) & BM_IR_CTRL_SIR_GAP)
#define BV_IR_CTRL_SIR_GAP__GAP_10K 0x0
#define BV_IR_CTRL_SIR_GAP__GAP_5K  0x1
#define BV_IR_CTRL_SIR_GAP__GAP_1K  0x2
#define BV_IR_CTRL_SIR_GAP__GAP_500 0x3
#define BV_IR_CTRL_SIR_GAP__GAP_100 0x4
#define BV_IR_CTRL_SIR_GAP__GAP_50  0x5
#define BV_IR_CTRL_SIR_GAP__GAP_10  0x6
#define BV_IR_CTRL_SIR_GAP__GAP_0   0x7
#define BM_IR_CTRL_SIPEN 0x00000008
#define BM_IR_CTRL_TCEN 0x00000004
#define BM_IR_CTRL_TXEN 0x00000002
#define BM_IR_CTRL_RXEN 0x00000001
HW_REGISTER(HW_IR_TXDMA, REGS_IR_BASE, 0x00000010)
#define HW_IR_TXDMA_ADDR (REGS_IR_BASE + 0x00000010)
#define BM_IR_TXDMA_RUN 0x80000000
#define BM_IR_TXDMA_EMPTY 0x20000000
#define BM_IR_TXDMA_INT 0x10000000
#define BM_IR_TXDMA_CHANGE 0x08000000
#define BP_IR_TXDMA_NEW_MTA      24
#define BM_IR_TXDMA_NEW_MTA 0x07000000
#define BF_IR_TXDMA_NEW_MTA(v)  \
	(((v) << 24) & BM_IR_TXDMA_NEW_MTA)
#define BP_IR_TXDMA_NEW_MODE      22
#define BM_IR_TXDMA_NEW_MODE 0x00C00000
#define BF_IR_TXDMA_NEW_MODE(v)  \
	(((v) << 22) & BM_IR_TXDMA_NEW_MODE)
#define BP_IR_TXDMA_NEW_SPEED      19
#define BM_IR_TXDMA_NEW_SPEED 0x00380000
#define BF_IR_TXDMA_NEW_SPEED(v)  \
	(((v) << 19) & BM_IR_TXDMA_NEW_SPEED)
#define BM_IR_TXDMA_BOF_TYPE 0x00040000
#define BP_IR_TXDMA_XBOFS      12
#define BM_IR_TXDMA_XBOFS 0x0003F000
#define BF_IR_TXDMA_XBOFS(v)  \
	(((v) << 12) & BM_IR_TXDMA_XBOFS)
#define BP_IR_TXDMA_XFER_COUNT      0
#define BM_IR_TXDMA_XFER_COUNT 0x00000FFF
#define BF_IR_TXDMA_XFER_COUNT(v)  \
	(((v) << 0) & BM_IR_TXDMA_XFER_COUNT)
HW_REGISTER(HW_IR_RXDMA, REGS_IR_BASE, 0x00000020)
#define HW_IR_RXDMA_ADDR (REGS_IR_BASE + 0x00000020)
#define BM_IR_RXDMA_RUN 0x80000000
#define BP_IR_RXDMA_XFER_COUNT      0
#define BM_IR_RXDMA_XFER_COUNT 0x000003FF
#define BF_IR_RXDMA_XFER_COUNT(v)  \
	(((v) << 0) & BM_IR_RXDMA_XFER_COUNT)
HW_REGISTER(HW_IR_DBGCTRL, REGS_IR_BASE, 0x00000030)
#define HW_IR_DBGCTRL_ADDR (REGS_IR_BASE + 0x00000030)
#define BM_IR_DBGCTRL_VFIRSWZ 0x00001000
#define BV_IR_DBGCTRL_VFIRSWZ__NORMAL 0
#define BV_IR_DBGCTRL_VFIRSWZ__SWAP   1
#define BM_IR_DBGCTRL_RXFRMOFF 0x00000800
#define BM_IR_DBGCTRL_RXCRCOFF 0x00000400
#define BM_IR_DBGCTRL_RXINVERT 0x00000200
#define BM_IR_DBGCTRL_TXFRMOFF 0x00000100
#define BM_IR_DBGCTRL_TXCRCOFF 0x00000080
#define BM_IR_DBGCTRL_TXINVERT 0x00000040
#define BM_IR_DBGCTRL_INTLOOPBACK 0x00000020
#define BM_IR_DBGCTRL_DUPLEX 0x00000010
#define BM_IR_DBGCTRL_MIO_RX 0x00000008
#define BM_IR_DBGCTRL_MIO_TX 0x00000004
#define BM_IR_DBGCTRL_MIO_SCLK 0x00000002
#define BM_IR_DBGCTRL_MIO_EN 0x00000001
HW_REGISTER(HW_IR_INTR, REGS_IR_BASE, 0x00000040)
#define HW_IR_INTR_ADDR (REGS_IR_BASE + 0x00000040)
#define BM_IR_INTR_RXABORT_IRQ_EN 0x00400000
#define BV_IR_INTR_RXABORT_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_RXABORT_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_SPEED_IRQ_EN 0x00200000
#define BV_IR_INTR_SPEED_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_SPEED_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_RXOF_IRQ_EN 0x00100000
#define BV_IR_INTR_RXOF_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_RXOF_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_TXUF_IRQ_EN 0x00080000
#define BV_IR_INTR_TXUF_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_TXUF_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_TC_IRQ_EN 0x00040000
#define BV_IR_INTR_TC_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_TC_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_RX_IRQ_EN 0x00020000
#define BV_IR_INTR_RX_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_RX_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_TX_IRQ_EN 0x00010000
#define BV_IR_INTR_TX_IRQ_EN__DISABLED 0x0
#define BV_IR_INTR_TX_IRQ_EN__ENABLED  0x1
#define BM_IR_INTR_RXABORT_IRQ 0x00000040
#define BV_IR_INTR_RXABORT_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_RXABORT_IRQ__REQUEST    0x1
#define BM_IR_INTR_SPEED_IRQ 0x00000020
#define BV_IR_INTR_SPEED_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_SPEED_IRQ__REQUEST    0x1
#define BM_IR_INTR_RXOF_IRQ 0x00000010
#define BV_IR_INTR_RXOF_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_RXOF_IRQ__REQUEST    0x1
#define BM_IR_INTR_TXUF_IRQ 0x00000008
#define BV_IR_INTR_TXUF_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_TXUF_IRQ__REQUEST    0x1
#define BM_IR_INTR_TC_IRQ 0x00000004
#define BV_IR_INTR_TC_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_TC_IRQ__REQUEST    0x1
#define BM_IR_INTR_RX_IRQ 0x00000002
#define BV_IR_INTR_RX_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_RX_IRQ__REQUEST    0x1
#define BM_IR_INTR_TX_IRQ 0x00000001
#define BV_IR_INTR_TX_IRQ__NO_REQUEST 0x0
#define BV_IR_INTR_TX_IRQ__REQUEST    0x1
HW_REGISTER_0(HW_IR_DATA, REGS_IR_BASE, 0x00000050)
#define HW_IR_DATA_ADDR (REGS_IR_BASE + 0x00000050)
#define BP_IR_DATA_DATA      0
#define BM_IR_DATA_DATA 0xFFFFFFFF
#define BF_IR_DATA_DATA(v)   (v)
HW_REGISTER_0(HW_IR_STAT, REGS_IR_BASE, 0x00000060)
#define HW_IR_STAT_ADDR (REGS_IR_BASE + 0x00000060)
#define BM_IR_STAT_PRESENT 0x80000000
#define BV_IR_STAT_PRESENT__UNAVAILABLE 0x0
#define BV_IR_STAT_PRESENT__AVAILABLE   0x1
#define BP_IR_STAT_MODE_ALLOWED      29
#define BM_IR_STAT_MODE_ALLOWED 0x60000000
#define BF_IR_STAT_MODE_ALLOWED(v)  \
	(((v) << 29) & BM_IR_STAT_MODE_ALLOWED)
#define BV_IR_STAT_MODE_ALLOWED__VFIR 0x0
#define BV_IR_STAT_MODE_ALLOWED__FIR  0x1
#define BV_IR_STAT_MODE_ALLOWED__MIR  0x2
#define BV_IR_STAT_MODE_ALLOWED__SIR  0x3
#define BM_IR_STAT_ANY_IRQ 0x10000000
#define BV_IR_STAT_ANY_IRQ__NO_REQUEST 0x0
#define BV_IR_STAT_ANY_IRQ__REQUEST    0x1
#define BM_IR_STAT_RXABORT_SUMMARY 0x00400000
#define BV_IR_STAT_RXABORT_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_RXABORT_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_SPEED_SUMMARY 0x00200000
#define BV_IR_STAT_SPEED_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_SPEED_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_RXOF_SUMMARY 0x00100000
#define BV_IR_STAT_RXOF_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_RXOF_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_TXUF_SUMMARY 0x00080000
#define BV_IR_STAT_TXUF_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_TXUF_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_TC_SUMMARY 0x00040000
#define BV_IR_STAT_TC_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_TC_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_RX_SUMMARY 0x00020000
#define BV_IR_STAT_RX_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_RX_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_TX_SUMMARY 0x00010000
#define BV_IR_STAT_TX_SUMMARY__NO_REQUEST 0x0
#define BV_IR_STAT_TX_SUMMARY__REQUEST    0x1
#define BM_IR_STAT_MEDIA_BUSY 0x00000004
#define BM_IR_STAT_RX_ACTIVE 0x00000002
#define BM_IR_STAT_TX_ACTIVE 0x00000001
HW_REGISTER(HW_IR_TCCTRL, REGS_IR_BASE, 0x00000070)
#define HW_IR_TCCTRL_ADDR (REGS_IR_BASE + 0x00000070)
#define BM_IR_TCCTRL_INIT 0x80000000
#define BM_IR_TCCTRL_GO 0x40000000
#define BM_IR_TCCTRL_BUSY 0x20000000
#define BM_IR_TCCTRL_TEMIC 0x01000000
#define BV_IR_TCCTRL_TEMIC__LOW  0x0
#define BV_IR_TCCTRL_TEMIC__HIGH 0x1
#define BP_IR_TCCTRL_EXT_DATA      16
#define BM_IR_TCCTRL_EXT_DATA 0x00FF0000
#define BF_IR_TCCTRL_EXT_DATA(v)  \
	(((v) << 16) & BM_IR_TCCTRL_EXT_DATA)
#define BP_IR_TCCTRL_DATA      8
#define BM_IR_TCCTRL_DATA 0x0000FF00
#define BF_IR_TCCTRL_DATA(v)  \
	(((v) << 8) & BM_IR_TCCTRL_DATA)
#define BP_IR_TCCTRL_ADDR      5
#define BM_IR_TCCTRL_ADDR 0x000000E0
#define BF_IR_TCCTRL_ADDR(v)  \
	(((v) << 5) & BM_IR_TCCTRL_ADDR)
#define BP_IR_TCCTRL_INDX      1
#define BM_IR_TCCTRL_INDX 0x0000001E
#define BF_IR_TCCTRL_INDX(v)  \
	(((v) << 1) & BM_IR_TCCTRL_INDX)
#define BM_IR_TCCTRL_C 0x00000001
HW_REGISTER_0(HW_IR_SI_READ, REGS_IR_BASE, 0x00000080)
#define HW_IR_SI_READ_ADDR (REGS_IR_BASE + 0x00000080)
#define BM_IR_SI_READ_ABORT 0x00000100
#define BP_IR_SI_READ_DATA      0
#define BM_IR_SI_READ_DATA 0x000000FF
#define BF_IR_SI_READ_DATA(v)  \
	(((v) << 0) & BM_IR_SI_READ_DATA)
HW_REGISTER_0(HW_IR_DEBUG, REGS_IR_BASE, 0x00000090)
#define HW_IR_DEBUG_ADDR (REGS_IR_BASE + 0x00000090)
#define BM_IR_DEBUG_TXDMAKICK 0x00000020
#define BM_IR_DEBUG_RXDMAKICK 0x00000010
#define BM_IR_DEBUG_TXDMAEND 0x00000008
#define BM_IR_DEBUG_RXDMAEND 0x00000004
#define BM_IR_DEBUG_TXDMAREQ 0x00000002
#define BM_IR_DEBUG_RXDMAREQ 0x00000001
HW_REGISTER_0(HW_IR_VERSION, REGS_IR_BASE, 0x000000a0)
#define HW_IR_VERSION_ADDR (REGS_IR_BASE + 0x000000a0)
#define BP_IR_VERSION_MAJOR      24
#define BM_IR_VERSION_MAJOR 0xFF000000
#define BF_IR_VERSION_MAJOR(v) \
	(((v) << 24) & BM_IR_VERSION_MAJOR)
#define BP_IR_VERSION_MINOR      16
#define BM_IR_VERSION_MINOR 0x00FF0000
#define BF_IR_VERSION_MINOR(v)  \
	(((v) << 16) & BM_IR_VERSION_MINOR)
#define BP_IR_VERSION_STEP      0
#define BM_IR_VERSION_STEP 0x0000FFFF
#define BF_IR_VERSION_STEP(v)  \
	(((v) << 0) & BM_IR_VERSION_STEP)
#endif /* __ARCH_ARM___IR_H */
