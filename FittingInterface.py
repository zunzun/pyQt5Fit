import os, sys, pickle
import pyeq3

from PyQt5.QtWidgets import *


# local imports
import DataForControls as dfc



class InterfaceWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        
        grid = QGridLayout()
        self.setLayout(grid)
 
         # ROW 0 - empty labels as visual buffers
        row, col = (0, 0) # left edge
        l = QLabel("   ")
        grid.addWidget(l, row, col)
        row, col = (0, 2) # center
        l = QLabel("     ")
        grid.addWidget(l, row, col)
        row, col = (0, 4) # right edge
        l = QLabel("   ")
        grid.addWidget(l, row, col)

        # ROW 1 - text data entry labels
        # no "self" needed as no later references exist
        row, col = (1, 1)
        l = QLabel("<b>--- 2D Data Text Editor ---</b>") # bold tags
        grid.addWidget(l, row, col)
        
        row, col = (1, 3)
        l = l = QLabel("<b>--- 3D Data Text Editor ---</b>") # bold tags
        grid.addWidget(l, row, col)

        # ROW 2 - text data input, no line wrap
        row, col = (2, 1)
        self.text_2D = QPlainTextEdit(dfc.exampleText_2D) # plain text
        grid.addWidget(self.text_2D, row, col)

        row, col = (2, 3)
        self.text_3D = QPlainTextEdit(dfc.exampleText_3D) # plain text
        grid.addWidget(self.text_3D, row, col)

        # ROW 3 - empty label as visual buffer
        row, col = (3, 0)
        l = QLabel("   ")
        grid.addWidget(l, row, col)

        # ROW 4 - equation selection labels
        # no "self" needed as no later references exist
        row, col = (4, 1)
        l = QLabel("<b>--- Example 2D Equations ---</b>") # bold tags
        grid.addWidget(l, row, col)
        
        row, col = (4, 3)
        l = QLabel("<b>--- Example 3D Equations ---</b>") # bold tags
        grid.addWidget(l, row, col)

        # ROW 5 - equation selection radio buttons
        row, col = (5, 1)
        self.eqSelectButtonGroup_2D = QButtonGroup()
        w = QWidget()
        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        w.setLayout(vBox)
        grid.addWidget(w, row, col)

        index=0
        for exampleEquationText in dfc.exampleEquationList_2D:
            rb = QRadioButton(exampleEquationText)
            rb.toggled.connect(lambda:self.onEquationSelect_2D())
            if index == 0:
                rb.setChecked(True)
            vBox.addWidget(rb)
            self.eqSelectButtonGroup_2D.addButton(rb, index)
            index += 1
            
        row, col = (5, 3)
        self.eqSelectButtonGroup_3D = QButtonGroup()
        w = QWidget()
        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        w.setLayout(vBox)
        grid.addWidget(w, row, col)

        index=0
        for exampleEquationText in dfc.exampleEquationList_3D:
            rb = QRadioButton(exampleEquationText)
            rb.toggled.connect(lambda:self.onEquationSelect_3D())
            if index == 0:
                rb.setChecked(True)
            vBox.addWidget(rb)
            self.eqSelectButtonGroup_3D.addButton(rb, index)
            index += 1

        # ROW 6 - empty label as visual buffer
        row, col = (6, 0)
        l = QLabel("   ")
        grid.addWidget(l, row, col)

        # ROW 7 - fitting target selection labels
        # no "self" needed as no later references exist
        row, col = (7, 1)
        l = QLabel("<b>--- Fitting Target 2D ---</b>") # bold tags
        grid.addWidget(l, row, col)
        
        row, col = (7, 3)
        l = QLabel("<b>--- Fitting Target 3D ---</b>") # bold tags
        grid.addWidget(l, row, col)

        # ROW 8 - fitting target selection radio buttons
        row, col = (8, 1)
        self.targetSelectButtonGroup_2D = QButtonGroup()
        w = QWidget()
        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        w.setLayout(vBox)
        grid.addWidget(w, row, col)

        index=0
        for exampleEquationText in dfc.fittingTargetList:
            rb = QRadioButton(exampleEquationText)
            rb.toggled.connect(lambda:self.onTargetSelect_2D())
            if index == 0:
                rb.setChecked(True)
            vBox.addWidget(rb)
            self.targetSelectButtonGroup_2D.addButton(rb, index)
            index += 1

        row, col = (8, 3)
        self.targetSelectButtonGroup_3D = QButtonGroup()
        w = QWidget()
        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        w.setLayout(vBox)
        grid.addWidget(w, row, col)

        index=0
        for exampleEquationText in dfc.fittingTargetList:
            rb = QRadioButton(exampleEquationText)
            rb.toggled.connect(lambda:self.onTargetSelect_3D())
            if index == 0:
                rb.setChecked(True)
            vBox.addWidget(rb)
            self.targetSelectButtonGroup_3D.addButton(rb, index)
            index += 1

            # ROW 9 - empty label as visual buffer
            row, col = (9, 0)
        l = QLabel("   ")
        grid.addWidget(l, row, col)

        # ROW 10 - fitting buttons
        row, col = (10, 1)
        self.buttonFit_2D = QPushButton("Fit 2D Text Data", self)
        self.buttonFit_2D.clicked.connect(self.onFit_2D)
        grid.addWidget(self.buttonFit_2D, row, col)
    
        row, col = (10, 3)
        self.buttonFit_3D = QPushButton("Fit 3D Text Data", self)
        self.buttonFit_3D.clicked.connect(self.onFit_3D)
        grid.addWidget(self.buttonFit_3D, row, col)

        # ROW 11 - empty label as visual buffer
        row, col = (11, 0)
        l = QLabel("   ")
        grid.addWidget(l, row, col)


    def onFit_2D(self):
        print('2D fitting button')


    def onFit_3D(self):
        print('3D fitting button')


    def onTargetSelect_2D(self):
        ID = self.targetSelectButtonGroup_2D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        print('2D target:', ID) # ID was set using QButtonGroup's addButton() method above


    def onTargetSelect_3D(self):
        ID = self.targetSelectButtonGroup_3D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        print('3D target:', ID) # ID was set using QButtonGroup's addButton() method above


    def onEquationSelect_2D(self):
        ID = self.eqSelectButtonGroup_2D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        print('2D Eq:', ID) # ID was set using QButtonGroup's addButton() method above


    def onEquationSelect_3D(self):
        ID = self.eqSelectButtonGroup_3D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        print('3D Eq:', ID) # ID was set using QButtonGroup's addButton() method above





if __name__ == "__main__":
    qApp = QApplication(sys.argv)

    aw = InterfaceWindow()
    aw.show()
    sys.exit(qApp.exec_())
