from PIL import Image
import numpy as np
from matplotlib import pyplot

# Beaucoup d'information sur la gestion d'image pour calculs en Python ici
# https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

# load image as pixel array
image = Image.open("/tmp/test.png")
# summarize shape of the pixel array
# display the array of pixels as an image
pyplot.imshow(image)
pyplot.show()

imageData = np.asarray(image)
imageData = np.fft.fft2(imageData)
imageData = np.fft.fftshift(imageData)

pyplot.imshow(Image.fromarray(imageData))
pyplot.show()
