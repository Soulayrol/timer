from PyQt5 import QtCore, QtWidgets


class TimerWidget(QtWidgets.QWidget):
    """
    TimerWidget to manage a timer with a button to start/stop it.
    """

    def __init__(self, title=None, display_button=True, start_at=(0, 0, 0), is_started=False, time_format="hh:mm:ss",
                 *args, **kwargs):
        """
        Create the Timer widget
        :param str title: Title of the timer (if None, the title will not be display)
        :param bool display_button: True to display the button
        :param tuple(int, int, int) start_at: int h = 0, int m = 0, int s = 0
        :param bool is_started: If True, the timer will start directly after the UI creation
        :param str time_format: Qt format display (see QTime.toString)
        :param list args: Qt args for QWidget
        :param dict kwargs: Qt kwargs for QWidget
        """
        super(TimerWidget, self).__init__(*args, **kwargs)
        self.time_format = time_format
        self.is_started = is_started
        self.title = title

        self.timer = QtCore.QTimer()  # Create a QTimer to manage the time
        self.time = QtCore.QTime(*start_at)  # Create a time value starting at the start_at argument
        self.timer.timeout.connect(self.update_time)

        # UI
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Update the label with the start_at time
        time_display = self.time.toString(self.time_format)
        self.label.setText(time_display)

        # Custom UI
        if display_button:
            self.toggle_button = QtWidgets.QPushButton("Stop" if is_started else "Start")
            self.toggle_button.clicked.connect(self.toggle_timer)
        if title:
            self.title_label = ClickableLabel(title)
            self.title_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.title_label.setAlignment(QtCore.Qt.AlignCenter)
            self.title_label.clicked.connect(self.rename_title)
            layout.addWidget(self.title_label)
        if is_started:
            self.timer.start(1000)  # Start the timer every 1s

        layout.addWidget(self.label)
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)

    def update_time(self):
        """
        Update the time value and update the display
        """
        self.time = self.time.addSecs(1)
        time_display = self.time.toString(self.time_format)
        self.label.setText(time_display)

    def toggle_timer(self):
        """
        Toggle the timer status (Start or Stop the timer depending on the previous status)
        """
        if self.is_started:
            self.timer.stop()
            if hasattr(self, "toggle_button"):
                self.toggle_button.setText("Start")
        else:
            self.timer.start(1000)  # Start the timer every 1s
            if hasattr(self, "toggle_button"):
                self.toggle_button.setText("Stop")
        self.is_started = not self.is_started

    def rename_title(self):
        title, ok = QtWidgets.QInputDialog().getText(self, "Timer name ?", "Choose a new timer name",
                                                     QtWidgets.QLineEdit.Normal, self.title)
        if not ok:
            return
        self.title_label.setText(title)
        self.title = title

    def get_time(self):
        """
        Get the time of the timer
        :return: int h = 0, int m = 0, int s = 0
        :rtype: tuple(int, int, int)
        """
        return self.time.hour(), self.time.minute(), self.time.second()


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.clicked.emit()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    timer_widget = TimerWidget(title="My Awesome Stopwatch", is_started=True)
    timer_widget.show()
    sys.exit(app.exec_())
