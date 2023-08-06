# -*- coding: utf-8 -*-

"""
define the tail feature widget
"""

from ..ui.tail_ff_ui import Ui_tail_status

from PyQt5.QtWidgets import QWidget

class TailWidget(Ui_tail_status, QWidget):
    def __init__(self, parent=None):
        super(TailWidget, self).__init__(parent)

        self.setupUi(self)