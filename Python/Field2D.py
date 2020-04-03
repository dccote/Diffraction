from numpy import *
from matplotlib import pyplot as plt
from PIL import Image

I = complex(0,1)
class Field2D:
    def __init__(self, ds:float, wavelength=float, N:int = None, array2D:ndarray = None):
        self.dx = ds
        self.dy = ds
        self.wavelength= wavelength
        if array2D is None and N is not None:
            self.values = zeros((N, N),dtype=cdouble)
        elif array2D is not None and N is None:
            if array2D.dtype != cdouble:
                raise ValueError("Array must be complex")
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
        return self.dx*linspace(-N/2, N/2, num=N, endpoint=False)

    @property
    def y(self) -> float:
        (dummy,N) = self.values.shape
        return self.dy*linspace(-N/2, N/2, num=N, endpoint=False)

    def showIntensity(self):
        plt.imshow(Image.fromarray(real(self.values*conjugate(self.values))))
        plt.show()

    def showField(self):
        plt.imshow(Image.fromarray(abs(self.values)))
        plt.show()

    def showPhase(self):
        plt.imshow(Image.fromarray(angle(self.values)))
        plt.show()

    def propagate(self, distance:float):
        raise Error("Not Implemented")

    @classmethod
    def Gaussian(self, ds:float, N:int, width:float, wavelength:float, amplitude:float = 1.0):
        allXs = ds*linspace(-N/2, N/2, num=N, endpoint=False)
        allYs = ds*linspace(-N/2, N/2, num=N, endpoint=False)

        values = zeros((N, N),dtype=cdouble)
        for (i,x) in enumerate(allXs):
            for (j,y) in enumerate(allYs):
                values[i,j] = amplitude*exp(-(x*x+y*y)/(width*width))
        return Field2D(array2D=values, ds=ds, wavelength=wavelength)

if __name__ == "__main__":
    f = Field2D.Gaussian(width=10, amplitude=16.0, ds=0.1, N=1024, wavelength=2)
    f.showIntensity()
    f.showPhase()
    f.showField()
