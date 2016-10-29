# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 19:16:21 2016

@author: Pierre
"""
from tkinter import *

class noeud():
    def __init__(self, x, y):
        self.parent = self
        self.colonne = x
        self.ligne = y
        self.coutF = 0
        self.coutG = 0
        self.coutH = 0

    
class representationGrille(Canvas):
    def __init__(self,master, nombreLignes, nombreColonnes, tailleCase, *args, **kwargs):
        #*args: plusieurs arguments taille à souhait
        #**keywordargs: plusieur argument dictionaire taille à souhait
        self.master = master
        self.tailleCase = tailleCase
        self.nombreLignes = nombreLignes
        self.nombreColonnes = nombreColonnes

        # Creation de la zone de dessin canvas(.tk), attention il faut rajouter 1 pixel pour les lignes de bordure en bas et a droite :
        Canvas.__init__(self, master, width = (tailleCase*nombreColonnes)+1, height = (tailleCase*nombreLignes)+1, highlightthickness=0, *args, **kwargs)    
        # Creation de la grille vide:
        for i in range(nombreColonnes*tailleCase):
            self.create_line(0,i*tailleCase,nombreColonnes*tailleCase,i*tailleCase,fill='black')
        for j in range(nombreLignes*tailleCase):
            self.create_line(j*tailleCase,0,j*tailleCase,nombreLignes*tailleCase,fill='black')
        #Creation de la liste des cases représentées:    
        self.case=[]
        for ligne in range(nombreLignes):
            self.case.append([])
            for colonne in range(nombreColonnes):
                self.case[ligne].append(0) #vide=0
                
        #bind click action :
        self.bind("<Button-1>", self.actionClicGauche)
        self.bind("<Button-3>", self.actionClicDroit)
        #bind moving while clicking :
        self.bind("<B1-Motion>", self.actionClicGauche)
        self.bind("<B3-Motion>", self.actionClicDroit)
        
        self.caseDepart = 0,0
        self.dessinerCase(0,0,'green')
        self.caseArrivee = nombreLignes-1, nombreColonnes-1
        self.dessinerCase(nombreLignes-1,nombreColonnes-1,'red')
            
    def dessinerCase(self, ligne, colonne, couleur):
        xmin = colonne*self.tailleCase
        ymin = ligne*self.tailleCase
        xmax = xmin + self.tailleCase
        ymax = ymin + self.tailleCase
        self.create_rectangle(xmin, ymin, xmax, ymax, fill = couleur)

    def eventCoords(self, event):
        if event.x > 0 and event.x < self.nombreColonnes*self.tailleCase and event.y > 0 and event.y < self.nombreLignes*self.tailleCase:
            indice_ligne = int(event.y / self.tailleCase)
            indice_colonne = int(event.x / self.tailleCase)
            return indice_ligne, indice_colonne   

    def actionClicGauche(self, event):
        if self.eventCoords(event)== None or self.eventCoords(event) == self.caseDepart or self.eventCoords(event) == self.caseArrivee:
            return
        numLigne, numColonne = self.eventCoords(event)
        self.dessinerCase(numLigne, numColonne, "black")
        self.case[numLigne][numColonne]=1
        
    def actionClicDroit(self, event):
        if self.eventCoords(event)== None or self.eventCoords(event) == self.caseDepart or self.eventCoords(event) == self.caseArrivee:
            return
        numLigne, numColonne = self.eventCoords(event)
        self.dessinerCase(numLigne, numColonne, "white")
        self.case[numLigne][numColonne]=0
        
        
fenetre = Tk()
nombreLignes, nombreColonnes, tailleCase=50,100,10
grillePerso = representationGrille(fenetre, nombreLignes, nombreColonnes, tailleCase)
grillePerso.pack()

fenetre.mainloop()
