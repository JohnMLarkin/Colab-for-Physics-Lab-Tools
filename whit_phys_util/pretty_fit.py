import numpy as np
import pandas as pd

def fitTable(fitParam, fitCov, paramLabels = ['slope', 'intercept']):
    return pd.DataFrame(data = [fitParam, 2*np.sqrt(np.diagonal(fitCov))], columns = paramLabels, index = ['value', 'uncertainty'])

def prettyPolyFit(x, y, deg, paramLabels = ['slope', 'intercept']):
    fitPoly, fitCov = np.polyfit(x, y, deg, cov=True)
    return (fitTable(fitPoly, fitCov, paramLabels), np.poly1d(fitPoly)) 