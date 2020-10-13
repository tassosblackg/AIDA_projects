import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-2, 2,0.005)

y = np.power(x,2)

plt.figure(1)
plt.plot(x,y)
plt.xlabel('x values in [-19:20],step=0.05')
plt.ylabel('y(x^2)')
plt.title(' Plot of x^2')
plt.show()
