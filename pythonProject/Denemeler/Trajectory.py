from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

datafile = "ClusteredKeyboardPlayer3372trial1.npy"
image_file = "png"
data_array = np.load(datafile)
duration= data_array[:,0]
xpos = data_array[:, 1]
ypos = data_array[:, 2]
plt.plot(xpos[0],ypos[0],"ko")
plt.scatter(xpos,ypos,s=0.5,c=duration,cmap="plasma")
plt.plot(xpos[-1], ypos[-1],"ro")
filename = "Plots/" + datafile.replace("npy", image_file)
plt.title(filename)
#plt.show()
plt.savefig(filename)


