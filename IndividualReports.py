import pickle, inspect, re
import pyeq3
import numpy, scipy

from PyQt5.QtWidgets import *

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.mplot3d import  Axes3D
from matplotlib import cm # to colormap 3D surfaces from blue to red
import matplotlib.pyplot as plt


graphWidth = 800 # units are pixels
graphHeight = 600 # units are pixels

# 3D contour plot lines
numberOfContourLines = 16


# this is used in several reports
def DataArrayStatisticsReport(titleString, tempdata):
    textToReturn = titleString + '\n\n'
    
    # must at least have max and min
    minData = min(tempdata)
    maxData = max(tempdata)
    
    if maxData == minData:
        textToReturn += 'All data has the same value,\n'
        textToReturn += "value = %-.16E\n" % (minData)
        textToReturn += 'statistics cannot be calculated.\n'
    else:
        textToReturn += "max = %-.16E\n" % (maxData)
        textToReturn += "min = %-.16E\n" % (minData)
        
        try:
            temp = scipy.mean(tempdata)
            textToReturn += "mean = %-.16E\n" % (temp)
        except:
            textToReturn += "mean gave error in calculation\n"

        try:
            temp = scipy.stats.sem(tempdata)
            textToReturn += "standard error of mean = %-.16E\n" % (temp)
        except:
            textToReturn += "standard error of mean gave error in calculation\n"

        try:
            temp = scipy.median(tempdata)
            textToReturn += "median = %-.16E\n" % (temp)
        except:
            textToReturn += "median gave error in calculation\n"

        try:
            temp = scipy.var(tempdata)
            textToReturn += "variance = %-.16E\n" % (temp)
        except:
            textToReturn += "variance gave error in calculation\n"

        try:
            temp = scipy.std(tempdata)
            textToReturn += "std. deviation = %-.16E\n" % (temp)
        except:
            textToReturn += "std. deviation gave error in calculation\n"

        try:
            temp = scipy.stats.skew(tempdata)
            textToReturn += "skew = %-.16E\n" % (temp)
        except:
            textToReturn += "skew gave error in calculation\n"

        try:
            temp = scipy.stats.kurtosis(tempdata)
            textToReturn += "kurtosis = %-.16E\n" % (temp)
        except:
            textToReturn += "kurtosis gave error in calculation\n"
            
    return textToReturn
    

def CoefficientAndFitStatistics(equation):
    textToReturn = ''
    if equation.upperCoefficientBounds or equation.lowerCoefficientBounds:
        textToReturn += 'This model has coefficient bounds. Parameter statistics may\n'
        textToReturn += 'not be valid for parameter values at or near the bounds.\n'
        textToReturn += '\n'
    
    textToReturn += 'Degress of freedom error ' + str(equation.df_e) + '\n'
    textToReturn += 'Degress of freedom regression ' + str(equation.df_r) + '\n'
    
    if equation.rmse == None:
        textToReturn += 'Root Mean Squared Error (RMSE): n/a\n'
    else:
        textToReturn += 'Root Mean Squared Error (RMSE): ' + str(equation.rmse) + '\n'
    
    if equation.r2 == None:
        textToReturn += 'R-squared: n/a\n'
    else:
        textToReturn += 'R-squared: ' + str(equation.r2) + '\n'
    
    if equation.r2adj == None:
        textToReturn += 'R-squared adjusted: n/a\n'
    else:
        textToReturn += 'R-squared adjusted: ' + str(equation.r2adj) + '\n'
    
    if equation.Fstat == None:
        textToReturn += 'Model F-statistic: n/a\n'
    else:
        textToReturn += 'Model F-statistic: ' + str(equation.Fstat) + '\n'
    
    if equation.Fpv == None:
        textToReturn += 'Model F-statistic p-value: n/a\n'
    else:
        textToReturn += 'Model F-statistic p-value: ' + str(equation.Fpv) + '\n'
    
    if equation.ll == None:
        textToReturn += 'Model log-likelihood: n/a\n'
    else:
        textToReturn += 'Model log-likelihood: ' + str(equation.ll) + '\n'
    
    if equation.aic == None:
        textToReturn += 'Model AIC: n/a\n'
    else:
        textToReturn += 'Model AIC: ' + str(equation.aic) + '\n'
    
    if equation.bic == None:
        textToReturn += 'Model BIC: n/a\n'
    else:
        textToReturn += 'Model BIC: ' + str(equation.bic) + '\n'
    
    
    textToReturn += '\n'
    textToReturn += "Individual Parameter Statistics:\n"
    for i in range(len(equation.solvedCoefficients)):
        if type(equation.tstat_beta) == type(None):
            tstat = 'n/a'
        else:
            tstat = '%-.5E' %  (equation.tstat_beta[i])
    
        if type(equation.pstat_beta) == type(None):
            pstat = 'n/a'
        else:
            pstat = '%-.5E' %  ( equation.pstat_beta[i])
    
        if type(equation.sd_beta) != type(None):
            textToReturn += "Coefficient %s = %-.16E, std error: %-.5E\n" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i], equation.sd_beta[i])
        else:
            textToReturn += "Coefficient %s = %-.16E, std error: n/a\n" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i])
        textToReturn += "          t-stat: %s, p-stat: %s, 95 percent confidence intervals: [%-.5E, %-.5E]\n" % (tstat,  pstat, equation.ci[i][0], equation.ci[i][1])
            
    textToReturn += '\n'
    textToReturn += "Coefficient Covariance Matrix:\n"
    for i in  equation.cov_beta:
        textToReturn += str(i) + '\n'
        
    return textToReturn


def CoefficientListing(equation):
    textToReturn = ''
    cd = equation.GetCoefficientDesignators()
    for i in range(len(equation.solvedCoefficients)):
        textToReturn += "%s = %-.16E\n" % (cd[i], equation.solvedCoefficients[i])

    return textToReturn


def SourceCodeReport(equation, lanuageNameString):
    return eval('pyeq3.outputSourceCodeService().GetOutputSourceCode' + lanuageNameString + '(equation)')


def AbsoluteErrorGraph(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)
    dep_data = equation.dataCache.allDataCacheDictionary['DependentData']
    abs_error = equation.modelAbsoluteError
    axes.plot(dep_data, abs_error, 'D')
    
    if equation.GetDimensionality() == 2: # used for labels only
        axes.set_title('Absolute Error vs. X Data')
        axes.set_xlabel('X Data')
    else:
        axes.set_title('Absolute Error vs. Z Data')
        axes.set_xlabel('Z Data')
        
    axes.set_ylabel(" Absolute Error") # Y axis label is always absolute error

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def PercentErrorGraph(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)
    dep_data = equation.dataCache.allDataCacheDictionary['DependentData']
    per_error = equation.modelPercentError
    axes.plot(dep_data, per_error, 'D')
    
    if equation.GetDimensionality() == 2: # used for labels only
        axes.set_title('Percent Error vs. X Data')
        axes.set_xlabel('X Data')
    else:
        axes.set_title('Percent Error vs. Z Data')
        axes.set_xlabel('Z Data')
        
    axes.set_ylabel(" Percent Error") # Y axis label is always percent error

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def AbsoluteErrorHistogram(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)
    abs_error = equation.modelAbsoluteError
    bincount = len(abs_error)//2 # integer division
    if bincount < 5:
        bincount = 5
    if bincount > 25:
        bincount = 25
    n, bins, patches = axes.hist(abs_error, bincount, rwidth=0.8)
    
    # some axis space at the top of the graph
    ylim = axes.get_ylim()
    if ylim[1] == max(n):
        axes.set_ylim(0.0, ylim[1] + 1)

    axes.set_title('Absolute Error Histogram') # add a title
    axes.set_xlabel('Absolute Error') # X axis data label
    axes.set_ylabel(" Frequency") # Y axis label is frequency

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def PercentErrorHistogram(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)
    per_error = equation.modelPercentError
    bincount = len(per_error)//2 # integer division
    if bincount < 5:
        bincount = 5
    if bincount > 25:
        bincount = 25
    n, bins, patches = axes.hist(per_error, bincount, rwidth=0.8)
    
    # some axis space at the top of the graph
    ylim = axes.get_ylim()
    if ylim[1] == max(n):
        axes.set_ylim(0.0, ylim[1] + 1)

    axes.set_title('Percent Error Histogram') # add a title
    axes.set_xlabel('Percent Error') # X axis data label
    axes.set_ylabel(" Frequency") # Y axis label is frequency

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def ModelScatterConfidenceGraph(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)
    y_data = equation.dataCache.allDataCacheDictionary['DependentData']
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]

    # create data for the fitted equation plot
    xModel = numpy.linspace(min(x_data), max(x_data))

    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([xModel, xModel])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    yModel = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache # restore the original data cache

    # first the raw data as a scatter plot
    axes.plot(x_data, y_data,  'D')

    # now the model as a line plot
    axes.plot(xModel, yModel)

    # now calculate confidence intervals
    # http://support.sas.com/documentation/cdl/en/statug/63347/HTML/default/viewer.htm#statug_nlin_sect026.htm
    # http://www.staff.ncl.ac.uk/tom.holderness/software/pythonlinearfit
    mean_x = numpy.mean(x_data)
    n = equation.nobs

    t_value = scipy.stats.t.ppf(0.975, equation.df_e) # (1.0 - (a/2)) is used for two-sided t-test critical value, here a = 0.05

    confs = t_value * numpy.sqrt((equation.sumOfSquaredErrors/equation.df_e)*(1.0/n + (numpy.power((xModel-mean_x),2.0)/
                                                                                       ((numpy.sum(numpy.power(x_data,2.0)))-n*(numpy.power(mean_x,2.0))))))

    # get lower and upper confidence limits based on predicted y and confidence intervals
    upper = yModel + abs(confs)
    lower = yModel - abs(confs)

    # mask off any numbers outside the existing plot limits
    booleanMask = yModel > axes.get_ylim()[0]
    booleanMask &= (yModel < axes.get_ylim()[1])

    # color scheme improves visibility on black background lines or points
    axes.plot(xModel[booleanMask], lower[booleanMask], linestyle='solid', color='white')
    axes.plot(xModel[booleanMask], upper[booleanMask], linestyle='solid', color='white')
    axes.plot(xModel[booleanMask], lower[booleanMask], linestyle='dashed', color='blue')
    axes.plot(xModel[booleanMask], upper[booleanMask], linestyle='dashed', color='blue')

    axes.set_title('Model With 95% Confidence Intervals') # add a title
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def SurfacePlot(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    
    matplotlib.pyplot.grid(True)
    axes = Axes3D(f)
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    xModel = numpy.linspace(min(x_data), max(x_data), 20)
    yModel = numpy.linspace(min(y_data), max(y_data), 20)
    X, Y = numpy.meshgrid(xModel, yModel)

    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([X, Y])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    Z = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache# restore the original data cache

    axes.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)

    axes.scatter(x_data, y_data, z_data)

    axes.set_title('Surface Plot (click-drag with mouse)') # add a title for surface plot
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label
    axes.set_zlabel('Z Data') # Z axis data label

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def ContourPlot(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    axes = f.add_subplot(111)

    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    xModel = numpy.linspace(min(x_data), max(x_data), 20)
    yModel = numpy.linspace(min(y_data), max(y_data), 20)
    X, Y = numpy.meshgrid(xModel, yModel)
        
    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([X, Y])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    Z = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache # restore the original data cache
        
    axes.plot(x_data, y_data, 'o')

    axes.set_title('Contour Plot') # add a title for contour plot
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label
    
    CS = matplotlib.pyplot.contour(X, Y, Z, numberOfContourLines, colors='k')
    matplotlib.pyplot.clabel(CS, inline=1, fontsize=10) # labels for contours

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def ScatterPlot(equation):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    canvas = FigureCanvas(f)
    
    matplotlib.pyplot.grid(True)
    axes = Axes3D(f)
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    axes.scatter(x_data, y_data, z_data)

    axes.set_title('Scatter Plot (click-drag with mouse)')
    axes.set_xlabel('X Data')
    axes.set_ylabel('Y Data')
    axes.set_zlabel('Z Data')

    plt.close('all') # clean up after using pyplot or else thaere can be memory and process problems
    return canvas


def AllEquationReport(dim):
        htmlToReturn = '' # build this as we progress
        
        if dim == 2:
            module = pyeq3.Models_2D
        else:
            module = pyeq3.Models_3D
            
        htmlToReturn += '<table border=1>'
        
        for submodule in inspect.getmembers(module):
            if inspect.ismodule(submodule[1]):
                for equationClass in inspect.getmembers(submodule[1]):
                    if inspect.isclass(equationClass[1]):
                        for extendedVersionName in ['Default', 'Offset']:
                            if (-1 != extendedVersionName.find('Offset')) and (equationClass[1].autoGenerateOffsetForm == False):
                                continue
        
                            equation = equationClass[1]('SSQABS', extendedVersionName)
                            htmlToReturn += '<tr>'
                            htmlToReturn += '<td nowrap><b>' + str(dim) + 'D ' + submodule[0] + '</b></td>'
                            htmlToReturn += '<td nowrap><i>' + equation.GetDisplayName() + '>/i></td>'
                            htmlToReturn += '<td nowrap>' + equation.GetDisplayHTML() + '</td>'
                            htmlToReturn += '</tr>'
                            
        htmlToReturn += '</table>'
        
        return htmlToReturn
