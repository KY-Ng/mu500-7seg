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

class Qt7Seg(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = []
        self.pixmaps = []
        self.createWidgets()
        self.createLayouts()
        
    IS_VERTICAL_ELEMENT=[False, True, True, False, True, True, False, True]
    def createWidgets(self):
        for i in range(8):
            self.labels.append(QLabel())
            if Qt7Seg.IS_VERTICAL_ELEMENT[i]:
                self.pixmaps.append(QPixmap(10, 40))
            else:
                self.pixmaps.append(QPixmap(40, 10))
            self.off(i)

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

    def setValue(self, value):
        for i in range(7):
            if value & 0x1 == 1:
                self.on(i)
            else:
                self.off(i)
            value = value >> 1

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
        self.init_button(boxLay)

        self.setWindowTitle('MU500 7Seg')
        self.show()

    def init_7seg(self, layout):
        self.w7segs = []
        for i in range(4):
            hboxlay = QHBoxLayout()
            layout.addLayout(hboxlay)
            for j in range(16):
                w7seg = Qt7Seg()
                hboxlay.addWidget(w7seg)
                self.w7segs.append(w7seg)

    def init_leds(self, layout):
        self.leds = []
        for j in range(4):
            hboxlay = QHBoxLayout()
            layout.addLayout(hboxlay)
            for i in range(2):
                ls = []
                for i in range(8):
                    led = QtLED()
                    hboxlay.addWidget(led)
                    ls.append(led)
                self.leds.extend(ls[::-1])

    def init_button(self, layout):
        self.buttons = []
        for j in range(4):
            hboxylay = QHBoxLayout()
            layout.addLayout(hboxylay)
            for i in range(4):
                b = QPushButton("○", self)
                self.buttons.append(b)
                hboxylay.addWidget(b)
                b.pressed.connect(self.pressed_button)
                b.released.connect(self.released_button)

    def init_socket(self):
        # for receive
        self.port = 65007
        self.send_port = 65008
        self.sock = QUdpSocket()
        self.sock.bind(self.port)
        self.sock.readyRead.connect(self.recv)

    def sendi(self, offset, byte):
        self.send(format(offset, "02x"), format(byte, "02x"))

    def send(self, offset, byte):
        str = offset + byte + ";"
        self.sock.writeDatagram(str.encode('utf-8'), QHostAddress.LocalHost, self.send_port)
        print("sent: " + str)

    def pressed_button(self):
        i = self.buttons.index(self.sender())
        offset = int(i / 8) + 0x48
        value = 1 << (i % 8)
        self.sendi(offset, value)

    def released_button(self):
        i = self.buttons.index(self.sender())
        offset = int(i / 8) + 0x48
        self.sendi(offset, 0) #XXX multiple button

    def decode(self, offset, value):
        if 0 <= offset and offset < 0x40:
            self.w7segs[offset].setValue(value)
        elif 0x40 <= offset and offset <= 0x47:
            led_num = offset - 0x40 
            for i in range(8):
                if value & 0x01 == 0:
                    self.leds[led_num*8 + i].off()
                else:
                    self.leds[led_num*8 + i].on()
                value = value >> 1

    def recv(self):
        try:
            (data, addr, port) = self.sock.readDatagram(4)
            print(data)

            string = data.decode('utf-8')
            
            offset = int(string[0:2], 16)
            data = int(string[2:4], 16)
            print("recvd: %d %d" % (offset, data))
            self.decode(offset, data)
        except:
            print('error')
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Mu5007Seg()
    sys.exit(app.exec_())
