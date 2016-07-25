import os, sys, pickle
import pyeq3

from PyQt5.QtWidgets import *

# local imports
import IndividualReports
import AdditionalInfo


class ResultsWidget(QTabWidget):
    
    def __init__(self, pickledEquationFileName, parent = None):
        QTabWidget.__init__(self, parent)
        
        # first, load the fitted equation
        equationFile = open(pickledEquationFileName, 'rb')
        equation = pickle.load(equationFile)
        equationFile.close()
        
        '''
        topLevelNotebook = ttk.Notebook(self)
        topLevelNotebook.pack()

        # the "graph reports" notebook tab
        nbGraphReports = ttk.Notebook(topLevelNotebook)
        nbGraphReports.pack()
        topLevelNotebook.add(nbGraphReports, text='Graph Reports')

        if equation.GetDimensionality() == 2:
            report = IndividualReports.ModelScatterConfidenceGraph(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Model With 95%Confidence")
        else:
            report = IndividualReports.SurfacePlot(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Surface Plot")
            
            report = IndividualReports.ContourPlot(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Contour Plot")
            
            report = IndividualReports.ScatterPlot(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Scatter Plot")

        report = IndividualReports.AbsoluteErrorGraph(nbGraphReports, equation)
        nbGraphReports.addTab(textTab, "Absolute Error")

        report = IndividualReports.AbsoluteErrorHistogram(nbGraphReports, equation)
        nbGraphReports.addTab(textTab, "Absolute Error Histogram")

        if equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.PercentErrorGraph(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Percent Error")

            report = IndividualReports.PercentErrorHistogram(nbGraphReports, equation)
            nbGraphReports.addTab(textTab, "Percent Error Histogram")
'''
        # the "text reports" notebook tab
        nbTextReports = QTabWidget()
        self.addTab(nbTextReports,'Text Reports')
                
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
        self.addTab(nbSourceCodeReports,'Source Code')

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
        self.addTab(nbAdditionalInfo,'Additional Information')

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
        self.addTab(textTab, "List Of All Standard " + str(dim) + "D Equations")







if __name__ == "__main__":
   app = QApplication(sys.argv)
   ex = ResultsWidget('pickledEquationFile')
   ex.show()
   sys.exit(app.exec_())
