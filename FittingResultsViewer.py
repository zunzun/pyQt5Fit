import os, sys, pickle
import pyeq3

from PyQt5.QtWidgets import *
from PyQt5 import QtCore # only for QtCore.Qt.WA_DeleteOnClose

# local imports
import IndividualReports
import AdditionalInfo


class ResultsWindow(QMainWindow):
    def __init__(self, pickledEquationFileName):
        QMainWindow.__init__(self)

        # without this, application hangs on close - arrrgh!
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.graphReportsListForPDF = []
        self.textReportsListForPDF = []
        self.sourceCodeReportsListForPDF = []

        # first, load the fitted equation
        equationFile = open(pickledEquationFileName, 'rb')
        self.equation = pickle.load(equationFile)
        equationFile.close()
        
        self.central_widget = QTabWidget(self)

        # the "graph reports" notebook tab
        nbGraphReports = QTabWidget()
        self.central_widget.addTab(nbGraphReports,'Graph Reports')
                
        if self.equation.GetDimensionality() == 2:
            report = IndividualReports.ModelScatterConfidenceGraph(self.equation)
            reportTitle = "Model With 95%Confidence"
            nbGraphReports.addTab(report[0], reportTitle)
            self.graphReportsListForPDF.append([report[1], reportTitle])
        else:
            report = IndividualReports.SurfacePlot(self.equation)
            reportTitle = "Surface Plot"
            nbGraphReports.addTab(report[0], reportTitle)
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
            report = IndividualReports.ContourPlot(self.equation)
            nbGraphReports.addTab(report[0], "Contour Plot")
            
            report = IndividualReports.ScatterPlot(self.equation)
            nbGraphReports.addTab(report[0], "Scatter Plot")

        report = IndividualReports.AbsoluteErrorGraph(self.equation)
        reportTitle = "Absolute Error"
        nbGraphReports.addTab(report[0], reportTitle)
        self.graphReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.AbsoluteErrorHistogram(self.equation)
        reportTitle = "Absolute Error Histogram"
        nbGraphReports.addTab(report[0], reportTitle)
        self.graphReportsListForPDF.append([report[1], reportTitle])

        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.PercentErrorGraph(self.equation)
            reportTitle = "Percent Error"
            nbGraphReports.addTab(report[0], reportTitle)
            self.graphReportsListForPDF.append([report[1], reportTitle])

            report = IndividualReports.PercentErrorHistogram(self.equation)
            reportTitle = "Percent Error Histogram"
            nbGraphReports.addTab(report[0], reportTitle)
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
        # the "text reports" notebook tab
        nbTextReports = QTabWidget()
        self.central_widget.addTab(nbTextReports,'Text Reports')
                
        report = IndividualReports.CoefficientAndFitStatistics(self.equation)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "Coefficient And Fit Statistics"
        nbTextReports.addTab(textTab, reportTitle)
        self.textReportsListForPDF.append([report, reportTitle])

        report = IndividualReports.CoefficientListing(self.equation)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "Coefficient Listing"
        nbTextReports.addTab(textTab, reportTitle)
        self.textReportsListForPDF.append([report, reportTitle])

        report = IndividualReports.DataArrayStatisticsReport('Absolute Error Statistics', self.equation.modelAbsoluteError)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "Absolute Error Statistics"
        nbTextReports.addTab(textTab, reportTitle)
        self.textReportsListForPDF.append([report, reportTitle])
        
        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.DataArrayStatisticsReport('Percent Error Statistics', self.equation.modelPercentError)
            textWidget = QPlainTextEdit(report) # plain text
            vbox = QVBoxLayout()
            vbox.addWidget(textWidget)
            textTab = QTabWidget()
            textTab.setLayout(vbox)
            reportTitle = "Percent Error Statistics"
        nbTextReports.addTab(textTab, reportTitle)
        self.textReportsListForPDF.append([report, reportTitle])

        # the "source code" notebook tab
        nbSourceCodeReports = QTabWidget()
        self.central_widget.addTab(nbSourceCodeReports,'Source Code')

        report = IndividualReports.SourceCodeReport(self.equation, 'CPP')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "C++"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'CSHARP')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "CSHARP"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'VBA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "VBA"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'PYTHON')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "PYTHON"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'JAVA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "JAVA"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'JAVASCRIPT')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "JAVASCRIPT"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'JULIA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "JULIA"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'SCILAB')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "SCILAB"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'MATLAB')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "MATLAB"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])
    
        report = IndividualReports.SourceCodeReport(self.equation,'FORTRAN90')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        reportTitle = "FORTRAN90"
        nbSourceCodeReports.addTab(textTab, reportTitle)
        self.sourceCodeReportsListForPDF.append([report, reportTitle])

        # the "additional information" notebook tab
        nbAdditionalInfo = QTabWidget()
        self.central_widget.addTab(nbAdditionalInfo,'Additional Information')

        textWidget = QPlainTextEdit(AdditionalInfo.history) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbAdditionalInfo.addTab(textTab, "Fitting History")

        textWidget = QPlainTextEdit(AdditionalInfo.author) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbAdditionalInfo.addTab(textTab, "Author History")

        textWidget = QPlainTextEdit(AdditionalInfo.links) # plain text
        textWidget.setLineWrapMode(QPlainTextEdit.NoWrap)
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbAdditionalInfo.addTab(textTab, "Web Links")

        # the "list of all standard equations" notebook tab
        dim = self.equation.GetDimensionality()
        allEquationsHTML = IndividualReports.AllEquationReport(dim)
        textWidget = QTextEdit(allEquationsHTML) # allow superscript, etc.
        textWidget.setLineWrapMode(QTextEdit.NoWrap)
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        self.central_widget.addTab(textTab, "List Of All Standard " + str(dim) + "D Equations")

        self.central_widget.setFocus()
        self.setCentralWidget(self.central_widget)
        
        # the "Save To PDF" tab
        fSaveTab = QTabWidget()
        self.central_widget.addTab(fSaveTab,"PDF File")
        
        # make button width the width of text
        btnText = "Save To PDF"
        self.buttonSavePDF = QPushButton(btnText, self)
        width = self.buttonSavePDF.fontMetrics().boundingRect(btnText).width() + 7
        self.buttonSavePDF.setMaximumWidth(width)
        self.buttonSavePDF.clicked.connect(self.createPDF)

        hbox = QHBoxLayout()
        hbox.addWidget(self.buttonSavePDF)
        fSaveTab.setLayout(hbox)

        # center window on the screen
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() // 2) - (self.frameSize().width() // 2),
                  (resolution.height() // 2) - (self.frameSize().height() // 2))


    def createPDF(self):
        try:
            import reportlab
        except:
            QMessageBox.question(self, 'Error',
                     "\nCould not import reportlab.\n\nPlease install using the command\n\n'pip3 install reportlab'",
                     QMessageBox.Ok)
            return

        fName = QFileDialog.getSaveFileName(self, 'PDF file name', 
                '',"PDF Files (*.pdf)")
        
        if fName[0]: # note use of [0] here
            import pdfCode
            pdfCode.CreatePDF(fName[0], # note use of [0] here
                              self.equation,
                              self.graphReportsListForPDF,
                              self.textReportsListForPDF,
                              self.sourceCodeReportsListForPDF
                              )
            QMessageBox.question(self, 'Success',
                     "\nSuccessfully created PDF file.",
                     QMessageBox.Ok)



if __name__ == "__main__":
    qApp = QApplication(sys.argv)

    aw = ResultsWindow('pickledEquationFile')
    aw.show()
    sys.exit(qApp.exec_())
