from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

# Beaucoup d'information sur la gestion d'image pour calculs en Python ici
# https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

image = Image.open("arbitraire.tif")
imageData = np.asarray(image,dtype=np.float64)    # Convertit en point-flottant
imageData = np.fft.fft2(imageData)                # Transformee de Fourier 2D
imageData = np.abs(np.fft.fftshift(imageData))**2 # Puissance reelle

normalization = np.max(imageData)                 # Pour normaliser
intensityFactor = 10000                           # Pour voir les ailes

imageData = imageData/normalization*intensityFactor
plt.imshow(Image.fromarray(imageData))
plt.show()


