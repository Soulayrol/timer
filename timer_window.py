import os.path
import uuid
import json
from os.path import dirname, join, abspath
from PyQt5 import QtCore, QtWidgets, QtGui

from timer_wiget import TimerWidget
from action_widget import ActionWidget

json_path = join(dirname(abspath(__file__)), "timers_data.json")


class TimerWindow(QtWidgets.QWidget):
    """
    The timer window is call be the application and manege the widget.
    """
    ICON_WIDTH = 50

    def __init__(self, icon_path, *args, **kwargs):
        super(TimerWindow, self).__init__(*args, **kwargs)
        #                            Always on top           Remove taskbar          Make frameless
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Transparent background
        self.icon_path = icon_path
        self.timer_widgets = QtWidgets.QWidget()
        self.timers = dict()
        self.action_widget = ActionWidget()
        self.timer_widget_is_visible = False
        self.old_position = None
        self.is_delete_mode = False
        self.setup_ui()
        self.load_timers_data()

    def setup_ui(self):
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        icon_widget = QtWidgets.QLabel()
        icon_pixmap = QtGui.QPixmap(self.icon_path)
        icon_pixmap = icon_pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
        icon_widget.setPixmap(icon_pixmap)
        icon_widget.setObjectName("IconWidget")

        self.action_widget.add_signal.connect(self.add_timer)
        self.action_widget.remove_signal.connect(self.remove_timer)

        main_layout.addWidget(icon_widget)
        main_layout.addWidget(self.action_widget)
        main_layout.addWidget(self.timer_widgets)

        timer_layout = QtWidgets.QHBoxLayout()
        timer_layout.setContentsMargins(0, 0, 0, 0)
        self.timer_widgets.setLayout(timer_layout)

        self.setLayout(main_layout)
        self.resize(self.ICON_WIDTH, self.ICON_WIDTH)  # Resize
        # Update visibility
        self.timer_widgets.setVisible(self.timer_widget_is_visible)
        self.action_widget.setVisible(self.timer_widget_is_visible)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

    def mouseDoubleClickEvent(self, event):  # Can be replace by mouseReleaseEvent for 1 click only
        widget = self.childAt(event.pos())
        if widget is not None and widget.objectName() == "IconWidget":
            self.toggle_timer_widget()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.old_position = event.globalPos()
        if self.is_delete_mode:
            widget_at = QtWidgets.QApplication.widgetAt(event.globalPos())
            if hasattr(widget_at, "parent") and type(widget_at.parent()) == TimerWidget:
                widget_at.parent().deleteLater()
                # Resize the window after 100s to be sure the time is correctly deleted
                QtCore.QTimer.singleShot(100, lambda: self.setFixedSize(self.layout().sizeHint()))
            self.is_delete_mode = False
            QtWidgets.QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        delta = QtCore.QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()

    def toggle_timer_widget(self):
        """
        Toggle the timer widget visibility
        """
        previous_height = self.height()
        self.timer_widget_is_visible = not self.timer_widget_is_visible
        self.timer_widgets.setVisible(self.timer_widget_is_visible)
        self.action_widget.setVisible(self.timer_widget_is_visible)
        self.setFixedSize(self.layout().sizeHint())
        self.move(self.x(), self.y() - int((self.height() - previous_height) / 2))  # Move the height to avoid bump

    def add_timer(self):
        """
        Add a timer, ask the title if needed
        """
        title, ok = QtWidgets.QInputDialog.getText(self, "Timer name ?", "Choose a timer name.\n"
                                                                         "Let it empty if you don't want one.")
        if not ok:
            return
        timer_widget = TimerWidget(title=title or None)
        timer_widget.setStyleSheet("QWidget { padding: 5px; border-radius: 5px; background: white; }")
        self.timer_widgets.layout().addWidget(timer_widget)
        # Resize the window after 100s to be sure the widget is correctly created
        QtCore.QTimer.singleShot(100, lambda: self.setFixedSize(self.layout().sizeHint()))
        self.timers[uuid.uuid4().hex] = timer_widget

    def remove_timer(self):
        """
        Change the mode to be delete mode.
        Look at the mousePressEvent if this mode is enable for the widget remove
        """
        self.is_delete_mode = True

    def save_timers_data(self):
        """
        Save the timers data into a json file
        """
        time_data = dict()
        for uuid_hex, widget in self.timers.items():
            time_data[uuid_hex] = {
                "time":  widget.get_time(),
                "title": widget.title
            }
        time_data["window_position"] = {"x": self.pos().x(), "y": self.pos().y()}
        with open(json_path, "w+") as json_file:
            json_file.write(json.dumps(time_data))

        print("Timers saved")

    def load_timers_data(self):
        """
        Load timers data
        """
        timers_data = dict()
        if not os.path.exists(json_path):
            return
        # Read file
        with open(json_path, "r") as json_file:
            timers_data = json.load(json_file)
        # Re-create the widgets
        for uuid_hex, timer_data in timers_data.items():
            if uuid_hex == "window_position":
                self.move(timer_data["x"], timer_data["y"])
                continue
            timer_widget = TimerWidget(title=timer_data["title"] or None, start_at=timer_data["time"])
            timer_widget.setStyleSheet("QWidget { padding: 5px; border-radius: 5px; background: white; }")
            self.timer_widgets.layout().addWidget(timer_widget)
            # Resize the window after 100s to be sure the widget is correctly created
            QtCore.QTimer.singleShot(100, lambda: self.setFixedSize(self.layout().sizeHint()))
            self.timers[uuid_hex] = timer_widget
        QtCore.QTimer.singleShot(100, lambda: self.setFixedSize(self.layout().sizeHint()))


if __name__ == '__main__':
    import sys
    from os.path import dirname, join, abspath
    app = QtWidgets.QApplication(sys.argv)
    timer_win = TimerWindow(join(dirname(abspath(__file__)), "src", "clock.png"))
    timer_win.show()
    sys.exit(app.exec_())
