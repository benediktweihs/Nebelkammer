from converter import *
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
"""calc background with area without decays"""

def getBackground():
    """return systematic background, std deviation of background, std Error of systematic Background
    systematic background (mean of grey scale image without decays) should be subtracted from all measurements and
    consequently all measurements will have the systematic uncertainty of the error of the mean (=std Error)
    the std deviation is an intrinsic error of all measurements (statistical error) which will be visible on all
    plots"""
    # get values from area without decays
    data = np.array(convert("background", "csv", ","), dtype=float)
    pixels = data[0]
    values = data[1]

    def const(x,c):
        return c

    # fit const to data and determine stddeviation and systematic background
    # stderror will then be the systematic error!
    popt, pcov = curve_fit(const, pixels, values)

    # save result
    pixelsFit = np.linspace(pixels[0], pixels[-1], 1000)
    plt.plot(pixels, values, 'ro', markersize=1)
    plt.plot(pixelsFit, [popt[0]]*len(pixelsFit), 'k-', lw=.6)
    #plt.show()
    plt.close()

    return popt[0], np.sqrt(pcov[0][0]), np.sqrt(pcov[0][0])/np.sqrt(len(pixels))