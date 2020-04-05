from converter import *
from calcBackground import getBackground
from scipy import integrate
from uncertainties import *
from uncertainties import unumpy
from matplotlib import rc
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
data = np.array(convert("gimp15-13-03","csv",","), dtype=float)
pixels = np.array(data[0], dtype=int)
values = data[1]
energyPolDecay = 6.78  # MeV
offset, stdDev, stdErr = getBackground()
valuesUncert = unumpy.uarray(values-offset, stdDev)

# TODO necessary?
# pixel to m
conversion = ufloat(29.3,1.4)

# integrate for energy in arbitrary units
e = sum(valuesUncert)

# integrate up to one point to get energy(x) in MeV
# the statictical error of 1 = data[0][i+1] - data[0][i]
# will be negelcted i.e. two pixels always have the same
# distance from each other
def energy(x, const):
    """const should be equal to integral over values
    but the error of this should not propagate because
    it is systematic. so use const = nominal_value(e)"""
    return energyPolDecay - sum(valuesUncert[:int(x):])*(energyPolDecay/const)


# plot (E, dE/dx)
scaleX, scaleY = 1, 1
domain = np.array([nominal_value(energy(x, nominal_value(e))) for x in pixels], dtype=float)
errorX = np.array([np.array(std_dev(energy(x, nominal_value(e)))) for x in pixels], dtype=float)
plt.xscale('log')
plt.yscale('log')
plt.ylabel(r'$\frac{dE}{dx} \textbf{ in  } \frac{MeV}{px}$')
plt.xlabel(r'$E \textbf{ in } MeV$')
#plt.xlim(0,energyPolDecay)
valuesUncert = valuesUncert / nominal_value(conversion)  # convert y axis from MeV/px to MeV/cm
plt.errorbar(scaleX * domain, scaleY * unumpy.nominal_values(valuesUncert*(energyPolDecay/nominal_value(e))), yerr=scaleY * unumpy.std_devs(valuesUncert*(energyPolDecay/nominal_value(e))), xerr=scaleX * errorX, fmt='ro',
                    linewidth=0.8, capsize=2, capthick=0.6, markersize=0)
plt.show()


def replaceImageJ():
    """plot average greyscale(x)"""
    plt.plot(pixels, unumpy.nominal_values(valuesUncert * (energyPolDecay / nominal_value(e))), 'ro', markersize=1)
    plt.show()
    plt.close()
replaceImageJ()