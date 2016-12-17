################################################
#                                              #
#       Multiplication modulaire               #
#                                              #
# Par Erwan Dessailly et Colin Baumgard        #
#                                              #
################################################

import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import animation

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter.messagebox import *
import os


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
        self.zoneDeControleStatique = LabelFrame(self.zoneDeControle, text='Contrôle statiques')

                # label description:
        self.labelDescription = Label(self.zoneDeControleStatique, text='Table des a modulo')

                # spin a
        self.labelA = Label(self.zoneDeControleStatique, text='a:')
        self.valeurA = Spinbox(self.zoneDeControleStatique, from_=1, to_=1000, command=self.actualiser)
        self.valeurA.delete(0, 'end')
        self.valeurA.insert('end', 2)

                # spin mod
        self.labelMod = Label(self.zoneDeControleStatique, text='modulo:')
        self.valeurMod = Spinbox(self.zoneDeControleStatique, from_=1, to_=1000, command=self.actualiser)
        self.valeurMod.delete(0, 'end')
        self.valeurMod.insert('end', 20)

                #construction grille
        self.labelDescription.grid(row=0, column=0)

        self.labelA.grid(row=1, column=0)
        self.valeurA.grid(row=1, column=1)

        self.labelMod.grid(row=2, column=0)
        self.valeurMod.grid(row=2, column=1)


            #Zone de controle animation
        self.zoneDeControleAnimation = LabelFrame(self.zoneDeControle, text="Création d'animations")

                #Paramètres:

                    # de... à... par frequence de ...
        self.labelDe = Label(self.zoneDeControleAnimation, text='A variant de: ')
        self.spinDe = Spinbox(self.zoneDeControleAnimation, from_=1, to=1000, increment=10, command=self.verifier)
        self.spinDe.delete(0, 'end')
        self.spinDe.insert('end', 50)

        self.labelA = Label(self.zoneDeControleAnimation, text='à: ')
        self.spinA = Spinbox(self.zoneDeControleAnimation, from_=1, to=1000, increment=10, command=self.verifier)
        self.spinA.delete(0, 'end')
        self.spinA.insert('end', 200)

        self.labelDuree = Label(self.zoneDeControleAnimation, text="durée de l'animation(s): ")
        self.spinDuree = Spinbox(self.zoneDeControleAnimation, from_=1, to=50, increment=1)
        self.spinDuree.delete(0, 'end')
        self.spinDuree.insert('end', 10)


                # bouton de lancement
        self.lancerAnimation = Button(self.zoneDeControleAnimation, text="Générer l'animation", command=self.animation)

                # Témoin de calcul
        self.labelAvancement = Label(self.zoneDeControleAnimation, text='')

                #construction grille:

        self.labelDe.grid(row=0, column=0)
        self.spinDe.grid(row=0, column=1)
        self.labelA.grid(row=0, column=2)
        self.spinA.grid(row=0, column=3)

        self.labelDuree.grid(row=1, column=0)
        self.spinDuree.grid(row=1, column=1)

        self.lancerAnimation.grid(row=2, column=0, columnspan=2)
        self.labelAvancement.grid(row=2, column=2)


        #construction grille fenetre

        self.zoneGraphique.grid(row=0, column=0)
        self.zoneDeControleStatique.grid(row=0, column=0, padx=50)
        self.zoneDeControleAnimation.grid(row=0, column=1, padx=50)

        self.zoneDeControle.grid(row=1, column=0)





    def animation2(self):
        self.calculerFrequence()




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


    def verifier(self):

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

    def animation(self):

        showinfo('Animation', 'Le rendu peut prendre un peu de temps, soyez patient...')

        self.aLoop = 0
        self.modLoop = 200


        self.figureAnim = Figure(figsize=(10, 10), dpi=500)
        self.graphiqueAnim = self.figureAnim.add_subplot(111, projection='polar')
        self.canvasAnim = FigureCanvasTkAgg(self.figureAnim, self.zoneGraphique)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Colin Baumgard'), bitrate=10000)

        #with writer.saving(self.figureAnim, 'anim.mp4', 500):
         #   for i in range(3):
          #      self.genererAnimation()
           #     writer.grab_frame()


        anim = animation.FuncAnimation(self.figureAnim, self.genererAnimation, frames=150, interval=50, blit= False, repeat=False)
        anim.save('anim.mp4', writer=writer)


        os.system("explorer.exe /e,"+ os.getcwd())
        print("Témoin de passage animation")



    def genererAnimation(self, i):

        print("Témoin de passage generer animation")


        self.graphiqueAnim.clear()

        if self.modLoop != 0:
            delta = 2 * np.pi / self.modLoop
        else:
            delta = 0

        for b in range(0, self.modLoop):
            alpha = b * delta
            beta = ((self.aLoop * b) % self.modLoop) * delta

            self.graphiqueAnim.plot([alpha, beta], [1,1], c='b')

        self.aLoop = round(self.aLoop, 2) + 0.05

        return self.graphiqueAnim,




fenetre = Tk()
fenetre.title('MultiMod')
interface = Interface(fenetre)

interface.mainloop()
