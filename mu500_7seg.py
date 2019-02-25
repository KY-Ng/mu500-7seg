import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

class QtLED(QLabel):
    def __init__(self):
        super().__init__("  ")
        self.pix = QPixmap(20, 10)
        self.off()

    def setFillColor(self, color):
        self.pix.fill(color)
        self.setPixmap(self.pix)

    def on(self):
        self.setFillColor(Qt.yellow)

    def off(self):
        self.setFillColor(Qt.black)

# https://github.com/aboutNisblee/SevenSegmentDisplay/blob/master/src/gui/displaynode_p.hpp#L362
class Qt7Seg(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = []
        self.pixmaps = []
        self.createWidgets()
        self.createLayouts()
        self.show()

    IS_VERTICAL_ELEMENT=[False, True, True, False, True, True, False]
    def createWidgets(self):
        for i in range(7):
            self.labels.append(QLabel())
            if Qt7Seg.IS_VERTICAL_ELEMENT[i]:
                self.pixmaps.append(QPixmap(10, 40))
            else:
                self.pixmaps.append(QPixmap(40, 10))
            self.on(i)

    def createLayouts(self):
        layouts = [
            (0, 1), #0
            (1, 2), #1
            (3, 2), #2
            (4, 1), #3
            (3, 0), #4
            (1, 0), #5
            (2, 1), #6
        ]

        grid = QGridLayout()
        for i, t in enumerate(layouts):
            grid.addWidget(self.labels[i], t[0], t[1])
        grid.setHorizontalSpacing(0)
        self.setLayout(grid)

    def setFillColor(self, i, color):
        self.pixmaps[i].fill(color)
        self.labels[i].setPixmap(self.pixmaps[i])

    def on(self, i):
        self.setFillColor(i, Qt.yellow)

    def off(self, i):
        self.setFillColor(i, Qt.black)

class Mu5007Seg(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_socket()

    def init_ui(self):
        boxLay = QVBoxLayout()
        self.setLayout(boxLay)

        self.init_leds(boxLay)
        self.init_7seg(boxLay)

        Stool = QSlider(Qt.Horizontal, self)
        boxLay.addWidget(Stool)
        Stool.valueChanged.connect(self.w7segs[0].display)

        self.setGeometry(500, 500, 300, 500)
        self.setWindowTitle('EventTest')
        self.show()

    def init_7seg(self, layout):
        self.w7segs = []
        for i in range(4):
            hboxlay = QHBoxLayout()
            layout.addLayout(hboxlay)
            for j in range(4):
                w7seg = QLCDNumber(self)
                w7seg.setHexMode()
                w7seg.display("0000")
                hboxlay.addWidget(w7seg)
                self.w7segs.append(w7seg)

    def init_leds(self, layout):
        self.leds = []
        for j in range(4):
            hboxlay = QHBoxLayout()
            layout.addLayout(hboxlay)
            for i in range(16):
                led = QtLED()
                hboxlay.addWidget(led)
                self.leds.append(led)

    def init_socket(self):
        self.port = 65007
        self.sock = QUdpSocket()
        self.sock.bind(self.port)
        self.sock.readyRead.connect(self.recv)

    def decode_7seg(self, value):
        pass

    def decode(self, offset, value):
        if offset == 0:
            self.w7segs[0].display(str(value))
        elif offset >= 0x10:
            led_num = offset - 0x10
            for i in range(8):
                if (value >> i) & 0x01 == 0:
                    self.leds[led_num*4 + i].off()
                else:
                    self.leds[led_num*4 + i].on()

    def recv(self):
        (data, addr, port) = self.sock.readDatagram(4)

        string = data.decode('utf-8')
        
        offset = int(string[0:2], 16)
        data = int(string[2], 16)
        print("recvd: %d %s" % (offset, data))
        self.decode(offset, data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Mu5007Seg()
    sys.exit(app.exec_())
