/*
 * Copyright 2004-2009 Freescale Semiconductor, Inc. All Rights Reserved.
 *
 */

/*
 * The code contained herein is licensed under the GNU Lesser General
 * Public License.  You may obtain a copy of the GNU Lesser General
 * Public License Version 2.1 or later at the following locations:
 *
 * http://www.opensource.org/licenses/lgpl-license.html
 * http://www.gnu.org/copyleft/lgpl.html
 */

/*!
 * @file mxc_ipu_hl_lib.h
 *
 * @brief IPU high level library implementation
 *
 * How to use ipu lib?
 *
 * 1. mxc_ipu_lib_task_init()
 *
 * First, call mxc_ipu_lib_task_init() function with user defined setting.
 * user could set input/overlay/output setting like width/height/format/
 * input crop/output to framebuffer etc.
 * User can allocate input, overlay and output buffer by themselves(must be
 * physical continuous), if user allocated buffers by themselves, they must set
 * parameter user_def_paddr in ipu_lib_input_param_t/ipu_lib_output_param_t.
 * For OP_STREAM_MODE mode, they should set both of user_def_paddr[2], for
 * OP_NORMAL_MODE mode they only need set user_def_paddr[0].
 * mxc_ipu_lib_task_init() will return inbuf_start/ovbuf_start/outbuf_start
 * in ipu_handle if user did not set user_def_paddr, these are virtual buffer
 * start address allocated by ipu lib.
 * User should fill input/overlay data into user_def_paddr or inbuf_start/
 * ovbuf_start before call function mxc_ipu_lib_task_buf_update().
 *
 * NOTE: overlay is a special function of ipu, which can combine input and
 * overlay to one output based on alpha and color-key setting. Both global
 * alpha blending and local alpha blending are supported. You should set
 * corresponding enable flag in ipu_lib_overlay_param_t. If you want to use
 * local alpha blending, you need set user_def_alpha_paddr in
 * ipu_lib_overlay_param_t and fill in alpha data before call function
 * mxc_ipu_lib_task_init(). Pay attention that overlay's width/height
 * should be the same as output. If user do not want to use overlay function,
 * then just let this parameter to NULL.
 *
 * 2. mxc_ipu_lib_task_buf_update()
 *
 * User should call mxc_ipu_lib_task_buf_update() function after they finish fill
 * input/overlay data into input/overlay user_def_paddr(user allocated buffer)
 * or inbuf_start/ovbuf_start(ipu lib allocated buffer).
 * At first time calling this update function, for OP_STREAM_MODE mode,
 * user should fill data to both input buffer inbuf_start[2], for
 * OP_NORMAL_MODE mode user only need to fill inbuf_start[0]; next time
 * calling this update function, user only need to fill buffer accoring to the index
 * return by mxc_ipu_lib_task_buf_update() last time.
 * Above method is using buffers allocated by ipu lib, user can also use buffers
 * allocated by themselves:
 *
 * User defined buffer queue example(OP_STREAM_MODE mode):
 * a. user allocate 5 physical continuous memory buffers: paddr[0~4];
 * b. set input.user_def_paddr[2] as paddr[0] and paddr[1];
 * c. call mxc_ipu_lib_task_init();
 * d. fill input data to paddr[0] and paddr[1];
 * e. call mxc_ipu_lib_task_buf_update();
 * f. fill input data to paddr[2];
 * g. call mxc_ipu_lib_task_buf_update(..&paddr[2]..);
 *
 * In mxc_ipu_lib_task_buf_update() function, ipu lib will call
 * output_callback(void *arg, int output_buf_index)
 * (if user set this call back function in parameter) while there is output data,
 * user could handle output data by paddr[output_buf_index]/outbuf_start[output_buf_index].
 * Please find detail info in the fucntion description below.
 *
 * 3. mxc_ipu_lib_task_uninit()
 *
 * User should call uninit function after they want to disable ipu task.
 *
 * @ingroup IPU
 */
#ifndef __MXC_IPU_HL_LIB_H__
#define __MXC_IPU_HL_LIB_H__

#ifdef __cplusplus
extern "C"{
#endif

#include <linux/ipu.h>
#include <linux/mxcfb.h>

/*
 * ipu task modes.
 *
 * User can specify what IPU-IC task they want, like ENV, VF or PP.
 * User can specify what kind of operation mode they want, like normal mode
 * for single buffer method, stream mode for double buffer method.
 */
enum {
	TASK_ENC_MODE = 0x1,
	TASK_VF_MODE = 0x2,
	TASK_PP_MODE = 0x4,

	OP_NORMAL_MODE = 0x10,
	OP_STREAM_MODE = 0x20,
};

/*
 * input parameter settings.
 *
 * These settings include input crop setting, which can get crop window
 * needed from input image for ipu task. The pos means the input crop window
 * position in the input image and win_w/win_h mean the width/height of input
 * crop window.
 *
 * User can define allocated input buffer phyaddr by setting paddr parameter.
 * If user define it, ipu lib will not allocate new dma buffer for task.
 * (NOTE: If use OP_STREAM_MODE mode, user should specify two paddr value.)
 * If not, ipu lib will allocate new dma buffer for task, and will give out
 * the virtual address(after mmap) through ipu_handle.inbuf_start.
 */
typedef struct {
	unsigned int width;
	unsigned int height;
	unsigned int fmt;

	struct {
		struct mxcfb_pos pos;
		unsigned int win_w;
		unsigned int win_h;
	} input_crop_win;

	dma_addr_t user_def_paddr[2];
} ipu_lib_input_param_t;

typedef struct {
	unsigned int width;
	unsigned int height;
	unsigned int fmt;

	struct {
		struct mxcfb_pos pos;
		unsigned int win_w;
		unsigned int win_h;
	} ov_crop_win;

	dma_addr_t user_def_paddr[2];
	dma_addr_t user_def_alpha_paddr[2];

	unsigned char global_alpha_en;
	unsigned char local_alpha_en;
	unsigned char key_color_en;
	unsigned char alpha; /* 0 ~ 255*/
	unsigned int key_color; /* RBG 24bit */
} ipu_lib_overlay_param_t;

/*
 * output parameter settings.
 *
 * These settings include output window setting if user enabled show to
 * framebuffer, which include fb device number want to display and its
 * position.
 *
 * User can define allocated output buffer phyaddr by setting paddr parameter.
 * If user define it, ipu lib will not allocate new dma buffer for task.
 * (NOTE: If use OP_STREAM_MODE mode, user should specify two paddr value.)
 * If not, ipu lib will allocate new dma buffer for task, and will give out
 * the virtual address(after mmap) through ipu_handle.outbuf_start.
 *
 * If user want display output to framebuffer dirrectly, please set show_to_fb
 * as true value, and parameter pos control the windows position of display window
 * in fb, fb_num is the fb device index number, for example, fb_num = 2 means
 * display to fb device /dev/fb2.
 *
 * Please do not set paddr if you want to display output to fb dirrectly.
 */
typedef struct {
	unsigned int width;
	unsigned int height;
	unsigned int fmt;
	unsigned int rot;

	dma_addr_t user_def_paddr[2];

	int show_to_fb;
	struct {
		struct mxcfb_pos pos;
		unsigned int fb_num;
	} fb_disp;

	/* output_win is doing similar thing as fb_disp */
	/* they output data to part of the whole output */
	struct {
		struct mxcfb_pos pos;
		unsigned int win_w;
		unsigned int win_h;
	} output_win;
} ipu_lib_output_param_t;

/*
 * ipu task handle.
 *
 * This handle will be return after mxc_ipu_lib_task_init function.
 * If user did not define paddr of input/output buffer, then they can get
 * virtual address of input/output buffer by inbuf_start/outbuf_start
 * which allocated by ipu lib.
 * The ifr_size/ofr_size indicate the size of input/output buffer.
 * User should not care the priv parameter and DO NOT change it.
 */
typedef struct {
        void * inbuf_start[2];
        void * ovbuf_start[2];
        void * ovbuf_alpha_start[2];
	void * outbuf_start0[2];
	void * outbuf_start1[2];
	int ifr_size;
	int ovfr_size;
	int ovfr_alpha_size;
	int ofr_size[2];

	void * priv;
} ipu_lib_handle_t;

/*!
 * This function init the ipu task according to param setting.
 *
 * @param	input		Input parameter for ipu task.
 *
 * @param	overlay		Overlay parameter for ipu task.
 *
 * @param	output0		The first output paramter for ipu task.
 *
 * @param	output1 	Ipu can support 2 output after postprocess
 * 				from 1 input, this is second one's setting.
 * 				If user want 2 outputs both display to fb,
 * 				please make sure output0 is on fb0.
 *
 * @param	mode		The ipu mode user can define, refer to
 * 				header file.
 *
 * @param	ipu_handle	User just allocate this structure for init.
 * 				this parameter will provide some necessary
 * 				info after task init function.
 *
 * @return	This function returns 0 on success or negative error code on
 * 		fail.
 */
int mxc_ipu_lib_task_init(ipu_lib_input_param_t * input,
		ipu_lib_overlay_param_t * overlay,
		ipu_lib_output_param_t * output0,
		ipu_lib_output_param_t * output1,
		int mode, ipu_lib_handle_t * ipu_handle);

/*!
 * This function uninit the ipu task for special ipu handle.
 *
 * @param	ipu_handle	The ipu task handle need to un-init.
 *
 * @return	This function returns 0 on success or negative error code on
 * 		fail.
 */
void mxc_ipu_lib_task_uninit(ipu_lib_handle_t * ipu_handle);

/*!
 * This function update the buffer for special ipu task, it must be run after
 * init function.
 * For OP_STREAM_MODE mode, ipu task will take double buffer method, this function
 * will return the next need-update buffer index number(0 or 1) on success, user
 * should update input buffer according to it.
 * Similar with it, output_callback's second parameter indicates the current output
 * buffer index number(0 or 1), user should read output data from exact buffer
 * according to it.
 * For OP_NORMAL_MODE mode, ipu task will take single buffer method, so this function
 * will always return 0 on success(next update buffer will keep on index 0), the same,
 * output_callback's second parameter will keep on 0 too.
 * How to update input buffer? If user has phys buffer themselves, please just update
 * the phys buffer address by parameter phyaddr; if not, user can fill the input data
 * to ipu_handle->inbuf_start[].
 *
 * @param	ipu_handle	The ipu task handle need to update buffer.
 *
 * @param	new_inbuf_paddr	User can set phyaddr to their own allocated
 * 				buffer addr, ipu lib will update the buffer
 * 				from this address for process. If user do not
 * 				want to use it, please let it be zero, and
 * 				fill the buffer according to inbuf_start
 * 				parameter in ipu_handle.
 *
 * @param	new_ovbuf_paddr User defined overlay physical buffer address.
 *
 * @param	new_ovbuf_alpha_paddr User defined overlay local alpha blending
 *		physical buffer address.
 *
 * @param	output_callback	IPU lib will call output_callback funtion
 * 				when there is output data.
 *
 * @param	output_cb_arg	The argument will be passed to output_callback.
 *
 * @return	This function returns the next update buffer index number on success
 * 		or negative error code on fail.
 */
int mxc_ipu_lib_task_buf_update(ipu_lib_handle_t * ipu_handle,
	dma_addr_t new_inbuf_paddr, dma_addr_t new_ovbuf_paddr,
	dma_addr_t new_ovbuf_alpha_paddr, void (output_callback)(void *, int),
	void * output_cb_arg);

#ifdef __cplusplus
}
#endif

#endif
