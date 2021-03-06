#
# This file is part of the PyRDP project.
# Copyright (C) 2018 GoSecure Inc.
# Licensed under the GPLv3 or later.
#

import logging

from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QShortcut, QTabWidget, QWidget

from pyrdp.logging import LOGGER_NAMES


class BaseWindow(QTabWidget):
    """
    Class that encapsulates the common logic to manage a QtTabWidget to display RDP connections,
    regardless of their origin (network or file).
    """

    def __init__(self, parent: QWidget = None, maxTabCount = 250):
        super().__init__(parent)
        self.closeTabShortcut = QShortcut(QKeySequence("Ctrl+W"), self, self.closeCurrentTab)
        self.maxTabCount = maxTabCount
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.onTabClosed)
        self.log = logging.getLogger(LOGGER_NAMES.PLAYER)

    def closeCurrentTab(self):
        if self.count() > 0:
            self.onTabClosed(self.currentIndex())

    def onTabClosed(self, index):
        """
        Gracefully closes the tab by calling the onClose method
        :param index: Index of the closed tab
        """
        tab = self.widget(index)
        tab.onClose()
        self.removeTab(index)
