import os, sys, queue, pickle, time
import pyeq3

from PyQt5.QtWidgets import *

# local imports
import DataForControls as dfc


class InterfaceWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.queue = queue.Queue()

        self.equationSelect_2D = 0
        self.equationSelect_3D = 0
        self.fittingTargetSelect_2D = 0
        self.fittingTargetSelect_3D = 0
        
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
        textData = self.text_2D.toPlainText()
        equationSelection = dfc.exampleEquationList_2D[self.equationSelect_2D]
        fittingTargetSelection = dfc.fittingTargetList[self.fittingTargetSelect_2D]

        # the GUI's fitting target string contains what we need - extract it
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        if equationSelection == 'Linear Polynomial':
            self.equation = pyeq3.Models_2D.Polynomial.Linear(fittingTarget)
        if equationSelection == 'Quadratic Polynomial':
            self.equation = pyeq3.Models_2D.Polynomial.Quadratic(fittingTarget)
        if equationSelection == 'Cubic Polynomial':
            self.equation = pyeq3.Models_2D.Polynomial.Cubic(fittingTarget)
        if equationSelection == 'Witch Of Maria Agnesi A':
            self.equation = pyeq3.Models_2D.Miscellaneous.WitchOfAgnesiA(fittingTarget)
        if equationSelection == 'VanDeemter Chromatography':
            self.equation = pyeq3.Models_2D.Engineering.VanDeemterChromatography(fittingTarget)
        if equationSelection == 'Gamma Ray Angular Distribution (degrees) B':
            self.equation = pyeq3.Models_2D.LegendrePolynomial.GammaRayAngularDistributionDegreesB(fittingTarget)
        if equationSelection == 'Exponential With Offset':
            self.equation = pyeq3.Models_2D.Exponential.Exponential(fittingTarget, 'Offset')

        # convert text to numeric data checking for log of negative numbers, etc.
        try:
            pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(textData, self.equation, False)
        except:
            QMessageBox.question(self, 'Warning',
                     self.equation.reasonWhyDataRejected, QMessageBox.Ok)
            return

        # check for number of coefficients > number of data points to be fitted
        coeffCount = len(self.equation.GetCoefficientDesignators())
        dataCount = len(self.equation.dataCache.allDataCacheDictionary['DependentData'])
        if coeffCount > dataCount:
            QMessageBox.question(self, 'Warning',
                     "This equation requires a minimum of " + str(coeffCount) + " data points, you have supplied " + repr(dataCount) + ".", QMessageBox.Ok)
            return
        
    '''
        # Now the status dialog is used. Disable fitting buttons until thread completes
        self.buttonFit_2D.config(state=tk.DISABLED)
        self.buttonFit_3D.config(state=tk.DISABLED)
        
        # create simple top-level text dialog to display status as fitting progresses
        # when the fitting thread completes, it will close the status box
        self.statusBox = tk.Toplevel()
        self.statusBox.title("Fitting Status")
        self.statusBox.text = tk.Text(self.statusBox)
        self.statusBox.text.pack()
        
        # in tkinter the status box must be manually centered
        self.statusBox.update_idletasks()
        width = self.statusBox.winfo_width()
        height = self.statusBox.winfo_height()
        x = (self.statusBox.winfo_screenwidth() // 2) - (width // 2) # integer division
        y = (self.statusBox.winfo_screenheight() // 2) - (height // 2) # integer division
        self.statusBox.geometry('{}x{}+{}+{}'.format(width, height, x, y))        

        # thread will automatically start to run
        # "status update" handler will re-enable buttons
        self.fittingWorkerThread = FittingThread.FittingThread(self, self.equation)
'''


    def onFit_3D(self):
        print('3D fitting button')


    def onTargetSelect_2D(self):
        ID = self.targetSelectButtonGroup_2D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        self.fittingTargetSelect_2D = ID


    def onTargetSelect_3D(self):
        ID = self.targetSelectButtonGroup_3D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        self.fittingTargetSelect_3D = ID


    def onEquationSelect_2D(self):
        ID = self.eqSelectButtonGroup_2D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        self.equationSelect_2D = ID


    def onEquationSelect_3D(self):
        ID = self.eqSelectButtonGroup_3D.checkedId()
        if ID < 0: # initializes at -1, should be zero
            ID = 0
        self.equationSelect_3D = ID



if __name__ == "__main__":
    qApp = QApplication(sys.argv)

    aw = InterfaceWindow()
    aw.show()
    sys.exit(qApp.exec_())
