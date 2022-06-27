"""
Little widget to be add in the timer window.
This window will manage the action buttons widget
"""

from PyQt5 import QtWidgets, QtCore, QtGui


class ActionWidget(QtWidgets.QWidget):

    # Signals
    add_signal = QtCore.pyqtSignal()
    remove_signal = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ActionWidget, self).__init__(*args, **kwargs)

        # UI
        layout = QtWidgets.QVBoxLayout()

        add_timer_bt = QtWidgets.QPushButton("+")
        add_timer_bt.setToolTip("Add timer")
        add_timer_bt.setMaximumSize(QtCore.QSize(30, 30))

        remove_timer_bt = QtWidgets.QPushButton("-")
        remove_timer_bt.setToolTip("Remove timer.\nClick on this button then on the timer that you want to remove")
        remove_timer_bt.setMaximumSize(QtCore.QSize(30, 30))

        add_timer_bt.clicked.connect(self.add)
        remove_timer_bt.clicked.connect(self.remove)

        layout.addWidget(add_timer_bt)
        layout.addWidget(remove_timer_bt)
        self.setLayout(layout)

    def add(self):
        self.add_signal.emit()

    def remove(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_signal.emit()
