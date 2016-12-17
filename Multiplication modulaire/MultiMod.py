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
from matplotlib import animation

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *



class Interface(Frame):

    def __init__(self, fenetre, **kwargs):

        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.imagePasSeconde = 12

        self.atest = 0
        self.idImage = 0


        self.fenetre = fenetre

        # variables globales

        self.a = DoubleVar()
        self.mod = DoubleVar()


        # Zone de graphique:
        self.zoneGraphique = Frame(self.fenetre)

        self.figure = Figure(figsize=(7, 7), dpi=100)
        self.graphique = self.figure.add_subplot(111, projection='polar')

        self.canvas = FigureCanvasTkAgg(self.figure, self.zoneGraphique)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()



        # Interface de contrôle
        self.zoneDeControle = Frame(self.fenetre)


            #zoneControleStatique
        self.zoneDeControleStatique = Frame(self.zoneDeControle)

                # Scrollbar a
        self.labelA = Label(self.zoneDeControleStatique, text='a')
        self.scaleA = Scale(self.zoneDeControleStatique, variable=self.a, orient='horizontal', command=self.actualiser)

                # Scrollbar mod
        self.labelMod = Label(self.zoneDeControleStatique, text='modulo')
        self.scaleMod = Scale(self.zoneDeControleStatique, variable=self.mod, orient='horizontal', command=self.actualiser)

                #construction grille
        self.labelA.grid(row=0, column=0)
        self.scaleA.grid(row=0, column=1)

        self.labelMod.grid(row=1, column=0)
        self.scaleMod.grid(row=1, column=1)


            #Zone de controle animation
        self.zoneDeControleAnimation = Frame(self.zoneDeControle, bd=2)

                #Paramètres:
                    #on fait varier mod ou a:
        self.choix = StringVar()
        self.choix.set('a')
        self.boutonA = Radiobutton(self.zoneDeControleAnimation, text='a', variable=self.choix, value="a")
        self.boutonMod = Radiobutton(self.zoneDeControleAnimation, text='modulo', variable=self.choix, value="mod")


                    # de... à... par frequence de ...
        self.labelDe = Label(self.zoneDeControleAnimation, text='De: ')
        self.spinDe = Spinbox(self.zoneDeControleAnimation, from_=1, to=100, increment=10, command=self.calculerFrequence)
        self.labelA = Label(self.zoneDeControleAnimation, text='à: ')
        self.spinA = Spinbox(self.zoneDeControleAnimation, from_=1, to=300, increment=10, command=self.calculerFrequence)

        self.labelFrequence = Label(self.zoneDeControleAnimation, text='frequence: ')
        self.spinFrequence = Spinbox(self.zoneDeControleAnimation, from_=0.0001, to=100, increment=0.05, command=self.calculerDuree)
        self.labelDuree = Label(self.zoneDeControleAnimation, text='durée: ')
        self.spinDuree = Spinbox(self.zoneDeControleAnimation, from_=1, to=20, increment=1, command=self.calculerFrequence)

        self.calculerFrequence()


                # bouton de lancement
        self.lancerAnimation = Button(self.zoneDeControleAnimation, text="Lancer", command=self.animTest)

                #construction grille:
        self.boutonA.grid(row=0, column=1)
        self.boutonMod.grid(row=0, column=2)

        self.labelDe.grid(row=1, column=0)
        self.spinDe.grid(row=1, column=1)
        self.labelA.grid(row=1, column=2)
        self.spinA.grid(row=1, column=3)

        self.labelFrequence.grid(row=2, column=0)
        self.spinFrequence.grid(row=2, column=1)
        self.labelDuree.grid(row=2, column=2)
        self.spinDuree.grid(row=2, column=3)

        self.lancerAnimation.grid(row=3, column=1, columnspan=2)


        #construction grille fenetre

        self.zoneGraphique.grid(row=0, column=0)
        self.zoneDeControleStatique.grid(row=0, column=0, padx=50)
        self.zoneDeControleAnimation.grid(row=0, column=1, padx=50)

        self.zoneDeControle.grid(row=1, column=0)





    def animation(self):
        self.calculerFrequence()

        self.animTemp()



    def actualiser(self, adsf):

        # self.a += 1
        a = int(self.a.get())
        mod = int(self.mod.get())

        self.afficher(a, mod)


    def afficher(self, a, mod):

        self.graphique.clear()


        if mod != 0:
            delta = 2 * np.pi / mod
        else:
            delta = 0


        for b in range(0, mod):

            alpha = b * delta
            beta = ((a * b) % mod) * delta

            self.graphique.plot([alpha, beta], [1, 1], c='r')

        self.canvas.show()

        self.canvas.get_tk_widget().pack()


    ###### Fonctions tests Colin ######


    def calculerFrequence(self):

        duree = float(self.spinDuree.get())

        nbDeframe = duree*self.imagePasSeconde
        min = float(self.spinDe.get())
        max = float(self.spinA.get())


        self.spinFrequence.delete(0, 'end')
        self.spinFrequence.insert('end', str((round(((max - min)/nbDeframe), 3))))

    def calculerDuree(self):

        frequence = float(self.spinFrequence.get())
        min = float(self.spinDe.get())
        max = float(self.spinA.get())

        self.spinDuree.delete(0, 'end')
        self.spinDuree.insert(0, str((round((max - min) / (frequence * self.imagePasSeconde), 3))))

    def animTest(self):

        matplotlib.use("Agg")
        self.aLoop = 0
        self.modLoop = 200

        self.iMax = 0
        self.listeFrames = []
        self.done = False
        #self.line, = self.graphique.plot([0, 0], [1,1])


        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)



        anim = animation.FuncAnimation(self.figure, self.afficher2, 25, interval=50, repeat=True)
        anim.save('anim.mp4', writer=writer)

        self.listeFrames = []

        #self.canvas.show()
        #self.canvas.get_tk_widget().pack()
        matplotlib.use("TkAgg")


    def afficher2(self, i):


        self.graphique.clear()

        if self.modLoop != 0:
            delta = 2 * np.pi / self.modLoop
        else:
            delta = 0

        for b in range(0, self.modLoop):
            alpha = b * delta
            beta = ((self.aLoop * b) % self.modLoop) * delta

            self.graphique.plot([alpha, beta], [1,1], c='b')

        self.aLoop = round(self.aLoop, 2) + 0.05

        return self.graphique,

    def afficher3(self, i):

        print(len(self.listeFrames), ' >? ', i)

        if not self.done:

            self.listeFrames.append(self.figure.add_subplot(111, projection='polar'))
            self.listeFrames[i].clear()

            if self.modLoop != 0:
                delta = 2 * np.pi / self.modLoop
            else:
                delta = 0

            for b in range(0, self.modLoop):
                alpha = b * delta
                beta = ((self.aLoop * b) % self.modLoop) * delta

                self.listeFrames[i].plot([alpha, beta], [1, 1], c='b')

            self.aLoop = round(self.aLoop, 2) + 0.05

            if i < self.iMax:
                self.done = True
            else:
                self.iMax = i

        return self.listeFrames[i],



fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
