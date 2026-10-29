from Classes_basiques.cellule import *
from Autres.Autre import (
    Position,
    LARGEUR,
    HAUTEUR,
    LARGEUR_FENETRE,
    HAUTEUR_FENETRE,
    TAILLE_GRILLE_MAX,
    TITRE,
)

class Plateau:
    def __init__(self, largeur=LARGEUR, hauteur=HAUTEUR,
                 largeur_fenetre=LARGEUR_FENETRE, hauteur_fenetre=HAUTEUR_FENETRE,
                 taille_grille_max=TAILLE_GRILLE_MAX, titre=TITRE):

        self.largeur = largeur
        self.hauteur = hauteur
        self.largeur_fenetre = largeur_fenetre
        self.hauteur_fenetre = hauteur_fenetre
        self.decalage_x = (self.largeur_fenetre - self.largeur) // 2
        self.decalage_y = (self.hauteur_fenetre - self.hauteur) // 2

        if largeur > hauteur:
            self.nb_cellule_colonne = taille_grille_max
            self.taille_cellule = self.largeur // self.nb_cellule_colonne
            self.nb_cellule_ligne = self.hauteur // self.taille_cellule
        else:
            self.nb_cellule_ligne = taille_grille_max
            self.taille_cellule = self.hauteur // self.nb_cellule_ligne
            self.nb_cellule_colonne = self.largeur // self.taille_cellule

        self.ecran = pygame.display.set_mode((self.largeur_fenetre, self.hauteur_fenetre))
        pygame.display.set_caption(titre)

        self.grille = {
            Position(colonne, ligne): Cellule_vide(ligne, colonne, self.taille_cellule)
            for colonne in range(self.nb_cellule_colonne)
            for ligne in range(self.nb_cellule_ligne)
        }

    def get_nb_cellule_colonne(self):
        return self.nb_cellule_colonne

    def get_nb_cellule_ligne(self):
        return self.nb_cellule_ligne

    def get_taille_cellule(self):
        return self.taille_cellule