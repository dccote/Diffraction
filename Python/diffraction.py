import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from numpy import *
import numpy as np

I = complex(0,1)

def diffraction(sCoords, sAmplitudes, k, r, screenCoords, progressMessage="Computing diffraction"):
    """ This is the core of the diffraction code.  Yes it is.
    sum all spherical waves of amplitude A from the source at sCoords
    on the screen at yCoords. Done. """

    if len(sCoords) != len(sAmplitudes):
        raise ValueError("Array not same size coords={0:d}, amplitude={1:d}".format(len(sCoords), len(sAmplitudes)))

    Efield=[0]*len(screenCoords) # Initialize with no field for a given r
    for j,y_source in enumerate(sCoords):
        A = sAmplitudes[j]
        reportProgress(j,len(sCoords), progressMessage)
        for i,y_screen in enumerate(screenCoords):
            Ro = sqrt( (y_screen-y_source)**2 + r**2)
            # we don't divide by r because we keep everything normalized
            Efield[i] += A * exp(-I*k*Ro) 

    return Efield

def createFigure():
    fig, axes = plt.subplots(figsize=(10, 7))
    axes.set(xlabel='Distance', ylabel='Intensite')
    axes.set_title("Profil de Diffraction")
    return fig, axes

def showDiffractedIntensity(screenCoordinates, Efield, envelope=None, title=""):
    fig, axes = createFigure()

    axes.plot(screenCoordinates, abs(Efield*conjugate(Efield)), linewidth=1,label="Diffracted beam")

    if envelope is not None:
        axes.plot(screenCoordinates, envelope, linestyle=":", linewidth=1,label="Envelope")

    axes.set(xlabel='Position [µm]', ylabel='Intensite')
    axes.set_title(title, ha='center',size=13)
    plt.show()


def reportProgress(i, N, label=""):
    """ i goes from 0 to N-1 """
    tenPercent = int(N/10)
    percent = int((i+1)*100/N)
    if i % tenPercent == 0:
        print("{0} {1:.0f}%".format(label, percent))


def singleSlitOpaqueWall(a, da):
    """ We return two lists: one with the space coordinates, one with the 
    amplitude at the corresponding coordinate. 
    Amplitude is zero outside of coordinates from aCoords. """

    Na = int(a/da)
    amplitude = (1/float(Na)) # normalized

    aCoords = [(j-Na/2)*da for j in range(Na+1)] # space coordinates
    amplitudes = [ amplitude for y in aCoords] # constant amplitude

    return (aCoords, amplitudes)

def gratingFromSingleSlit(aCoords, amplitudes, b, Nb):
    """ We repeat the provided amplitudes, every 'b' distance, Nb times.  This is
    therefore a "grating" """

    bCoords = [(j-Nb/2)*b for j in range(Nb)]

    gCoords = []
    gratingAmplitudes = []
    for x in bCoords:
        gCoords.extend([ x+y for y in aCoords])
        gratingAmplitudes.extend( [(A/Nb) for A in amplitudes] )

    return (gCoords, gratingAmplitudes)

def singleSlitWithLinearPhaseOpaqueWall(a, da, minPhase, maxPhase):
    """ We return the coordinates and amplitude of a single slit with a linear phase from
    minPhase (at x = 0) to maxPhase (at x = a).
    """
    (aCoords, amplitudes) = singleSlitOpaqueWall(a, da)

    phaseSlope = (maxPhase - minPhase)
    phaseIntercept = minPhase - phaseSlope*aCoords[0] # We want minPhase at aCoords[0]
    phaseMask = [ exp(-I * (phaseSlope*x + phaseIntercept) ) for x in aCoords] 
    maskedAmplitudes = np.multiply(amplitudes, phaseMask)

    return (aCoords, maskedAmplitudes)


if __name__ == "__main__":
    """ This code computes the diffraction pattern in the simplest way possible:
    by adding spherical ways from the diffraction objstacle. It is extremely
    inefficient and slow, but it is trivial to understand. """

    wavelength = 1
    k = 2*pi/wavelength


    # Common definition: Distance to screen
    R = 8000 # Distance source-screen in µm

    # Common definition: We sample as a function of theta every dTheta
    Y = 8000
    dY = 10
    Ny = int(Y/dY)
    screenCoords = [(j-(Ny-1)/2)*dY for j in range(Ny)]

    # First example: single slit
    a = 5
    da = 0.1
    (aCoords, amplitudes) = singleSlitOpaqueWall(a=5, da=0.1)
    Efield = diffraction(aCoords, amplitudes, k, R, screenCoords, progressMessage="Calculating single slit")
    showDiffractedIntensity(screenCoords, Efield,title="Figure: Profil à R={0} mm d'une fente de largeur a={1} µm".format(R/1000,a))
    envelope = abs(Efield*conjugate(Efield))

    # Second example: 2 slits separated by small distance (b-a)
    (aCoords, amplitudes) = singleSlitOpaqueWall(a=5, da=0.1)
    b = 10
    Nb = 2
    (gratingCoords, gratingAmplitudes) = gratingFromSingleSlit(aCoords, amplitudes, b=b, Nb=Nb)
    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calculating double slit")
    showDiffractedIntensity( screenCoords, Efield, envelope=envelope, title="Figure: Profil à R={0} mm de 2 fentes de largeur a=5 µm séparées par {1:d} µm".format(R/1000, b-a))

    # Third example: 10 slits separated by small distance (b-a)
    (aCoords, amplitudes) = singleSlitOpaqueWall(a=a, da=da)
    b = 10
    Nb = 10
    (gratingCoords, gratingAmplitudes) = gratingFromSingleSlit(aCoords, amplitudes, b=b, Nb=Nb)
    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calculating {0} slits".format(Nb))
    showDiffractedIntensity(screenCoords, Efield, envelope=envelope, title="Figure: Profil à R={0} mm de 10 fentes de largeur a=5 µm séparées par {1:d} µm".format(R/1000, b-a))

    # Fourth example: single slit with a linear phase mask from minPhase to maxPhase
    d = 0.2
    n = 1.5
    minPhase=k*d
    maxPhase=k*d*n
    (aCoords, amplitudes) = singleSlitWithLinearPhaseOpaqueWall(a=a, da=da, minPhase=minPhase, maxPhase=maxPhase)
    Efield = diffraction(aCoords, amplitudes, k, R, screenCoords, progressMessage="Calculating single slit with mask")
    showDiffractedIntensity(screenCoords, Efield,title="Figure: Profil à R={0} mm d'une fente de largeur a=5 µm\navec un masque de phase lineaire de {1:0.2f} rad à {2:0.2f} rad\nNotez le deplacement vers la droite.".format(R/1000, minPhase, maxPhase))

    # Fifth example: repeated slit from #4 with a linear phase mask from minPhase to maxPhase
    (aCoords, amplitudes) = singleSlitWithLinearPhaseOpaqueWall(a=a, da=da, minPhase=minPhase, maxPhase=maxPhase)
    (gratingCoords, gratingAmplitudes) = gratingFromSingleSlit(aCoords, amplitudes, b=10, Nb=5)
    envelope = abs(Efield*conjugate(Efield)) # The field from example #4 gives us the envelope

    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calculating grating with mask")
    showDiffractedIntensity(screenCoords, Efield, envelope=envelope, title="Figure: Profil à R={0} mm de 10 fentes de largeur a=5 µm\navec un masque de phase lineaire de {1:0.2f} rad à {2:0.2f} rad".format(R/1000, minPhase, maxPhase))

    # Sixth example: single slit, but in Fresnel zone (very close!)
    (aCoords, amplitudes) = singleSlitOpaqueWall(a, da)
    Rclose = 10
    screenCoordsClose = [(j-(Ny-1)/2)*dY/200 for j in range(Ny)]

    Efield = diffraction(aCoords, amplitudes, k, Rclose, screenCoordsClose, progressMessage="Calculating single slit")
    showDiffractedIntensity(screenCoordsClose, Efield,title="Figure: Profil dans le regime de Fresnel à R={0} µm d'une fente de largeur a={1} µm".format(Rclose,a))

    # Seventh example: single slit diffraction regime from fresnel (very close) to fraunhofer (very far)
    rCoords = [2,5,10,20,50,100]
    screenCoordsClose = [(j-Ny/2)*dY/30 for j in range(Ny)]
    fig, axes = createFigure()
    for idx,r in enumerate(rCoords):
        Efield = diffraction(aCoords, amplitudes, k, r, screenCoordsClose, progressMessage="Calculating single slit at distance r={0}".format(r))
        axes.plot(screenCoordsClose, abs(Efield*conjugate(Efield)), linewidth=1, label="Intensity at r={0}".format(r))
    axes.set(xlabel='Distance', ylabel='Intensite')
    axes.set_title("Figure: Transition de Fresnel a Fraunhofer".format(a,R/1000), ha='center',size=13)
    axes.legend()
    plt.show()


