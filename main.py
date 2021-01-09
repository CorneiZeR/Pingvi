import start
from PyQt5 import QtWidgets
import db
import sys
from os import system

db.check_first_run()

class Start(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = start.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.save.clicked.connect(self.save)
        self.ui.start.clicked.connect(self.start)

        self.update()

    def update(self):
        temp = db.get_settings()[1:]
        self.ui.count_days.setText(str(temp[0]))
        self.ui.caption.setText(temp[1])
        self.ui.time.setText(temp[2])
        self.ui.time_start.setText(str(temp[3]))

    def save(self):
        db.edit_settings(self.ui.count_days.text(), self.ui.caption.text(), self.ui.time.text(), self.ui.time_start.text())

    def start(self):
        system('bot.exe')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = Start()
    my_app.show()
    sys.exit(app.exec_())

