#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################
#                                              #
#       Multiplication modulaire               #
#                                              #
# Par Erwan Dessailly et Colin Baumgard        #
#                                              #
################################################

# import des modules de matplotlib
import matplotlib
matplotlib.use('TkAgg')  # on initialise le backend de matplotlib pour l'utiliser avec tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import animation

import numpy as np


from tkinter import *
from tkinter.messagebox import *

import os
from threading import Thread
import time

import logging
from logging.handlers import RotatingFileHandler

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)


class AnimGenerator(Thread):
    # Cet objet nous permet de lancer la generation de l'animation sur un thread et donc de ne pas bloquer le programme

    def __init__(self, interface):

        logger.info('Initialisation du thread AnimGenerator')

        Thread.__init__(self)
        self.setDaemon(True)  # on définie le thread comme deamon (le programme s'arrete si il ne reste que des deamons)
        self.interface = interface  # on récupère le 'lien' vers l'objet parent pour pouvoir récuperer des infos

        self.generate = False

    def run(self):
        logger.info('Lancement du thread AnimGenerator')
        while 1:
            if self.generate:
                self.draw()
                self.generate = False
            else:
                time.sleep(0.1)

    def draw(self):

        logger.info('Appel de la foonction draw du thread AnimGenerator')

        self.interface.lancerAnimation.config(state=DISABLED)

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=self.interface.imageParSeconde, metadata=dict(artist='Colin Baumgard'), bitrate=10000)

        with writer.saving(self.interface.figure, "Animation.mp4", 500):
            logger.info('Debut de la boucle de generation de la fonction draw du thread AnimGenerator')

            for i in range(0, self.interface.nbDeFrames):
                self.loopAnim()
                self.interface.canvas.show()
                writer.grab_frame()
                self.interface.textAvancement.set("Calcul: " + str(i + 1) + "/" + str(self.interface.nbDeFrames))

            logger.info('Fin de la boucle de generation de la fonction draw du thread AnimGenerator')


        os.system("explorer.exe /e," + os.getcwd())
        self.interface.lancerAnimation.config(state=NORMAL)

        logger.info('Fin de la fonction draw du thread AnimGenerator')


    def loopAnim(self):
        self.interface.graphique.clear()
        self.interface.figure.suptitle(('Table de {} \nmodulo {}'.format(round(self.interface.aLoop, 2), self.interface.modLoop)))
        self.interface.graphique.grid(False)
        self.interface.graphique.axis([0, 1, 0, 1], )
        self.interface.graphique.set_xticklabels([])
        self.interface.graphique.set_yticklabels([])

        red, green, blue = 215 / 255, 0, 86 / 255

        if self.interface.modLoop != 0:
            delta = 2 * np.pi / self.interface.modLoop
            delta_color = 1 / self.interface.modLoop
        else:
            delta = 0
            delta_color = 0

        for b in range(0, self.interface.modLoop):
            alpha = b * delta
            beta = ((self.interface.aLoop * b) % self.interface.modLoop) * delta

            self.interface.graphique.plot([alpha, beta], [1,1], c=[red, green, blue])
            green += delta_color

        self.interface.aLoop = round(self.interface.aLoop, 2) + self.interface.pas

        return self.interface.graphique,

    def setGenerate(self):
        self.generate = True

class Fenetre(Frame):

    def __init__(self, fenetre, **kwargs):

        logger.info('Initialisation de l interface')


        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        # variables globales

        self.animGenerator = AnimGenerator(self) # création de l'objet pour l'animation
        self.animGenerator.start() # on lance le thread qui est maintenant prêt à travailler

        self.imageParSeconde = 12 # constante
        self.fenetre = fenetre

        #Construction graphique:

        # Zone de graphique:
        self.zoneGraphique = Frame(self.fenetre)

        self.figure = Figure(figsize=(5, 5), dpi=100)
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
        self.zoneDeControleStatique = LabelFrame(self.zoneDeControle, text='Contrôles statiques')

                # label description:
        self.labelDescription = Label(self.zoneDeControleStatique, text='Table des a modulo')

                # spin a
        self.labelA = Label(self.zoneDeControleStatique, text='a:')
        self.valeurA = Spinbox(self.zoneDeControleStatique, from_=1, to_=1000, command=self.afficher)
        self.valeurA.delete(0, 'end')
        self.valeurA.insert('end', 2)

                # spin mod
        self.labelMod = Label(self.zoneDeControleStatique, text='modulo:')
        self.valeurMod = Spinbox(self.zoneDeControleStatique, from_=1, to_=1000, command=self.afficher)
        self.valeurMod.delete(0, 'end')
        self.valeurMod.insert('end', 20)

                #construction grille
        self.labelDescription.grid(row=0, column=0)

        self.labelA.grid(row=1, column=0)
        self.valeurA.grid(row=1, column=1)

        self.labelMod.grid(row=2, column=0)
        self.valeurMod.grid(row=2, column=1)


            # Zone de controle animation
        self.zoneDeControleAnimation = LabelFrame(self.zoneDeControle, text="Création d'animations")

                # Paramètres:

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

        self.afficher()

        logger.info("Fin d'initialisation de l'interface")




    def afficher(self):

        a = float(self.valeurA.get())
        mod = int(self.valeurMod.get())

        self.graphique.clear()
        self.figure.suptitle(('Table de {} \nmodulo {}'.format(round(a, 2), mod)))

        red, green, blue = 62/255, 103/255, 235/255
        red_fin, green_fin, blue_fin = 250/255, 16/255, 87/255



        if mod != 0:
            delta = 2 * np.pi / mod
            delta_red = (red_fin - red)/mod
            delta_green = (green_fin - green) / mod
            delta_blue = (blue_fin - blue) / mod

        else:
            delta = 0
            delta_red = 0
            delta_green = 0
            delta_blue = 0


        for b in range(0, mod):

            alpha = b * delta
            beta = ((a * b) % mod) * delta

            self.graphique.plot([alpha, beta], [1, 1], c=[red, green, blue])
            self.graphique.grid(False)
            self.graphique.axis([0, 1, 0, 1], )
            self.graphique.set_xticklabels([])
            self.graphique.set_yticklabels([])

            red += delta_red
            green += delta_green
            blue += delta_blue

        self.canvas.show()



    def verifier(self):

        if float(self.spinDe.get()) > float(self.spinA.get()):
            self.spinA.delete(0, 'end')
            self.spinA.insert('end', float(self.spinDe.get()))



    def animation(self):

        logger.info("Demande de lancement de la génératin de l'animation")

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
                                 'Voulez vous lancer la simulation ?'
                                 ''.format(self.aLoop, limite, self.modLoop, duree, self.nbDeFrames, round((self.nbDeFrames*1.5)/60, 2))):

            #self.animGenerator.draw()
            self.animGenerator.setGenerate()

        logger.info("Fin de la génération de l'animation (Objet Interafce)")




fenetre = Tk()
fenetre.title('MultiMod')
interface = Fenetre(fenetre)

interface.mainloop()
