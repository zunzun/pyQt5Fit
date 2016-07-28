import os, sys, pickle
import pyeq3

from PyQt5.QtWidgets import *
from PyQt5 import QtCore # inly for QtCore.Qt.WA_DeleteOnClose

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# local imports
import IndividualReports
import AdditionalInfo


class ApplicationWindow(QMainWindow):
    def __init__(self, pickledEquationFileName):
        QMainWindow.__init__(self)

        # without this, application hangs on close - arrrgh!
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # first, load the fitted equation
        equationFile = open(pickledEquationFileName, 'rb')
        equation = pickle.load(equationFile)
        equationFile.close()
        
        self.central_widget = QTabWidget(self)

        # the "graph reports" notebook tab
        nbGraphReports = QTabWidget()
        self.central_widget.addTab(nbGraphReports,'Graph Reports')
                
        if equation.GetDimensionality() == 2:
            report = IndividualReports.ModelScatterConfidenceGraph(equation)
            nbGraphReports.addTab(report, "Model With 95%Confidence")
        else:
            report = IndividualReports.SurfacePlot(equation)
            nbGraphReports.addTab(report, "Surface Plot")
            
            report = IndividualReports.ContourPlot(equation)
            nbGraphReports.addTab(report, "Contour Plot")
            
            report = IndividualReports.ScatterPlot(equation)
            nbGraphReports.addTab(report, "Scatter Plot")

        report = IndividualReports.AbsoluteErrorGraph(equation)
        nbGraphReports.addTab(report, "Absolute Error")

        report = IndividualReports.AbsoluteErrorHistogram(equation)
        nbGraphReports.addTab(report, "Absolute Error Histogram")

        if equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.PercentErrorGraph(equation)
            nbGraphReports.addTab(report, "Percent Error")

            report = IndividualReports.PercentErrorHistogram(equation)
            nbGraphReports.addTab(report, "Percent Error Histogram")
            
        # the "text reports" notebook tab
        nbTextReports = QTabWidget()
        self.central_widget.addTab(nbTextReports,'Text Reports')
                
        report = IndividualReports.CoefficientAndFitStatistics(equation)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbTextReports.addTab(textTab, "Coefficient And Fit Statistics")
        
        report = IndividualReports.CoefficientListing(equation)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbTextReports.addTab(textTab, "Coefficient Listing")

        report = IndividualReports.DataArrayStatisticsReport('Absolute Error Statistics', equation.modelAbsoluteError)
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbTextReports.addTab(textTab, "Absolute Error Statistics")
        
        if equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.DataArrayStatisticsReport('Percent Error Statistics', equation.modelPercentError)
            textWidget = QPlainTextEdit(report) # plain text
            vbox = QVBoxLayout()
            vbox.addWidget(textWidget)
            textTab = QTabWidget()
            textTab.setLayout(vbox)
            nbTextReports.addTab(textTab, "Percent Error Statistics")

        # the "source code" notebook tab
        nbSourceCodeReports = QTabWidget()
        self.central_widget.addTab(nbSourceCodeReports,'Source Code')

        report = IndividualReports.SourceCodeReport(equation, 'CPP')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "C++")
    
        report = IndividualReports.SourceCodeReport(equation,'CSHARP')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "CSHARP")
    
        report = IndividualReports.SourceCodeReport(equation,'VBA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "VBA")
    
        report = IndividualReports.SourceCodeReport(equation,'PYTHON')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "PYTHON")
    
        report = IndividualReports.SourceCodeReport(equation,'JAVA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "JAVA")
    
        report = IndividualReports.SourceCodeReport(equation,'JAVASCRIPT')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "JAVASCRIPT")
    
        report = IndividualReports.SourceCodeReport(equation,'JULIA')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "JULIA")
    
        report = IndividualReports.SourceCodeReport(equation,'SCILAB')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "SCILAB")
    
        report = IndividualReports.SourceCodeReport(equation,'MATLAB')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "MATLAB")
    
        report = IndividualReports.SourceCodeReport(equation,'FORTRAN90')
        textWidget = QPlainTextEdit(report) # plain text
        vbox = QVBoxLayout()
        vbox.addWidget(textWidget)
        textTab = QTabWidget()
        textTab.setLayout(vbox)
        nbSourceCodeReports.addTab(textTab, "FORTRAN90")

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
        dim = equation.GetDimensionality()
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



qApp = QApplication(sys.argv)

aw = ApplicationWindow('pickledEquationFile')
aw.show()
sys.exit(qApp.exec_())
