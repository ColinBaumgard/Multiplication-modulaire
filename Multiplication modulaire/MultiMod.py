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
from tkinter.messagebox import *
import os
from threading import Thread
import time


class AnimGenerator(Thread):

    def __init__(self, interface):
        Thread.__init__(self)
        self.interface = interface
        self.quit = False

    def run(self):
        while not self.quit:
            time.sleep(0.1)

    def draw(self):

        self.interface.lancerAnimation.config(state=DISABLED)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=self.interface.imageParSeconde, metadata=dict(artist='Colin Baumgard'), bitrate=10000)

        with writer.saving(self.interface.figure, "Animation.mp4", 500):

            for i in range(0, self.interface.nbDeFrames):
                self.loopAnim()
                self.interface.canvas.show()
                writer.grab_frame()
                self.interface.textAvancement.set("Calcul: " + str(i + 1) + "/" + str(self.interface.nbDeFrames))


        os.system("explorer.exe /e," + os.getcwd())
        self.interface.lancerAnimation.config(state=NORMAL)

    def loopAnim(self):
        self.interface.graphique.clear()
        self.interface.figure.suptitle(('Table de {} \nmodulo {}'.format(round(self.interface.aLoop, 2), self.interface.modLoop)))
        self.interface.graphique.grid(False)
        self.interface.graphique.axis([0, 1, 0, 1], )
        self.interface.graphique.set_xticklabels([])
        self.interface.graphique.set_yticklabels([])

        if self.interface.modLoop != 0:
            delta = 2 * np.pi / self.interface.modLoop
        else:
            delta = 0

        for b in range(0, self.interface.modLoop):
            alpha = b * delta
            beta = ((self.interface.aLoop * b) % self.interface.modLoop) * delta

            self.interface.graphique.plot([alpha, beta], [1,1], c='b')

        self.interface.aLoop = round(self.interface.aLoop, 2) + self.interface.pas

        return self.interface.graphique,

    def stop(self):
        self.quit = True



class Interface(Frame):

    def __init__(self, fenetre, **kwargs):

        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.animGenerator = AnimGenerator(self)
        self.animGenerator.start()


        self.imageParSeconde = 12

        #self.atest = 0
        #self.idImage = 0


        self.fenetre = fenetre

        # variables globales

        # Zone de graphique:
        self.zoneGraphique = Frame(self.fenetre)

        self.figure = Figure(figsize=(7, 7), dpi=100)
        self.graphique = self.figure.add_subplot(111, projection='polar')
        self.graphique.grid(False)
        self.graphique.axis([0, 1, 0, 1], )
        self.graphique.set_xticklabels([])
        self.graphique.set_yticklabels([])


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
        self.spinDe.insert('end', 2)

        self.labelA = Label(self.zoneDeControleAnimation, text='à: ')
        self.spinA = Spinbox(self.zoneDeControleAnimation, from_=1, to=1000, increment=10, command=self.verifier)
        self.spinA.delete(0, 'end')
        self.spinA.insert('end', 5)

        self.labelDuree = Label(self.zoneDeControleAnimation, text="durée(s): ")
        self.spinDuree = Spinbox(self.zoneDeControleAnimation, from_=1, to=50, increment=1)
        self.spinDuree.delete(0, 'end')
        self.spinDuree.insert('end', 10)

        self.labelMod = Label(self.zoneDeControleAnimation, text="modulo: ")
        self.spinMod = Spinbox(self.zoneDeControleAnimation, from_=1, to=1000, increment=1)
        self.spinMod.delete(0, 'end')
        self.spinMod.insert('end', 200)


                # bouton de lancement
        self.lancerAnimation = Button(self.zoneDeControleAnimation, text="Générer l'animation", command=self.animation)

                # Témoin de calcul
        self.textAvancement = StringVar()
        self.labelAvancement = Label(self.zoneDeControleAnimation, textvariable=self.textAvancement)

                # construction grille:

        self.labelDe.grid(row=0, column=0)
        self.spinDe.grid(row=0, column=1)
        self.labelA.grid(row=0, column=2)
        self.spinA.grid(row=0, column=3)


        self.labelMod.grid(row=1, column=0)
        self.spinMod.grid(row=1, column=1)
        self.labelDuree.grid(row=1, column=2)
        self.spinDuree.grid(row=1, column=3)

        self.lancerAnimation.grid(row=2, column=0, columnspan=2)
        self.labelAvancement.grid(row=2, column=2)


        #construction grille fenetre

        self.zoneGraphique.grid(row=0, column=0)
        self.zoneDeControleStatique.grid(row=0, column=0, padx=50)
        self.zoneDeControleAnimation.grid(row=0, column=1, padx=50)

        self.zoneDeControle.grid(row=1, column=0)

        self.actualiser()



    def actualiser(self):

        a = float(self.valeurA.get())
        mod = int(self.valeurMod.get())

        self.afficher(a, mod)


    def afficher(self, a, mod):

        self.graphique.clear()
        self.figure.suptitle(('Table de {} \nmodulo {}'.format(round(a, 2), mod)))


        if mod != 0:
            delta = 2 * np.pi / mod
        else:
            delta = 0


        for b in range(0, mod):

            alpha = b * delta
            beta = ((a * b) % mod) * delta

            self.graphique.plot([alpha, beta], [1, 1], c='r')
            self.graphique.grid(False)
            self.graphique.axis([0,1,0,1], )
            self.graphique.set_xticklabels([])
            self.graphique.set_yticklabels([])

        self.canvas.show()



    ###### Fonctions tests Colin ######


    def verifier(self):

        if float(self.spinDe.get()) > float(self.spinA.get()):
            self.spinA.delete(0, 'end')
            self.spinA.insert('end', float(self.spinDe.get()))



    def animation(self):

        self.verifier()

        self.aLoop = float(self.spinDe.get())
        self.modLoop = int(self.spinMod.get())
        limite = float(self.spinA.get())
        duree = float(self.spinDuree.get())

        self.nbDeFrames = int(self.imageParSeconde * duree)

        delta = limite - self.aLoop

        self.pas = round(delta / self.nbDeFrames, 3)

        if askyesno('Animation', 'Récapitulatif:\n'
                                 '- A variant de {} à {} modulo {}\n'
                                 '- Durée: {}s\n'
                                 '- Nombre de calcul: {}\n'
                                 '- Temps max estimé: {}min\n'
                                 'Voulez vous lancer la simulation ?'.format(self.aLoop, limite, self.modLoop, duree, self.nbDeFrames, round((self.nbDeFrames*1.5)/60, 2))):

            self.animGenerator.draw()


    def stop(self):
        self.animGenerator.stop()




fenetre = Tk()
fenetre.title('MultiMod')
interface = Interface(fenetre)

interface.mainloop()

interface.stop()
