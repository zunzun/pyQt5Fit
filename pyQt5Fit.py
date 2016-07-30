import os, sys
from PyQt5.QtWidgets import *

import FittingInterface

qApp = QApplication(sys.argv)

aw = FittingInterface.InterfaceWindow()
aw.show()
sys.exit(qApp.exec_())
