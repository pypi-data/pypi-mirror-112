__version__ = "1.0.0"

'''
////////////////////////////////////////////////////////////
//  Ver.1.0.0  (2021.06.8) 
////////////////////////////////////////////////////////////
●正式版初版

////////////////////////////////////////////////////////////
//  Ver.0.0.12  (2021.04.12) 
////////////////////////////////////////////////////////////
●プレビュー版
'''

import numpy as np
import sys
import time
from typing import Union, List, Tuple

from acapy import acaplib2

# pylint: disable=W0311

# クラス名の置き換え
class ACL_BUFF_INFO_RESIZE(acaplib2.ACL_BUFF_INFO_RESIZE):
    pass

class ACL_BUFF_INFO_ROI(acaplib2.ACL_BUFF_INFO_ROI):
    pass

class ACL_REGION(acaplib2.ACL_REGION):
    pass

class ACL_BUFF_INFO_DIVIDE(acaplib2.ACL_BUFF_INFO_DIVIDE):
    pass

class AcaPy():
    '''Python bindings for AVALDATA AcapLib2
    '''

    # クラス変数
    OK : int								= acaplib2.ACL_RTN_OK		# エラーなし
    ERROR : int							    = acaplib2.ACL_RTN_ERROR	# エラーあり

    def __init__(self, board_id: int = 0, ch: int = 1, debug_print: bool = True):
        '''Initialize the device

        Parameters
        ----------
        board_id : int
            Specify board number which is set up
        ch : int
            The channel(>=1) to open  
        debug_print : bool
            True to output debug information.

        Returns
        -------
            AcaPy class object

        '''

        # プロパティ初期値

        # AcapLib2のDLLファイルバージョンの取得
        ret, self.__acaplib2_version = acaplib2.AcapGetFileVersion(acaplib2._acap_dll_path)
        #self.__acaplib2_version = self.__acaplib2_version.split('.')

        self.__hHandle = acaplib2.INVALID_HANDLE_VALUE
        self.__board_name = b''
        self.__board_id = board_id
        self.__ch = ch
        self.__scan_system = 0
        self.__width = 640
        self.__height = 480
        self.__mem_num : int = 4
        self.__x_delay = 0
        self.__y_delay = 0
        self.__y_total = 480
        self.__camera_bit = 8
        self.__board_bit = 8
        self.__pix_shift = 0
        self.__timeout = 1000
        self.__cc_polarity = 0
        self.__trigger_polarity = 0
        self.__cc1_polarity = 0
        self.__cc2_polarity = 0
        self.__cc3_polarity = 0
        self.__cc4_polarity = 0
        self.__cc_cycle = 0
        self.__cc_cycle_ex = 0
        self.__exposure = 0
        self.__exposure_ex = 0
        self.__cc_delay = 0
        self.__cc_out_no = 0
        self.__rolling_shutter = 0
        self.__external_trigger_enable = 0
        self.__external_trigger_mode = 0
        self.__external_trigger_chatter = 0
        self.__external_trigger_delay = 0
        self.__encoder_enable = 0
        self.__encoder_start = 0
        self.__encoder_mode = 0
        self.__encoder_phase = 0
        self.__encoder_direction = 0
        self.__encoder_z_phase = 0
        self.__encoder_compare_reg_1 = 0
        self.__encoder_compare_reg_2 = 0
        self.__encoder_abs_mode = 0
        self.__encoder_abs_start = 0
        self.__strobe_enable = 0
        self.__strobe_delay = 0
        self.__strobe_time = 0
        self.__reverse_dma_enable = 0
        self.__dval_enable = 0

        self.__tap_num = 0
        self.__tap_arrange = 0
        self.__tap_arrange_x_size = 0

        self.__tap_direction1 = 0
        self.__tap_direction2 = 0
        self.__tap_direction3 = 0
        self.__tap_direction4 = 0
        self.__tap_direction5 = 0
        self.__tap_direction6 = 0
        self.__tap_direction7 = 0
        self.__tap_direction8 = 0

        self.__sync_lt = 0
        self.__gpout_sel = 0
        self.__gpout_pol = 0
        self.__interrupt_line = 0
        self.__trigger_enable = 0
        self.__data_mask_lower = 0
        self.__data_mask_upper = 0
        self.__chatter_separate = 0
        self.__gpin_pin_sel = 0
        self.__sync_ch = 0
        self.__bayer_enable = 0
        self.__bayer_grid = 0
        self.__bayer_input_bit = 0
        self.__bayer_output_bit = 0
        self.__strobe_pol = 0
        self.__vertical_remap = 0
        self.__express_link = 0
        self.__fpga_version = 0
        self.__lval_delay = 0
        self.__line_reverse = 0
        self.__start_frame_no = 0
        self.__buffer_zero_fill = 0
        self.__cc_stop = 0
        self.__lvds_cclk_sel = 0
        self.__lvds_phase_sel = 0
        self.__lvds_synclt_sel = 0
        self.__pocl_lite_enable = 0

        self.__cxp_link_speed = 0
        self.__cxp_bitrate = 0
        self.__cxp_acquision_start_address = 0
        self.__cxp_acquision_start_value = 0
        self.__cxp_acquision_stop_address = 0
        self.__cxp_acquision_stop_value = 0
        self.__cxp_pixel_format_address = 0
        self.__cxp_pixel_format = 0
        self.__rgb_swap_enable = 0
        self.__narrow10bit_enable = 0

        self.__virtual_comport = 0
        self.__driver_name = 0
        self.__hw_protect = 0
        self.__images : List[np.ndarray] = []

        self.__is_opened : bool = False
        self.__is_grab = False
        self.__last_frame_no = 0
        self.__input_num = 0

        self.__is_serial_open = False

        self.__debug_print = debug_print

        self.__infrared_enable = 0 # ACL_INFRARED_ENABLE

        # ボード情報の取得
        ret, bdInfo = acaplib2.AcapGetBoardInfoEx()
        if ret != AcaPy.OK:
            self.print_last_error()

        boardnum = bdInfo.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        # 指定されたボード番号の検索
        board_index = None
        for i in range(boardnum):
            if board_id == bdInfo.boardIndex[i].nBoardID:
                board_index = bdInfo.boardIndex[i]
                break

        if board_index is None:
            # 指定されたボード番号が見つからなかったとき
            return

        # ch == 0 の全チャンネルオープンは非対応
        if ch < 1:
            return      
        # チャンネル番号の確認
        if ch > board_index.nChannelNum:
            return

        # プロパティの値を取得
        self.__board_id = board_id
        self.__board_name = board_index.pBoardName
        self.__device = board_index.nDevice
        self.__custom = board_index.nCustom
        self.__channel_num = board_index.nChannelNum
        self.__serial_no = board_index.nSerialNo

        # ボードオープン
        self.__hHandle = acaplib2.AcapOpen(board_index.pBoardName, board_index.nBoardID, ch)
        if self.__hHandle == acaplib2.INVALID_HANDLE_VALUE:
            # 二重オープンなど
            self.print_last_error()
            return
        else:
            self._debug_print("Python version:", sys.version)
            self._debug_print("AcaPy version:", __version__)
            self._debug_print("AcapLib2 version:", self.__acaplib2_version)
            self._debug_print("AcapOpen: boardname = {0}, bordID = {1}, Ch = {2}, handle = {3}".format(board_index.pBoardName, board_index.nBoardID, ch, self.__hHandle))
            
        self.__ch = ch

        self.__is_opened = True
        self.__refrect_param_flag = True # refrect_paramが必要な場合はTrue

        # イベント登録
        self._set_event(acaplib2.ACL_INT_GRABSTART, 1)
        self._set_event(acaplib2.ACL_INT_FRAMEEND, 1)
        self._set_event(acaplib2.ACL_INT_GRABEND, 1)
        self._set_event(acaplib2.ACL_INT_GPIN, 1)

    def __del__(self):

        if self.__is_grab == True:
            self.grab_abort()

        self.serial_close()

        if self.__hHandle != acaplib2.INVALID_HANDLE_VALUE:
            # バッファを解除
            acaplib2.AcapSetBufferAddress(
                self.__hHandle, 
                self.__ch, 
                acaplib2.ACL_IMAGE_PTR, 
                0, 
                0)
            # イベント解除
            self._set_event(acaplib2.ACL_INT_GRABSTART, 0)
            self._set_event(acaplib2.ACL_INT_FRAMEEND, 0)
            self._set_event(acaplib2.ACL_INT_GRABEND, 0)
            self._set_event(acaplib2.ACL_INT_GPIN, 0)
            # ボードクローズ
            acaplib2.AcapClose(self.__hHandle, self.__ch)
            self._debug_print("AcapClose")

    ##############################################################

    @property
    def is_opened(self):
        '''Gets true if the grabber board is open.'''
        return self.__is_opened 

    @property
    def is_grab(self):
        '''Gets true when in a grab.'''
        return self.__is_grab

    @property
    def acaplib2_version(self):
        '''Get the version of AcapLib2.'''
        return self.__acaplib2_version 

    @property
    def handle(self):
        '''Get a library handle for AcapLib2.'''
        return self.__hHandle 

    @property
    def board_id(self):
        '''Get the configured board ID.'''
        return self.__board_id

    @property
    def board_name(self):
        '''Get the name of the board in use.'''
        return self.__board_name

    @property
    def device(self):
        '''Get the device name.'''
        return self.__device

    @property
    def custom(self):
        '''Get the FPGA customization number.'''
        return self.__custom

    @property
    def channel_num(self):
        '''Get the total number of channels on the board.'''
        return self.__channel_num

    @property
    def serial_no(self):
        '''Get the serial number of the board.'''
        return self.__serial_no

    @property
    def ch(self):
        '''Get the specified channel number.'''
        return self.__ch

    @property
    def scan_system(self):
        return self.__scan_system
    @scan_system.setter
    def scan_system(self, value):
        '''Get or set the type of camera(area or line).

        Parameters
        ----------
        value : int
            0 : Area sensor
            1 : Line sensor
        '''
        ret = self.set_info(acaplib2.ACL_SCAN_SYSTEM, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__scan_system = value

    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value : int):
        '''Gets or set the number of pixels for the width of the image to be acquired.
        '''
        ret = self.set_info(acaplib2.ACL_X_SIZE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__width = value
            self.create_ring_buffer()

    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value : int):
        '''Gets or set the number of pixels for the height of the image to be acquired.
        '''        
        ret = self.set_info(acaplib2.ACL_Y_SIZE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__height = value
        if self.__y_total != 0:
            ret = self.set_info(acaplib2.ACL_Y_TOTAL, value)
            if ret == acaplib2.ACL_RTN_OK:
                self.__y_total = value
        self.create_ring_buffer()

    @property
    def mem_num(self):
        return self.__mem_num
    @mem_num.setter
    def mem_num(self, value : int):
        '''Get or set the number of images in the ring buffer.'''
        ret = self.set_info(acaplib2.ACL_MEM_NUM, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__mem_num = value
            self.create_ring_buffer()

    @property
    def x_delay(self):
        return self.__x_delay
    @x_delay.setter
    def x_delay(self, value : int):
        '''Get or set the X-direction delay of camera input'''
        ret = self.set_info(acaplib2.ACL_X_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__x_delay = value

    @property
    def y_delay(self):
        return self.__y_delay
    @y_delay.setter
    def y_delay(self, value : int):
        '''Get or set the X-direction delay of camera input'''
        ret = self.set_info(acaplib2.ACL_Y_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__y_delay = value

    @property
    def y_total(self):
        return self.__y_total
    @y_total.setter
    def y_total(self, value : int):
        '''Get or set the number of lines to be input from the camera.'''
        ret = self.set_info(acaplib2.ACL_Y_TOTAL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__y_total = value

    @property
    def camera_bit(self):
        return self.__camera_bit
    @camera_bit.setter
    def camera_bit(self, value : int):
        '''Gets or set the number of bits in the camera image.'''
        ret = self.set_info(acaplib2.ACL_CAM_BIT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__camera_bit = value
        ret, value = self.get_info(acaplib2.ACL_BOARD_BIT)
        if ret == acaplib2.ACL_RTN_OK:
            self.__board_bit = value
        self.create_ring_buffer()

    @property
    def board_bit(self):
        return self.__board_bit

    @property
    def pix_shift(self):
        return self.__pix_shift
    @pix_shift.setter
    def pix_shift(self, value : int):
        '''Get or set the number of bits to be right-shifted in the camera image data.'''
        ret = self.set_info(acaplib2.ACL_PIX_SHIFT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__pix_shift = value

    @property
    def timeout(self):
        return self.__timeout
    @timeout.setter
    def timeout(self, value : int):
        '''Get or set the timeout period in milliseconds for waiting for image input.'''
        ret = self.set_info(acaplib2.ACL_TIME_OUT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__timeout = value

    @property
    def cc_polarity(self):
        return self.__cc_polarity
    @cc_polarity.setter
    def cc_polarity(self, value : int):
        '''Get or set the output logic of the exposure signal.'''
        ret = self.set_info(acaplib2.ACL_EXP_POL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_polarity = value

    @property
    def trigger_polarity(self):
        return self.__trigger_polarity
    @trigger_polarity.setter
    def trigger_polarity(self, value : int):
        '''Get or set the output logic of the exposure signal.'''
        self.__trigger_polarity = value
        self.cc_polarity = value

    @property
    def cc1_polarity(self):
        return self.__cc1_polarity
    @cc1_polarity.setter
    def cc1_polarity(self, value : int):
        '''Get or set the signal output level of CC1.'''
        ret = self.set_info(acaplib2.ACL_CC1_LEVEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc1_polarity = value

    @property
    def cc2_polarity(self):
        return self.__cc2_polarity
    @cc2_polarity.setter
    def cc2_polarity(self, value : int):
        '''Get or set the signal output level of CC2.'''
        ret = self.set_info(acaplib2.ACL_CC2_LEVEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc2_polarity = value

    @property
    def cc3_polarity(self):
        return self.__cc3_polarity
    @cc3_polarity.setter
    def cc3_polarity(self, value : int):
        '''Get or set the signal output level of CC3.'''
        ret = self.set_info(acaplib2.ACL_CC3_LEVEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc3_polarity = value

    @property
    def cc4_polarity(self):
        return self.__cc4_polarity
    @cc4_polarity.setter
    def cc4_polarity(self, value : int):
        '''Get or set the signal output level of CC4.'''
        ret = self.set_info(acaplib2.ACL_CC4_LEVEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc4_polarity = value

    @property
    def cc_cycle(self):
        return self.__cc_cycle
    @cc_cycle.setter
    def cc_cycle(self, value : int):
        '''Get or set the exposure cycle.'''
        if value <= self.__exposure:
            self._debug_print("[Error] set cc_cycle: 'cc_cycle'({0}) must be larger  than 'exposure'({1}).".format(value, self.__exposure))
            return

        ret = self.set_info(acaplib2.ACL_EXP_CYCLE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_cycle = value
        ret, value = self.get_info(acaplib2.ACL_EXP_CYCLE_EX)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_cycle_ex = value


    @property
    def cc_cycle_ex(self):
        return self.__cc_cycle_ex
    @cc_cycle_ex.setter
    def cc_cycle_ex(self, value : int):
        '''Get or set the exposure cycle(100nsec).'''
        if value <= self.__exposure_ex:
            self._debug_print("[Error] set cc_cycle_ex: 'cc_cycle_ex'({0}) must be larger  than 'exposure_ex'({1}).".format(value, self.__exposure_ex))
            return
        ret = self.set_info(acaplib2.ACL_EXP_CYCLE_EX, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_cycle_ex = value
        ret, value = self.get_info(acaplib2.ACL_EXP_CYCLE)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_cycle = value


    @property
    def exposure(self):
        return self.__exposure
    @exposure.setter
    def exposure(self, value : int):
        '''Get or set the exposure time.'''
        if value >= self.__cc_cycle:
            #self._debug_print(f"[Error] set exposure: 'exposure'({value}) must be smaller than 'cc_cycle'({self.__cc_cycle}).")
            self._debug_print("[Error] set exposure: 'exposure'({0}) must be smaller than 'cc_cycle'({1}).".format(value, self.__cc_cycle))
            return
        ret = self.set_info(acaplib2.ACL_EXPOSURE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__exposure = value
        ret, value = self.get_info(acaplib2.ACL_EXPOSURE_EX)
        if ret == acaplib2.ACL_RTN_OK:
            self.__exposure_ex = value          

    @property
    def exposure_ex(self):
        return self.__exposure_ex
    @exposure_ex.setter
    def exposure_ex(self, value : int):
        '''Get or set the exposure time(100nsec).'''
        if value >= self.__cc_cycle_ex:
            #self._debug_print(f"[Error] set exposure_ex: 'exposure_ex'({value}) must be smaller than 'cc_cycle_ex'({self.__cc_cycle_ex}).")
            self._debug_print("[Error] set exposure_ex: 'exposure_ex'({0}) must be smaller than 'cc_cycle_ex'({1}).".format(value, self.__cc_cycle_ex))
            return
        ret = self.set_info(acaplib2.ACL_EXPOSURE_EX, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__exposure_ex = value
        ret, value = self.get_info(acaplib2.ACL_EXPOSURE)
        if ret == acaplib2.ACL_RTN_OK:
            self.__exposure = value             

    @property
    def cc_delay(self):
        return self.__cc_delay
    @cc_delay.setter
    def cc_delay(self, value : int):
        '''Get or set the delay time(usec) for the exposure signal output.'''
        ret = self.set_info(acaplib2.ACL_CC_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_delay = value

    @property
    def cc_out_no(self):
        return self.__cc_out_no
    @cc_out_no.setter
    def cc_out_no(self, value : int):
        '''Get or set the channel for the exposure signal.'''
        ret = self.set_info(acaplib2.ACL_EXP_CC_OUT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_out_no = value


    @property
    def rolling_shutter(self):
        return self.__rolling_shutter
    @rolling_shutter.setter
    def rolling_shutter(self, value : int):
        '''Get or set to use or not use the rolling shutter.'''
        ret = self.set_info(acaplib2.ACL_ROLLING_SHUTTER, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__rolling_shutter = value

    @property
    def external_trigger_enable(self):
        return self.__external_trigger_enable
    @external_trigger_enable.setter
    def external_trigger_enable(self, value : int):
        '''Get or set the signal to be used for the external trigger.'''
        ret = self.set_info(acaplib2.ACL_EXT_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__external_trigger_enable = value


    @property
    def external_trigger_mode(self):
        return self.__external_trigger_mode
    @external_trigger_mode.setter
    def external_trigger_mode(self, value : int):
        '''Get or set the method of outputting the CC signal with a single external trigger.'''
        ret = self.set_info(acaplib2.ACL_EXT_MODE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__external_trigger_mode = value

    @property
    def external_trigger_chatter(self):
        return self.__external_trigger_chatter
    @external_trigger_chatter.setter
    def external_trigger_chatter(self, value : int):
        '''Get or set the external trigger detection disable time(usec).'''
        ret = self.set_info(acaplib2.ACL_EXT_CHATTER, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__external_trigger_chatter = value

    @property
    def external_trigger_delay(self):
        return self.__external_trigger_delay
    @external_trigger_delay.setter
    def external_trigger_delay(self, value : int):
        '''Get or set the external trigger detection delay time.'''
        ret = self.set_info(acaplib2.ACL_EXT_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__external_trigger_delay = value

    @property
    def encoder_enable(self):
        return self.__encoder_enable
    @encoder_enable.setter
    def encoder_enable(self, value : int):
        '''Get or set the delay time(usec) for external trigger detection.
        0: Do not use the encoder
        1: Relative count mode
        2: Absolute count mode
        '''
        ret = self.set_info(acaplib2.ACL_ENC_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_enable = value

    @property
    def encoder_start(self):
        return self.__encoder_start
    @encoder_start.setter
    def encoder_start(self, value : int):
        '''Get or set how the external trigger is used by the encoder.'''
        ret = self.set_info(acaplib2.ACL_ENC_START, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_start = value

    @property
    def encoder_mode(self):
        return self.__encoder_mode
    @encoder_mode.setter
    def encoder_mode(self, value : int):
        '''Get or set the operation mode of the encoder.'''
        ret = self.set_info(acaplib2.ACL_ENC_MODE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_mode = value

    @property
    def encoder_phase(self):
        return self.__encoder_phase
    @encoder_phase.setter
    def encoder_phase(self, value : int):
        '''Get or set the encoder input pulses.'''
        ret = self.set_info(acaplib2.ACL_ENC_PHASE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_phase = value

    @property
    def encoder_direction(self):
        return self.__encoder_direction
    @encoder_direction.setter
    def encoder_direction(self, value : int):
        '''Get or set the rotation direction of the encoder.'''
        ret = self.set_info(acaplib2.ACL_ENC_DIRECTION, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_direction = value

    @property
    def encoder_z_phase(self):
        return self.__encoder_z_phase
    @encoder_z_phase.setter
    def encoder_z_phase(self, value : int):
        '''Get or set the use or non-use of phase Z for encoder startup.'''
        ret = self.set_info(acaplib2.ACL_ENC_ZPHASE_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_z_phase = value

    @property
    def encoder_compare_reg_1(self):
        return self.__encoder_compare_reg_1
    @encoder_compare_reg_1.setter
    def encoder_compare_reg_1(self, value : int):
        '''Get or set the number of encoder delay pulses.'''
        ret = self.set_info(acaplib2.ACL_ENC_COMPARE_1, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_compare_reg_1 = value

    @property
    def encoder_compare_reg_2(self):
        return self.__encoder_compare_reg_2
    @encoder_compare_reg_2.setter
    def encoder_compare_reg_2(self, value : int):
        '''Get or set the number of dividing pulses of the encoder.'''
        ret = self.set_info(acaplib2.ACL_ENC_COMPARE_2, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_compare_reg_2 = value

    @property
    def encoder_abs_mode(self):
        return self.__encoder_abs_mode
    @encoder_abs_mode.setter
    def encoder_abs_mode(self, value : int):
        '''Get or set the encoder absolute count mode.'''
        ret = self.set_info(acaplib2.ACL_ENC_ABS_MODE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_abs_mode = value

    @property
    def encoder_abs_start(self):
        return self.__encoder_abs_start
    @encoder_abs_start.setter
    def encoder_abs_start(self, value : int):
        '''Get or set the status of the absolute count (operating or stopped).'''
        ret = self.set_info(acaplib2.ACL_ENC_ABS_START, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__encoder_abs_start = value

    @property
    def encoder_abs_count(self) -> int:
        '''Get the absolute count value of the encoder.'''
        _, count = self.get_info(acaplib2.ACL_ENC_ABS_COUNT)
        return count

    @property
    def strobe_enable(self):
        return self.__strobe_enable
    @strobe_enable.setter
    def strobe_enable(self, value : int):
        '''Get or set the strobe enable(1)/disable(0) setting.'''
        ret = self.set_info(acaplib2.ACL_STROBE_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__strobe_enable = value

    @property
    def strobe_delay(self):
        return self.__strobe_delay
    @strobe_delay.setter
    def strobe_delay(self, value : int):
        '''Get or set the strobe signal output delay time(usec).'''
        ret = self.set_info(acaplib2.ACL_STROBE_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__strobe_delay = value

    @property
    def strobe_time(self):
        return self.__strobe_time
    @strobe_time.setter
    def strobe_time(self, value):
        '''Get or set the strobe signal output time(usec).'''
        ret = self.set_info(acaplib2.ACL_STROBE_TIME, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__strobe_time = value

    @property
    def reverse_dma_enable(self):
        return self.__reverse_dma_enable
    @reverse_dma_enable.setter
    def reverse_dma_enable(self, value : int):
        '''Enables(1)/Disables(0) reverse DMA in the Y direction.'''
        ret = self.set_info(acaplib2.ACL_REVERSE_DMA, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__reverse_dma_enable = value

    @property
    def dval_enable(self):
        return self.__dval_enable
    @dval_enable.setter
    def dval_enable(self, value : int):
        '''Get or set whether or not to refer to the DVAL signal when inputting camera data.'''
        ret = self.set_info(acaplib2.ACL_DVAL_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__dval_enable = value

    @property
    def tap_num(self):
        return self.__tap_num
    @tap_num.setter
    def tap_num(self, value : int):
        '''Get or set the number of input taps.'''
        ret = self.set_info(acaplib2.ACL_TAP_NUM, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_num = value

    @property
    def tap_arrange(self):
        return self.__tap_arrange
    @tap_arrange.setter
    def tap_arrange(self, value : int):
        '''Get or set the tap rearrangement method for camera data input.'''
        ret = self.set_info(acaplib2.ACL_TAP_ARRANGE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_arrange = value

    @property
    def tap_arrange_x_size(self):
        return self.__tap_arrange_x_size
    @tap_arrange_x_size.setter
    def tap_arrange_x_size(self, value : int):
        '''Get or set the total number of pixels that the camera outputs as one line.'''
        ret = self.set_info(acaplib2.ACL_ARRANGE_XSIZE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_arrange_x_size = value

    @property
    def tap_direction1(self):
        return self.__tap_direction1
    @tap_direction1.setter
    def tap_direction1(self, value : int):
        '''Get or set the input direction for Camera Link tap1.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -1)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction1 = value

    @property
    def tap_direction2(self):
        return self.__tap_direction2
    @tap_direction2.setter
    def tap_direction2(self, value : int):
        '''Get or set the input direction for Camera Link tap2.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -2)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction2 = value

    @property
    def tap_direction3(self):
        return self.__tap_direction3
    @tap_direction3.setter
    def tap_direction3(self, value : int):
        '''Get or set the input direction for Camera Link tap3.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -3)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction3 = value

    @property
    def tap_direction4(self):
        return self.__tap_direction4
    @tap_direction4.setter
    def tap_direction4(self, value : int):
        '''Get or set the input direction for Camera Link tap4.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -4)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction4 = value

    @property
    def tap_direction5(self):
        return self.__tap_direction5
    @tap_direction5.setter
    def tap_direction5(self, value : int):
        '''Get or set the input direction for Camera Link tap5.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -5)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction5 = value

    @property
    def tap_direction6(self):
        return self.__tap_direction6
    @tap_direction6.setter
    def tap_direction6(self, value : int):
        '''Get or set the input direction for Camera Link tap6.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -6)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction6 = value

    @property
    def tap_direction7(self):
        return self.__tap_direction7
    @tap_direction7.setter
    def tap_direction7(self, value : int):
        '''Get or set the input direction for Camera Link tap7.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -7)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction7 = value

    @property
    def tap_direction8(self):
        return self.__tap_direction8
    @tap_direction8.setter
    def tap_direction8(self, value : int):
        '''Get or set the input direction for Camera Link tap8.'''
        ret = self.set_info(acaplib2.ACL_TAP_DIRECTION, value, -8)
        if ret == acaplib2.ACL_RTN_OK:
            self.__tap_direction8 = value

    @property
    def sync_lt(self):
        return self.__sync_lt
    @sync_lt.setter
    def sync_lt(self, value : int):
        '''Get or set whether or not to synchronize the exposure signal output with the SYNCLT input.'''
        ret = self.set_info(acaplib2.ACL_SYNC_LT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__sync_lt = value

    @property
    def gpout_sel(self):
        return self.__gpout_sel
    @gpout_sel.setter
    def gpout_sel(self, value : int):
        '''Get or set whether the output of the GP_OUT pin is a general-purpose output(1) or a capture flag(0).'''
        ret = self.set_info(acaplib2.ACL_GPOUT_SEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__gpout_sel = value

    @property
    def gpout_pol(self):
        return self.__gpout_pol
    @gpout_pol.setter
    def gpout_pol(self, value : int):
        '''Get or set the output level of the GP_OUT pin.'''
        ret = self.set_info(acaplib2.ACL_GPOUT_POL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__gpout_pol = value

    @property
    def interrupt_line(self):
        return self.__interrupt_line
    @interrupt_line.setter
    def interrupt_line(self, value : int):
        '''Get or set the count interval of the number of input lines for one frame.'''
        ret = self.set_info(acaplib2.ACL_INTR_LINE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__interrupt_line = value

    @property
    def cc_enable(self):
        return self.__trigger_enable
    @cc_enable.setter
    def cc_enable(self, value : int):
        '''Get or set whether the exposure signal output is enabled or disabled.'''
        self.trigger_enable = value

    @property
    def trigger_enable(self):
        return self.__trigger_enable
    @trigger_enable.setter
    def trigger_enable(self, value : int):
        '''Get or set whether the exposure signal output is enabled or disabled.'''
        ret = self.set_info(acaplib2.ACL_EXP_EN, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__trigger_enable = value

    @property
    def data_mask_lower(self):
        return self.__data_mask_lower
    @data_mask_lower.setter
    def data_mask_lower(self, value : int):
        '''Get or set the mask value of Camera Link port (A to D).'''
        ret = self.set_info(acaplib2.ACL_DATA_MASK_LOWER, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__data_mask_lower = value

    @property
    def data_mask_upper(self):
        return self.__data_mask_upper
    @data_mask_upper.setter
    def data_mask_upper(self, value : int):
        '''Get or set the mask value of Camera Link port (E to H).'''
        ret = self.set_info(acaplib2.ACL_DATA_MASK_UPPER, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__data_mask_upper = value

    @property
    def encoder_count(self):
        '''Get the relative count value when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_COUNT)
        return count

    @property
    def encoder_all_count(self):
        '''Get the total count value when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_RLT_ALL_COUNT)
        return count

    @property
    def encoder_agr_count(self):
        '''Get the number of matched pulses when using relative count.'''
        _, count = self.get_info(acaplib2.ACL_ENC_AGR_COUNT)
        return count

    @property
    def a_cw_ccw(self):
        '''Get the rotation direction of phase A.'''
        _, count = self.get_info(acaplib2.ACL_A_CW_CCW)
        return count

    @property
    def b_cw_ccw(self):
        '''Get the rotation direction of phase B.'''
        _, count = self.get_info(acaplib2.ACL_B_CW_CCW)
        return count

    @property
    def freq_a(self):
        '''Get the frequency of phase A.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_A)
        return count

    @property
    def freq_b(self):
        '''Get the frequency of phase B.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_B)
        return count

    @property
    def freq_z(self):
        '''Get the frequency of phase Z.'''
        _, count = self.get_info(acaplib2.ACL_FREQ_Z)
        return count

    @property
    def chatter_separate(self):
        return self.__chatter_separate
    @chatter_separate.setter
    def chatter_separate(self, value):
        '''Get or set the setting method of the external trigger detection disable time.'''
        ret = self.set_info(acaplib2.ACL_EXT_CHATTER_SEPARATE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__chatter_separate = value

    @property
    def gpin_pin_sel(self):
        return self.__gpin_pin_sel
    @gpin_pin_sel.setter
    def gpin_pin_sel(self, value : int):
        '''Get or set the external trigger pins that are assigned as GPIN interrupt to the specified channel.'''
        ret = self.set_info(acaplib2.ACL_GPIN_PIN_SEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__gpin_pin_sel = value

    @property
    def sync_ch(self):
        return self.__sync_ch
    @sync_ch.setter
    def sync_ch(self, value : int):
        '''Get or set which channel to synchronize the acquisition of the specified channel with.'''
        ret = self.set_info(acaplib2.ACL_SYNC_CH, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__sync_ch = value

    @property
    def bayer_enable(self):
        return self.__bayer_enable
    @bayer_enable.setter
    def bayer_enable(self, value : int):
        '''Get or set the Enable/Disable setting for the Bayer transform.'''
        ret = self.set_info(acaplib2.ACL_BAYER_ENABLE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__bayer_enable = value

    @property
    def bayer_grid(self):
        return self.__bayer_grid
    @bayer_grid.setter
    def bayer_grid(self, value : int):
        '''Get or set the pattern for the start position of the Bayer transform.
        0:BGGR
        1:RGGB
        2:GBRG
        3:GRBG
        '''
        ret = self.set_info(acaplib2.ACL_BAYER_GRID, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__bayer_grid = value

    @property
    def bayer_lut_edit(self):
        _, value = self.get_info(acaplib2.ACL_BAYER_LUT_EDIT)
        return value
    @bayer_lut_edit.setter
    def bayer_lut_edit(self, value : int):
        '''Get or set the edit status of the BayerLUT.'''
        self.set_info(acaplib2.ACL_BAYER_LUT_EDIT, value)

    @property
    def bayer_lut_data(self):
        data = []
        for i in range(1024):
            ret, value = self.get_info(acaplib2.ACL_BAYER_LUT_DATA, i)
            if ret != AcaPy.OK:
                return None
            data.append(value)
        return data
    @bayer_lut_data.setter
    def bayer_lut_data(self, lut_data_list):
        '''Reads or writes the BayerLUT table data of the specified channel.'''
        for i in range(len(lut_data_list)):
            ret = self.set_info(acaplib2.ACL_BAYER_LUT_DATA, lut_data_list[i], i)
            if ret != AcaPy.OK:
                return

    @property
    def bayer_input_bit(self):
        return self.__bayer_input_bit
    @bayer_input_bit.setter
    def bayer_input_bit(self, value : int):
        '''Get or set the input bit width of a single pixel in a Bayer image.'''
        ret = self.set_info(acaplib2.ACL_BAYER_INPUT_BIT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__bayer_input_bit = value

    @property
    def bayer_output_bit(self):
        return self.__bayer_output_bit
    @bayer_output_bit.setter
    def bayer_output_bit(self, value : int):
        '''Get or set the bit width of a single pixel of the image after Bayer conversion.'''
        ret = self.set_info(acaplib2.ACL_BAYER_OUTPUT_BIT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__bayer_output_bit = value

    @property
    def power_supply(self):
        _, value = self.get_info(acaplib2.ACL_POWER_SUPPLY)
        return value
    @power_supply.setter
    def power_supply(self, value : int):
        '''Get or set the status(ON:1, OFF:0) of power supply to the camera.'''
        self.set_info(acaplib2.ACL_POWER_SUPPLY, value, 3000)

    @property
    def power_state(self):
        _, value = self.get_info(acaplib2.ACL_POWER_STATE)
        return value
    @power_state.setter
    def power_state(self, value : int):
        '''Get or set the camera power supply error status.'''
        return self.set_info(acaplib2.ACL_POWER_STATE, value)

    @property
    def strobe_pol(self):
        return self.__strobe_pol
    @strobe_pol.setter
    def strobe_pol(self, value : int):
        '''Get or set strobe signal polarity.'''
        self.__strobe_pol = value
        self.set_info(acaplib2.ACL_STROBE_POL, value)

    @property
    def vertical_remap(self):
        return self.__vertical_remap
    @vertical_remap.setter
    def vertical_remap(self, value : int):
        '''Get or set the VERTICAL REMAP (Y direction special DMA) and DUAL LINE enable/disable setting.'''
        ret = self.set_info(acaplib2.ACL_VERTICAL_REMAP, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__vertical_remap = value

    @property
    def express_link(self):
        '''Get the link width negotiated for the PCI-Express bus.'''
        return self.__express_link

    @property
    def fpga_version(self):
        '''Get the current FPGA version.'''
        return self.__fpga_version

    @property
    def lval_delay(self):
        return self.__lval_delay
    @lval_delay.setter
    def lval_delay(self, value : int):
        '''Get or set the input direction for each tap.'''
        ret = self.set_info(acaplib2.ACL_LVAL_DELAY, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__lval_delay = value

    @property
    def line_reverse(self):
        return self.__line_reverse
    @line_reverse.setter
    def line_reverse(self, value : int):
        '''Get ot set whether or not to flip the line data left or right.'''
        ret = self.set_info(acaplib2.ACL_LINE_REVERSE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__line_reverse = value

    @property
    def camera_state(self):
        '''Get the connection status of the camera.'''
        _, value = self.get_info(acaplib2.ACL_CAMERA_STATE)
        return value

    @property
    def gpin_pol(self):
        '''Get the GPIN level as Bit information.'''
        _, value = self.get_info(acaplib2.ACL_GPIN_POL)
        return value

    @property
    def board_error(self):
        '''Get the board error information by Bit information.'''
        _, value = self.get_info(acaplib2.ACL_BOARD_ERROR)
        return value

    @board_error.setter
    def board_error(self, value : int):
        '''Clears the board error of the specified channel.'''
        self.set_info(acaplib2.ACL_BOARD_ERROR, value)

    @property
    def start_frame_no(self):
        return self.__start_frame_no
    @start_frame_no.setter
    def start_frame_no(self, value : int):
        '''Get ot set the number of frames to be input from the buffer at the start of acquisition.'''
        ret = self.set_info(acaplib2.ACL_START_FRAME_NO, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__start_frame_no = value

    @property
    def cancel_initialize(self):
        _, value = self.get_info(acaplib2.ACL_CANCEL_INITIALIZE)
        return value
    @cancel_initialize.setter
    def cancel_initialize(self, value : int):
        '''Get ot set whether or not to cancel initialization and internal buffer allocation.'''
        self.set_info(acaplib2.ACL_CANCEL_INITIALIZE, value)

    @property
    def buffer_zero_fill(self):
        ret, value = self.get_info(acaplib2.ACL_BUFFER_ZERO_FILL)
        if ret == acaplib2.ACL_RTN_OK:
            self.__buffer_zero_fill = value
        return self.__buffer_zero_fill
    @buffer_zero_fill.setter
    def buffer_zero_fill(self, value : int):
        '''Get or set whether to clear the buffer to zero'''
        ret = self.set_info(acaplib2.ACL_BUFFER_ZERO_FILL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__buffer_zero_fill = value

    @property
    def cc_stop(self):
        ret, value = self.get_info(acaplib2.ACL_CC_STOP)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_stop = value
        return self.__cc_stop
    @cc_stop.setter
    def cc_stop(self, value : int):
        '''Get or set the output/stop of CC after the input is stopped.'''
        ret = self.set_info(acaplib2.ACL_CC_STOP, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cc_stop = value

    @property
    def lvds_cclk_sel(self):
        return self.__lvds_cclk_sel
    @lvds_cclk_sel.setter
    def lvds_cclk_sel(self, value : int):
        '''Get or set the camera drive clock'''
        ret = self.set_info(acaplib2.ACL_LVDS_CCLK_SEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__lvds_cclk_sel = value

    @property
    def lvds_phase_sel(self):
        return self.__lvds_phase_sel
    @lvds_phase_sel.setter
    def lvds_phase_sel(self, value : int):
        '''Get or set the phase setting of the input sampling.'''
        ret = self.set_info(acaplib2.ACL_LVDS_PHASE_SEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__lvds_phase_sel = value

    @property
    def lvds_synclt_sel(self):
        return self.__lvds_synclt_sel
    @lvds_synclt_sel.setter
    def lvds_synclt_sel(self, value : int):
        '''Get or set the direction of the SYNCLT pin.'''
        ret = self.set_info(acaplib2.ACL_LVDS_SYNCLT_SEL, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__lvds_synclt_sel = value

    @property
    def count_cc(self):
        '''Get the number of output of CC1/trigger packet.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_CC)
        return value

    @property
    def count_fval(self):
        '''Get the number of times FVAL is input.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_FVAL)
        return value

    @property
    def count_lval(self):
        '''Get the number of LVAL inputs.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_LVAL)
        return value

    @property
    def count_exttrig(self):
        '''Get the number of EXTTRIG (external trigger) inputs.'''
        _, value = self.get_info(acaplib2.ACL_COUNT_EXTTRIG)
        return value

    @property
    def interval_exttrig_1(self):
        '''Get the time of the recognized external trigger interval (the latest count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_1)
        return value

    @property
    def interval_exttrig_2(self):
        '''Get the time of the recognized external trigger interval (the second most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_2)
        return value

    @property
    def interval_exttrig_3(self):
        '''Get the time of the recognized external trigger interval (the third most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_3)
        return value

    @property
    def interval_exttrig_4(self):
        '''Get the time of the recognized external trigger interval (the fourth most recent count value).'''
        _, value = self.get_info(acaplib2.ACL_INTERVAL_EXTTRIG_4)
        return value

    @property
    def virtual_comport(self):
        '''Get the virtual COM port number.'''
        _, value = self.get_info(acaplib2.ACL_VIRTUAL_COMPORT)
        self.__virtual_comport = value
        return value

    @property
    def pocl_lite_enable(self):
        return self.__pocl_lite_enable
    @pocl_lite_enable.setter
    def pocl_lite_enable(self, value : int):
        '''Get or set the setting values for PoCL-Lite camera connection.'''
        ret = self.set_info(acaplib2.ACL_POCL_LITE_ENABLE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__pocl_lite_enable = value

    @property
    def cxp_link_speed(self):
        return self.__cxp_link_speed
    @cxp_link_speed.setter
    def cxp_link_speed(self, value : int):
        '''Get or set the bit rate to and from the CoaXPress camera.'''
        #self.set_info(acaplib2._ACL_CXP_LINK_SPEED, value)
        ret = self.set_info(acaplib2.ACL_CXP_BITRATE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_link_speed = value
            self.__cxp_bitrate = value

    @property
    def cxp_bitrate(self):
        return self.__cxp_bitrate
    @cxp_bitrate.setter
    def cxp_bitrate(self, value : int):
        '''Get or set the bit rate to and from the CoaXPress camera.'''
        ret = self.set_info(acaplib2.ACL_CXP_BITRATE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_link_speed = value
            self.__cxp_bitrate = value
    @property
    def cxp_acquision_start_address(self):
        return self.__cxp_acquision_start_address
    @cxp_acquision_start_address.setter
    def cxp_acquision_start_address(self, value : int):
        '''Get or set the address value of AcquisitionStart.'''
        ret = self.set_info(acaplib2.ACL_CXP_ACQ_START_ADR, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_acquision_start_address = value

    @property
    def cxp_acquision_start_value(self):
        return self.__cxp_acquision_start_value
    @cxp_acquision_start_value.setter
    def cxp_acquision_start_value(self, value : int):
        '''Get or set the value of AcquisitionStart.'''
        ret = self.set_info(acaplib2.ACL_CXP_ACQ_START_VALUE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_acquision_start_value = value

    @property
    def cxp_acquision_stop_address(self):
        return self.__cxp_acquision_stop_address
    @cxp_acquision_stop_address.setter
    def cxp_acquision_stop_address(self, value : int):
        '''Get or set the address value of AcquisitionStop.'''
        ret = self.set_info(acaplib2.ACL_CXP_ACQ_STOP_ADR, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_acquision_stop_address = value

    @property
    def cxp_acquision_stop_value(self):
        return self.__cxp_acquision_stop_value
    @cxp_acquision_stop_value.setter
    def cxp_acquision_stop_value(self, value : int):
        '''Get or set the value of AcquisitionStop.'''
        ret = self.set_info(acaplib2.ACL_CXP_ACQ_STOP_VALUE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_acquision_stop_value = value

    @property
    def cxp_pixel_format_address(self):
        return self.__cxp_pixel_format_address
    @cxp_pixel_format_address.setter
    def cxp_pixel_format_address(self, value : int):
        '''Get or set the address to change the output bit width of the CoaXPress camera.'''
        ret = self.set_info(acaplib2.ACL_CXP_PIX_FORMAT_ADR, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_pixel_format_address = value

    @property
    def cxp_pixel_format(self):
        return self.__cxp_pixel_format
    @cxp_pixel_format.setter
    def cxp_pixel_format(self, value : int):
        '''Get or set the output bit width of the CoaXPress camera.'''
        ret = self.set_info(acaplib2.ACL_CXP_PIX_FORMAT, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__cxp_pixel_format = value

    @property
    def rgb_swap_enable(self):
        return self.__rgb_swap_enable
    @rgb_swap_enable.setter
    def rgb_swap_enable(self, value : int):
        ret = self.set_info(acaplib2.ACL_RGB_SWAP_ENABLE, value)
        if ret == acaplib2.ACL_RTN_OK:
            self.__rgb_swap_enable = value

    @property
    def freq_lval(self):
        '''Get the frequency of LVAL.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_LVAL)
        return value

    @property
    def freq_fval(self):
        '''Get the frequency of FVAL.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_FVAL)
        return value

    @property
    def freq_ttl1(self):
        '''Get the frequency of TTL1.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL1)
        return value

    @property
    def freq_ttl2(self):
        '''Get the frequency of TTL2.'''
        _, value = self.get_info(acaplib2.ACL_FREQ_TTL2)
        return value

    @property
    def fifo_full(self):
        '''Get the status of the FIFO on the frame grabber board.'''
        _, value = self.get_info(acaplib2.ACL_FIFO_FULL)
        return value

    @property
    def board_temp(self):
        '''Get the temperature of the frame grabber board(APX-3334 only). '''
        _, value = self.get_info(acaplib2.ACL_BOARD_TEMP)
        return value

    @property
    def fpga_temp(self):
        '''Get the temperature of the FPGA.'''
        _, value = self.get_info(acaplib2.ACL_FPGA_TEMP)
        return value

    @property
    def capture_flag(self):
        '''Gets the capture status (capturing(1) or stopped(0)).'''
        _, value = self.get_info(acaplib2.ACL_CAPTURE_FLAG)
        return value

    @property
    def narrow10bit_enable(self):
        return self.__narrow10bit_enable
    @narrow10bit_enable.setter
    def narrow10bit_enable(self, value):
        '''Get or set enable/disable for data stuffing transfer.'''
        ret = self.set_info(acaplib2.ACL_NARROW10BIT_ENABLE, value)  
        if ret == acaplib2.ACL_RTN_OK:
            self.__narrow10bit_enable = value

    # Ver.7.2.3
    @property
    def infrared_enable(self):
        return self.__infrared_enable
    @infrared_enable.setter
    def infrared_enable(self, value):
        '''Get or set the enable/disable status of RGBI.'''
        ret = self.set_info(acaplib2.ACL_INFRARED_ENABLE, value)  
        if ret == acaplib2.ACL_RTN_OK:
            self.__infrared_enable = value


    ##############################################################
    # Meathod
    ##############################################################
   
    @staticmethod
    def bgr2rgb(bgr_image : np.ndarray) -> np.ndarray:
        '''Converts the data sequence of a color image from BGR to RGB or RGB to BGR.

        Parameters
        ----------
        bgr_image : ndarray
            Color image with data sequence BGR

        Returns
        -------
        rgb_image : np.ndarray
            Color image with RGB data sequence
        '''
        return acaplib2.bgr2rgb(bgr_image)

    @staticmethod
    def get_boardInfo() -> Tuple[int, acaplib2.ACAPBOARDINFOEX]:
        '''Get the information of the connected board.

        Returns
        -------
        ret : int
            Error information
        board_info : acaplib2.ACAPBOARDINFOEX
            Board Information  
        '''
        return acaplib2.AcapGetBoardInfoEx()

    @staticmethod
    def get_enable_board_ch_list() -> List[Tuple[int, int]]:
        '''Get the available board list information.

        Returns
        -------
        board_ch_list : List[Tuple[int, int]
            board_id : int
                Board Number
            ch : int
                Channel Number
        '''
        _, info = acaplib2.AcapGetBoardInfoEx()

        boardnum = info.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        info_list = []
        for i in range(boardnum):
            for ch in range(info.boardIndex[i].nChannelNum):
                info_list.append((info.boardIndex[i].nBoardID, ch + 1))

        return info_list

    def get_info(self, value_id : int, mem_num : int = 0) -> Tuple[int, int]:
        '''Get the setting value of the board by specifying the setting ID.

        Parameters
        ----------
        value_id : int
            ID of the value to set
        mem_num : int
            The meaning changes depending on the value_id.

        Returns
        -------
        ret : int
            Error information
        value : int
            Get value of ID
        '''

        ret, value = acaplib2.AcapGetInfo(self.__hHandle, self.__ch, value_id, mem_num)
        if ret != self.OK:
            value = 0
            self._debug_print("[Not Implemented] get_info: value_id =", acaplib2.get_error_name(value_id))
        return ret, value

    def set_info(self, value_id : int, value : int, mem_num : int = -1) -> int:
        '''Set the setting value of the board by specifying the setting ID.

        Parameters
        ----------
        value_id : int
            ID of the value to set.
        value : int
            Setting value of the board.
        mem_num : int
            The meaning changes depending on the value_id.

        Returns
        -------
        ret : int
            Error information
        '''

        if mem_num < 0:
            self.__refrect_param_flag = True
        ret = acaplib2.AcapSetInfo(self.__hHandle, self.__ch, value_id, mem_num, value)
        if ret != self.OK:
            error_info = self.get_last_error()
            if str(acaplib2.get_error_name(error_info.dwBoardErrorCode & 0x00FF)) == "NO_ERROR":
                self._debug_print("[Not Implemented] set_info: value_id =", acaplib2.get_error_name(value_id), ": Value = ", value)
            else:
                self._debug_print("[Error] set_info: value_id =", acaplib2.get_error_name(value_id), ": Value = ", value)
                self.print_last_error()
        return ret

    def refrect_param(self, force_execution : bool = False) -> int:
        '''Reflects the set values on the board.

        Parameters
        ----------
        force_execution : bool
            True:  Force execution.
            False: Execute based on internal flags. 

        Returns
        -------
        ret : int
            Error information
        '''

        if force_execution == False:
            if self.__refrect_param_flag == False:
                return self.OK
        self.__refrect_param_flag = False

        return acaplib2.AcapReflectParam(self.__hHandle, self.__ch)

    def _select_file(self, inifilename : str) -> int:
        '''Load the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).
        
        Returns
        -------
        ret : int
            Error information
        '''

        # バッファ確保を行わない
        #self.set_info(acaplib2.ACL_CANCEL_INITIALIZE, 1)
        self.__refrect_param_flag = True # refrect_patamが必要

        ret = acaplib2.AcapSelectFile(self.__hHandle, self.__ch, inifilename)
        if ret != acaplib2.ACL_RTN_OK:
            self.print_last_error()
            return ret
        # 各種情報の取得
        ret, self.__scan_system = self.get_info(acaplib2.ACL_SCAN_SYSTEM)
        ret, self.__width = self.get_info(acaplib2.ACL_X_SIZE)
        ret, self.__height = self.get_info(acaplib2.ACL_Y_SIZE)
        ret, self.__x_delay = self.get_info(acaplib2.ACL_X_DELAY)
        ret, self.__y_delay = self.get_info(acaplib2.ACL_Y_DELAY)
        ret, self.__y_total = self.get_info(acaplib2.ACL_Y_TOTAL)
        ret, self.__camera_bit = self.get_info(acaplib2.ACL_CAM_BIT)
        ret, self.__board_bit = self.get_info(acaplib2.ACL_BOARD_BIT)
        ret, self.__pix_shift = self.get_info(acaplib2.ACL_PIX_SHIFT)
        ret, self.__timeout = self.get_info(acaplib2.ACL_TIME_OUT)
        ret, self.__mem_num = self.get_info(acaplib2.ACL_MEM_NUM)

        ret, self.__cc_polarity = self.get_info(acaplib2.ACL_EXP_POL)
        ret, self.__cc1_polarity = self.get_info(acaplib2.ACL_CC1_LEVEL)
        ret, self.__cc2_polarity = self.get_info(acaplib2.ACL_CC2_LEVEL)
        ret, self.__cc3_polarity = self.get_info(acaplib2.ACL_CC3_LEVEL)
        ret, self.__cc4_polarity = self.get_info(acaplib2.ACL_CC4_LEVEL)
        self.__trigger_polarity = self.__cc_polarity

        ret, self.__cc_cycle = self.get_info(acaplib2.ACL_EXP_CYCLE)
        ret, self.__cc_cycle_ex = self.get_info(acaplib2.ACL_EXP_CYCLE_EX)

        ret, self.__exposure = self.get_info(acaplib2.ACL_EXPOSURE)
        ret, self.__exposure_ex = self.get_info(acaplib2.ACL_EXPOSURE_EX)

        ret, self.__cc_out_no = self.get_info(acaplib2.ACL_EXP_CC_OUT)
        ret, self.__cc_delay = self.get_info(acaplib2.ACL_CC_DELAY)
        ret, self.__rolling_shutter = self.get_info(acaplib2.ACL_ROLLING_SHUTTER)

        ret, self.__external_trigger_enable = self.get_info(acaplib2.ACL_EXT_EN)
        ret, self.__external_trigger_mode = self.get_info(acaplib2.ACL_EXT_MODE)
        ret, self.__external_trigger_chatter = self.get_info(acaplib2.ACL_EXT_CHATTER)
        ret, self.__external_trigger_delay = self.get_info(acaplib2.ACL_EXT_DELAY)
        
        ret, self.__encoder_enable = self.get_info(acaplib2.ACL_ENC_EN)
        ret, self.__encoder_start = self.get_info(acaplib2.ACL_ENC_START)
        ret, self.__encoder_mode = self.get_info(acaplib2.ACL_ENC_MODE)
        ret, self.__encoder_phase = self.get_info(acaplib2.ACL_ENC_PHASE)
        ret, self.__encoder_direction = self.get_info(acaplib2.ACL_ENC_DIRECTION)
        ret, self.__encoder_z_phase = self.get_info(acaplib2.ACL_ENC_ZPHASE_EN)
        ret, self.__encoder_compare_reg_1 = self.get_info(acaplib2.ACL_ENC_COMPARE_1)
        ret, self.__encoder_compare_reg_2 = self.get_info(acaplib2.ACL_ENC_COMPARE_2)
        ret, self.__encoder_abs_mode = self.get_info(acaplib2.ACL_ENC_ABS_MODE)
        ret, self.__encoder_abs_start = self.get_info(acaplib2.ACL_ENC_ABS_START)
        
        ret, self.__strobe_enable = self.get_info(acaplib2.ACL_STROBE_EN)
        ret, self.__strobe_delay = self.get_info(acaplib2.ACL_STROBE_DELAY)
        ret, self.__strobe_time = self.get_info(acaplib2.ACL_STROBE_TIME)
        ret, self.__strobe_pol = self.get_info(acaplib2.ACL_STROBE_POL)
        
        ret, self.__reverse_dma_enable = self.get_info(acaplib2.ACL_REVERSE_DMA)
        ret, self.__dval_enable = self.get_info(acaplib2.ACL_DVAL_EN)
        ret, self.__tap_num = self.get_info(acaplib2.ACL_TAP_NUM)
        ret, self.__tap_arrange = self.get_info(acaplib2.ACL_TAP_ARRANGE)
        ret, self.__tap_arrange_x_size = self.get_info(acaplib2.ACL_ARRANGE_XSIZE)
        
        ret, self.__tap_direction1 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 1)
        ret, self.__tap_direction2 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 2)
        ret, self.__tap_direction3 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 3)
        ret, self.__tap_direction4 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 4)
        ret, self.__tap_direction5 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 5)
        ret, self.__tap_direction6 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 6)
        ret, self.__tap_direction7 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 7)
        ret, self.__tap_direction8 = self.get_info(acaplib2.ACL_TAP_DIRECTION, 8)
        
        ret, self.__sync_lt = self.get_info(acaplib2.ACL_SYNC_LT)
        ret, self.__gpout_sel = self.get_info(acaplib2.ACL_GPOUT_SEL)
        ret, self.__gpout_pol = self.get_info(acaplib2.ACL_GPOUT_POL)

        ret, self.__interrupt_line = self.get_info(acaplib2.ACL_INTR_LINE)

        ret, self.__trigger_enable = self.get_info(acaplib2.ACL_EXP_EN)

        ret, self.__data_mask_lower = self.get_info(acaplib2.ACL_DATA_MASK_LOWER)
        ret, self.__data_mask_upper = self.get_info(acaplib2.ACL_DATA_MASK_UPPER)

        ret, self.__chatter_separate = self.get_info(acaplib2.ACL_EXT_CHATTER_SEPARATE)

        ret, self.__gpin_pin_sel = self.get_info(acaplib2.ACL_GPIN_PIN_SEL)
        
        ret, self.__sync_ch = self.get_info(acaplib2.ACL_SYNC_CH)

        ret, self.__bayer_enable = self.get_info(acaplib2.ACL_BAYER_ENABLE)
        ret, self.__bayer_grid = self.get_info(acaplib2.ACL_BAYER_GRID)
        ret, self.__bayer_input_bit = self.get_info(acaplib2.ACL_BAYER_INPUT_BIT)
        ret, self.__bayer_output_bit = self.get_info(acaplib2.ACL_BAYER_OUTPUT_BIT)


        ret, self.__vertical_remap = self.get_info(acaplib2.ACL_VERTICAL_REMAP)

        ret, self.__express_link = self.get_info(acaplib2.ACL_EXPRESS_LINK)

        ret, self.__fpga_version = self.get_info(acaplib2.ACL_FPGA_VERSION)


        ret, self.__lval_delay = self.get_info(acaplib2.ACL_LVAL_DELAY)
        ret, self.__line_reverse = self.get_info(acaplib2.ACL_LINE_REVERSE)

        ret, self.__start_frame_no = self.get_info(acaplib2.ACL_START_FRAME_NO)

        #ret, self.__cancel_initialize = self.get_info(acaplib2.ACL_CANCEL_INITIALIZE)

        ret, self.__buffer_zero_fill = self.get_info(acaplib2.ACL_BUFFER_ZERO_FILL)

        ret, self.__cc_stop = self.get_info(acaplib2.ACL_CC_STOP)

        ret, self.__cc_stop = self.get_info(acaplib2.ACL_CC_STOP)

        ret, self.__lvds_cclk_sel = self.get_info(acaplib2.ACL_LVDS_CCLK_SEL)
        ret, self.__lvds_phase_sel = self.get_info(acaplib2.ACL_LVDS_PHASE_SEL)
        ret, self.__lvds_synclt_sel = self.get_info(acaplib2.ACL_LVDS_SYNCLT_SEL)

        ret, self.__virtual_comport = self.get_info(acaplib2.ACL_VIRTUAL_COMPORT)
        
        ret, self.__pocl_lite_enable = self.get_info(acaplib2.ACL_POCL_LITE_ENABLE)

        ret, self.__cxp_bitrate = self.get_info(acaplib2.ACL_CXP_BITRATE)
        #ret, self.__cxp_link_speed = self.get_info(acaplib2._ACL_CXP_LINK_SPEED) #_ACL_CXP_LINK_SPEEDは下位互換→最新：ACL_CXP_BITRATE
        self.__cxp_link_speed = self.__cxp_bitrate

        ret, self.__cxp_acquision_start_address = self.get_info(acaplib2.ACL_CXP_ACQ_START_ADR)
        ret, self.__cxp_acquision_start_value = self.get_info(acaplib2.ACL_CXP_ACQ_START_VALUE)
        ret, self.__cxp_acquision_stop_address = self.get_info(acaplib2.ACL_CXP_ACQ_STOP_ADR)
        ret, self.__cxp_acquision_stop_value = self.get_info(acaplib2.ACL_CXP_ACQ_STOP_VALUE)
        ret, self.__cxp_pixel_format_address = self.get_info(acaplib2.ACL_CXP_PIX_FORMAT_ADR)
        ret, self.__cxp_pixel_format = self.get_info(acaplib2.ACL_CXP_PIX_FORMAT)
        
        ret, self.__rgb_swap_enable = self.get_info(acaplib2.ACL_RGB_SWAP_ENABLE)

        #ret, self.__camera_state = self.get_info(acaplib2.ACL_CAMERA_STATE)
        #ret, self.__gpin_pol = self.get_info(acaplib2.ACL_GPIN_POL)
        
        ret, self.__narrow10bit_enable = self.get_info(acaplib2.ACL_NARROW10BIT_ENABLE)

        ret, self.__infrared_enable = self.get_info(acaplib2.ACL_INFRARED_ENABLE)
        
        ##Ver.7.1.0
        #ACL_A_CW_CCW					= 0x1A01	# A相の回転方向 (0:CW)
        #ACL_B_CW_CCW					= 0x1A02	# B相の回転方向 (0:CW)
        #ACL_FREQ_A						= 0x1A03	# A相の周波数  (Hz単位)
        #ACL_FREQ_B						= 0x1A04	# B相の周波数  (Hz単位) 
        #ACL_FREQ_Z						= 0x1A05	# Z相の周波数  (Hz単位)
        #ACL_FREQ_TTL1					= 0x1A08	# TTL1の周波数 (Hz単位)
        #ACL_FREQ_TTL2					= 0x1A09	# TTL2の周波数 (Hz単位)
        #ACL_FREQ_TTL3					= 0x1A0A	# TTL3の周波数 (Hz単位)
        #ACL_FREQ_TTL4					= 0x1A0B	# TTL4の周波数 (Hz単位)
        #ACL_FREQ_TTL5					= 0x1A0C	# TTL5の周波数 (Hz単位)
        #ACL_FREQ_TTL6					= 0x1A0D	# TTL6の周波数 (Hz単位)
        #ACL_FREQ_TTL7					= 0x1A0E	# TTL7の周波数 (Hz単位)
        #ACL_FREQ_TTL8					= 0x1A0F	# TTL8の周波数 (Hz単位)
        #ACL_FREQ_OPT1					= 0x1A10	# OPT1の周波数 (Hz単位)
        #ACL_FREQ_OPT2					= 0x1A11	# OPT2の周波数 (Hz単位)
        #ACL_FREQ_OPT3					= 0x1A12	# OPT3の周波数 (Hz単位)
        #ACL_FREQ_OPT4					= 0x1A13	# OPT4の周波数 (Hz単位)
        #ACL_FREQ_OPT5					= 0x1A14	# OPT5の周波数 (Hz単位)
        #ACL_FREQ_OPT6					= 0x1A15	# OPT6の周波数 (Hz単位)
        #ACL_FREQ_OPT7					= 0x1A16	# OPT7の周波数 (Hz単位)
        #ACL_FREQ_OPT8					= 0x1A17	# OPT8の周波数 (Hz単位)
        #ACL_FREQ_D						= 0x1A18	# D相の周波数  (Hz単位)

        ret, self.__driver_name = self.get_info(acaplib2.ACL_DRIVER_NAME)
        ret, self.__hw_protect = self.get_info(acaplib2.ACL_HW_PROTECT)

        ret = self.refrect_param()

        # リングバッファの確保
        ret = self.create_ring_buffer()
        if ret != self.OK:
            self.print_last_error()

        # グラブ中のフラグ
        self.__is_grab = False

        # 設定値の反映
        #ret = self.refrect_param() # create_ring_buffer中で行われている

        return self.OK
        
    def load_inifile(self, inifilename : str) -> int:
        '''Load the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).
        
        Returns
        -------
        ret : int
            Error information
        '''

        ret = self._select_file(inifilename)
            
        return ret

    def save_inifile(self, inifilename : str) -> int:
        '''Save the board configuration file (ini file).

        Parameters
        ----------
        inifilename : str
            Path of the board configuration file (ini file).
        
        Returns
        -------
        ret : int
            Error information
        '''

        ret = acaplib2.AcapSelectFile(self.__hHandle, self.__ch, inifilename, 1)
        if ret != acaplib2.ACL_RTN_OK:
            ret = self.print_last_error()
            return ret

        return ret

    def set_power_supply(self, value : int, wait_time : int = 3000) -> int:
        '''Controls the power supply to the camera

        Parameters
        ----------
        value : int
            Power OFF (0)
            Power ON  (1)
        wait_time : int
            This is the time to wait after changing the power supply to the camera until the camera clock is checked.          
        
        Returns
        -------
        ret : int
            Error information
        '''
        if wait_time < 100:
            wait_time = 100

        return self.set_info(acaplib2.ACL_POWER_SUPPLY, value, wait_time)

    def grab_start(self, input_num : int = 0) -> int:
        '''Start image input.

        Parameters
        ----------
        input_num : int
            Set the input method for the image.
        
        Returns
        -------
        ret : int
            Error information
        '''

        if len(self.__images) == 0:
            self.create_ring_buffer()

        if self.__refrect_param_flag == True:
            self.refrect_param()

        self.__input_num = input_num
        self.__last_frame_no = 0

        ret = acaplib2.AcapGrabStart(self.__hHandle, self.__ch, input_num )
        if ret != AcaPy.OK:
            #AcapGrabStartに失敗した場合
            self.print_last_error()
            self.__is_grab = False
        else:
            self.__is_grab = True

        return ret

    def grab_stop(self) -> int:
        '''Stop image input.

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapGrabStop(self.__hHandle, self.__ch)
        self.__is_grab = False
        return ret

    def grab_abort(self) -> int:
        '''Abort image input.

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapGrabAbort(self.__hHandle, self.__ch)
        self.__is_grab = False
        return ret

    def wait_grab_start(self, timeout = 0) -> int:
        '''Wait for Grab to start.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' is 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
        '''

        if timeout == 0:
            timeout = self.__timeout

        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABSTART, timeout)

    def wait_frame_end(self, timeout = -1) -> int:
        '''Wait for the completion of frame image input.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
        '''

        if timeout < 0:
            timeout = self.__timeout

        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_FRAMEEND, self.__timeout)

    def wait_grab_end(self, timeout = -1) -> int:
        '''Wait for the image input to stop.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
        '''

        if timeout < 0:
            timeout = self.__timeout
            if self.__input_num != 0:
                timeout = self.__timeout * self.__input_num

        ret = acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GRABEND, timeout)
        self.__is_grab = False

        return ret

    def wait_gpin(self, timeout = -1) -> int:
        '''Wait for gpin.

        Parameters
        ----------
        timeout : int
            Timeout period(mSec)
            When 'timeout' < 0, the timeout time in the ini file setting is used.

        Returns
        -------
        ret : int
            Error information
        '''

        if timeout < 0:
            timeout = self.__timeout

        return acaplib2.AcapWaitEvent(self.__hHandle, self.__ch, acaplib2.ACL_INT_GPIN, timeout)

    def get_frame_no(self) -> Tuple[int, int, int , int]:
        '''Get the current frame number, line number, and memory index number.

        Returns
        -------
        ret : int
            Error information
        frame_no : int
            Current frame number
        line : int
            Current line number
        index : int
            Current memory index number(1, 2, 3・・・)
        '''
        return acaplib2.AcapGetFrameNo(self.__hHandle, self.__ch)
    
    def read(self, copy : bool = False, wait_frame : bool = True) -> Tuple[int, Union[np.ndarray, None], int, int]:
        '''Get the frame image currently being input during Grab.

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 
        wait_frame : bool
            Specifies whether to wait for the frame input to complete.
            True : Wait  
            False :Don't wait           
        
        Returns
        -------
        ret : int
            Error information
        frame : np.ndarray
            Frame image
        frame_no : int
            Current frame number
        line : int
            Number of lines that have been entered
        '''

        if wait_frame == True:
            ret = self.wait_frame_end() # フレームの入力完了を待つ
            if ret != self.OK: # タイムアウトエラー
                self._debug_print("[Error] wait_frame_end: Time out")
                return ret, None, 0, 0

        # 現在のフレーム番号の取得
        ret, frame_no, line, index = self.get_frame_no()
        if ret != self.OK:
            return ret, None, 0, 0

        frame = self.__images[index - 1] # 画像データ(ndarray)

        if copy == True:
            frame = frame.copy()

        return ret, frame, frame_no, line

    def read_frames(self, copy : bool = False) -> Tuple[int, Union[List[np.ndarray], None], int, int]:
        '''
        Get the frame image from the previous frame image to the current frame image during Grab.

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 

        Returns
        ----------
        ret : int
            Error information(success(1), Failure(0, Time out), Frame overwritten(< 0))
        frames : List[np.ndarray]
            Array of frame images from the previous frame image to the current frame image.
        count : int
            Number of frame images acquired.
        frame_no : int
            Frame number where the current input was completed.
        '''

        ret_frame_end = self.wait_frame_end() # フレームの入力完了を待つ
        # 取得した画像までを返すために、ここではエラー処理をしない

        # 現在のフレーム番号の取得
        ret, frame_no, _, index = self.get_frame_no()
        index -= 1

        if ret != self.OK:
            self.print_last_error()
            return ret, None, 0, 0

        count = frame_no - self.__last_frame_no

        if count > self.__mem_num:
            ret = self.__mem_num - count # 不足した枚数を負で返す
            self._debug_print("[Warning] read_frames: {0} frames overwritten".format(-ret))
            
        elif count == 0:
            #self._debug_print("[Error] wait_frame_end: Time out")
            #return self.ERROR, None, 0, 0
            if ret_frame_end == self.OK:
                return self.read_frames(copy)
            else:
                return ret_frame_end, None, 0, 0
        else:
            ret = self.OK

        frames = []

        # 前回のフレーム番号の次から、現在のフレーム番号までを処理する
        for fno in range(self.__last_frame_no + 1, frame_no + 1):
            index_no = (index + fno - frame_no + self.__mem_num) % self.__mem_num
            image = self.__images[index_no] # 画像データ(ndarray)
            if copy == True:
                frames.append(image.copy())
            else:
                frames.append(image)

        self.__last_frame_no = frame_no

        return ret, frames, count, frame_no

    def create_ring_buffer(self):
        ''' リングバッファの確保（mem_numの設定時、サイズ変更時に同時に行う）'''

        # バッファを解除
        ret = acaplib2.AcapSetBufferAddress(
            self.__hHandle, 
            self.__ch, 
            acaplib2.ACL_IMAGE_PTR,
            0,
            None)

        self.__refrect_param_flag = True

        if ret != self.OK:
            self.print_last_error()

        self.__images = acaplib2.CreateRingBuf(self.__hHandle, self.__ch, self.__mem_num)

        for i in range(self.__mem_num):

            ret = acaplib2.AcapSetBufferAddress(
                self.__hHandle, 
                self.__ch, 
                acaplib2.ACL_IMAGE_PTR, 
                -(i + 1), 
                acaplib2.GetImageBufPointer(self.__images[i])
                )
            if ret != self.OK:
                # 最初の１回目だけLastErrorを表示する
                if i == 0:
                    self.print_last_error()
                # 毎回エラーを表示する
                print("[Error] AcapSetBufferAddress")
                
        ret = self.refrect_param()
        if ret != self.OK:
            self.print_last_error()

        return ret

    def get_image_data(self, index : int) -> Union[np.ndarray, None]:
        '''
        Get the data of the ring buffer by specifying the index number(0, 1, 2...).

        Parameters
        ----------
        index : int
            Index number of the ring buffer

        Returns
        ----------
        image : np.ndarray
            data of the ring buffer
        '''

        if index >= len(self.__images) or index < 0:
            return None

        return self.__images[index]

    def snap(self, copy : bool = False) -> Tuple[int, Union[np.ndarray, None]]:
        '''Get a single image.(For continuous acquisition, use Grab.)

        Parameters
        ----------
        copy : bool
            Specifies whether or not to copy and retrieve image data.
            True : Copy  
            False :Not copy 

        Returns
        -------
        ret : int
            Error information
        frame : np.ndarray
            Frame image
        '''

        if (self.__is_grab == True):
            return AcaPy.ERROR, None

        # 入力開始
        if self.grab_start(1) != AcaPy.OK:
            return AcaPy.ERROR, None

        # フレーム画像の読込
        ret, image, _, _ = self.read(copy)
        if ret != AcaPy.OK:
            self.print_last_error()
            self.grab_stop()
            return AcaPy.ERROR, None

        # 入力停止
        if self.grab_stop() != AcaPy.OK:
            self.print_last_error()
            return AcaPy.ERROR, None

        # 現在のフレーム番号の取得
        return ret, image

    def count_reset(self) -> bool:
        '''Reset all counters. No meaning to the set value.'''
        return self.set_info(acaplib2.ACL_COUNT_RESET, 0)

    def cxp_link_reset(self) -> bool:
        '''Establishes the camera connection (reinitialization) for the connected camera.The value has no meaning.'''
        return self.set_info(acaplib2.ACL_CXP_LINK_RESET, 0)
 
    def opt_link_reset(self) -> bool:
        '''This command resets (reinitializes) the Opt-C:Link board.'''
        return self.set_info(acaplib2.ACL_OPT_LINK_RESET, 0, 0) 

    def print_acapy_values(self):
        '''Print the value set by acapy on the terminal.'''
        for key, value in self.__dict__.items():
            if key.startswith("_AcaPy__images") == False:
                key_len = len(key[8:])
                tab_count = key_len // 8
                tab_count = 4 - tab_count
                if tab_count < 1:
                    tab_count = 1
                self._debug_print(key[8:] + "\t" * tab_count, value)

    def _debug_print(self, str1, str2 = "", str3 = "", str4 = "", str5 = ""):
        if self.__debug_print == False:
            return
        print(str1, str2, str3, str4, str5)

    def get_last_error(self, error_reset : bool = False) -> acaplib2.ACAPERRORINFO:
        '''Get information about the last error that occurred.

        Parameters
        ----------
        error_reset : bool
            When True, resets the stored value.

        Returns
        -------
        error_info : acaplib2.ACAPERRORINFO
            Error information
        '''
        return acaplib2.AcapGetLastErrorCode(error_reset)

    def print_last_error(self) -> acaplib2.ACAPERRORINFO:
        '''Print the last error information that occurred in the terminal.

        Returns
        -------
        error_info : acaplib2.ACAPERRORINFO
            Error information
        '''
        error_info = self.get_last_error()

        extend_error = str(acaplib2.get_error_name(error_info.dwExtendErrorCode))
        if extend_error == "NO_ERROR":
            extend_error = ""

        self._debug_print(
            "------------------ Error --------------------\n" +
            "Common\t:"+ str(acaplib2.get_error_name(error_info.dwCommonErrorCode)) + "\n" +
            "Board\t:" + str(acaplib2.get_error_name(error_info.dwBoardErrorCode & 0x00FF)) + "\n" +
            "Extend\t:" + extend_error + "\n" +
            "---------------------------------------------"
            )
        return error_info

    def _set_event(self, event_id : int, event_enable : int) -> int:
        '''Registering interrupt events

        Parameters
        ----------
        event_id : int
            Specify the interrupt to register event notification.
            acaplib2.ACL_INT_GRABSTART
            acaplib2.ACL_INT_FRAMEEND
            acaplib2.ACL_INT_GRABEND
            acaplib2.ACL_INT_GPIN
        event_enable : int
            0:Exclude
            1:Registration

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetEvent(
                self.__hHandle, self.__ch, 
                event_id, event_enable
                )
        if ret != self.OK:
            self.print_last_error()
        return ret

    def set_shutter_trigger(self, exp_cycle : int, exposure : int, exp_pol : int, exp_unit : int, cc_sel : int) -> int:
        '''Setting the area sensor shutter trigger

        Parameters
        ----------
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        exp_unit : int
            Non support
        cc_sel : int
            Number of the CC signal to be output

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetShutterTrigger(
                self.__hHandle, self.__ch, 
                exp_cycle, exposure, exp_pol, exp_unit, cc_sel
                )
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_shutter_trigger(self) -> Tuple[int, int, int, int, int, int]:
        '''Get the shutter trigger setting.

        Returns
        -------
        ret : int
            Error information
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        exp_unit : int
            Non support
        cc_sel : int
            Number of the CC signal to be output
        '''
        ret = acaplib2.AcapGetShutterTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_line_trigger(self, exp_cycle : int, exposure : int, exp_pol : int) -> int:
        '''Set up the line trigger

        Parameters
        ----------
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetLineTrigger(self.__hHandle, self.__ch, exp_cycle, exposure, exp_pol)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_line_trigger(self) -> Tuple[int, int, int, int]:
        '''Get line trigger setting

        Returns
        -------
        ret : int
            Error information
        exp_cycle : int
            CC output cycle (1uSec unit)
        exposure : int
            CC Output width (1uSec unit)
        exp_pol : int
            Output logic
            0:negative logic
            1:positive logic
        '''
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetLineTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_external_trigger(self, exp_trg_en : int, ext_trg_mode : int, ext_trg_dly : int, ext_trg_chatter : int, timeout : int) -> int:
        '''External trigger setting

        Parameters
        ----------
        exp_trg_en : int
            Select the signal to be used as an external trigger
            0 : Disable
            1: TTL trigger
            2: Differential trigger (shared with encoder)
            3: New differential trigger
            4: OPT trigger
        ext_trg_mode : int
            External trigger mode
            0 : Mode in which CC is output once by one external trigger (Continuous external trigger mode)
            1 : Mode in which CC is output periodically by one external trigger (single shot external trigger mode)
        ext_trg_dly : int
            External trigger detection delay time (1uSec unit)
        ext_trg_chatter : int
            External trigger detection disable time (1uSec unit)
        timeout : int
            Detection standby time (1mSec unit)

        Returns
        -------
        ret : int
            Error information

        '''
        ret = acaplib2.AcapSetExternalTrigger(self.__hHandle, self.__ch, exp_trg_en, ext_trg_mode, ext_trg_dly, ext_trg_chatter, timeout)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_external_trigger(self) -> Tuple[int, int, int, int, int, int]:
        '''Get external trigger setting

        Returns
        -------
        ret : int
            Error information
        exp_trg_en : int
            Select the signal to be used as an external trigger
            0 : Disable
            1: TTL trigger
            2: Differential trigger (shared with encoder)
            3: New differential trigger
            4: OPT trigger
        ext_trg_mode : int
            External trigger mode
            0 : Mode in which CC is output once by one external trigger (Continuous external trigger mode)
            1 : Mode in which CC is output periodically by one external trigger (single shot external trigger mode)
        ext_trg_dly : int
            External trigger detection delay time (1uSec unit)
        ext_trg_chatter : int
            External trigger detection disable time (1uSec unit)
        timeout : int
            Detection standby time (1mSec unit)
        '''
        # -> exp_cycle, exposure, exp_pol, exp_unit, cc_sel
        ret = acaplib2.AcapGetExternalTrigger(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_strobe(self, strobe_en : int, strobe_delay : int, strobe_time : int) -> int:
        '''Strobe setting

        Parameters
        ----------
        strobe_en : int
            Strobe Use setting
            0 : Disable
            1: Enabled
        strobe_delay : int
            Delay time until strobe pulse is output (1uSec unit) 0~65535
        strobe_time : int
            Strobe pulse output time (1uSec unit) 0~65535

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetStrobe(self.__hHandle, self.__ch, strobe_en, strobe_delay, strobe_time)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_strobe(self) -> Tuple[int, int, int, int]:
        '''Get strobe setting

        Returns
        -------
        ret : int
            Error information
        strobe_en : int
            Strobe Use setting
            0 : Disable
            1: Enabled
        strobe_delay : int
            Delay time until strobe pulse is output (1uSec unit) 0~65535
        strobe_time : int
            Strobe pulse output time (1uSec unit) 0~65535
        '''
        ret = acaplib2.AcapGetStrobe(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_encoder(self, enc_enable : int, enc_mode : int, enc_start : int, enc_phase : int, enc_direction : int, z_phase_enable : int, compare1 : int, compare2 : int) -> int:
        '''Encoder settings

        Parameters
        ----------
        enc_enable : int
            Encoder use setting
            0 : Disable
            1: Enabled
        enc_mode : int
            Encoder mode
            0 : Encoder scan mode
            1 : Encoder line selection mode
        enc_start : int
            How to start the encoder
            0 : Start the encoder by CPU
            1 : Start the encoder with an external trigger
            2 : Start the encoder with the CPU and use the external trigger as matching pulses
        enc_phase : int
            Encoder phase
            0 : AB phase
            1 : A phase
        enc_direction : int
            Encoder rotation direction
            0 : CW
            1 : CCW
        z_phase_enable : int
            Z-phase usage settings
            0 : Not used
            1 : Use
        compare1 : int
            Comparison register 1 (delay pulse setting) 0~4294967295
        compare2 : int
            Comparison register 2 (interval pulse setting) 1~4294967295

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSetEncoder(self.__hHandle, self.__ch, enc_enable, enc_mode, enc_start, enc_phase, enc_direction, z_phase_enable, compare1, compare2)
        if ret != self.OK:
            self.print_last_error()
        return ret

    def get_encoder(self) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        '''Get the encoder setting value

        Returns
        -------
        ret : int
            Error information
        enc_enable : int
            Encoder use setting
            0 : Disable
            1: Enabled
        enc_mode : int
            Encoder mode
            0 : Encoder scan mode
            1 : Encoder line selection mode
        enc_start : int
            How to start the encoder
            0 : Start the encoder by CPU
            1 : Start the encoder with an external trigger
            2 : Start the encoder with the CPU and use the external trigger as matching pulses
        enc_phase : int
            Encoder phase
            0 : AB phase
            1 : A phase
        enc_direction : int
            Encoder rotation direction
            0 : CW
            1 : CCW
        z_phase_enable : int
            Z-phase usage settings
            0 : Not used
            1 : Use
        compare1 : int
            Comparison register 1 (delay pulse setting) 0~4294967295
        compare2 : int
            Comparison register 2 (interval pulse setting) 1~4294967295
        comp2_count : int
            Encoder count value
        '''
        ret = acaplib2.AcapGetEncoder(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret

    def set_encoder_abs_multipoint(self, point_no : int, abs_count : int) -> int:
        '''Set the multipoint value of the encoder absolute count.

        Parameters
        ----------
        point_no : int
            Multipoint number
        abs_count : int
            Absolute count value

        Returns
        -------
        ret : int
            Error information
        '''
        return self.set_info(acaplib2.ACL_ENC_ABS_MP_COUNT, abs_count, point_no)

    def get_encoder_abs_multipoint(self, point_no : int) -> Tuple[int, int]:
        '''Get the multipoint value of the encoder absolute count.

        Parameters
        ----------
        point_no : int
            Multipoint number

        Returns
        -------
        ret : int
            Error information
        abs_count : int
            Absolute count value
        '''
        return self.get_info(acaplib2.ACL_ENC_ABS_MP_COUNT, point_no)

    #def set_bit_assign_ex(self, bit_assign_info):
    #    ret = acaplib2.AcapSetBitAssignEx(self.__hHandle, self.__ch, bit_assign_info)
    #    if ret != self.OK:
    #        self.print_last_error()
    #    return ret

    #def get_bit_assign_ex(self):
    #    ret = acaplib2.AcapGetBitAssignEx(self.__hHandle, self.__ch)
    #    if ret[0] != self.OK:
    #        self.print_last_error()
    #    return ret

    #def set_dma_option_ex(self, mem_num, acl_buffer_info):
    #    ret = acaplib2.AcapSetDmaOptionEx(self.__hHandle, self.__ch, mem_num, acl_buffer_info)
    #    if ret != self.OK:
    #        self.print_last_error()
    #    return ret

    #def get_dma_option_ex(self, mem_num):
    #    ret = acaplib2.AcapGetDmaOptionEx(self.__hHandle, self.__ch, mem_num)
    #    if ret[0] != self.OK:
    #        self.print_last_error()
    #    return ret


    def _serial_set_parameter(self, baud_rate = 9600, data_bit = 8, parity = 0, stop_bit = 0, flow = 0) -> int:
        
        # Open後にしか設定できない
        if self.__is_serial_open == False:
            return self.ERROR

        ret = acaplib2.AcapSerialSetParameter(self.__hHandle, self.__ch, 
            baud_rate, data_bit, parity, stop_bit, flow)

        if ret != self.OK:
            self.print_last_error()

        return ret

    def serial_get_parameter(self) -> Tuple[int, int, int, int, int, int]:
        '''Get the parameters for serial communication.

        Returns
        -------
        ret : int
            Error information
        baud_rate : int
            baud rate
        data_bit : int
            Data bits (5 to 8) are stored.
        parity : int
            The parity setting information is stored.
            0 : None
            1 : Odd number
            2 : Even number
            3 : Mark
            4 : Space
        stop_bit : int
            Stop bit
            0 : 1bit
            1 : 1.5bit
            2 : 2bit
        flow : int
            Flow control information
            0 : None
            1 : Xon / Xoff
            2 : Hardware
        '''
        baud_rate = 0
        data_bit = 0
        parity = 0
        stop_bit = 0
        flow = 0
        
        # Open後にしか取得できない
        if self.__is_serial_open == False:
            return self.ERROR, baud_rate, data_bit, parity, stop_bit, flow

        # ret, npBaudRate.value, npDataBit.value, npParity.value, npStopBit.value, npFlow.value
        ret, baud_rate, data_bit, parity, stop_bit, flow = acaplib2.AcapSerialGetParameter(self.__hHandle, self.__ch)

        if ret != self.OK:
            self.print_last_error()

        return ret, baud_rate, data_bit, parity, stop_bit, flow

    def serial_open(self, baud_rate : int = 9600, data_bit : int = 8, parity : int = 0, stop_bit : int = 0, flow : int = 0) -> int:
        '''Open the serial port.

        Parameters
        ----------
        baud_rate : int
            Baud rate
        baud_rate : int
            Baud rate
            9600, 19200, 38400, 57600, 115200​
        data_bit : int
            Data bit(8 only)
        parity : int
            Parity(0 only)
            0 : None
            1 : Odd number
            2 : Even number
            3 : Mark
            4 : Space
        stop_bit : int
            Stop bit(0 only)
            0 : 1bit
            1 : 1.5bit
            2 : 2bit
        flow : int
            Flow control information(0 only)
            0 : None
            1 : Xon / Xoff
            2 : Hardware

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSerialOpen(self.__hHandle, self.__ch)
        if ret != self.OK:
            self.print_last_error()
            return self.ERROR

        self.__is_serial_open = True

        ret = self._serial_set_parameter( baud_rate, data_bit, parity, stop_bit, flow)

        return ret

    def serial_close(self) -> int:
        '''Close the serial port.

        Returns
        -------
        ret : int
            Error information
        '''

        if self.__is_serial_open == False:
            return

        if self.__hHandle == acaplib2.INVALID_HANDLE_VALUE:
            return

        ret = acaplib2.AcapSerialClose(self.__hHandle, self.__ch)
        if ret != self.OK:
            self.print_last_error()

        self.__is_serial_open = False

        return ret

    def serial_write(self, write_command : str, asc : bool = True, start_str : Union[str, None] = None, end_str : Union[str, None] = "\r") -> int:
        
        '''Serial transmission

        Parameters
        ----------
        write_command : str
            Commands to be sent to serial
        asc : bool
            Specifies the code for characters to be written (sent) to the serial.
            False : Hexadecimal (HEX) notation
            True : ASCII
        start_str : str
            Can be specified when 'asc' is TRUE.
            Command start string (ASCII notation)
        end_str : str
            Can be specified when 'asc' is TRUE.
            Command terminator string (ASCII notation)

        Returns
        -------
        ret : int
            Error information
        '''
        ret = acaplib2.AcapSerialWrite(self.__hHandle, self.__ch, asc, write_command, start_str, end_str)
        if ret != self.OK:
            self.print_last_error()
        return ret
    
    def serial_read(self, asc : bool = True, time_out : int = 100, buffer_size : int = 511, end_str : Union[str, None] = None) -> Tuple[int, str, int]:
        '''Serial Reception

        Parameters
        ----------
        asc : bool
            Specifies the code for characters to be written (sent) to the serial.
            False : Hexadecimal (HEX) notation
            True : ASCII
        time_out : int
            Specifies the timeout [mSec] until the end of the received data buffer matches the terminated string.
            If 0 is specified, the data is received without waiting.
        buffer_size : int
            Specifies the command string storage buffer size.
        end_str : Union[str, None]
            Set the command terminator string.

        Returns
        -------
        ret : int
            Error information
        read_command : str
            Received command string
        read_bytes
            Size of the received string (in bytes)
        '''

        recieve = ""
        recieve_flag = True
        recieve_size = 0
        zero_count = 0

        while recieve_flag == True:
            ret, text, str_len = acaplib2.AcapSerialRead(self.__hHandle, self.__ch, asc, time_out, buffer_size, end_str)
            recieve += text
            recieve_size += str_len
            if str_len == 0:
                time.sleep(0.2)
                zero_count += 1
            else:
                zero_count = 0
            if zero_count >= 2 or end_str is not None:
                # 2回連続で受信バッファが何も無ければ受信を抜ける、最後はここで抜ける
                recieve_flag = False #念のため
                break

        if ret != acaplib2.ACL_RTN_OK and end_str is None:
            if recieve_size > 0:
                ret = acaplib2.ACL_RTN_OK

        return ret, recieve, recieve_size

    def set_gpout(self, output_level : int) -> int:
        '''Set the GPOUT level.

        Parameters
        ----------
        output_level : int
            GPOUT level

        Returns
        -------
        ret : int
            Error information
        '''

        ret = acaplib2.AcapSetGPOut(self.__hHandle, self.__ch, output_level)
        if ret != self.OK:
            self.print_last_error()
        return ret


    def get_gpout(self) -> Tuple[int, int]:
        '''Get the GPOUT level.

        Returns
        -------
        ret : int
            Error information
        output_level : int
            GPOUT level
        '''
        ret = acaplib2.AcapGetGPOut(self.__hHandle, self.__ch)
        if ret[0] != self.OK:
            self.print_last_error()
        return ret
