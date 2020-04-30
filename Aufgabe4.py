from converter import *
from calcBackground import getBackground
from calcBackground import meanArr
from scipy import integrate
from uncertainties import *
from uncertainties import unumpy
from matplotlib import rc
from scipy.optimize import curve_fit
import numpy as np
import scipy
import matplotlib.pyplot as plt
import os

# Latex
rc('text', usetex=True)

# Ordner für Graphen
if not os.path.exists("Graphen"):
    os.mkdir("Graphen")

# TODO is error of conversion negligible + 6.78 MeV correct?
# get data
data = np.array(convert("try","csv",","), dtype=float)
pixels = np.array(data[0], dtype=int)
values = data[1]
energyPolDecay = 6.78  # MeV
offset, stdDev, stdErr = getBackground()
#valuesUncert = unumpy.uarray(values-offset, stdDev)
m = 3727.37940  # MeV

# data is very difficult to deal with.
# take mean from bins data points
bins = 1
values = meanArr(values, bins, False)
pixels = meanArr(pixels, bins, False)
#print(values)
#print(pixels)
valuesUncert = unumpy.uarray(values-offset, stdDev)

# TODO necessary?
# pixel to m
conversion = ufloat(29.3,1.4)

# integrate for energy in arbitrary units
e = sum(valuesUncert)*bins
print(stdDev/nominal_value(e))
# integrate up to one point to get energy(x) in MeV
# the statictical error of 1 = data[0][i+1] - data[0][i]
# will be negelcted i.e. two pixels always have the same
# distance from each other
def energy(x, const):
    """const should be equal to integral over values
    but the error of this should not propagate because
    it is systematic. so use const = nominal_value(e)"""
    return energyPolDecay - sum(valuesUncert[:int(x)//bins:])*(energyPolDecay/const)*bins

# bethe bloch eq
def betheBloch(E, I, c):
    temp = E + m
    gamma = temp/m
    beta = np.sqrt(1 - 1 / gamma**2)
    return c*(
        (1/beta**2) * np.log( (2 * m * (gamma**2) * (beta**2)) / I ) - 1
    )


# fit data with bethe bloch
cutMax, cutMin = -len(values), 1
domain = np.array([nominal_value(energy(x, nominal_value(e))) for x in pixels], dtype=float)
print(domain)
errorX = np.array([np.array(std_dev(energy(x, nominal_value(e)))) for x in pixels], dtype=float)
popt, pcov = curve_fit(betheBloch, domain[cutMin:-cutMax:], unumpy.nominal_values(valuesUncert)[cutMin:-cutMax:],
                      sigma=unumpy.std_devs(valuesUncert)[cutMin:-cutMax:], p0=[0.3, 0.4])
eFit = np.linspace(domain[cutMin:-cutMax:][0], domain[cutMin:-cutMax:][-1], 10000)
yFit = betheBloch(eFit, *popt)
print(popt)


# plot (E, dE/dx)
scaleX, scaleY = 1, 1
plt.figure(figsize=(5,1))
plt.xscale('log')
plt.yscale('log')
plt.ylabel(r'$-\frac{dE}{dx} \textbf{ in  } \frac{MeV}{cm}$')
plt.xlabel(r'$E \textbf{ in } MeV$')
valuesUncert = valuesUncert / nominal_value(conversion)  # convert y axis from MeV/px to MeV/cm
#plt.errorbar(scaleX * domain, scaleY * unumpy.nominal_values(valuesUncert*(energyPolDecay/nominal_value(e))), yerr=scaleY * unumpy.std_devs(valuesUncert*(energyPolDecay/nominal_value(e))), xerr=scaleX * errorX, fmt='ro',
#                    linewidth=0.8, capsize=2, capthick=0.6, markersize=0)
plt.plot(eFit, (yFit*(energyPolDecay/nominal_value(e))) / nominal_value(conversion), 'k-', lw=.6)
plt.savefig("Graphen\\dEdx_von_E.pdf", dpi=500, bbox_inches='tight')


def replaceImageJ():
    """plot average greyscale(x)"""
    plt.plot(pixels, unumpy.nominal_values(valuesUncert * (energyPolDecay / nominal_value(e))), 'ro', markersize=1)
    plt.show()
    plt.close()
#replaceImageJ()