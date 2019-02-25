from mu500_7seg import Qt7Seg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Mu5007Seg()
    sys.exit(app.exec_())
