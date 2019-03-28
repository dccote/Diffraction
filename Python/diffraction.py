import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from numpy import *
import numpy as np

# This code computes the diffraction pattern in the simplest way possible:
# by adding spherical ways from the diffraction objstacle. It is extremely
# inefficient and slow, but it is trivial to understand.

# Everything in microns
wavelength = 1
k = 2*pi/wavelength
I = complex(0,1)


# Distance to screen
R = 30000 # Distance source-screen
Nr = 100
dR = R/Nr

# Screen size in µm
Y = 1000
dy = 1
Ny = int(Y/dy)
yCoords = [(j-Ny/2)*dy for j in range(Ny)]

# Source size
S = 50
ds = 0.1
Ns = int(S/ds)
sCoords = [(j-Ns/2)*ds for j in range(Ns)]


tenPercent = int(Ns/10)
if tenPercent == 0:
    tenPercent = 1

for r in range(Nr): 
    Efield=[0]*Ny # Initialize with no field
    R  = (r+1)*dR
    for s in range(Ns):
        if s % tenPercent == 0:
            print("Progress {0:.0f}%".format(100*s/Ns))

        ys = (s-Ns/2)*ds
        for i in range(Ny):
            yf = (i-Ny/2)*dy
            rf = sqrt( (yf-ys)*(yf-ys)+R*R)
            Efield[i] = Efield[i] + exp(-I*k*rf)/float(Ns)


    fig, axes = plt.subplots(figsize=(10, 7))

    axes.set(xlabel='Distance', ylabel='Intensite', title="Profile de Diffraction")
    axes.set_ylim([0,1])
    axes.plot(yCoords, abs(Efield*conjugate(Efield)), linewidth=1)

    if Nr == 1:
        plt.show()

    fig.savefig("diffraction-{0:03d}.png".format(r), dpi=150)
    plt.close('all')


def reportProgress(r, Nr):
    print("Progress R={0:.0f}/{1}".format(r,Nr))
