import numpy as np
import pandas as pd

def fitTable(fitParam, fitCov, paramLabels = ['slope', 'intercept'], ci_factor = 2):
    """
    fitTable

    Produces a pandas DataFrame with fit values and their uncertainties given
    array of fit parameters and covariance matrix.

    INPUTS:
        fitParam - a NumPy array with the fit parameters
        fitCov - covariance matrix from the fit algorithm

    KEYWORDS:
        paramLabels=['slope', 'intercept'] - list of strings, default assumes linear fit with slope first
        ci_factor=2 - confidence interval factor (1 = 68%, 2 = 95.4%, etc.)

    RETURNS:
        pandas DataFrame
    """
    return pd.DataFrame(data = [fitParam, ci_factor*np.sqrt(np.diagonal(fitCov))], columns = paramLabels, index = ['value', 'uncertainty'])

def prettyPolyFit(x, y, deg = 1, yerr = None, paramLabels = None, ci_factor = 2):
    """
    prettyPolyFit

    Performs a polynomial fit and returns in the results in a pandas DataFrame and a polynomial best fit function.

    INPUTS:
        x - NumPy array of independent values
        y - NumPy array of dependent values
        
    
    KEYWORDS:
        deg=1 - degree of polynomial fit to data (1 = line, 2 = quadratic)
        yerr=None - NumPy array of uncertainties in dependent values
        paramLabels=None - list of strings, if None it will be set to default dependent on value of deg
          If deg = 1 then paramLabels=['slope','intercept']
          If deg > 1 then paramLabels=['c0','c1','c2',...]
        ci_factor=2 - confidence interval factor (1 = 68%, 2 = 95.4%, etc.), only used if yerr=None. If yerr provided then confidence interval is same as those uncertainties.

    RETURNS:
        (fit_table, fit_func) where
            fit_table is a DataFrame with values and uncertainities of the fit parameters
            fit_func is polynomial function representing the best fit
    """
    if yerr is not None:
        ci_factor = 1
        fitPoly, fitCov = np.polyfit(x, y, deg, w=1/yerr, cov=True)
    else:
        fitPoly, fitCov = np.polyfit(x, y, deg, cov=True)
    if paramLabels is None:
        if deg == 1:
            paramLabels = ['slope','intercept']
        else:
            paramLabels = []
            for i in range(deg):
                paramLabels.append(f"c{i}")
    return (fitTable(fitPoly, fitCov, paramLabels=paramLabels, ci_factor=ci_factor), np.poly1d(fitPoly)) 