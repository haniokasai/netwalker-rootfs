/*
 * STMP AUDIOOUT Register Definitions
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

#ifndef __ARCH_ARM___AUDIOOUT_H
#define __ARCH_ARM___AUDIOOUT_H  1

#include <mach/stmp3xxx_regs.h>

#define REGS_AUDIOOUT_BASE (REGS_BASE + 0x48000)
#define REGS_AUDIOOUT_BASE_PHYS (0x80048000)
#define REGS_AUDIOOUT_SIZE 0x00002000
HW_REGISTER(HW_AUDIOOUT_CTRL, REGS_AUDIOOUT_BASE, 0x00000000)
#define HW_AUDIOOUT_CTRL_ADDR (REGS_AUDIOOUT_BASE + 0x00000000)
#define BM_AUDIOOUT_CTRL_SFTRST 0x80000000
#define BM_AUDIOOUT_CTRL_CLKGATE 0x40000000
#define BP_AUDIOOUT_CTRL_DMAWAIT_COUNT      16
#define BM_AUDIOOUT_CTRL_DMAWAIT_COUNT 0x001F0000
#define BF_AUDIOOUT_CTRL_DMAWAIT_COUNT(v)  \
	(((v) << 16) & BM_AUDIOOUT_CTRL_DMAWAIT_COUNT)
#define BM_AUDIOOUT_CTRL_LR_SWAP 0x00004000
#define BM_AUDIOOUT_CTRL_EDGE_SYNC 0x00002000
#define BM_AUDIOOUT_CTRL_INVERT_1BIT 0x00001000
#define BP_AUDIOOUT_CTRL_SS3D_EFFECT      8
#define BM_AUDIOOUT_CTRL_SS3D_EFFECT 0x00000300
#define BF_AUDIOOUT_CTRL_SS3D_EFFECT(v)  \
	(((v) << 8) & BM_AUDIOOUT_CTRL_SS3D_EFFECT)
#define BM_AUDIOOUT_CTRL_WORD_LENGTH 0x00000040
#define BM_AUDIOOUT_CTRL_DAC_ZERO_ENABLE 0x00000020
#define BM_AUDIOOUT_CTRL_LOOPBACK 0x00000010
#define BM_AUDIOOUT_CTRL_FIFO_UNDERFLOW_IRQ 0x00000008
#define BM_AUDIOOUT_CTRL_FIFO_OVERFLOW_IRQ 0x00000004
#define BM_AUDIOOUT_CTRL_FIFO_ERROR_IRQ_EN 0x00000002
#define BM_AUDIOOUT_CTRL_RUN 0x00000001
HW_REGISTER(HW_AUDIOOUT_STAT, REGS_AUDIOOUT_BASE, 0x00000010)
#define HW_AUDIOOUT_STAT_ADDR (REGS_AUDIOOUT_BASE + 0x00000010)
#define BM_AUDIOOUT_STAT_DAC_PRESENT 0x80000000
HW_REGISTER(HW_AUDIOOUT_DACSRR, REGS_AUDIOOUT_BASE, 0x00000020)
#define HW_AUDIOOUT_DACSRR_ADDR (REGS_AUDIOOUT_BASE + 0x00000020)
#define BM_AUDIOOUT_DACSRR_OSR 0x80000000
#define BV_AUDIOOUT_DACSRR_OSR__OSR6  0x0
#define BV_AUDIOOUT_DACSRR_OSR__OSR12 0x1
#define BP_AUDIOOUT_DACSRR_BASEMULT      28
#define BM_AUDIOOUT_DACSRR_BASEMULT 0x70000000
#define BF_AUDIOOUT_DACSRR_BASEMULT(v)  \
	(((v) << 28) & BM_AUDIOOUT_DACSRR_BASEMULT)
#define BV_AUDIOOUT_DACSRR_BASEMULT__SINGLE_RATE 0x1
#define BV_AUDIOOUT_DACSRR_BASEMULT__DOUBLE_RATE 0x2
#define BV_AUDIOOUT_DACSRR_BASEMULT__QUAD_RATE   0x4
#define BP_AUDIOOUT_DACSRR_SRC_HOLD      24
#define BM_AUDIOOUT_DACSRR_SRC_HOLD 0x07000000
#define BF_AUDIOOUT_DACSRR_SRC_HOLD(v)  \
	(((v) << 24) & BM_AUDIOOUT_DACSRR_SRC_HOLD)
#define BP_AUDIOOUT_DACSRR_SRC_INT      16
#define BM_AUDIOOUT_DACSRR_SRC_INT 0x001F0000
#define BF_AUDIOOUT_DACSRR_SRC_INT(v)  \
	(((v) << 16) & BM_AUDIOOUT_DACSRR_SRC_INT)
#define BP_AUDIOOUT_DACSRR_SRC_FRAC      0
#define BM_AUDIOOUT_DACSRR_SRC_FRAC 0x00001FFF
#define BF_AUDIOOUT_DACSRR_SRC_FRAC(v)  \
	(((v) << 0) & BM_AUDIOOUT_DACSRR_SRC_FRAC)
HW_REGISTER(HW_AUDIOOUT_DACVOLUME, REGS_AUDIOOUT_BASE, 0x00000030)
#define HW_AUDIOOUT_DACVOLUME_ADDR (REGS_AUDIOOUT_BASE + 0x00000030)
#define BM_AUDIOOUT_DACVOLUME_VOLUME_UPDATE_LEFT 0x10000000
#define BM_AUDIOOUT_DACVOLUME_EN_ZCD 0x02000000
#define BM_AUDIOOUT_DACVOLUME_MUTE_LEFT 0x01000000
#define BP_AUDIOOUT_DACVOLUME_VOLUME_LEFT      16
#define BM_AUDIOOUT_DACVOLUME_VOLUME_LEFT 0x00FF0000
#define BF_AUDIOOUT_DACVOLUME_VOLUME_LEFT(v)  \
	(((v) << 16) & BM_AUDIOOUT_DACVOLUME_VOLUME_LEFT)
#define BM_AUDIOOUT_DACVOLUME_VOLUME_UPDATE_RIGHT 0x00001000
#define BM_AUDIOOUT_DACVOLUME_MUTE_RIGHT 0x00000100
#define BP_AUDIOOUT_DACVOLUME_VOLUME_RIGHT      0
#define BM_AUDIOOUT_DACVOLUME_VOLUME_RIGHT 0x000000FF
#define BF_AUDIOOUT_DACVOLUME_VOLUME_RIGHT(v)  \
	(((v) << 0) & BM_AUDIOOUT_DACVOLUME_VOLUME_RIGHT)
HW_REGISTER(HW_AUDIOOUT_DACDEBUG, REGS_AUDIOOUT_BASE, 0x00000040)
#define HW_AUDIOOUT_DACDEBUG_ADDR (REGS_AUDIOOUT_BASE + 0x00000040)
#define BM_AUDIOOUT_DACDEBUG_ENABLE_DACDMA 0x80000000
#define BP_AUDIOOUT_DACDEBUG_RAM_SS      8
#define BM_AUDIOOUT_DACDEBUG_RAM_SS 0x00000F00
#define BF_AUDIOOUT_DACDEBUG_RAM_SS(v)  \
	(((v) << 8) & BM_AUDIOOUT_DACDEBUG_RAM_SS)
#define BM_AUDIOOUT_DACDEBUG_SET_INTERRUPT1_CLK_CROSS 0x00000020
#define BM_AUDIOOUT_DACDEBUG_SET_INTERRUPT0_CLK_CROSS 0x00000010
#define BM_AUDIOOUT_DACDEBUG_SET_INTERRUPT1_HAND_SHAKE 0x00000008
#define BM_AUDIOOUT_DACDEBUG_SET_INTERRUPT0_HAND_SHAKE 0x00000004
#define BM_AUDIOOUT_DACDEBUG_DMA_PREQ 0x00000002
#define BM_AUDIOOUT_DACDEBUG_FIFO_STATUS 0x00000001
HW_REGISTER(HW_AUDIOOUT_HPVOL, REGS_AUDIOOUT_BASE, 0x00000050)
#define HW_AUDIOOUT_HPVOL_ADDR (REGS_AUDIOOUT_BASE + 0x00000050)
#define BM_AUDIOOUT_HPVOL_VOLUME_UPDATE_PENDING 0x10000000
#define BM_AUDIOOUT_HPVOL_EN_MSTR_ZCD 0x02000000
#define BM_AUDIOOUT_HPVOL_MUTE 0x01000000
#define BM_AUDIOOUT_HPVOL_SELECT 0x00010000
#define BP_AUDIOOUT_HPVOL_VOL_LEFT      8
#define BM_AUDIOOUT_HPVOL_VOL_LEFT 0x00007F00
#define BF_AUDIOOUT_HPVOL_VOL_LEFT(v)  \
	(((v) << 8) & BM_AUDIOOUT_HPVOL_VOL_LEFT)
#define BP_AUDIOOUT_HPVOL_VOL_RIGHT      0
#define BM_AUDIOOUT_HPVOL_VOL_RIGHT 0x0000007F
#define BF_AUDIOOUT_HPVOL_VOL_RIGHT(v)  \
	(((v) << 0) & BM_AUDIOOUT_HPVOL_VOL_RIGHT)
HW_REGISTER(HW_AUDIOOUT_RESERVED, REGS_AUDIOOUT_BASE, 0x00000060)
#define HW_AUDIOOUT_RESERVED_ADDR (REGS_AUDIOOUT_BASE + 0x00000060)
HW_REGISTER(HW_AUDIOOUT_PWRDN, REGS_AUDIOOUT_BASE, 0x00000070)
#define HW_AUDIOOUT_PWRDN_ADDR (REGS_AUDIOOUT_BASE + 0x00000070)
#define BM_AUDIOOUT_PWRDN_SPEAKER 0x01000000
#define BM_AUDIOOUT_PWRDN_SELFBIAS 0x00100000
#define BM_AUDIOOUT_PWRDN_RIGHT_ADC 0x00010000
#define BM_AUDIOOUT_PWRDN_DAC 0x00001000
#define BM_AUDIOOUT_PWRDN_ADC 0x00000100
#define BM_AUDIOOUT_PWRDN_CAPLESS 0x00000010
#define BM_AUDIOOUT_PWRDN_HEADPHONE 0x00000001
HW_REGISTER(HW_AUDIOOUT_REFCTRL, REGS_AUDIOOUT_BASE, 0x00000080)
#define HW_AUDIOOUT_REFCTRL_ADDR (REGS_AUDIOOUT_BASE + 0x00000080)
#define BM_AUDIOOUT_REFCTRL_FASTSETTLING 0x04000000
#define BM_AUDIOOUT_REFCTRL_RAISE_REF 0x02000000
#define BM_AUDIOOUT_REFCTRL_XTAL_BGR_BIAS 0x01000000
#define BP_AUDIOOUT_REFCTRL_VBG_ADJ      20
#define BM_AUDIOOUT_REFCTRL_VBG_ADJ 0x00700000
#define BF_AUDIOOUT_REFCTRL_VBG_ADJ(v)  \
	(((v) << 20) & BM_AUDIOOUT_REFCTRL_VBG_ADJ)
#define BM_AUDIOOUT_REFCTRL_LOW_PWR 0x00080000
#define BM_AUDIOOUT_REFCTRL_LW_REF 0x00040000
#define BP_AUDIOOUT_REFCTRL_BIAS_CTRL      16
#define BM_AUDIOOUT_REFCTRL_BIAS_CTRL 0x00030000
#define BF_AUDIOOUT_REFCTRL_BIAS_CTRL(v)  \
	(((v) << 16) & BM_AUDIOOUT_REFCTRL_BIAS_CTRL)
#define BM_AUDIOOUT_REFCTRL_VDDXTAL_TO_VDDD 0x00004000
#define BM_AUDIOOUT_REFCTRL_ADJ_ADC 0x00002000
#define BM_AUDIOOUT_REFCTRL_ADJ_VAG 0x00001000
#define BP_AUDIOOUT_REFCTRL_ADC_REFVAL      8
#define BM_AUDIOOUT_REFCTRL_ADC_REFVAL 0x00000F00
#define BF_AUDIOOUT_REFCTRL_ADC_REFVAL(v)  \
	(((v) << 8) & BM_AUDIOOUT_REFCTRL_ADC_REFVAL)
#define BP_AUDIOOUT_REFCTRL_VAG_VAL      4
#define BM_AUDIOOUT_REFCTRL_VAG_VAL 0x000000F0
#define BF_AUDIOOUT_REFCTRL_VAG_VAL(v)  \
	(((v) << 4) & BM_AUDIOOUT_REFCTRL_VAG_VAL)
#define BP_AUDIOOUT_REFCTRL_DAC_ADJ      0
#define BM_AUDIOOUT_REFCTRL_DAC_ADJ 0x00000007
#define BF_AUDIOOUT_REFCTRL_DAC_ADJ(v)  \
	(((v) << 0) & BM_AUDIOOUT_REFCTRL_DAC_ADJ)
HW_REGISTER(HW_AUDIOOUT_ANACTRL, REGS_AUDIOOUT_BASE, 0x00000090)
#define HW_AUDIOOUT_ANACTRL_ADDR (REGS_AUDIOOUT_BASE + 0x00000090)
#define BM_AUDIOOUT_ANACTRL_SHORT_CM_STS 0x10000000
#define BM_AUDIOOUT_ANACTRL_SHORT_LR_STS 0x01000000
#define BP_AUDIOOUT_ANACTRL_SHORTMODE_CM      20
#define BM_AUDIOOUT_ANACTRL_SHORTMODE_CM 0x00300000
#define BF_AUDIOOUT_ANACTRL_SHORTMODE_CM(v)  \
	(((v) << 20) & BM_AUDIOOUT_ANACTRL_SHORTMODE_CM)
#define BP_AUDIOOUT_ANACTRL_SHORTMODE_LR      17
#define BM_AUDIOOUT_ANACTRL_SHORTMODE_LR 0x00060000
#define BF_AUDIOOUT_ANACTRL_SHORTMODE_LR(v)  \
	(((v) << 17) & BM_AUDIOOUT_ANACTRL_SHORTMODE_LR)
#define BP_AUDIOOUT_ANACTRL_SHORT_LVLADJL      12
#define BM_AUDIOOUT_ANACTRL_SHORT_LVLADJL 0x00007000
#define BF_AUDIOOUT_ANACTRL_SHORT_LVLADJL(v)  \
	(((v) << 12) & BM_AUDIOOUT_ANACTRL_SHORT_LVLADJL)
#define BP_AUDIOOUT_ANACTRL_SHORT_LVLADJR      8
#define BM_AUDIOOUT_ANACTRL_SHORT_LVLADJR 0x00000700
#define BF_AUDIOOUT_ANACTRL_SHORT_LVLADJR(v)  \
	(((v) << 8) & BM_AUDIOOUT_ANACTRL_SHORT_LVLADJR)
#define BM_AUDIOOUT_ANACTRL_HP_HOLD_GND 0x00000020
#define BM_AUDIOOUT_ANACTRL_HP_CLASSAB 0x00000010
HW_REGISTER(HW_AUDIOOUT_TEST, REGS_AUDIOOUT_BASE, 0x000000a0)
#define HW_AUDIOOUT_TEST_ADDR (REGS_AUDIOOUT_BASE + 0x000000a0)
#define BP_AUDIOOUT_TEST_HP_ANTIPOP      28
#define BM_AUDIOOUT_TEST_HP_ANTIPOP 0x70000000
#define BF_AUDIOOUT_TEST_HP_ANTIPOP(v)  \
	(((v) << 28) & BM_AUDIOOUT_TEST_HP_ANTIPOP)
#define BM_AUDIOOUT_TEST_TM_ADCIN_TOHP 0x04000000
#define BM_AUDIOOUT_TEST_TM_LOOP 0x02000000
#define BM_AUDIOOUT_TEST_TM_HPCOMMON 0x01000000
#define BP_AUDIOOUT_TEST_HP_I1_ADJ      22
#define BM_AUDIOOUT_TEST_HP_I1_ADJ 0x00C00000
#define BF_AUDIOOUT_TEST_HP_I1_ADJ(v)  \
	(((v) << 22) & BM_AUDIOOUT_TEST_HP_I1_ADJ)
#define BP_AUDIOOUT_TEST_HP_IALL_ADJ      20
#define BM_AUDIOOUT_TEST_HP_IALL_ADJ 0x00300000
#define BF_AUDIOOUT_TEST_HP_IALL_ADJ(v)  \
	(((v) << 20) & BM_AUDIOOUT_TEST_HP_IALL_ADJ)
#define BM_AUDIOOUT_TEST_VAG_CLASSA 0x00002000
#define BM_AUDIOOUT_TEST_VAG_DOUBLE_I 0x00001000
#define BM_AUDIOOUT_TEST_ADCTODAC_LOOP 0x00000008
#define BM_AUDIOOUT_TEST_DAC_CLASSA 0x00000004
#define BM_AUDIOOUT_TEST_DAC_DOUBLE_I 0x00000002
#define BM_AUDIOOUT_TEST_DAC_DIS_RTZ 0x00000001
HW_REGISTER(HW_AUDIOOUT_BISTCTRL, REGS_AUDIOOUT_BASE, 0x000000b0)
#define HW_AUDIOOUT_BISTCTRL_ADDR (REGS_AUDIOOUT_BASE + 0x000000b0)
#define BM_AUDIOOUT_BISTCTRL_FAIL 0x00000008
#define BM_AUDIOOUT_BISTCTRL_PASS 0x00000004
#define BM_AUDIOOUT_BISTCTRL_DONE 0x00000002
#define BM_AUDIOOUT_BISTCTRL_START 0x00000001
HW_REGISTER(HW_AUDIOOUT_BISTSTAT0, REGS_AUDIOOUT_BASE, 0x000000c0)
#define HW_AUDIOOUT_BISTSTAT0_ADDR (REGS_AUDIOOUT_BASE + 0x000000c0)
#define BP_AUDIOOUT_BISTSTAT0_DATA      0
#define BM_AUDIOOUT_BISTSTAT0_DATA 0x00FFFFFF
#define BF_AUDIOOUT_BISTSTAT0_DATA(v)  \
	(((v) << 0) & BM_AUDIOOUT_BISTSTAT0_DATA)
HW_REGISTER(HW_AUDIOOUT_BISTSTAT1, REGS_AUDIOOUT_BASE, 0x000000d0)
#define HW_AUDIOOUT_BISTSTAT1_ADDR (REGS_AUDIOOUT_BASE + 0x000000d0)
#define BP_AUDIOOUT_BISTSTAT1_STATE      24
#define BM_AUDIOOUT_BISTSTAT1_STATE 0x1F000000
#define BF_AUDIOOUT_BISTSTAT1_STATE(v)  \
	(((v) << 24) & BM_AUDIOOUT_BISTSTAT1_STATE)
#define BP_AUDIOOUT_BISTSTAT1_ADDR      0
#define BM_AUDIOOUT_BISTSTAT1_ADDR 0x000000FF
#define BF_AUDIOOUT_BISTSTAT1_ADDR(v)  \
	(((v) << 0) & BM_AUDIOOUT_BISTSTAT1_ADDR)
HW_REGISTER(HW_AUDIOOUT_ANACLKCTRL, REGS_AUDIOOUT_BASE, 0x000000e0)
#define HW_AUDIOOUT_ANACLKCTRL_ADDR (REGS_AUDIOOUT_BASE + 0x000000e0)
#define BM_AUDIOOUT_ANACLKCTRL_CLKGATE 0x80000000
#define BM_AUDIOOUT_ANACLKCTRL_INVERT_DACCLK 0x00000010
#define BP_AUDIOOUT_ANACLKCTRL_DACDIV      0
#define BM_AUDIOOUT_ANACLKCTRL_DACDIV 0x00000007
#define BF_AUDIOOUT_ANACLKCTRL_DACDIV(v)  \
	(((v) << 0) & BM_AUDIOOUT_ANACLKCTRL_DACDIV)
HW_REGISTER(HW_AUDIOOUT_DATA, REGS_AUDIOOUT_BASE, 0x000000f0)
#define HW_AUDIOOUT_DATA_ADDR (REGS_AUDIOOUT_BASE + 0x000000f0)
#define BP_AUDIOOUT_DATA_HIGH      16
#define BM_AUDIOOUT_DATA_HIGH 0xFFFF0000
#define BF_AUDIOOUT_DATA_HIGH(v) \
	(((v) << 16) & BM_AUDIOOUT_DATA_HIGH)
#define BP_AUDIOOUT_DATA_LOW      0
#define BM_AUDIOOUT_DATA_LOW 0x0000FFFF
#define BF_AUDIOOUT_DATA_LOW(v)  \
	(((v) << 0) & BM_AUDIOOUT_DATA_LOW)
HW_REGISTER(HW_AUDIOOUT_SPEAKERCTRL, REGS_AUDIOOUT_BASE, 0x00000100)
#define HW_AUDIOOUT_SPEAKERCTRL_ADDR (REGS_AUDIOOUT_BASE + 0x00000100)
#define BM_AUDIOOUT_SPEAKERCTRL_MUTE 0x01000000
#define BP_AUDIOOUT_SPEAKERCTRL_I1_ADJ      22
#define BM_AUDIOOUT_SPEAKERCTRL_I1_ADJ 0x00C00000
#define BF_AUDIOOUT_SPEAKERCTRL_I1_ADJ(v)  \
	(((v) << 22) & BM_AUDIOOUT_SPEAKERCTRL_I1_ADJ)
#define BP_AUDIOOUT_SPEAKERCTRL_IALL_ADJ      20
#define BM_AUDIOOUT_SPEAKERCTRL_IALL_ADJ 0x00300000
#define BF_AUDIOOUT_SPEAKERCTRL_IALL_ADJ(v)  \
	(((v) << 20) & BM_AUDIOOUT_SPEAKERCTRL_IALL_ADJ)
#define BP_AUDIOOUT_SPEAKERCTRL_POSDRIVER      14
#define BM_AUDIOOUT_SPEAKERCTRL_POSDRIVER 0x0000C000
#define BF_AUDIOOUT_SPEAKERCTRL_POSDRIVER(v)  \
	(((v) << 14) & BM_AUDIOOUT_SPEAKERCTRL_POSDRIVER)
#define BP_AUDIOOUT_SPEAKERCTRL_NEGDRIVER      12
#define BM_AUDIOOUT_SPEAKERCTRL_NEGDRIVER 0x00003000
#define BF_AUDIOOUT_SPEAKERCTRL_NEGDRIVER(v)  \
	(((v) << 12) & BM_AUDIOOUT_SPEAKERCTRL_NEGDRIVER)
HW_REGISTER_0(HW_AUDIOOUT_VERSION, REGS_AUDIOOUT_BASE, 0x00000200)
#define HW_AUDIOOUT_VERSION_ADDR (REGS_AUDIOOUT_BASE + 0x00000200)
#define BP_AUDIOOUT_VERSION_MAJOR      24
#define BM_AUDIOOUT_VERSION_MAJOR 0xFF000000
#define BF_AUDIOOUT_VERSION_MAJOR(v) \
	(((v) << 24) & BM_AUDIOOUT_VERSION_MAJOR)
#define BP_AUDIOOUT_VERSION_MINOR      16
#define BM_AUDIOOUT_VERSION_MINOR 0x00FF0000
#define BF_AUDIOOUT_VERSION_MINOR(v)  \
	(((v) << 16) & BM_AUDIOOUT_VERSION_MINOR)
#define BP_AUDIOOUT_VERSION_STEP      0
#define BM_AUDIOOUT_VERSION_STEP 0x0000FFFF
#define BF_AUDIOOUT_VERSION_STEP(v)  \
	(((v) << 0) & BM_AUDIOOUT_VERSION_STEP)
#endif /* __ARCH_ARM___AUDIOOUT_H */