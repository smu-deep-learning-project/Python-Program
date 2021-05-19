from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import detector


class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.qtxt1 = QTextEdit(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.qtxt1)
        self.setLayout(vbox)

        self.setGeometry(500, 500, 300, 300)

class Test:
    def __init__(self):
        name = ""

# 쓰레드
class Worker(QThread):
    sec_changed = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    def run(self):
        print("hello")

        md = detector.MyDetector().start()
        md.video(self.state, self.sec_changed)


    @pyqtSlot("PyQt_PyObject")
    def recive_instance_singal(self, inst):
        print(inst.name)


class MyMain(MyMainGUI):
    add_sec_signal = pyqtSignal()
    send_instance_singal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.th = Worker(parent=self)

        self.send_instance_singal.connect(self.th.recive_instance_singal)
        self.show()
        self.th.start()

    @pyqtSlot()
    def time_start(self):
        self.th.start()
        self.th.working = True

    @pyqtSlot()
    def add_sec(self):
        print(".... add singal emit....")
        self.add_sec_signal.emit()

    @pyqtSlot(str)
    def time_update(self, msg):
        self.qtxt1.append(msg)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()