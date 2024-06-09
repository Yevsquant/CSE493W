#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: runyingchen
# GNU Radio version: 3.8.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import epy_block_0
import math
import osmosdr
import time

from gnuradio import qtgui

class fmcwRadar(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fmcwRadar")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.update_period = update_period = 0.5e-4
        self.tx_rx_sps = tx_rx_sps = 2e6
        self.transition_width = transition_width = 5e4
        self.sweep_bandwidth = sweep_bandwidth = 1e6
        self.source_freq = source_freq = 1e3
        self.samp_rate = samp_rate = 10e6
        self.radar_freq = radar_freq = 2e9
        self.delay_ = delay_ = 50
        self.cutoff_freq = cutoff_freq = 0
        self.RF_tx = RF_tx = 50
        self.RF_rx = RF_rx = 50
        self.IF_tx = IF_tx = 30
        self.IF_rx = IF_rx = 30
        self.BB_tx = BB_tx = 30
        self.BB_rx = BB_rx = 30

        ##################################################
        # Blocks
        ##################################################
        self._delay__range = Range(0, 5e3, 5, 50, 200)
        self._delay__win = RangeWidget(self._delay__range, self.set_delay_, 'Delay', "counter_slider", float)
        self.top_layout.addWidget(self._delay__win)
        self._cutoff_freq_range = Range(0, 30e6, 1e2, 0, 200)
        self._cutoff_freq_win = RangeWidget(self._cutoff_freq_range, self.set_cutoff_freq, 'cutoff_freq', "counter_slider", float)
        self.top_layout.addWidget(self._cutoff_freq_win)
        self._RF_tx_range = Range(10, 100, 5, 50, 200)
        self._RF_tx_win = RangeWidget(self._RF_tx_range, self.set_RF_tx, 'RF Gain (tx)', "counter_slider", float)
        self.top_layout.addWidget(self._RF_tx_win)
        self._RF_rx_range = Range(10, 100, 5, 50, 200)
        self._RF_rx_win = RangeWidget(self._RF_rx_range, self.set_RF_rx, 'RF Gain (rx)', "counter_slider", float)
        self.top_layout.addWidget(self._RF_rx_win)
        self._IF_tx_range = Range(10, 100, 5, 30, 200)
        self._IF_tx_win = RangeWidget(self._IF_tx_range, self.set_IF_tx, 'IF Gain (tx)', "counter_slider", float)
        self.top_layout.addWidget(self._IF_tx_win)
        self._IF_rx_range = Range(10, 100, 5, 30, 200)
        self._IF_rx_win = RangeWidget(self._IF_rx_range, self.set_IF_rx, 'IF Gain (rx)', "counter_slider", float)
        self.top_layout.addWidget(self._IF_rx_win)
        self._BB_tx_range = Range(10, 100, 5, 30, 200)
        self._BB_tx_win = RangeWidget(self._BB_tx_range, self.set_BB_tx, 'BB Gain (tx)', "counter_slider", float)
        self.top_layout.addWidget(self._BB_tx_win)
        self._BB_rx_range = Range(10, 100, 5, 30, 200)
        self._BB_rx_win = RangeWidget(self._BB_rx_range, self.set_BB_rx, 'BB Gain (rx)', "counter_slider", float)
        self.top_layout.addWidget(self._BB_rx_win)
        self.qtgui_time_sink_x_4 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "beat frequency in time domain", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_4.set_update_time(update_period)
        self.qtgui_time_sink_x_4.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4.enable_tags(True)
        self.qtgui_time_sink_x_4.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4.enable_autoscale(False)
        self.qtgui_time_sink_x_4.enable_grid(False)
        self.qtgui_time_sink_x_4.enable_axis_labels(True)
        self.qtgui_time_sink_x_4.enable_control_panel(False)
        self.qtgui_time_sink_x_4.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_4.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_4.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_win = sip.wrapinstance(self.qtgui_time_sink_x_4.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "T and R", #name
            2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(update_period)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 2)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Transmitted signal', 'Received signal', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            1024,
            100,
            -10,
            10,
            "",
            1
        )

        self.qtgui_histogram_sink_x_0.set_update_time(update_period)
        self.qtgui_histogram_sink_x_0.enable_autoscale(False)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_histogram_sink_x_0_win)
        self.qtgui_freq_sink_x_4 = qtgui.freq_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "beat frequency", #name
            1
        )
        self.qtgui_freq_sink_x_4.set_update_time(update_period)
        self.qtgui_freq_sink_x_4.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_4.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_4.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_4.enable_autoscale(False)
        self.qtgui_freq_sink_x_4.enable_grid(False)
        self.qtgui_freq_sink_x_4.set_fft_average(1.0)
        self.qtgui_freq_sink_x_4.enable_axis_labels(True)
        self.qtgui_freq_sink_x_4.enable_control_panel(False)


        self.qtgui_freq_sink_x_4.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_4.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_4.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_4.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_4.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_4.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_4_win = sip.wrapinstance(self.qtgui_freq_sink_x_4.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_4_win)
        self.qtgui_freq_sink_x_2 = qtgui.freq_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "T and R", #name
            2
        )
        self.qtgui_freq_sink_x_2.set_update_time(update_period)
        self.qtgui_freq_sink_x_2.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_2.enable_grid(False)
        self.qtgui_freq_sink_x_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2.enable_control_panel(False)


        self.qtgui_freq_sink_x_2.set_plot_pos_half(not True)

        labels = ['Transmitted signal', 'Received signal', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "hackrf=1"
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(tx_rx_sps)
        self.osmosdr_source_0.set_center_freq(radar_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(RF_rx, 0)
        self.osmosdr_source_0.set_if_gain(IF_rx, 0)
        self.osmosdr_source_0.set_bb_gain(BB_rx, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.osmosdr_sink_0_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + "hackrf=0"
        )
        self.osmosdr_sink_0_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0_0.set_sample_rate(tx_rx_sps)
        self.osmosdr_sink_0_0.set_center_freq(radar_freq, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(RF_tx, 0)
        self.osmosdr_sink_0_0.set_if_gain(IF_tx, 0)
        self.osmosdr_sink_0_0.set_bb_gain(BB_tx, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(0, 0)
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                cutoff_freq,
                transition_width,
                firdes.WIN_HAMMING,
                6.76))
        self.hilbert_fc_0 = filter.hilbert_fc(65, firdes.WIN_HAMMING, 6.76)
        self.fft_vxx_0 = fft.fft_vfc(1024, True, window.blackmanharris(1024), 1)
        self.epy_block_0 = epy_block_0.blk(bw=sweep_bandwidth)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 1024)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, 2*math.pi*sweep_bandwidth, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 1024)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay_)
        self.blocks_complex_to_real_1_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_TRI_WAVE, source_freq, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_freq_sink_x_2, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_real_1_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_2, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_time_sink_x_4, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.hilbert_fc_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_complex_to_real_1_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.hilbert_fc_0, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_4, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_real_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fmcwRadar")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_update_period(self):
        return self.update_period

    def set_update_period(self, update_period):
        self.update_period = update_period
        self.qtgui_freq_sink_x_2.set_update_time(self.update_period)
        self.qtgui_freq_sink_x_4.set_update_time(self.update_period)
        self.qtgui_histogram_sink_x_0.set_update_time(self.update_period)
        self.qtgui_time_sink_x_1.set_update_time(self.update_period)
        self.qtgui_time_sink_x_4.set_update_time(self.update_period)

    def get_tx_rx_sps(self):
        return self.tx_rx_sps

    def set_tx_rx_sps(self, tx_rx_sps):
        self.tx_rx_sps = tx_rx_sps
        self.osmosdr_sink_0_0.set_sample_rate(self.tx_rx_sps)
        self.osmosdr_source_0.set_sample_rate(self.tx_rx_sps)

    def get_transition_width(self):
        return self.transition_width

    def set_transition_width(self, transition_width):
        self.transition_width = transition_width
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_sweep_bandwidth(self):
        return self.sweep_bandwidth

    def set_sweep_bandwidth(self, sweep_bandwidth):
        self.sweep_bandwidth = sweep_bandwidth
        self.epy_block_0.bw = self.sweep_bandwidth

    def get_source_freq(self):
        return self.source_freq

    def set_source_freq(self, source_freq):
        self.source_freq = source_freq
        self.analog_sig_source_x_0.set_frequency(self.source_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_2.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_4.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4.set_samp_rate(self.samp_rate)

    def get_radar_freq(self):
        return self.radar_freq

    def set_radar_freq(self, radar_freq):
        self.radar_freq = radar_freq
        self.osmosdr_sink_0_0.set_center_freq(self.radar_freq, 0)
        self.osmosdr_source_0.set_center_freq(self.radar_freq, 0)

    def get_delay_(self):
        return self.delay_

    def set_delay_(self, delay_):
        self.delay_ = delay_
        self.blocks_delay_0.set_dly(self.delay_)

    def get_cutoff_freq(self):
        return self.cutoff_freq

    def set_cutoff_freq(self, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff_freq, self.transition_width, firdes.WIN_HAMMING, 6.76))

    def get_RF_tx(self):
        return self.RF_tx

    def set_RF_tx(self, RF_tx):
        self.RF_tx = RF_tx
        self.osmosdr_sink_0_0.set_gain(self.RF_tx, 0)

    def get_RF_rx(self):
        return self.RF_rx

    def set_RF_rx(self, RF_rx):
        self.RF_rx = RF_rx
        self.osmosdr_source_0.set_gain(self.RF_rx, 0)

    def get_IF_tx(self):
        return self.IF_tx

    def set_IF_tx(self, IF_tx):
        self.IF_tx = IF_tx
        self.osmosdr_sink_0_0.set_if_gain(self.IF_tx, 0)

    def get_IF_rx(self):
        return self.IF_rx

    def set_IF_rx(self, IF_rx):
        self.IF_rx = IF_rx
        self.osmosdr_source_0.set_if_gain(self.IF_rx, 0)

    def get_BB_tx(self):
        return self.BB_tx

    def set_BB_tx(self, BB_tx):
        self.BB_tx = BB_tx
        self.osmosdr_sink_0_0.set_bb_gain(self.BB_tx, 0)

    def get_BB_rx(self):
        return self.BB_rx

    def set_BB_rx(self, BB_rx):
        self.BB_rx = BB_rx
        self.osmosdr_source_0.set_bb_gain(self.BB_rx, 0)





def main(top_block_cls=fmcwRadar, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
