################################################
#                                              #
#       Multiplication modulaire               #
#                                              #
# Par Erwan Dessailly et Colin Baumgard        #
#                                              #
################################################


import matplotlib.pyplot as plt
import numpy as np


def calculModulo(a, p):
    l = []
    for b in range(0,p):
        l.append([b, (a*b)%p])
    print(l)
    return l


a = 2
mod = 100

listeCouples = calculModulo(a,mod)

ax = plt.subplot(111, projection='polar')

nPoints = mod
nCouples = len(listeCouples)

delta = 2*np.pi/nPoints

for i in range(0, nCouples):
        alpha = listeCouples[i][0]*delta
        beta = listeCouples[i][1]*delta
        print(alpha, beta)

        ax.plot([alpha, beta], [1,1])



plt.show()
