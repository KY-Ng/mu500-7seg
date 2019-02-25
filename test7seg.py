from mu500_7seg import Qt7Seg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QHBoxLayout()
    a1 = Qt7Seg()
    layout.addWidget(a1)
    layout.addWidget(Qt7Seg())
    layout.addWidget(Qt7Seg())
    layout.addWidget(Qt7Seg())
    layout.addWidget(Qt7Seg())
    win.setLayout(layout)
    win.show()
    a1.off(1)
    sys.exit(app.exec_())
