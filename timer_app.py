import sys
from os.path import dirname, join, abspath

from PyQt5 import QtGui, QtWidgets, QtCore

from timer_window import TimerWindow

icon_path = join(dirname(abspath(__file__)), "src", "clock.png")


class TimerApplication(QtWidgets.QApplication):
    
    def __init__(self, *args, **kwargs):
        super(TimerApplication, self).__init__(*args, **kwargs)
        # Create the tray icon
        self.w = QtWidgets.QWidget()
        self.tray_icon = SystemTrayIcon(QtGui.QIcon(icon_path), self, self.w)
        self.tray_icon.show()
        # Display the window
        self.timer_win = TimerWindow(icon_path)
        self.timer_win.show()

    def exit(self, *args):
        self.timer_win.save_timers_data()
        super(TimerApplication, self).exit(*args)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, application, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exit_action = menu.addAction("Exit")
        self.setContextMenu(menu)
        exit_action.triggered.connect(lambda: application.exit())


if __name__ == '__main__':
    app = TimerApplication(sys.argv)
    sys.exit(app.exec_())
