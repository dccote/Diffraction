import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from numpy import *
import numpy as np

I = complex(0,1)

def diffraction(sCoords, A, k, r, yCoords):
    """ This is the core of the diffraction code.  Yes it is.
    sum all spherical waves of amplitude A from the source at sCoords
    on the screen at yCoords """

    Efield=[0]*Ny # Initialize with no field for a given r
    for ys in sCoords:
        for i,yf in enumerate(yCoords):
            R = sqrt( (yf-ys)*(yf-ys)+r*r)
            # we don't divide by r because we keep everything normalized
            Efield[i] = Efield[i] + A * exp(-I*k*R) 

    return Efield

def createFigure():
    fig, axes = plt.subplots(figsize=(10, 7))
    axes.set(xlabel='Distance', ylabel='Intensite', title="Profile de Diffraction")
    axes.set_ylim([0,1])
    return fig, axes


def reportProgress(r, Nr):
    tenPercent = int(Nr/10)
    if tenPercent == 0:
        tenPercent = 1

    #if r % tenPercent == 0:
    print("Progress {0:.0f}%".format(100*r/Nr))

if __name__ == "__main__":
      # This code computes the diffraction pattern in the simplest way possible:
    # by adding spherical ways from the diffraction objstacle. It is extremely
    # inefficient and slow, but it is trivial to understand.

    # Distance to screen
    R = 30000 # Distance source-screen in µm
    Nr = 2
    dR = R/Nr
    rCoords = [(r+1)*dR for r in range(Nr)]

    # Screen size in µm
    Y = 1000
    dy = 1
    Ny = int(Y/dy)
    yCoords = [(j-Ny/2)*dy for j in range(Ny)]

    # Source size in µm
    S = 50
    ds = 0.1
    Ns = int(S/ds)
    sCoords = [(j-Ns/2)*ds for j in range(Ns)]
    amplitude = (1/float(Ns)) # normalized

    wavelength = 1
    k = 2*pi/wavelength

    for idx,r in enumerate(rCoords): 
        reportProgress(idx,Nr)

        Efield = diffraction(sCoords, amplitude, k, r, yCoords)
        
        fig, axes = createFigure()
        axes.plot(yCoords, abs(Efield*conjugate(Efield)), linewidth=1)
        plt.show()

