import numpy as np 
from matplotlib import pyplot as plt
from PIL import Image

class Field2D:
    def __init__(self, ds:float, wavelength=float, N:int = None, array2D:np.ndarray = None):
        self.dx = ds
        self.dy = ds
        self.wavelength= wavelength
        if array2D is None and N is not None:
            self.values = np.zeros((N, N))
        elif array2D is not None and N is None:
            self.values = array2D
        else:
            raise ValueError("You must provide either the number of points N or an array")

    def __eq__(self, rhs):
        self.values = rhs.values
        self.dx = rhs.dx
        self.dy = rhs.dy

    @property
    def x(self) -> float:
        (N,dummy) = self.values.shape
        return self.dx*np.linspace(-N/2, N/2, num=N, endpoint=False)

    @property
    def y(self) -> float:
        (dummy,N) = self.values.shape
        return self.dy*np.linspace(-N/2, N/2, num=N, endpoint=False)

    def display(self):
        plt.imshow(Image.fromarray(self.values))
        plt.show()

    def setGaussian(self, width:float, amplitude:float = 1.0):
        for (i,x) in enumerate(self.x):
            for (j,y) in enumerate(self.y):
                self.values[i,j] = amplitude*np.exp(-(x*x+y*y)/(width*width))


if __name__ == "__main__":
    f=Field2D(ds=0.1, N=1024)
    f.setGaussian(width=10, amplitude=255.0)
    g = f
    g.display()
    g.setGaussian(width=20, amplitude=255.0)
    g.display()
