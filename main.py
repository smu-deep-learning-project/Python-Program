from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import detector


class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        data1 = 13
        data2 = 2.3

        self.lbl_box2 = QLabel('분당 깜빡임 : %d회' % data1)
        self.lbl_box3 = QLabel('속도 : %.1f' % data2)
        self.lbl_box1 = QLabel('')
        self.lbl_box2.setStyleSheet(
            "color: black;" "border-style: dashed;" "border-width: 2px;" "border-color: #6799FF;" "border-radius: 3px")
        self.lbl_box3.setStyleSheet(
            "color: black;" "border-style: dashed;" "border-width: 2px;" "border-color: #6799FF;" "border-radius: 3px")
        self.lbl_box1.setStyleSheet(
            "color: blue;" "background-color: #87CEFA;" "border-style: soild;" "border-width: 3px;" "border-color: #1E90FF")

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_box1)
        vbox.addWidget(self.lbl_box2)
        vbox.addWidget(self.lbl_box3)
        self.setLayout(vbox)
        self.setWindowTitle('Information')

        self.setGeometry(500, 500, 300, 300)

class Test:
    def __init__(self):
        name = ""

# Thread
class Worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    # Thread start
    def run(self):
        md = detector.MyDetector()
        md.webcam(1, self.signal)



class MyMain(MyMainGUI):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.th = Worker(parent=self)

        # Thread signal connect
        self.th.signal.connect(self.state_update)
        self.show()
        self.th.start()

    # Thread event
    @pyqtSlot(str)
    def state_update(self, msg):
        perMinute = int(msg)
        print("webcaom window push 1 button")

        self.lbl_box2.setText('분당 깜빡임 : ' + str(perMinute))

        if perMinute < 2:
            self.lbl_box1.setText('눈을 깜빡여 주세요!!')
        else:
            self.lbl_box1.setText('')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()