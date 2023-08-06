# -*- coding: utf-8 -*-
"""
The main QtWidget
"""

# @File  : sim_widget.py
# @Author: Andy.yang
# @Date  : 2021/02/22
# @Software: VS Code

import time
import os
import sys
import json
from pathlib import Path
from threading import Thread

import numpy as np
import pandas as pd
from PyQt5.QtGui import QPainter, QFont, QStandardItemModel, QPen, QIcon, QPixmap, QPolygonF, QStandardItem
from PyQt5.QtWidgets import QWidget, QSlider, QToolButton, QSpinBox, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsLineItem, QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, Qt, QTimer, QSize, QRectF, QPointF, QPoint
from pyqtgraph import PlotWidget, GraphicsLayoutWidget, AxisItem, ViewBox, InfiniteLine, GridItem, ArrowItem, PlotDataItem, ScatterPlotItem, PlotCurveItem

from .camera_show import Camera

from ..ui.sim_ui import Ui_SimUI
from ..qmls.bsd_show import BsdWidget

from ..data.can_process import checkConnectStatusOfPeakCAN, readCanMsg, printOneCanMsg, filterCanID, writeCanMsg, switchStop, detection_mem_queue, startPushDetMem
from ..utils.utils import stopThread


class SimWidget(Ui_SimUI, QWidget):
    def __init__(self, parent=None):
        super(SimWidget, self).__init__(parent)
        self.setupUi(self)

        self._setSimWidgetUi()
        self._initVars()
        self._onPause()
        self.all_thread_list = []

    @pyqtSlot(int)
    def on_cBox_FF_currentIndexChanged(self, cur_id):
        """
        When the checked index of FF changed, show different widgets.

        Notice: only support bsd in current version
        """
        if (self.cBox_FF.currentIndex() == 1) and (not self.has_bsd_widget):
            # in bsd
            self.has_bsd_widget = True
            self.splitter_table.addWidget(self.bsd_widget)

            # render bsd-profile
            self._renderBsdZone()

        elif self.has_bsd_widget:
            self.has_bsd_widget = False
            self.splitter_table.widget(1).setParent(None)
            self.vb.removeItem(self.left_bsd_zone)
            self.vb.removeItem(self.right_bsd_zone)

    @pyqtSlot(int)
    def on_cBox_sim_stateChanged(self, status):
        if self.cBox_sim.isChecked():
            if self.cBox_FF.currentIndex() == 1:
                # in bsd mode
                DIR_PATH = os.path.dirname(
                    os.path.dirname(os.path.realpath(__file__)))
                sim_config_path = os.path.join(DIR_PATH, "config",
                                               "default_sim_input.json")
                with open(sim_config_path, 'r') as f:
                    data = json.load(f)
                    speed = data['vehicle_speed']
                    left_led = data['left_led']
                    right_led = data['right_led']
                    acc_st = data['acc']
                    en_st = data['enable']

                    self.bsd_widget.root_obj.update_speed(speed)
                    self.bsd_widget.root_obj.update_acc(acc_st)
                    self.bsd_widget.root_obj.update_enable(en_st)
                    self.bsd_widget.root_obj.update_left_indi(left_led)
                    self.bsd_widget.root_obj.update_right_indi(right_led)
        else:
            if self.cBox_FF.currentIndex() == 1:
                # in bsd mode
                self.bsd_widget.root_obj.update_speed(0)
                self.bsd_widget.root_obj.update_acc(1)
                self.bsd_widget.root_obj.update_enable(1)
                self.bsd_widget.root_obj.update_left_indi(1)
                self.bsd_widget.root_obj.update_right_indi(1)

    @pyqtSlot(int)
    def on_cBox_mode_currentIndexChanged(self, cur_id):
        """
        check the current play mode is in-line or off-line.
        If the current mode is in-line, the load-btn can't be clicked.
        """
        if self.cBox_mode.currentIndex() == 0:
            # off-Line mode
            self.btn_load.setEnabled(True)
            self.lab_data.setEnabled(True)
            self.lab_data.setText("Pls input the data")
            self.tBtn_start.setEnabled(False)
            self.tBtn_stop.setEnabled(False)
            self.cBox_save.setEnabled(False)

            self.stopAllThreads()
        else:
            # in-Line mode
            self.btn_load.setEnabled(False)
            self.lab_data.setEnabled(True)
            self.lab_data.setText("saved file name")
            self.tBtn_start.setEnabled(True)
            self.tBtn_stop.setEnabled(False)
            self.cBox_save.setEnabled(True)

            self.i_current_frame_num = 0
            # self.ts_len = 4294967296 is a error, because the value in range(-2147483647, 2147483647)
            self.ts_len = 2147483647
            # if self.cBox_cam.checkState() == 2:
            #     self.cam.openCamera()

            # set the maximum number
            self.slider.setMaximum(self.ts_len)
            self.slider.setValue(0)

            self.sBox_current_frame_num.setMaximum(self.ts_len)

            if checkConnectStatusOfPeakCAN():
                filterCanID()
                # printOneCanMsg()

                self.thread_getCanMsg = Thread(target=readCanMsg)
                # In order to close this all threads, should set Daemon.
                # See link: https://blog.csdn.net/whuzhang16/article/details/108627617
                self.thread_getCanMsg.setDaemon(True)
                self.all_thread_list.append(self.thread_getCanMsg)
                self.thread_getCanMsg.start()
            else:
                print("Peak-CAN is not connected")
                # raise Exception("Peak-CAN is not connected")

    @pyqtSlot()
    def on_btn_load_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select measurement file", "./", "json(*.json)")

        file_pth = Path(file_name)

        if (file_name is not None) and file_pth.suffix.lower() == ".json":
            self.lab_data.setText(file_pth.name)

            with open(file_name, 'r') as f_js:
                data_js = json.load(f_js)
                if "detections" in data_js.keys():
                    self.df_dection = pd.read_csv(data_js["detections"])
                    self.ts_len=max(self.df_dection.frame_id)
                    self.slider.setMaximum(self.ts_len)
                    self.slider.setValue(0)
                    self.sBox_current_frame_num.setMaximum(self.ts_len)
        else:
            QMessageBox.information(
                self, "Error", "No json file has been selected!")

    @pyqtSlot()
    def on_tBtn_start_clicked(self):
        """
        start to collect data
        """
        self.tBtn_start.setEnabled(False)
        self.tBtn_stop.setEnabled(True)

        switchStop(False)

        if self.thread_getCanMsg.is_alive():
            stopThread(self.thread_getCanMsg)

        filterCanID()

        self.thread_writeCanMsg = Thread(target=writeCanMsg)
        # In order to close this all threads, should set Daemon.
        # See link: https://blog.csdn.net/whuzhang16/article/details/108627617
        self.thread_writeCanMsg.setDaemon(True)
        self.all_thread_list.append(self.thread_writeCanMsg)

        self.thread_writeCanMsg.start()

        """
        if self.cBox_cam.checkState() == 2:
            # camera is checked
            self.cam.setWriteVideo(True)
        """
    @pyqtSlot()
    def on_tBtn_stop_clicked(self):
        """
        stop to collect data
        """
        self.tBtn_start.setEnabled(True)
        self.tBtn_stop.setEnabled(False)

        switchStop(True)
        
        # set 2s to store the json data
        time.sleep(2)
        
        fname, _ = QFileDialog.getSaveFileName(
            self, 'save file', './', "ALL (*.json*)")
        fname = Path(fname)
        if (fname is not None) and fname.suffix.lower() == ".json":
            self.lab_data.setText(fname.name)
        
        if self.thread_writeCanMsg.is_alive():
            stopThread(self.thread_writeCanMsg)
        """
        if self.cBox_cam.checkState() == 2:
            self.cam.setWriteVideo(False)
        """
        # self.cBox_mode.setCurrentIndex(0)
        # self.cBox_cam.setCheckState(0)

    @pyqtSlot(int)
    def on_cBox_cam_stateChanged(self, cur_st):
        if self.cBox_mode.currentIndex() == 1:
            # in-line mode
            if cur_st == 2:
                # check-camera
                self.cam.openCamera()
                # self.thread_camera = Thread(target= self.cam.openCamera())
                # self.thread_camera.setDaemon(True)
                # self.all_thread_list.append(self.thread_camera)
                # self.thread_camera.start()
            else:
                # uncheck-camera
                self.cam.closeCamera()
                # if self.thread_camera.is_alive():
                #     stopThread(self.thread_camera)
        else:
            # "off-line mode"
            print("Off-Line mode")

    def _setSimWidgetUi(self):
        """
        initialize the play, cycle, pause btn, and slider
        """
        # set the title and logo
        self.setWindowTitle("Deftech")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Sim/images/logo.png"), QIcon.Normal,
                       QIcon.Off)
        self.setWindowIcon(icon)

        # define btns
        iconsize = QSize(30, 30)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/Sim/images/cycle.png"), QIcon.Normal,
                       QIcon.Off)
        self.cycle_btn = QToolButton()
        self.cycle_btn.setIcon(icon)
        self.cycle_btn.setIconSize(iconsize)
        self.cycle_btn.setAutoRaise(True)
        self.cycle_btn.setToolTip('Play cycle')
        self.cycle_btn.clicked.connect(self._onCycle)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/Sim/images/play.png"), QIcon.Normal,
                       QIcon.Off)
        self.play_btn = QToolButton()
        self.play_btn.setIcon(icon)
        self.play_btn.setIconSize(iconsize)
        self.play_btn.setAutoRaise(True)
        self.play_btn.setToolTip('Play')
        self.play_btn.clicked.connect(self._onPlay)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/Sim/images/pause.png"), QIcon.Normal,
                       QIcon.Off)
        self.pause_btn = QToolButton()
        self.pause_btn.setIcon(icon)
        self.pause_btn.setIconSize(iconsize)
        self.pause_btn.setAutoRaise(True)
        self.pause_btn.setToolTip('Pause')
        self.pause_btn.setVisible(False)
        self.pause_btn.clicked.connect(self._onPause)

        # define slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._updateFromSliderValueChange)

        # define spin to show current frame
        self.sBox_current_frame_num = QSpinBox()
        self.sBox_current_frame_num.setMinimum(0)
        self.sBox_current_frame_num.setSingleStep(1)
        self.sBox_current_frame_num.valueChanged.connect(
            self._updateSliderFromSBox)

        # define the media-grid-layout which defined in map.ui
        self.gBox_bottom.addWidget(self.cycle_btn, 0, 0)
        self.gBox_bottom.addWidget(self.play_btn, 0, 1)
        self.gBox_bottom.addWidget(self.pause_btn, 0, 1)
        self.gBox_bottom.addWidget(self.slider, 0, 2)
        self.gBox_bottom.addWidget(self.sBox_current_frame_num, 0, 3)

        # set col stretch
        for i in range(4):
            self.gBox_bottom.setColumnMinimumWidth(i, 0)
            self.gBox_bottom.setColumnStretch(i, 1)

        self.gBox_bottom.setColumnStretch(2, 100)
        self.gBox_bottom.setColumnStretch(3, 1)

        # set table-view
        self.obj_model = QStandardItemModel(64, 4)
        self.obj_model.setHorizontalHeaderLabels(
            ['Range/m', 'Velocity(km/h)', 'Angel/deg', 'SNR/dB'])
        # self.obj_model.setHorizontalHeaderLabels(
        #     ['ID', 'Range/m', 'Velocity(m/s)', 'Angel(deg)'])
        self.tabView_track.setModel(self.obj_model)
        self.tabView_track.horizontalHeader().setStretchLastSection(True)
        self.tabView_track.verticalHeader().hide()

        # init radar-view
        self._initRadarView()

        self.cBox_mode.setCurrentIndex(0)

        self.cam = Camera(id_camera=0)

    def _initRadarView(self):
        self._setPen()
        self._renderRadarView()
        self._renderVehProfile()
        self._renderFOV()

    def _setPen(self):
        """
        set some pen to draw
        """
        self.background_Pen = QPen(Qt.white, 0.05, Qt.SolidLine, Qt.SquareCap,
                                   Qt.MiterJoin)
        self.fov_pen = QPen(Qt.white, 0.1, Qt.SolidLine, Qt.SquareCap,
                            Qt.MiterJoin)
        self.infLine_Pen = QPen(Qt.white, 0.05, Qt.SolidLine, Qt.SquareCap,
                                Qt.MiterJoin)
        self.pos_Pen = QPen(Qt.white, 0.05, Qt.SolidLine, Qt.SquareCap,
                            Qt.MiterJoin)
        self.vel_Pen = QPen(Qt.white, 0.05, Qt.SolidLine, Qt.RoundCap,
                            Qt.MiterJoin)
        self.warn_pen = QPen(Qt.yellow, 0.01, Qt.SolidLine, Qt.RoundCap,
                             Qt.MiterJoin)

    def _renderRadarView(self):
        left_axis = AxisItem(orientation='left')
        left_axis.setLabel(text='X', units='m')
        left_axis.enableAutoSIPrefix(False)
        self.radar_view_layout.ci.addItem(left_axis, 0, 0)

        # set vb
        self.vb = ViewBox(name='RadarView')
        self.radar_view_layout.ci.addItem(self.vb, 0, 1)

        # set bottom-axis
        bottom_axis = AxisItem(orientation='bottom')
        bottom_axis.setLabel(text='Y', units='m')
        bottom_axis.enableAutoSIPrefix(False)
        self.radar_view_layout.ci.addItem(bottom_axis, 1, 1)

        # set stretch
        layout = self.radar_view_layout.ci.layout
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        for i in range(2):
            layout.setRowPreferredHeight(i, 0)
            layout.setRowMinimumHeight(i, 0)
            layout.setRowSpacing(i, 10)
            layout.setRowStretchFactor(i, 1000)
        layout.setRowStretchFactor(1, 1)

        for i in range(2):
            layout.setColumnPreferredWidth(i, 0)
            layout.setColumnMinimumWidth(i, 0)
            layout.setColumnSpacing(i, 0)
            layout.setColumnStretchFactor(i, 1)
        layout.setColumnStretchFactor(1, 1000)

        # linx axis
        left_axis.linkToView(self.vb)
        bottom_axis.linkToView(self.vb)

        # invert left-axis
        self.vb.invertY()

        if self.cBox_view.currentIndex == 0:
            # set the default range
            self.vb.setXRange(-20, 20)
            self.vb.setYRange(0, -60)
        else:
            self.vb.setXRange(-20, 20)
            self.vb.setYRange(0, 100)

        # add grid
        grid = GridItem()
        self.vb.addItem(grid)

        # add inf-line
        h_line = InfiniteLine(pos=(0, 0), angle=0, pen=self.infLine_Pen)
        v_line = InfiniteLine(pos=(0, 0), angle=90, pen=self.infLine_Pen)
        self.vb.addItem(h_line)
        self.vb.addItem(v_line)

    def _renderVehProfile(self):
        DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        veh_static_path = os.path.join(DIR_PATH, "config",
                                       "default_veh_static.json")
        with open(veh_static_path, 'r') as f:
            data = json.load(f)

            veh_length = data["veh_length_m"]
            veh_width = data["veh_width_m"]
            veh_height = data["veh_height_m"]

            # add vehicle
            rect = QGraphicsRectItem(
                QRectF(-0.5 * veh_width, -veh_length, veh_width, veh_length))
            rect.setPen(self.background_Pen)
            self.vb.addItem(rect)

            pointF_list = []
            point1 = QPointF(QPoint(-0.5 * veh_width, 0))
            point2 = QPointF(QPoint(0.5 * veh_width, 0))
            point3 = QPointF(QPoint(0, veh_length))
            pointF_list.append(point1)
            pointF_list.append(point2)
            pointF_list.append(point3)
            pointF_list.append(point1)
            pointF = QPolygonF(pointF_list)
            triangle = QGraphicsPolygonItem(pointF)
            triangle.setPen(self.background_Pen)
            self.vb.addItem(triangle)

            # self.veh_director = ArrowItem(angle=90)
            # self.vb.addItem(self.veh_director)

    def _renderFOV(self):
        left_fov_line = InfiniteLine(pos=(0, 0),
                                     angle=-30,
                                     pen=self.infLine_Pen)
        right_fov_line = InfiniteLine(pos=(0, 0),
                                      angle=30,
                                      pen=self.infLine_Pen)
        self.vb.addItem(left_fov_line)
        self.vb.addItem(right_fov_line)

        # angle = np.radians(70)
        # line_len = 200
        # line_list=[]
        # # add rm-fov
        # end_point = (
        #     line_len * np.sin(angle),
        #     line_len * np.cos(angle))
        # print(end_point[0], end_point[1])
        # left_line  = QGraphicsLineItem(0, 0, end_point[0], -end_point[1])
        # right_line = QGraphicsLineItem(0, 0, -end_point[0], -end_point[1])

        # for line in line_list:
        #     line.setPen(self.fov_pen)
        #     self.vb.addItem(line)

    def updateData(self, count):
        """ when the timer is out, operate this funciton.
        """
        pass

    def _initVars(self):
        self.has_bsd_widget = False
        self.bsd_widget = BsdWidget()

        self.i_current_frame_num = 0

        self.ts_len = 50
        self.ts_period = 5

        # set the maximum number
        self.slider.setMaximum(self.ts_len)
        self.slider.setValue(0)

        self.sBox_current_frame_num.setMaximum(self.ts_len)

        self.all_items_need_to_remove = []

        # set the filter threshold value(m) of detection memory range
        self.filter_threshold_range = 0.001

        self.is_filter = True

    def _onPlay(self):
        # True means in play-status
        self.b_play = True
        self.b_pause = False

        # start push detection mem to queue
        startPushDetMem(True)
        self.five_detection_mem_data_pool = []

        self._updateBtns()
        self._play()

    def _onPause(self):
        # True means current is pause-status
        self.b_pause = True
        self.b_play = False
        self.b_cycle = False

        # stop push detection mem to queue
        startPushDetMem(False)

        self._updateBtns()
        self._updateSlider()

    def _onCycle(self):
        self.b_cycle = True
        self._onPlay()

    def _updateBtns(self):
        """
        switch the state in play, pause, cycle
        """
        if self.b_pause:  # pause-status
            # set play-btn
            self.play_btn.setVisible(True)
            self.play_btn.setEnabled(True)
            self.play_btn.setCheckable(True)
            # set pause-btn
            self.pause_btn.setVisible(False)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setCheckable(False)
            # set cycle-btn
            self.cycle_btn.setEnabled(True)
            self.cycle_btn.setCheckable(True)
            # set slider
            self.slider.setEnabled(True)
            # set sbox
            self.sBox_current_frame_num.setEnabled(True)
        else:  # play-status
            # set play-btn
            self.play_btn.setVisible(False)
            self.play_btn.setEnabled(False)
            self.play_btn.setCheckable(False)
            # set pause-btn
            self.pause_btn.setVisible(True)
            self.pause_btn.setEnabled(True)
            self.pause_btn.setCheckable(True)
            # set cycle-btn
            self.cycle_btn.setEnabled(False)
            self.cycle_btn.setCheckable(False)
            # set slider
            self.slider.setEnabled(False)
            # set sbox
            self.sBox_current_frame_num.setEnabled(False)

    def _updateSlider(self):
        """
        update the value of slider along with time
        """
        has_frame = self.i_current_frame_num >= 0
        if has_frame:
            self.slider.setValue(self.i_current_frame_num)
        else:
            self.slider.setMaximum(0)

    def _updateFromSliderValueChange(self, i_current_slider_num):
        # update current-frame-num
        self.i_current_frame_num = i_current_slider_num
        # update spin-box
        self.sBox_current_frame_num.setValue(i_current_slider_num)
        # update ui
        if self.cBox_mode.currentIndex() == 1:
            # inline mode
            self.readDetectionMemInfo()
        elif self.cBox_mode.currentIndex() == 0:
            # offline mode
            self.parseDetectionMemInfo()

    def _updateSliderFromSBox(self, i_current_sbox_num):
        self.slider.setValue(i_current_sbox_num)

    def _play(self):
        if self.b_play:
            if self.i_current_frame_num == self.ts_len:  # arrive to end
                if self.b_cycle:  # in cycle-status
                    self.i_current_frame_num = 0
                    self._play()
                else:  # in end-status
                    self._onPause()
            else:  # play-status
                self._updateSlider()
                self.timer = QTimer()
                # self.timer.setInterval(self.ts_period)
                self.timer.setSingleShot(True)
                self.timer.start(self.ts_period)
                self.timer.timeout.connect(self._updateFrameNum)

    def _updateFrameNum(self):
        if self.cBox_mode.currentIndex() == 1:
            # inline mode
            self.readDetectionMemInfo()
        elif self.cBox_mode.currentIndex() == 0:
            # offline mode
            self.parseDetectionMemInfo()
        self.i_current_frame_num += 1
        self._play()

    def _renderBsdZone(self):
        if self.cBox_FF.currentIndex() == 1:
            DIR_PATH = os.path.dirname(
                os.path.dirname(os.path.realpath(__file__)))
            bsd_zone_path = os.path.join(DIR_PATH, "config",
                                         "default_bsd_detect_zone.json")

            with open(bsd_zone_path, 'r') as f:
                data = json.load(f)

                start_point = data['left']['start_point']
                size = data['left']['size']

                self.left_bsd_zone = QGraphicsRectItem(
                    QRectF(start_point[0], start_point[1], size[0], size[1]))
                self.left_bsd_zone.setPen(self.warn_pen)
                self.vb.addItem(self.left_bsd_zone)

                start_point = data['right']['start_point']
                size = data['right']['size']
                self.right_bsd_zone = QGraphicsRectItem(
                    QRectF(start_point[0], start_point[1], size[0], size[1]))
                self.right_bsd_zone.setPen(self.warn_pen)
                self.vb.addItem(self.right_bsd_zone)

    def stopAllThreads(self):
        for th in self.all_thread_list:
            if th.is_alive():
                stopThread(th)

    def filterDetection(self, cur_data):
        self.one_detection_mem_data_pool=[]
        for itor in cur_data:
            rng, doppler_vel, angle, snr = itor
            if self.is_filter:
                # filter the detection mem with range-threshold and snr
                # if rng > self.filter_threshold_range:
                if rng > self.filter_threshold_range and snr > 0.999:
                    angle_rad = angle * np.pi / 180
                    rng_x = rng * np.cos(angle_rad)
                    rng_y = rng * np.sin(angle_rad)
                    vel_x = doppler_vel * np.cos(angle_rad)
                    vel_y = doppler_vel * np.sin(angle_rad)
                    detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                      doppler_vel, angle, snr)
                    self.one_detection_mem_data_pool.append(detection_data)
            else:
                angle_rad = angle * np.pi / 180
                rng_x = rng * np.cos(angle_rad)
                rng_y = rng * np.sin(angle_rad)
                vel_x = doppler_vel * np.cos(angle_rad)
                vel_y = doppler_vel * np.sin(angle_rad)
                detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                  doppler_vel, angle, snr)
                self.one_detection_mem_data_pool.append(detection_data)

        self._updateInLineData()
        self._updateTableDetMem()

    def parseDetectionMemInfo(self):
        if self.df_dection is not None:
            cur_dection_info = self.df_dection[self.df_dection.frame_id == (self.i_current_frame_num+1)]
            # print(cur_dection_info)
            splited_cur_detection_data = cur_dection_info.iloc[:, 5:].values
            self.filterDetection(splited_cur_detection_data)   

    def readDetectionMemInfo(self):
        """
        read the data in inline mode.
        """
        if detection_mem_queue.qsize() > 0:
            cur_detection_mem_info = detection_mem_queue.get()
            frame_id = cur_detection_mem_info[0]
            # self.sBox_current_frame_num.setValue(frame_id)
            cur_frame_data = cur_detection_mem_info[1:]

            rearranged_cur_frame_data = []
            for index, item in enumerate(cur_frame_data):
                if index%2==0:
                    rearranged_cur_frame_data.append([item[0], item[1]])
                else:
                    rearranged_cur_frame_data[-1].append(item[0])
                    rearranged_cur_frame_data[-1].append(item[1])
            
            if len(rearranged_cur_frame_data) != 64:
                raise ValueError(
                    "Detection-Mem-Data-length !=64 in function readDetectionMemInfo!"
                )

            self.filterDetection(rearranged_cur_frame_data)
            """
            self.one_detection_mem_data_pool=[]
            for itor in rearranged_cur_frame_data:
                rng, doppler_vel, angle, snr = itor
                if self.is_filter:
                    # filter the detection mem with range-threshold and snr
                    # if rng > self.filter_threshold_range:
                    if rng > self.filter_threshold_range and snr > 0.999:
                        angle_rad = angle * np.pi / 180
                        rng_x = rng * np.cos(angle_rad)
                        rng_y = rng * np.sin(angle_rad)
                        vel_x = doppler_vel * np.cos(angle_rad)
                        vel_y = doppler_vel * np.sin(angle_rad)
                        detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                          doppler_vel, angle, snr)
                        self.one_detection_mem_data_pool.append(detection_data)
                else:
                    angle_rad = angle * np.pi / 180
                    rng_x = rng * np.cos(angle_rad)
                    rng_y = rng * np.sin(angle_rad)
                    vel_x = doppler_vel * np.cos(angle_rad)
                    vel_y = doppler_vel * np.sin(angle_rad)
                    detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                      doppler_vel, angle, snr)
                    self.one_detection_mem_data_pool.append(detection_data)

            self._updateInLineData()
            self._updateTableDetMem()
            """

            """
            if frame_id % 5 == 0:
                self._updateInLineData()
                self._updateTableDetMem()
                self.five_detection_mem_data_pool = []
            for itor in rearranged_cur_frame_data:
                rng, doppler_vel, angle, snr = itor
                if self.is_filter:
                    # filter the detection mem with range-threshold and snr
                    # if rng > self.filter_threshold_range:
                    if rng > self.filter_threshold_range and snr > 0.999:
                        angle_rad = angle * np.pi / 180
                        rng_x = rng * np.cos(angle_rad)
                        rng_y = rng * np.sin(angle_rad)
                        vel_x = doppler_vel * np.cos(angle_rad)
                        vel_y = doppler_vel * np.sin(angle_rad)
                        detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                          doppler_vel, angle, snr)
                        self.five_detection_mem_data_pool.append(detection_data)  
                else:
                    angle_rad = angle * np.pi / 180
                    rng_x = rng * np.cos(angle_rad)
                    rng_y = rng * np.sin(angle_rad)
                    vel_x = doppler_vel * np.cos(angle_rad)
                    vel_y = doppler_vel * np.sin(angle_rad)
                    detection_data = (rng_x, rng_y, vel_x, vel_y, rng,
                                      doppler_vel, angle, snr)
                    self.five_detection_mem_data_pool.append(detection_data)  
            """
    def _updateInLineData(self):
        if len(self.one_detection_mem_data_pool)!=0:
            """
            if self.cBox_mode.currentIndex() == 1:
                #inline-mode
            """
            # clear the previous data-item
            for item in self.all_items_need_to_remove:
                self.vb.removeItem(item)
            # for item in self.vb.addedItems:
            #     if isinstance(item, pg.PlotDataItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.PlotCurveItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.CurvePoint):
            #         self.vb.removeItem(item)
            self.all_items_need_to_remove = []

            # plot Position
            current_posX = [
                detection[0] for detection in self.one_detection_mem_data_pool
            ]
            current_posY = [
                detection[1] for detection in self.one_detection_mem_data_pool
            ]
            current_pen = self.pos_Pen
            color = (255, 0, 0)
            pos_curve = ScatterPlotItem(x=current_posY,
                                        y=current_posX,
                                        pen=current_pen,
                                        symbolBrush=color,
                                        symbolPen='w',
                                        symbol='o',
                                        symbolSize=10)
            # set ZValue will show in the front of scene
            pos_curve.setZValue(100)
            self.vb.addItem(pos_curve, ignoreBounds=False)
            self.all_items_need_to_remove.append(pos_curve)

            # add vel
            for cur_row in self.one_detection_mem_data_pool:
                current_velX = cur_row[2]
                current_velY = cur_row[3]
                complex_vel = complex(current_velX, current_velY)
                vel = np.abs(complex_vel)
                angle_radian = np.angle(complex_vel)
                angle = np.angle(complex_vel, deg=True)
                # define a scale-factor to scale the vel
                scale_factor = 10
                vel_after_scale = vel / scale_factor
                current_velX_after_scale = vel_after_scale * np.cos(angle_radian)
                current_velY_after_scale = vel_after_scale * np.sin(angle_radian)
                current_velX_list = [current_posX[1], current_posX[1] + current_velX_after_scale]
                current_velY_list = [current_posY[1], current_posY[1] + current_velY_after_scale]
                vel_line = PlotCurveItem(x=current_velY_list,
                                            y=current_velX_list,
                                            pen=self.vel_Pen,
                                            antialias=True)
                self.vb.addItem(vel_line, ignoreBounds=False)
                self.all_items_need_to_remove.append(vel_line)

            """
            # add info-text
            info_curve_point = pg.CurvePoint(pos_curve, index=1)
            self.vb.addItem(info_curve_point, ignoreBounds=False)
            self.all_items_need_to_remove.append(info_curve_point)
            anchor_ = (-0.2, 0) if radar_loc == 'RM' else (0.8, 0)
            info_text = pg.TextItem(f"{radar_loc}\nTracker_ID:{tracker_id}\nVel:{vel:.2f}\nAngle:{angle:.2f}",
                                    anchor=anchor_)
            info_text.setParentItem(info_curve_point)
            """

    def _updateTableDetMem(self):
        """
        update the detection-mem-data in table
        """
        num_det_mem_rows = len(self.one_detection_mem_data_pool)
        if num_det_mem_rows !=0:
            """
            if self.cBox_mode.currentIndex() == 1:
                # inline mode
            """
            for row in range(64):
                if row < num_det_mem_rows:
                    cur_det_data = self.one_detection_mem_data_pool[row][4:]
                else:
                    cur_det_data = (0.0, 0.0, 0.0, 0.0)
                for column in range(4):
                    item = QStandardItem(f'{cur_det_data[column]}')
                    self.obj_model.setItem(row, column, item)