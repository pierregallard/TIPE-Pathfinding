# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 19:16:21 2016

@author: Pierre
"""
from tkinter import *
from math import sqrt
from functools import partial
 
class noeud():
    def __init__(self, x, y):
        self.parent = self
        self.colonne = x #Position x
        self.ligne = y #Position y
        self.coutF = 0 #somme de G et H
        self.coutG = 0 #distance de ascendant + cout G de son ascendant
        self.coutH = 0 #Distance heuristique : distance du noeud final

   
class representationGrille(Canvas):
    def __init__(self,master, nombreColonnes, nombreLignes, tailleCase, *args, **kwargs):
        #*args: plusieurs arguments taille à souhait
        #**keywordargs: plusieur argument dictionaire taille à souhait
        self.master = master
        self.tailleCase = tailleCase
        self.nombreColonnes = nombreColonnes        
        self.nombreLignes = nombreLignes
 
        # Creation de la zone de dessin canvas(.tk), attention il faut rajouter 1 pixel pour les lignes de bordure en bas et a droite :
        Canvas.__init__(self, master, width = (tailleCase*nombreColonnes)+1, height = (tailleCase*nombreLignes)+1, highlightthickness=0, *args, **kwargs)  
        # Creation de la grille vide:
        for i in range(nombreColonnes*tailleCase):
            self.create_line(i*tailleCase,0,i*tailleCase,nombreLignes*tailleCase,fill='black')
        for j in range(nombreLignes*tailleCase):
            self.create_line(0,j*tailleCase,nombreColonnes*tailleCase,j*tailleCase,fill='black')
        #Creation de la liste des cases représentées:  
        self.case=[]
        for x in range(nombreColonnes):
            self.case.append([])
            for y in range(nombreLignes):
                self.case[x].append(0) #vide=0
               
        #création des bouton que l'on lie a une action :
        self.bind("<Button-1>", self.actionClicGauche)
        self.bind("<Button-3>", self.actionClicDroit)
        #bind moving while clicking :
        self.bind("<B1-Motion>", self.actionClicGauche)
        self.bind("<B3-Motion>", self.actionClicDroit)
       
        self.caseDepart = 0,0
        self.dessinerCase(0,0,'green')
        self.caseArrivee = nombreColonnes-1, nombreLignes-1
        self.dessinerCase(nombreColonnes-1, nombreLignes-1,'red')
           
    def dessinerCase(self, colonne, ligne, couleur):
        xmin = colonne*self.tailleCase
        ymin = ligne*self.tailleCase
        xmax = xmin + self.tailleCase
        ymax = ymin + self.tailleCase
        self.create_rectangle(xmin, ymin, xmax, ymax, fill = couleur)
 
    def eventCoords(self, event):
        if event.x > 0 and event.x < self.nombreColonnes*self.tailleCase and event.y > 0 and event.y < self.nombreLignes*self.tailleCase:
            indice_colonne = int(event.x / self.tailleCase)
            indice_ligne = int(event.y / self.tailleCase)
            return indice_colonne, indice_ligne  
 
    def actionClicGauche(self, event):
        if self.eventCoords(event)== None or self.eventCoords(event) == self.caseDepart or self.eventCoords(event) == self.caseArrivee:
            return
        numColonne, numLigne = self.eventCoords(event)
        self.dessinerCase(numColonne, numLigne, "black")
        self.case[numColonne][numLigne]=1
       
    def actionClicDroit(self, event):
        if self.eventCoords(event)== None or self.eventCoords(event) == self.caseDepart or self.eventCoords(event) == self.caseArrivee:
            return
        numColonne, numLigne = self.eventCoords(event)
        self.dessinerCase(numColonne, numLigne, "white")
        self.case[numColonne][numLigne]=0
       
    def distance(self,noeud1,noeud2):
        """il existe diférentes distance intereseente mis en commentaire"""
        a =  noeud2.ligne - noeud1.ligne
        b =  noeud2.colonne - noeud1.colonne
        return sqrt(a*a+b*b)
        #return (a*a+b*b)
        #return max(abs(a),abs(b))
        #return abs(a)+abs(b)
        #return 0
       
    def noeudDeMemeCoords (self, noeudTemp, liste):
        for noeudListe in liste:
            if noeudListe.ligne == noeudTemp.ligne and noeudListe.colonne == noeudTemp.colonne:
                return noeudListe
        return None
           
    def parcourirCasesAdjacentes(self, noeudCourant,liste_noeuds_fermes,liste_noeuds_ouverts):
        """deplacement dans selon 4 ou 8 voisins"""
        deplacements = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        #deplacements = [(-1,0),(0,1),(1,0),(0,-1)]
        for direction in deplacements:
            nouvellesCoords = (noeudCourant.colonne + direction[0],noeudCourant.ligne + direction[1])
            #On vérifie qu'on ne sort pas des limites (matrice):
            if nouvellesCoords[0] >= 0 and nouvellesCoords[0] <= self.nombreColonnes-1 and nouvellesCoords[1] >= 0 and nouvellesCoords[1] <= self.nombreLignes-1:
                #On continue si le voisin n'est pas un obstacle (vide=0, mur=1)
                if self.case[nouvellesCoords[0]][nouvellesCoords[1]] == 0:
                    #On crée un objet noeud au coordonnée du voisin
                    noeudTemp = noeud(nouvellesCoords[0],nouvellesCoords[1])
                    #Le noeud courant est son parent
                    noeudTemp.parent = noeudCourant
                    #Si le noeud fait déjà parti de la liste fermée, on ne continue pas :
                    if not self.noeudDeMemeCoords(noeudTemp,liste_noeuds_fermes):
                        #On implemente ses couts
                        noeudTemp.coutH = self.distance(noeudTemp,noeud(self.caseArrivee[0], self.caseArrivee[1]))
                        noeudTemp.coutG = noeudTemp.parent.coutG + self.distance(noeudTemp,noeudTemp.parent)
                        noeudTemp.coutF = noeudTemp.coutG + noeudTemp.coutH
                        #Si noeudTemp à déjà été ouvert, on met à jour ses couts :
                        noeudListe = self.noeudDeMemeCoords(noeudTemp,liste_noeuds_ouverts)
                        if noeudListe != None:                                    
                            #On compare son cout G avec celui de la liste ouverte, on met a jour les couts s'ils sont inferieurs ET on change le parent (nouveau chemin plus optimisé):
                            if noeudTemp.coutG < noeudListe.coutG:
                                noeudListe.parent = noeudCourant
                                noeudListe.coutG = noeudTemp.coutG
                                noeudListe.coutH = noeudTemp.coutH #inutile ?
                                noeudListe.coutF = noeudTemp.coutF
                        #lse : Ce noeud n'est pas déja présent dans le liste ouverte donc on l'y ajoute :
                        else:
                            liste_noeuds_ouverts.append(noeudTemp)
                            self.dessinerCase(noeudTemp.colonne, noeudTemp.ligne, "orange")  
                            self.master.update()

    def selectionerNoeudCoutMin(self, liste):
        #oon retourne le noeud le plus legers de la liste :
        meilleurNoeud = liste[0]
        coutMin = liste[0].coutF
        for noeudListe in liste:
            if noeudListe.coutF < coutMin:
                coutMin = noeudListe.coutF
                meilleurNoeud = noeudListe
        return meilleurNoeud

def RemonterListe(liste_noeuds_fermes): #cette fonction remonte le chemin d'ascendant en ascendant en partant du dernier noeud courant
    chemin = []
    n = liste_noeuds_fermes[-1]
    chemin.append(n)
    n = n.parent #On s'interesse au noeud parent à present
    while n.parent != n: #tant que le noeud n'est pas son propre parent (çad 1er noeud)
        chemin.append(n)
        n = n.parent #on ajoute le premier noeud à ne pas oublier
    chemin.append(n)
    return chemin

def distanceG(Grille):
    for x in range (Grille.nombreColonnes):
        for y in range (Grille.nombreLignes):
            Grille.create_text(x*(Grille.tailleCase),y*(Grille.tailleCase), text=round(distance(Grille,x ,y),2), anchor="nw") 
 
def Algorithme(Grille):
    """Boucle principale :
       - on met le meilleur noeud de la liste ouverte dans la liste fermée et on appelle la fonction qui va chercher ses voisins
       - lorsque le meilleur noeud correspond au noeud final on sort de la boucle pour afficher le chemin
       - si le noeud d'arivée n'est pas atteint et si la liste des noeuds à explorer est vide : il n'y a pas de solution"""
    liste_noeuds_ouverts = []
    liste_noeuds_fermes = []
 
    #Initialistion du noeudCourant avec le noeud de départ
    noeudCourant = noeud(Grille.caseDepart[0],Grille.caseDepart[1])
    noeudArrivee = noeud(Grille.caseArrivee[0],Grille.caseArrivee[1])
    noeudCourant.coutH = Grille.distance(noeudCourant, noeudArrivee)
    noeudCourant.coutF = noeudCourant.coutH
    #On le met dans la liste ouverte
    liste_noeuds_ouverts.append(noeudCourant)
    while (liste_noeuds_ouverts != [] and not(noeudCourant.ligne == noeudArrivee.ligne and noeudCourant.colonne == noeudArrivee.colonne)):
        # On choisi le meilleur noeud ce sera le noeud courant
        noeudCourant = Grille.selectionerNoeudCoutMin(liste_noeuds_ouverts)
        liste_noeuds_ouverts.remove(noeudCourant)
        liste_noeuds_fermes.append(noeudCourant)
       
        # création d'un carré correspondant au noeud courant en rose : très rapide (note: il existe des moyen de pauser)
        Grille.dessinerCase(noeudCourant.colonne,noeudCourant.ligne, 'pink')
       
        # Passe le dernier élément de la liste des carrés représentants les noeuds de la liste ferméé en rouge : trop rapide (note: rechercher moyen de mettre pause), inutile ?
        Grille.master.update()
        if liste_noeuds_fermes!=[]:
            Grille.dessinerCase(liste_noeuds_fermes[-1].colonne,liste_noeuds_fermes[-1].ligne, 'red')
           
        Grille.parcourirCasesAdjacentes(noeudCourant,liste_noeuds_fermes,liste_noeuds_ouverts)
    if noeudCourant.ligne == noeudArrivee.ligne and noeudCourant.colonne == noeudArrivee.colonne :
        for n in RemonterListe(liste_noeuds_fermes):
            Grille.dessinerCase(n.colonne, n.ligne, "blue")  
        print('FIN')
    elif liste_noeuds_ouverts == []:
        print('IMPOSSIBLE')
    else :
        print('bug')
        
fenetre = Tk()
nombreColonnes, nombreLignes, tailleCase=50,35,10
grillePerso = representationGrille(fenetre, nombreColonnes,nombreLignes , tailleCase)
grillePerso.pack()
action_with_arg = partial(Algorithme, grillePerso)
action_with_arg2 = partial(distanceG, grillePerso)
Boutton = Button(fenetre, text ="Lancer algorithme", command= action_with_arg)
Boutton.pack(fill=X)
 
fenetre.mainloop()