import numpy as np 
from scipy.optimize import curve_fit
import matplotlib.pyplot

def func(x, a, b):
	return a * x + b

x = np.linspace(0, 10, 100)

y = func(x, 1, 5)

yn = y + 0.9 * np.random.normal(size=len(x))

popt, pcov = curve_fit(func, x, yn)

print x
print y
print yn

print popt
print pcov

matplotlib.pyplot.plot(x,y)
matplotlib.pyplot.plot(x,yn)
matplotlib.pyplot.scatter(x, y)
matplotlib.pyplot.show()