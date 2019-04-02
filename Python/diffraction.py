import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from numpy import *
import numpy as np

I = complex(0,1)

def diffraction(sCoords, A, k, r, yCoords, progressMessage="Summing source contributions"):
    """ This is the core of the diffraction code.  Yes it is.
    sum all spherical waves of amplitude A from the source at sCoords
    on the screen at yCoords. Done. """

    Efield=[0]*Ny # Initialize with no field for a given r
    for j,y_source in enumerate(sCoords):
        reportProgress(j,len(sCoords), progressMessage)
        for i,y_screen in enumerate(yCoords):
            Ro = sqrt( (y_screen-y_source)**2 + r**2)
            # we don't divide by r because we keep everything normalized
            Efield[i] += A * exp(-I*k*Ro) 

    return Efield

def createFigure():
    fig, axes = plt.subplots(figsize=(10, 7))
    axes.set(xlabel='Distance', ylabel='Intensite')
    axes.set_title("Profil de Diffraction")
#    axes.set_ylim([0,1])
    return fig, axes


def reportProgress(i, N, label=""):
    tenPercent = int(N/10)
    if tenPercent == 0:
        tenPercent = 1

    if (i+1) % tenPercent == 0:
        print("{0} {1:.0f}%".format(label, 100*(i+1)/N))

if __name__ == "__main__":
      # This code computes the diffraction pattern in the simplest way possible:
    # by adding spherical ways from the diffraction objstacle. It is extremely
    # inefficient and slow, but it is trivial to understand.

    # Distance to screen
    R = 30000 # Distance source-screen in µm
    Nr = 1
    dR = R/Nr
    rCoords = [(r+1)*dR for r in range(Nr)]

    # Screen size in µm
    Y = 60000
    dy = 10
    Ny = int(Y/dy)
    yCoords = [(j-Ny/2)*dy for j in range(Ny)]

    # Source slit length in µm
    a = 4
    da = 0.1
    Na = int(a/da)
    aCoords = [(j-Na/2)*da for j in range(Na)]
    
    # Repetition of source slit a, every b microns
    b = 10
    Nb = 2
    bCoords = [(j-Nb/2)*b for j in range(Nb)]

    # Grating coordinates, i.e. repetition of slit 'a', every 'b' coordinate.
    gCoords = []
    for x in bCoords:
        gCoords.extend([ x+y for y in aCoords])

    amplitude = (1/float(Na)) # normalized

    wavelength = 1
    k = 2*pi/wavelength

    for idx,r in enumerate(rCoords): 
        reportProgress(idx,len(rCoords), "Calculation for r={0:1.0f}".format(r))

        Gfield = diffraction(gCoords, amplitude/Nb, k, r, yCoords, progressMessage="Calculating grating")
        Efield = diffraction(aCoords, amplitude, k, r, yCoords, progressMessage="Calculating single slit")
        
        fig, axes = createFigure()

        if Nb == 1:
            axes.plot(yCoords, abs(Efield*conjugate(Efield)), linewidth=1,label="Enveloppe d'une seule fente")
            axes.set(xlabel='Distance', ylabel='Intensite')
            axes.set_title("Figure: Profil d'intensite de diffraction a R={1} mm d'une fente de largeur a={0} µm".format(a,R/1000), ha='center',size=13)
        else:
            axes.plot(yCoords, abs(Gfield*conjugate(Gfield)), linewidth=1, label='Reseau de diffraction de {0} fentes'.format(Nb))
            axes.plot(yCoords, abs(Efield*conjugate(Efield)), linestyle=':', linewidth=1,label="Enveloppe d'une seule fente")
            axes.set(xlabel='Distance', ylabel='Intensite', title="Profil d'intensite de diffraction a R={2} mm\n {3} fentes de largeur a={0} µm, a tous les b={1} µm".format(a,b,R/1000, Nb))
            axes.legend()
        plt.show()

