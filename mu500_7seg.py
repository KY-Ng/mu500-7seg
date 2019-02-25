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
        self.labels = []
        self.pixmaps = []
        self.createWidgets()
        self.createLayouts()

    IS_VERTICAL_ELEMENT=[False, True, True, False, True, True, False]
    def createWidgets(self):
        for i in range(7):
            self.labels[i] = QLabel()
            if Qt7Seg.IS_VERTICAL_ELEMENT[i]:
                self.pixmaps[i] = QPixmap(10, 20)
            else:
                self.pixmaps[i] = QPixmap(20, 10)

    def createLayouts(self):
        vertical = QVBoxLayout()
        self.setLayout(vertical)

        vertical.addWidget(self.labels[0])

        h1 = QHBoxLayout()
        vertical.addLayout(h1)
        h1.addWidget(self.labels[5])
        h1.addWidget(self.labels[1])

        vertical.addWidget(self.labels[7])

        h2 = QHBoxLayout()
        vertical.addLayout(h2)
        h2.addWidget(self.labels[4])
        h2.addWidget(self.labels[2])

        vertical.addLayout(self.labels[3])

    def setFillColor(self, i, color):
        self.pixmaps[i].fill(color)
        self.labels[i].setPixmap(self.pixs[i])

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
