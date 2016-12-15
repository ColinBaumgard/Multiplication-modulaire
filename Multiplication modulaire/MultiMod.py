################################################
#                                              #
#       Multiplication modulaire               #
#                                              #
# Par Erwan Dessailly et Colin Baumgard        #
#                                              #
################################################

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


class Interface(Frame):

    def __init__(self, fenetre, **kwargs):

        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        # self.pack(fill=BOTH)

        self.fenetre = fenetre

        # variable globales

        self.a = DoubleVar()
        self.mod = DoubleVar()


        # Zone de graphique:
        self.zoneGraphique = Frame(self.fenetre)


        self.figure = Figure(figsize=(7,7), dpi=100)
        self.graphique = self.figure.add_subplot(111, projection='polar')
        self.graphique.plot(1,1)


        self.canvas = FigureCanvasTkAgg(self.figure, self.zoneGraphique)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()

        self.zoneGraphique.grid(row=0, column=0)


        # Interface de contrôle

        self.zoneDeControle = Frame(self.fenetre)

        # Scrollbar a
        labelA = Label(self.zoneDeControle, text='a')
        labelA.grid(row=0, column=0)
        scaleA = Scale(self.zoneDeControle, variable=self.a, orient='horizontal', command=self.actualiser)
        scaleA.grid(row=0, column=1)

        # Scrollbar mod
        labelMod = Label(self.zoneDeControle, text='modulo')
        labelMod.grid(row=1, column=0)
        scaleMod = Scale(self.zoneDeControle, variable=self.mod, orient='horizontal', command=self.actualiser)
        scaleMod.grid(row=1, column=1)

        self.zoneDeControle.grid(row=1, column=0)


    def actualiser(self, adsf):

        # self.a += 1
        a = int(self.a.get())
        mod = int(self.mod.get())

        self.afficher(a, mod)

    def calculModulo(self, a, p):
        l = []
        for b in range(0, p):
            l.append([b, (a * b) % p])
        return l

    def afficher(self, a, mod):

        listeCouples = self.calculModulo(a, mod)

        self.graphique.clear()


        nPoints = mod
        nCouples = len(listeCouples)

        if mod != 0:
            delta = 2 * np.pi / nPoints
        else:
            delta = 0

        for i in range(0, nCouples):
            alpha = listeCouples[i][0] * delta
            beta = listeCouples[i][1] * delta

            self.graphique.plot([alpha, beta], [1, 1], c='r')

        self.canvas.show()

        self.canvas.get_tk_widget().pack()


fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()