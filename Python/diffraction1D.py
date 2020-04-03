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

def showDiffractedIntensity(screenCoordinates, Efields, envelope=None, title="", comment=""):
    fig, axes = createFigure()

    for Efield in Efields:
        axes.plot(screenCoordinates, abs(Efield*conjugate(Efield)), linewidth=1,label="Diffracted beam")

    if envelope is not None:
        axes.plot(screenCoordinates, envelope, linestyle=":", linewidth=1,label="Envelope")

    axes.set(xlabel='Position [µm]', ylabel='Intensite')
    axes.set_title(title, ha='center',size=13)
    axes.text(0.05,0.95, comment, size=10, va='top', bbox=dict(boxstyle="square", fc='w',ec='k', lw=1,ls=":"), transform=axes.transAxes)
    plt.show()


def reportProgress(i, N, label=""):
    """ i goes from 0 to N-1 """
    tenPercent = int(N/10)
    percent = int((i+1)*100/N)
    if i % tenPercent == 0:
        print("{0} {1:.0f}%".format(label, percent))


def sourceSingleSlitOpaqueWall(a, da):
    """ We return two lists: one with the space coordinates, one with the 
    amplitude at the corresponding coordinate. 
    Amplitude is zero outside of coordinates from aCoords. """

    Na = int(a/da)
    amplitude = (1/float(Na)) # normalized

    aCoords = [(j-Na/2)*da for j in range(Na+1)] # space coordinates
    amplitudes = [ amplitude for y in aCoords] # constant amplitude

    return (aCoords, amplitudes)

def sourcePeriodicSlitOpaqueWall(aCoords, amplitudes, b, Nb):
    """ We repeat the provided amplitudes, every 'b' distance, Nb times.  This is
    therefore a "grating" """

    bCoords = [(j-Nb/2)*b for j in range(Nb)]

    gCoords = []
    gratingAmplitudes = []
    for x in bCoords:
        gCoords.extend([ x+y for y in aCoords])
        gratingAmplitudes.extend( [(A/Nb) for A in amplitudes] )

    return (gCoords, gratingAmplitudes)

def sourceSingleSlitWithLinearPhaseOpaqueWall(a, da, minPhase, maxPhase):
    """ We return the coordinates and amplitude of a single slit with a linear phase from
    minPhase (at x = 0) to maxPhase (at x = a).
    """
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a, da)

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
    R = 12000 # Distance source-screen in µm

    # Common definition: We calculate on a screen of size Y
    Y = 12000
    dY = 10
    Ny = int(Y/dY)
    screenCoords = [(j-(Ny-1)/2)*dY for j in range(Ny)]

    # First example: single slit
    a = 5
    da = 0.1
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a=5, da=0.1)
    Efield = diffraction(aCoords, amplitudes, k, R, screenCoords, progressMessage="Calcul fente simple")
    showDiffractedIntensity(screenCoords, [Efield],title="Figure: Profil à R={0} mm d'une fente de largeur a={1} µm".format(R/1000,a))
    envelope = abs(Efield*conjugate(Efield))

    # Second example: 2 slits separated by small distance (b-a)
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a=5, da=0.1)
    b = 10
    Nb = 2
    (gratingCoords, gratingAmplitudes) = sourcePeriodicSlitOpaqueWall(aCoords, amplitudes, b=b, Nb=Nb)
    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calcul fente double")
    showDiffractedIntensity( screenCoords, [Efield], envelope=envelope, 
        title="Figure: Profil à R={0} mm de 2 fentes de largeur a=5 µm séparées par {1:d} µm".format(R/1000, b-a),
        comment="Notez l'interference entre les {0} fentes\net l'enveloppe générale correspondant\nà une seule fente".format(Nb))

    # Third example: 10 slits separated by small distance (b-a)
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a=a, da=da)
    b = 10
    Nb = 10
    (gratingCoords, gratingAmplitudes) = sourcePeriodicSlitOpaqueWall(aCoords, amplitudes, b=b, Nb=Nb)
    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calcul {0} fentes".format(Nb))
    showDiffractedIntensity(screenCoords, [Efield], envelope=envelope, 
        title="Figure: Profil à R={0} mm de 10 fentes de largeur a=5 µm séparées par {1:d} µm".format(R/1000, b-a),
        comment="Notez l'interference plus mince entre\nles {0} fentes encore sous l'enveloppe\ngénérale correspondant à une\nseule fente".format(Nb))

    # Fourth example: single slit with a linear phase mask from minPhase to maxPhase
    d = 0.2
    n = 1.5
    minPhase=k*d
    maxPhase=k*d*n
    (aCoords, amplitudes) = sourceSingleSlitWithLinearPhaseOpaqueWall(a=a, da=da, minPhase=minPhase, maxPhase=maxPhase)
    Efield = diffraction(aCoords, amplitudes, k, R, screenCoords, progressMessage="Calcul fente simple avec masque")
    showDiffractedIntensity(screenCoords, [Efield],
        title="Figure: Profil à R={0} mm d'une fente de largeur a=5 µm\navec un masque de phase lineaire de {1:0.2f} rad à {2:0.2f} rad".format(R/1000, minPhase, maxPhase),
        comment="Notez le déplacement vers la droite\ndu patron de diffraction, dû à la phase\nlinéaire sur la fente")

    # Fifth example: grating of slits from #4 with a linear phase mask from minPhase to maxPhase
    (aCoords, amplitudes) = sourceSingleSlitWithLinearPhaseOpaqueWall(a=a, da=da, minPhase=minPhase, maxPhase=maxPhase)
    (gratingCoords, gratingAmplitudes) = sourcePeriodicSlitOpaqueWall(aCoords, amplitudes, b=10, Nb=5)
    envelope = abs(Efield*conjugate(Efield)) # The field from example #4 gives us the envelope
    Efield = diffraction(gratingCoords, gratingAmplitudes, k, R, screenCoords, progressMessage="Calcul reseau de fentes simples avec masque")
    showDiffractedIntensity(screenCoords, [Efield], envelope=envelope, 
        title="Figure: Profil à R={0} mm de 10 fentes de largeur a=5 µm\navec un masque de phase lineaire de {1:0.2f} rad à {2:0.2f} rad".format(R/1000, minPhase, maxPhase),
        comment="Notez le déplacement vers la droite\ndu patron de diffraction, dû à la phase\nlinéaire sur chaque fente. Maintenant,\nl'ordre 1 est maximum plutôt que l'ordre 0.")

    # Sixth example: single slit, but in Fresnel zone (very close!)
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a, da)
    Rclose = 10
    screenCoordsClose = [(j-(Ny-1)/2)*dY/200 for j in range(Ny)]
    Efield = diffraction(aCoords, amplitudes, k, Rclose, screenCoordsClose, progressMessage="Calcul fente simple, zone de Fresnel")
    showDiffractedIntensity(screenCoordsClose, [Efield],
        title="Figure: Profil dans le regime de Fresnel à R={0} µm d'une fente de largeur a={1} µm".format(Rclose,a),
        comment="Le patron de diffraction d'une fente\nrectangulaire n'est pas un sinc(x)\ndans le champ proche.")

    # Seventh example: single slit diffraction regime from fresnel (very close) to fraunhofer (very far)
    rCoords = [2,5,10,20,50,100]
    screenCoordsClose = [(j-Ny/2)*dY/60 for j in range(Ny)]
    fig, axes = createFigure()
    for idx,r in enumerate(rCoords):
        Efield = diffraction(aCoords, amplitudes, k, r, screenCoordsClose, progressMessage="Calculating single slit at distance r={0}".format(r))
        axes.plot(screenCoordsClose, abs(Efield*conjugate(Efield)), linewidth=1, label="Intensité à r={0}".format(r))
    axes.set(xlabel='Distance', ylabel='Intensite')
    axes.set_title("Figure: Transition de Fresnel a Fraunhofer", ha='center',size=13)
    axes.legend()
    plt.show()


    # Eighth example: 10 slits separated by small distance (b-a), multiple wavelengths
    (aCoords, amplitudes) = sourceSingleSlitOpaqueWall(a=a, da=da)
    b = 10
    Nb = 10
    R = 12000
    (gratingCoords, gratingAmplitudes) = sourcePeriodicSlitOpaqueWall(aCoords, amplitudes, b=b, Nb=Nb)
    Efield1 = diffraction(gratingCoords, gratingAmplitudes, 2*pi/1, R, screenCoords, progressMessage="Calcul {0} fentes".format(Nb))
    Efield2 = diffraction(gratingCoords, gratingAmplitudes, 2*pi/1.1, R, screenCoords, progressMessage="Calcul {0} fentes".format(Nb))
    Efield3 = diffraction(gratingCoords, gratingAmplitudes, 2*pi/1.2, R, screenCoords, progressMessage="Calcul {0} fentes".format(Nb))
    showDiffractedIntensity(screenCoords, [Efield1, Efield2, Efield3], 
        title="Figure: Profils à différentes longueurs d'onde, fente de a=5 µm séparées par {1:d} µm".format(R/1000, b-a),
        comment="Notez qu'à l'ordre 0, il y a superposition.\nÀ l'ordre 1, il y a séparation des couleurs.".format(Nb))
