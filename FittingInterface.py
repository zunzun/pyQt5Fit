import os, sys, queue, pickle, time, inspect
import pyeq3

import matplotlib # ensure this dependency imports for later use in fitting results

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# local imports
import DataForControls as dfc
import FittingThread


class StatusUpdateSignal(QObject):
    statusUpdate = pyqtSignal() 



class InterfaceWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # http://zetcode.com/gui/pyqt5/eventssignals/
        self.updateStatusSignal = StatusUpdateSignal()
        self.updateStatusSignal.statusUpdate.connect(self.onUpdateStatus)
        
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
        self.text_2D.setMinimumHeight(200)
        grid.addWidget(self.text_2D, row, col)

        row, col = (2, 3)
        self.text_3D = QPlainTextEdit(dfc.exampleText_3D) # plain text
        self.text_2D.setMinimumHeight(200)
        grid.addWidget(self.text_3D, row, col)

        # ROW 3 - empty label as visual buffer
        row, col = (3, 0)
        l = QLabel("   ")
        grid.addWidget(l, row, col)

        # ROW 4 - equation selection labels
        # no "self" needed as no later references exist
        row, col = (4, 1)
        l = QLabel("<b>--- Standard 2D Equations ---</b>") # bold tags
        grid.addWidget(l, row, col)
        
        row, col = (4, 3)
        l = QLabel("<b>--- Standard 3D Equations ---</b>") # bold tags
        grid.addWidget(l, row, col)

        # ROW 5 - equation selection
        row, col = (5, 1)
        self.cb_Modules2D = QComboBox(self)
        self.cb_Modules2D.activated.connect(self.moduleSelectChanged_2D)
        moduleNameList = list(dfc.eq_od2D.keys())
        self.cb_Modules2D.addItems(moduleNameList)
        self.cb_Modules2D.setCurrentIndex(moduleNameList.index('Polynomial'))
        
        self.cb_Equations2D = QComboBox(self)
        equationNameList = self.GetEquationListForModule(2, 'Polynomial')
        self.cb_Equations2D.addItems(equationNameList)
        self.cb_Equations2D.setCurrentIndex(equationNameList.index('1st Order (Linear)'))

        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        vBox.setContentsMargins(0,0,0,0)
        vBox.addWidget(self.cb_Modules2D)
        vBox.addWidget(self.cb_Equations2D)
        w = QWidget()
        w.setLayout(vBox)
        grid.addWidget(w, row, col)
            
        row, col = (5, 3)
        self.cb_Modules3D = QComboBox(self)
        self.cb_Modules3D.activated.connect(self.moduleSelectChanged_3D)
        moduleNameList = list(dfc.eq_od3D.keys())
        self.cb_Modules3D.addItems(moduleNameList)
        self.cb_Modules3D.setCurrentIndex(moduleNameList.index('Polynomial'))
        
        self.cb_Equations3D = QComboBox(self)
        equationNameList = self.GetEquationListForModule(3, 'Polynomial')
        self.cb_Equations3D.addItems(equationNameList)
        self.cb_Equations3D.setCurrentIndex(equationNameList.index('Linear'))

        vBox = QVBoxLayout()
        vBox.setSpacing(0)
        vBox.setContentsMargins(0,0,0,0)
        vBox.addWidget(self.cb_Modules3D)
        vBox.addWidget(self.cb_Equations3D)
        w = QWidget()
        w.setLayout(vBox)
        grid.addWidget(w, row, col)

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
        vBox.setContentsMargins(0,0,0,0)
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
        vBox.setContentsMargins(0,0,0,0)
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

        # center window on the screen
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() // 2) - (self.frameSize().width() // 2),
                  (resolution.height() // 2) - (self.frameSize().height() // 2))


    def GetEquationListForModule(self, inDimension, inModuleName):
        strModule = 'pyeq3.Models_' + str(inDimension) + 'D.' + inModuleName
        moduleMembers = inspect.getmembers(eval(strModule))
        returnList = []
        for equationClass in moduleMembers:
            if inspect.isclass(equationClass[1]):
                for extendedVersionName in ['Default', 'Offset']:
                    
                    # if the equation *already* has an offset,
                    # do not add an offset version here
                    if (-1 != extendedVersionName.find('Offset')) and (equationClass[1].autoGenerateOffsetForm == False):
                        continue
                        
                    # in this application, exclude equation than need extra input
                    if equationClass[1].splineFlag or \
                            equationClass[1].userSelectablePolynomialFlag or \
                            equationClass[1].userCustomizablePolynomialFlag or \
                            equationClass[1].userSelectablePolyfunctionalFlag or \
                            equationClass[1].userSelectableRationalFlag or \
                            equationClass[1].userDefinedFunctionFlag:
                        continue

                    equation = equationClass[1]('SSQABS', extendedVersionName)

                    returnList.append(equation.GetDisplayName())

        returnList.sort()
        return returnList


    def moduleSelectChanged_2D(self):
        listIndex = self.cb_Modules2D.currentIndex()
        moduleName = list(dfc.eq_od2D.keys())[listIndex]
        equationNameList = self.GetEquationListForModule(2, moduleName)
        self.cb_Equations2D.clear()
        self.cb_Equations2D.addItems(equationNameList)
        self.cb_Equations2D.setCurrentIndex(0)


    def moduleSelectChanged_3D(self):
        listIndex = self.cb_Modules3D.currentIndex()
        moduleName = list(dfc.eq_od3D.keys())[listIndex]
        equationNameList = self.GetEquationListForModule(3, moduleName)
        self.cb_Equations3D.clear()
        self.cb_Equations3D.addItems(equationNameList)
        self.cb_Equations3D.setCurrentIndex(0)


    def onFit_2D(self):
        textData = self.text_2D.toPlainText()

        moduleListIndex = self.cb_Modules2D.currentIndex()
        moduleName = list(dfc.eq_od2D.keys())[moduleListIndex]
        equationListIndex = self.cb_Equations2D.currentIndex()
        equationNameList = self.GetEquationListForModule(2, moduleName)
        equationName = equationNameList[equationListIndex]

        # the GUI's fitting target string contains what we need - extract it
        fittingTargetSelection = dfc.fittingTargetList[self.fittingTargetSelect_2D]
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od2D[moduleName][equationName]
        eqString = 'pyeq3.Models_2D.' + moduleName + '.' + item[0] + "('" + fittingTarget + "','" + item[1] + "')"
        self.equation = eval(eqString)

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
            

        # Now the status dialog is used. Disable fitting buttons until thread completes
        self.statusBox = QDialog(self)
        self.statusBox.text = QPlainTextEdit('', self.statusBox) # plain text
        self.statusBox.setGeometry(300, 300, 290, 150)
        self.statusBox.setWindowTitle('Fitting Status')

        # thread will automatically start to run
        self.fittingWorkerThread = FittingThread.FittingThread(self, self.equation)

        self.statusBox.exec_()  # blocks all other windows until this window is closed


    def onFit_3D(self):
        textData = self.text_3D.toPlainText()

        moduleListIndex = self.cb_Modules3D.currentIndex()
        moduleName = list(dfc.eq_od3D.keys())[moduleListIndex]
        equationListIndex = self.cb_Equations3D.currentIndex()
        equationNameList = self.GetEquationListForModule(3, moduleName)
        equationName = equationNameList[equationListIndex]

        # the GUI's fitting target string contains what we need - extract it
        fittingTargetSelection = dfc.fittingTargetList[self.fittingTargetSelect_3D]
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od3D[moduleName][equationName]
        eqString = 'pyeq3.Models_3D.' + moduleName + '.' + item[0] + "('" + fittingTarget + "','" + item[1] + "')"
        self.equation = eval(eqString)

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
            

        # Now the status dialog is used. Disable fitting buttons until thread completes
        self.statusBox = QDialog(self)
        self.statusBox.text = QPlainTextEdit('', self.statusBox) # plain text
        self.statusBox.setGeometry(300, 300, 290, 150)
        self.statusBox.setWindowTitle('Fitting Status')

        # thread will automatically start to run
        self.fittingWorkerThread = FittingThread.FittingThread(self, self.equation)

        self.statusBox.exec_()  # blocks all other windows until this window is closed


    def onUpdateStatus(self):
        data = self.queue.get_nowait()
        
        if type(data) == type(''): # text is used for status box display to user
            self.statusBox.text.appendPlainText(data + '\n')
        else: # the queue data is now the fitted equation.
            # write the fitted equation to a pickle file.  This
            # allows the possibility of archiving the fitted equations
            pickledEquationFile = open("pickledEquationFile", "wb")
            pickle.dump(data, pickledEquationFile)
            pickledEquationFile.close()
    
            # view fitting results
            # allow multiple result windows to open for comparisons
            p = os.popen(sys.executable + ' FittingResultsViewer.py')
            p.close()
            
            # close the now-unused status box
            self.statusBox.close()
        

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
