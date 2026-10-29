from Classes_basiques.Plateau import *
from Autres.Autre import (
    DEPART,
    ARRIVEE,
    COULOIR_HORIZONTAL,
    COULOIR_VERTICAL,
    COIN,
    TRIANGLE,
    CUL_DE_SAC,
)

class Manag_Plateau:
    def __init__(self):
        self.Plateau = Plateau()

    def get_plateau(self):
        return self.Plateau

    def reinitialisation_plateau(self):
        for key, values in self.Plateau.grille.items():
            if isinstance(key, Position):
                self.Plateau.grille[key] = Cellule_vide(colonne=key.get_position()[0],
                                                        ligne=key.get_position()[1],
                                                        taille=self.Plateau.taille_cellule)
            elif isinstance(key, tuple):
                self.Plateau.grille[key] = Cellule_vide(colonne=key[0],
                                                        ligne=key[1],
                                                        taille=self.Plateau.taille_cellule)

    def placement_piece(self, numero, pos:list, orientation=None):
        if numero == DEPART:
            for pos_cle, cellule in self.Plateau.grille.items():
                if isinstance(cellule, Tuille_depart):
                    self.Plateau.grille[pos_cle] = Cellule_vide(colonne=cellule.colonne,
                                                                ligne=cellule.ligne,
                                                                taille=self.Plateau.taille_cellule)
            piece_cree = Tuille_depart(colonne=pos[0],
                                       ligne=pos[1],
                                       taille=self.Plateau.taille_cellule)
        elif numero == ARRIVEE:
            piece_cree = Tuille_arrivee(colonne=pos[0],
                                       ligne=pos[1],
                                       taille=self.Plateau.taille_cellule)
        elif numero == COULOIR_HORIZONTAL:
            piece_cree = Couloir_horizontal(colonne=pos[0],
                                       ligne=pos[1],
                                       taille=self.Plateau.taille_cellule)
        elif numero == COULOIR_VERTICAL:
            piece_cree = Couloir_vertical(colonne=pos[0],
                                       ligne=pos[1],
                                       taille=self.Plateau.taille_cellule)
        elif numero == COIN:
            piece_cree = Couloir_coin(colonne=pos[0],
                                      ligne=pos[1],
                                      taille=self.Plateau.taille_cellule,
                                      orientation=orientation)
        elif numero == TRIANGLE:
            piece_cree = Couloir_triangle(colonne=pos[0],
                                          ligne=pos[1],
                                          taille=self.Plateau.taille_cellule,
                                          orientation=orientation)
        else:
            piece_cree = Cul_de_sac(colonne=pos[0],
                                    ligne=pos[1],
                                    taille=self.Plateau.taille_cellule,
                                    orientation=orientation)

        self.Plateau.grille[Position(pos[0], pos[1])] = piece_cree
        self.actualiser_pos_tuile_suivante()

    def actualiser_pos_tuile_suivante(self):
        for cellule in self.Plateau.grille.values():
            cellule.definir_pos_liee_f_orientation()

        nouvelles_connexions = {}
        for pos, cellule in self.Plateau.grille.items():
            if not cellule.pos_tuile_suivante:
                continue

            pos_actuelle = (cellule.colonne, cellule.ligne)
            voisins_valides = []
            for pos_voisin in cellule.pos_tuile_suivante:
                # Bord du plateau (hors grille) -> compté comme un mur
                if pos_voisin not in self.Plateau.grille:
                    continue

                voisin = self.Plateau.grille[pos_voisin]
                # Tuile vide / bloquée -> comptée comme un mur
                if voisin.bloquee or isinstance(voisin, Cellule_vide):
                    continue

                # Vérifie que la tuile voisine est bien ouverte vers la tuile actuelle (pas de mur entre les deux)
                if isinstance(voisin, Tuille_arrivee) or (
                    voisin.pos_tuile_suivante and pos_actuelle in voisin.pos_tuile_suivante
                ):
                    voisins_valides.append(pos_voisin)

            nouvelles_connexions[pos] = voisins_valides

        for pos, voisins_valides in nouvelles_connexions.items():
            self.Plateau.grille[pos].pos_tuile_suivante = voisins_valides

    def completer_tuile_depart(self):
        self.actualiser_pos_tuile_suivante()

    def verifier_plateau(self):
        pos_depart = None
        a_arrivee = False

        for cellule in self.Plateau.grille.values():
            if isinstance(cellule, Tuille_depart):
                pos_depart = (cellule.colonne, cellule.ligne)
            elif isinstance(cellule, Tuille_arrivee):
                a_arrivee = True

        if pos_depart is None or not a_arrivee:
            if pos_depart is None and not a_arrivee:
                print("Erreur : Il manque une tuile de départ et une tuile d'arrivée ! Veuillez refaire/compléter votre donjon.")
            elif pos_depart is None:
                print("Erreur : Il manque une tuile de départ ! Veuillez placer une tuile de départ.")
            else:
                print("Erreur : Il manque une tuile d'arrivée ! Veuillez placer une tuile d'arrivée.")
            return False

        self.actualiser_pos_tuile_suivante()

        file_attente = [pos_depart]
        visites = {pos_depart}
        chemin_trouve = False

        while file_attente:
            pos_courante = file_attente.pop(0)
            tuile_courante = self.Plateau.grille.get(pos_courante)
            if tuile_courante is None:
                continue
            if isinstance(tuile_courante, Tuille_arrivee):
                chemin_trouve = True
                break
            if tuile_courante.pos_tuile_suivante:
                for voisin in tuile_courante.pos_tuile_suivante:
                    if voisin not in visites:
                        visites.add(voisin)
                        file_attente.append(voisin)

        if not chemin_trouve:
            print("Erreur : Aucun chemin ne relie la tuile de départ à la tuile d'arrivée ! Veuillez modifier votre donjon.")
            return False

        return True

    def creation_couloir_horizontal(self):
        ligne_milieu = self.Plateau.nb_cellule_ligne // 2

        self.Plateau.grille[(0, ligne_milieu)] = Tuille_depart(ligne=ligne_milieu,
                                                               colonne=0,
                                                               taille=self.Plateau.taille_cellule)

        self.Plateau.grille[(0, ligne_milieu)].pos_tuile_suivante.append((1, ligne_milieu))


        for colonne in range(1, self.Plateau.get_nb_cellule_colonne()-1):
            obj_a_supr = self.Plateau.grille[(colonne, ligne_milieu)]
            self.Plateau.grille[(colonne, ligne_milieu)] = Couloir_horizontal(ligne=ligne_milieu,
                                                                            colonne=colonne,
                                                                            taille=self.Plateau.taille_cellule)
            del obj_a_supr

        derniere_colonne = self.Plateau.get_nb_cellule_colonne()-1
        self.Plateau.grille[(derniere_colonne, ligne_milieu)] = Tuille_arrivee(ligne=ligne_milieu,
                                                                               colonne=derniere_colonne,
                                                                               taille=self.Plateau.taille_cellule)
        self.actualiser_pos_tuile_suivante()

        return 0, ligne_milieu

    def creation_couloir_vertical(self):
        colonne_milieu = self.Plateau.nb_cellule_colonne // 2

        self.Plateau.grille[(colonne_milieu, 0)] = Tuille_depart(ligne=0,
                                                               colonne=colonne_milieu,
                                                               taille=self.Plateau.taille_cellule)

        self.Plateau.grille[(colonne_milieu, 0)].pos_tuile_suivante.append((colonne_milieu, 1))


        for ligne in range(1, self.Plateau.get_nb_cellule_ligne()-1):
            self.Plateau.grille[(colonne_milieu, ligne)] = Couloir_vertical(ligne=ligne,
                                                                            colonne=colonne_milieu,
                                                                            taille=self.Plateau.taille_cellule)

        derniere_ligne = self.Plateau.get_nb_cellule_ligne()-1
        self.Plateau.grille[(colonne_milieu, derniere_ligne)] = Tuille_arrivee(ligne=derniere_ligne,
                                                                               colonne=colonne_milieu,
                                                                               taille=self.Plateau.taille_cellule)
        self.actualiser_pos_tuile_suivante()

        return colonne_milieu, 0

    def creation_couloir_zigzag(self):
        ligne_milieu = self.Plateau.nb_cellule_ligne // 2
        taille = self.Plateau.taille_cellule

        self.Plateau.grille[(0, ligne_milieu)] = Tuille_depart(ligne=ligne_milieu,
                                                               colonne=0,
                                                               taille=taille)

        self.Plateau.grille[(0, ligne_milieu)].pos_tuile_suivante.append((1, ligne_milieu))

        # Montée en escalier vers le haut (colonnes 1 à 2)
        self.Plateau.grille[(1, 4)] = Couloir_coin(ligne=4, colonne=1, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(1, 3)] = Couloir_vertical(ligne=3, colonne=1, taille=taille)
        self.Plateau.grille[(1, 2)] = Couloir_coin(ligne=2, colonne=1, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(2, 2)] = Couloir_coin(ligne=2, colonne=2, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(2, 1)] = Couloir_coin(ligne=1, colonne=2, taille=taille, orientation=COIN_HAUT_GAUCHE)

        # Descente en escalier vers le bas (colonnes 3 à 5)
        self.Plateau.grille[(3, 1)] = Couloir_coin(ligne=1, colonne=3, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(3, 2)] = Couloir_coin(ligne=2, colonne=3, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(4, 2)] = Couloir_coin(ligne=2, colonne=4, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(4, 3)] = Couloir_vertical(ligne=3, colonne=4, taille=taille)
        self.Plateau.grille[(4, 4)] = Couloir_vertical(ligne=4, colonne=4, taille=taille)
        self.Plateau.grille[(4, 5)] = Couloir_coin(ligne=5, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(5, 5)] = Couloir_coin(ligne=5, colonne=5, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(5, 6)] = Couloir_coin(ligne=6, colonne=5, taille=taille, orientation=COIN_BAS_GAUCHE)

        # Remontée en escalier vers la tuile d'arrivée (colonnes 6 à 8)
        self.Plateau.grille[(6, 6)] = Couloir_coin(ligne=6, colonne=6, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(6, 5)] = Couloir_coin(ligne=5, colonne=6, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(7, 5)] = Couloir_coin(ligne=5, colonne=7, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(7, 4)] = Couloir_vertical(ligne=4, colonne=7, taille=taille)
        self.Plateau.grille[(7, 3)] = Couloir_coin(ligne=3, colonne=7, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(8, 3)] = Couloir_coin(ligne=3, colonne=8, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(8, 4)] = Couloir_coin(ligne=4, colonne=8, taille=taille, orientation=COIN_BAS_GAUCHE)

        derniere_colonne = self.Plateau.get_nb_cellule_colonne() - 1
        self.Plateau.grille[(derniere_colonne, ligne_milieu)] = Tuille_arrivee(ligne=ligne_milieu,
                                                                               colonne=derniere_colonne,
                                                                               taille=taille)
        self.actualiser_pos_tuile_suivante()

        return 0, ligne_milieu

    def creation_long_couloir(self):
        ligne_milieu = self.Plateau.nb_cellule_ligne // 2
        taille = self.Plateau.taille_cellule

        self.Plateau.grille[(0, ligne_milieu)] = Tuille_depart(ligne=ligne_milieu,
                                                               colonne=0,
                                                               taille=taille)

        self.Plateau.grille[(0, ligne_milieu)].pos_tuile_suivante.append((1, ligne_milieu))

        # 1. Avance puis 1er retour en arrière sur la ligne 3 vers la gauche
        self.Plateau.grille[(1, 4)] = Couloir_horizontal(ligne=4, colonne=1, taille=taille)
        self.Plateau.grille[(2, 4)] = Couloir_horizontal(ligne=4, colonne=2, taille=taille)
        self.Plateau.grille[(3, 4)] = Couloir_coin(ligne=4, colonne=3, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(3, 3)] = Couloir_coin(ligne=3, colonne=3, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(2, 3)] = Couloir_horizontal(ligne=3, colonne=2, taille=taille)
        self.Plateau.grille[(1, 3)] = Couloir_horizontal(ligne=3, colonne=1, taille=taille)
        self.Plateau.grille[(0, 3)] = Couloir_coin(ligne=3, colonne=0, taille=taille, orientation=COIN_BAS_GAUCHE)

        # 2. Remonte colonne 0 puis avance sur la ligne 0
        self.Plateau.grille[(0, 2)] = Couloir_vertical(ligne=2, colonne=0, taille=taille)
        self.Plateau.grille[(0, 1)] = Couloir_vertical(ligne=1, colonne=0, taille=taille)
        self.Plateau.grille[(0, 0)] = Couloir_coin(ligne=0, colonne=0, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(1, 0)] = Couloir_horizontal(ligne=0, colonne=1, taille=taille)
        self.Plateau.grille[(2, 0)] = Couloir_horizontal(ligne=0, colonne=2, taille=taille)
        self.Plateau.grille[(3, 0)] = Couloir_horizontal(ligne=0, colonne=3, taille=taille)
        self.Plateau.grille[(4, 0)] = Couloir_coin(ligne=0, colonne=4, taille=taille, orientation=COIN_HAUT_DROIT)

        # 3. 2e retour en arrière sur la ligne 1 vers la gauche
        self.Plateau.grille[(4, 1)] = Couloir_coin(ligne=1, colonne=4, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(3, 1)] = Couloir_horizontal(ligne=1, colonne=3, taille=taille)
        self.Plateau.grille[(2, 1)] = Couloir_horizontal(ligne=1, colonne=2, taille=taille)
        self.Plateau.grille[(1, 1)] = Couloir_coin(ligne=1, colonne=1, taille=taille, orientation=COIN_HAUT_GAUCHE)

        # 4. Repart à droite sur la ligne 2 puis remonte en ligne 0 jusqu'au bout
        self.Plateau.grille[(1, 2)] = Couloir_coin(ligne=2, colonne=1, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(2, 2)] = Couloir_horizontal(ligne=2, colonne=2, taille=taille)
        self.Plateau.grille[(3, 2)] = Couloir_horizontal(ligne=2, colonne=3, taille=taille)
        self.Plateau.grille[(4, 2)] = Couloir_horizontal(ligne=2, colonne=4, taille=taille)
        self.Plateau.grille[(5, 2)] = Couloir_coin(ligne=2, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(5, 1)] = Couloir_vertical(ligne=1, colonne=5, taille=taille)
        self.Plateau.grille[(5, 0)] = Couloir_coin(ligne=0, colonne=5, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(6, 0)] = Couloir_horizontal(ligne=0, colonne=6, taille=taille)
        self.Plateau.grille[(7, 0)] = Couloir_horizontal(ligne=0, colonne=7, taille=taille)
        self.Plateau.grille[(8, 0)] = Couloir_horizontal(ligne=0, colonne=8, taille=taille)
        self.Plateau.grille[(9, 0)] = Couloir_coin(ligne=0, colonne=9, taille=taille, orientation=COIN_HAUT_DROIT)

        # 5. 3e retour en arrière sur la ligne 1 vers la gauche
        self.Plateau.grille[(9, 1)] = Couloir_coin(ligne=1, colonne=9, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(8, 1)] = Couloir_horizontal(ligne=1, colonne=8, taille=taille)
        self.Plateau.grille[(7, 1)] = Couloir_horizontal(ligne=1, colonne=7, taille=taille)
        self.Plateau.grille[(6, 1)] = Couloir_coin(ligne=1, colonne=6, taille=taille, orientation=COIN_HAUT_GAUCHE)

        # 6. Repart à droite sur la ligne 2
        self.Plateau.grille[(6, 2)] = Couloir_coin(ligne=2, colonne=6, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(7, 2)] = Couloir_horizontal(ligne=2, colonne=7, taille=taille)
        self.Plateau.grille[(8, 2)] = Couloir_horizontal(ligne=2, colonne=8, taille=taille)
        self.Plateau.grille[(9, 2)] = Couloir_coin(ligne=2, colonne=9, taille=taille, orientation=COIN_HAUT_DROIT)

        # 7. 4e grand retour en arrière sur la ligne 3 (colonnes 9 à 4)
        self.Plateau.grille[(9, 3)] = Couloir_coin(ligne=3, colonne=9, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(8, 3)] = Couloir_horizontal(ligne=3, colonne=8, taille=taille)
        self.Plateau.grille[(7, 3)] = Couloir_horizontal(ligne=3, colonne=7, taille=taille)
        self.Plateau.grille[(6, 3)] = Couloir_horizontal(ligne=3, colonne=6, taille=taille)
        self.Plateau.grille[(5, 3)] = Couloir_horizontal(ligne=3, colonne=5, taille=taille)
        self.Plateau.grille[(4, 3)] = Couloir_coin(ligne=3, colonne=4, taille=taille, orientation=COIN_HAUT_GAUCHE)

        # 8. Redescend et repart à droite sur la ligne 4
        self.Plateau.grille[(4, 4)] = Couloir_coin(ligne=4, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(5, 4)] = Couloir_horizontal(ligne=4, colonne=5, taille=taille)
        self.Plateau.grille[(6, 4)] = Couloir_coin(ligne=4, colonne=6, taille=taille, orientation=COIN_HAUT_DROIT)

        # 9. 5e très grand retour en arrière sur la ligne 5 (colonnes 6 à 0)
        self.Plateau.grille[(6, 5)] = Couloir_coin(ligne=5, colonne=6, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(5, 5)] = Couloir_horizontal(ligne=5, colonne=5, taille=taille)
        self.Plateau.grille[(4, 5)] = Couloir_horizontal(ligne=5, colonne=4, taille=taille)
        self.Plateau.grille[(3, 5)] = Couloir_horizontal(ligne=5, colonne=3, taille=taille)
        self.Plateau.grille[(2, 5)] = Couloir_horizontal(ligne=5, colonne=2, taille=taille)
        self.Plateau.grille[(1, 5)] = Couloir_horizontal(ligne=5, colonne=1, taille=taille)
        self.Plateau.grille[(0, 5)] = Couloir_coin(ligne=5, colonne=0, taille=taille, orientation=COIN_HAUT_GAUCHE)

        # 10. Descend en bas à gauche et serpente sur les lignes 6 et 7
        self.Plateau.grille[(0, 6)] = Couloir_vertical(ligne=6, colonne=0, taille=taille)
        self.Plateau.grille[(0, 7)] = Couloir_coin(ligne=7, colonne=0, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(1, 7)] = Couloir_coin(ligne=7, colonne=1, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(1, 6)] = Couloir_coin(ligne=6, colonne=1, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(2, 6)] = Couloir_coin(ligne=6, colonne=2, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(2, 7)] = Couloir_coin(ligne=7, colonne=2, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(3, 7)] = Couloir_coin(ligne=7, colonne=3, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(3, 6)] = Couloir_coin(ligne=6, colonne=3, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(4, 6)] = Couloir_coin(ligne=6, colonne=4, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(4, 7)] = Couloir_coin(ligne=7, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(5, 7)] = Couloir_coin(ligne=7, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(5, 6)] = Couloir_coin(ligne=6, colonne=5, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(6, 6)] = Couloir_coin(ligne=6, colonne=6, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(6, 7)] = Couloir_coin(ligne=7, colonne=6, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(7, 7)] = Couloir_horizontal(ligne=7, colonne=7, taille=taille)
        self.Plateau.grille[(8, 7)] = Couloir_horizontal(ligne=7, colonne=8, taille=taille)
        self.Plateau.grille[(9, 7)] = Couloir_coin(ligne=7, colonne=9, taille=taille, orientation=COIN_BAS_DROIT)

        # 11. Dernier retour en arrière (colonnes 9 à 7) avant la tuile d'arrivée
        self.Plateau.grille[(9, 6)] = Couloir_vertical(ligne=6, colonne=9, taille=taille)
        self.Plateau.grille[(9, 5)] = Couloir_coin(ligne=5, colonne=9, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(8, 5)] = Couloir_coin(ligne=5, colonne=8, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(8, 6)] = Couloir_coin(ligne=6, colonne=8, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(7, 6)] = Couloir_coin(ligne=6, colonne=7, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(7, 5)] = Couloir_vertical(ligne=5, colonne=7, taille=taille)
        self.Plateau.grille[(7, 4)] = Couloir_coin(ligne=4, colonne=7, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(8, 4)] = Couloir_horizontal(ligne=4, colonne=8, taille=taille)

        derniere_colonne = self.Plateau.get_nb_cellule_colonne() - 1
        self.Plateau.grille[(derniere_colonne, ligne_milieu)] = Tuille_arrivee(ligne=ligne_milieu,
                                                                               colonne=derniere_colonne,
                                                                               taille=taille)
        self.actualiser_pos_tuile_suivante()

        return 0, ligne_milieu

    def creation_couloir_triangle(self):
        ligne_milieu = self.Plateau.nb_cellule_ligne // 2
        taille = self.Plateau.taille_cellule

        self.Plateau.grille[(0, ligne_milieu)] = Tuille_depart(ligne=ligne_milieu,
                                                               colonne=0,
                                                               taille=taille)

        self.Plateau.grille[(0, ligne_milieu)].pos_tuile_suivante.append((1, ligne_milieu))

        # Colonne 1 : bifurcation d'entrée (haut/bas) et embranchement ligne 3
        self.Plateau.grille[(1, 1)] = Couloir_coin(ligne=1, colonne=1, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(1, 2)] = Couloir_vertical(ligne=2, colonne=1, taille=taille)
        self.Plateau.grille[(1, 3)] = Couloir_triangle(ligne=3, colonne=1, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(1, 4)] = Couloir_triangle(ligne=4, colonne=1, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(1, 5)] = Couloir_vertical(ligne=5, colonne=1, taille=taille)
        self.Plateau.grille[(1, 6)] = Couloir_coin(ligne=6, colonne=1, taille=taille, orientation=COIN_BAS_GAUCHE)

        # Colonne 2 : liaisons horizontales
        self.Plateau.grille[(2, 1)] = Couloir_horizontal(ligne=1, colonne=2, taille=taille)
        self.Plateau.grille[(2, 3)] = Couloir_horizontal(ligne=3, colonne=2, taille=taille)
        self.Plateau.grille[(2, 6)] = Couloir_horizontal(ligne=6, colonne=2, taille=taille)

        # Colonne 3 : carrefours en T multiples
        self.Plateau.grille[(3, 1)] = Couloir_triangle(ligne=1, colonne=3, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(3, 2)] = Couloir_triangle(ligne=2, colonne=3, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(3, 3)] = Couloir_triangle(ligne=3, colonne=3, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(3, 4)] = Couloir_vertical(ligne=4, colonne=3, taille=taille)
        self.Plateau.grille[(3, 5)] = Couloir_triangle(ligne=5, colonne=3, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(3, 6)] = Couloir_triangle(ligne=6, colonne=3, taille=taille, orientation=TRIANGLE_BAS)

        # Colonnes 4 et 5 : boucles haut, milieu et bas avec intersections en T
        self.Plateau.grille[(4, 0)] = Couloir_coin(ligne=0, colonne=4, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(4, 1)] = Couloir_triangle(ligne=1, colonne=4, taille=taille, orientation=TRIANGLE_BAS)
        self.Plateau.grille[(4, 2)] = Couloir_triangle(ligne=2, colonne=4, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(4, 3)] = Couloir_vertical(ligne=3, colonne=4, taille=taille)
        self.Plateau.grille[(4, 4)] = Couloir_coin(ligne=4, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(4, 5)] = Couloir_horizontal(ligne=5, colonne=4, taille=taille)
        self.Plateau.grille[(4, 6)] = Couloir_triangle(ligne=6, colonne=4, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(4, 7)] = Couloir_coin(ligne=7, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)

        self.Plateau.grille[(5, 0)] = Couloir_coin(ligne=0, colonne=5, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(5, 1)] = Couloir_triangle(ligne=1, colonne=5, taille=taille, orientation=TRIANGLE_BAS)
        self.Plateau.grille[(5, 2)] = Couloir_triangle(ligne=2, colonne=5, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(5, 3)] = Couloir_vertical(ligne=3, colonne=5, taille=taille)
        self.Plateau.grille[(5, 4)] = Couloir_coin(ligne=4, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(5, 5)] = Couloir_horizontal(ligne=5, colonne=5, taille=taille)
        self.Plateau.grille[(5, 6)] = Couloir_triangle(ligne=6, colonne=5, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(5, 7)] = Couloir_coin(ligne=7, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)

        # Colonne 6 : carrefours en T multiples
        self.Plateau.grille[(6, 1)] = Couloir_triangle(ligne=1, colonne=6, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(6, 2)] = Couloir_triangle(ligne=2, colonne=6, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(6, 3)] = Couloir_triangle(ligne=3, colonne=6, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(6, 4)] = Couloir_vertical(ligne=4, colonne=6, taille=taille)
        self.Plateau.grille[(6, 5)] = Couloir_triangle(ligne=5, colonne=6, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(6, 6)] = Couloir_triangle(ligne=6, colonne=6, taille=taille, orientation=TRIANGLE_BAS)

        # Colonne 7 : liaisons horizontales
        self.Plateau.grille[(7, 1)] = Couloir_horizontal(ligne=1, colonne=7, taille=taille)
        self.Plateau.grille[(7, 3)] = Couloir_horizontal(ligne=3, colonne=7, taille=taille)
        self.Plateau.grille[(7, 6)] = Couloir_horizontal(ligne=6, colonne=7, taille=taille)

        # Colonne 8 : convergence vers la tuile d'arrivée
        self.Plateau.grille[(8, 1)] = Couloir_coin(ligne=1, colonne=8, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(8, 2)] = Couloir_vertical(ligne=2, colonne=8, taille=taille)
        self.Plateau.grille[(8, 3)] = Couloir_triangle(ligne=3, colonne=8, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(8, 4)] = Couloir_triangle(ligne=4, colonne=8, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(8, 5)] = Couloir_vertical(ligne=5, colonne=8, taille=taille)
        self.Plateau.grille[(8, 6)] = Couloir_coin(ligne=6, colonne=8, taille=taille, orientation=COIN_BAS_DROIT)

        derniere_colonne = self.Plateau.get_nb_cellule_colonne() - 1
        self.Plateau.grille[(derniere_colonne, ligne_milieu)] = Tuille_arrivee(ligne=ligne_milieu,
                                                                               colonne=derniere_colonne,
                                                                               taille=taille)
        self.actualiser_pos_tuile_suivante()

        return 0, ligne_milieu

    def creation_couloir_cul_de_sac(self):
        ligne_milieu = self.Plateau.nb_cellule_ligne // 2
        taille = self.Plateau.taille_cellule

        self.Plateau.grille[(0, ligne_milieu)] = Tuille_depart(ligne=ligne_milieu,
                                                               colonne=0,
                                                               taille=taille)

        self.Plateau.grille[(0, ligne_milieu)].pos_tuile_suivante.append((1, ligne_milieu))

        # Colonne 0 : impasses en haut et en bas
        self.Plateau.grille[(0, 0)] = Cul_de_sac(ligne=0, colonne=0, taille=taille, orientation=DROIT)
        self.Plateau.grille[(0, 5)] = Couloir_coin(ligne=5, colonne=0, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(0, 6)] = Cul_de_sac(ligne=6, colonne=0, taille=taille, orientation=HAUT)

        # Colonne 1 : axe vertical avec bifurcations vers les culs-de-sac
        self.Plateau.grille[(1, 0)] = Couloir_coin(ligne=0, colonne=1, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(1, 1)] = Couloir_vertical(ligne=1, colonne=1, taille=taille)
        self.Plateau.grille[(1, 2)] = Couloir_triangle(ligne=2, colonne=1, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(1, 3)] = Couloir_vertical(ligne=3, colonne=1, taille=taille)
        self.Plateau.grille[(1, 4)] = Couloir_triangle(ligne=4, colonne=1, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(1, 5)] = Couloir_triangle(ligne=5, colonne=1, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(1, 6)] = Couloir_coin(ligne=6, colonne=1, taille=taille, orientation=COIN_BAS_GAUCHE)

        # Colonne 2 : embranchements et 3 culs-de-sac
        self.Plateau.grille[(2, 0)] = Couloir_coin(ligne=0, colonne=2, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(2, 1)] = Couloir_vertical(ligne=1, colonne=2, taille=taille)
        self.Plateau.grille[(2, 2)] = Couloir_triangle(ligne=2, colonne=2, taille=taille, orientation=TRIANGLE_BAS)
        self.Plateau.grille[(2, 3)] = Couloir_coin(ligne=3, colonne=2, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(2, 4)] = Cul_de_sac(ligne=4, colonne=2, taille=taille, orientation=HAUT)
        self.Plateau.grille[(2, 6)] = Cul_de_sac(ligne=6, colonne=2, taille=taille, orientation=GAUCHE)
        self.Plateau.grille[(2, 7)] = Cul_de_sac(ligne=7, colonne=2, taille=taille, orientation=DROIT)

        # Colonne 3 : chemin principal et impasses haut/bas
        self.Plateau.grille[(3, 0)] = Couloir_coin(ligne=0, colonne=3, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(3, 1)] = Cul_de_sac(ligne=1, colonne=3, taille=taille, orientation=HAUT)
        self.Plateau.grille[(3, 2)] = Couloir_coin(ligne=2, colonne=3, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(3, 3)] = Couloir_triangle(ligne=3, colonne=3, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(3, 4)] = Couloir_vertical(ligne=4, colonne=3, taille=taille)
        self.Plateau.grille[(3, 5)] = Couloir_triangle(ligne=5, colonne=3, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(3, 6)] = Couloir_vertical(ligne=6, colonne=3, taille=taille)
        self.Plateau.grille[(3, 7)] = Couloir_coin(ligne=7, colonne=3, taille=taille, orientation=COIN_BAS_DROIT)

        # Colonnes 4 et 5 : fausses pistes en haut et en bas
        self.Plateau.grille[(4, 1)] = Cul_de_sac(ligne=1, colonne=4, taille=taille, orientation=BAS)
        self.Plateau.grille[(4, 2)] = Couloir_vertical(ligne=2, colonne=4, taille=taille)
        self.Plateau.grille[(4, 3)] = Couloir_coin(ligne=3, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(4, 5)] = Couloir_triangle(ligne=5, colonne=4, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(4, 6)] = Couloir_vertical(ligne=6, colonne=4, taille=taille)
        self.Plateau.grille[(4, 7)] = Couloir_coin(ligne=7, colonne=4, taille=taille, orientation=COIN_BAS_GAUCHE)

        self.Plateau.grille[(5, 0)] = Cul_de_sac(ligne=0, colonne=5, taille=taille, orientation=DROIT)
        self.Plateau.grille[(5, 2)] = Couloir_coin(ligne=2, colonne=5, taille=taille, orientation=COIN_HAUT_GAUCHE)
        self.Plateau.grille[(5, 3)] = Couloir_triangle(ligne=3, colonne=5, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(5, 4)] = Couloir_vertical(ligne=4, colonne=5, taille=taille)
        self.Plateau.grille[(5, 5)] = Couloir_coin(ligne=5, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(5, 6)] = Cul_de_sac(ligne=6, colonne=5, taille=taille, orientation=BAS)
        self.Plateau.grille[(5, 7)] = Couloir_coin(ligne=7, colonne=5, taille=taille, orientation=COIN_BAS_DROIT)

        # Colonnes 6 et 7 : bifurcations multiples vers des culs-de-sac
        self.Plateau.grille[(6, 0)] = Couloir_coin(ligne=0, colonne=6, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(6, 1)] = Couloir_triangle(ligne=1, colonne=6, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(6, 2)] = Couloir_triangle(ligne=2, colonne=6, taille=taille, orientation=TRIANGLE_BAS)
        self.Plateau.grille[(6, 4)] = Cul_de_sac(ligne=4, colonne=6, taille=taille, orientation=BAS)
        self.Plateau.grille[(6, 5)] = Couloir_vertical(ligne=5, colonne=6, taille=taille)
        self.Plateau.grille[(6, 6)] = Couloir_coin(ligne=6, colonne=6, taille=taille, orientation=COIN_BAS_GAUCHE)

        self.Plateau.grille[(7, 0)] = Cul_de_sac(ligne=0, colonne=7, taille=taille, orientation=DROIT)
        self.Plateau.grille[(7, 1)] = Couloir_horizontal(ligne=1, colonne=7, taille=taille)
        self.Plateau.grille[(7, 2)] = Couloir_coin(ligne=2, colonne=7, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(7, 3)] = Couloir_triangle(ligne=3, colonne=7, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(7, 4)] = Couloir_triangle(ligne=4, colonne=7, taille=taille, orientation=TRIANGLE_GAUCHE)
        self.Plateau.grille[(7, 5)] = Couloir_vertical(ligne=5, colonne=7, taille=taille)
        self.Plateau.grille[(7, 6)] = Couloir_triangle(ligne=6, colonne=7, taille=taille, orientation=TRIANGLE_DROIT)
        self.Plateau.grille[(7, 7)] = Couloir_coin(ligne=7, colonne=7, taille=taille, orientation=COIN_BAS_GAUCHE)

        # Colonnes 8 et 9 : impasses finales et accès à la tuile d'arrivée
        self.Plateau.grille[(8, 0)] = Couloir_coin(ligne=0, colonne=8, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(8, 1)] = Couloir_triangle(ligne=1, colonne=8, taille=taille, orientation=TRIANGLE_BAS)
        self.Plateau.grille[(8, 3)] = Couloir_horizontal(ligne=3, colonne=8, taille=taille)
        self.Plateau.grille[(8, 4)] = Couloir_triangle(ligne=4, colonne=8, taille=taille, orientation=TRIANGLE_HAUT)
        self.Plateau.grille[(8, 5)] = Couloir_vertical(ligne=5, colonne=8, taille=taille)
        self.Plateau.grille[(8, 6)] = Couloir_coin(ligne=6, colonne=8, taille=taille, orientation=COIN_BAS_GAUCHE)
        self.Plateau.grille[(8, 7)] = Couloir_horizontal(ligne=7, colonne=8, taille=taille)

        self.Plateau.grille[(9, 1)] = Couloir_coin(ligne=1, colonne=9, taille=taille, orientation=COIN_HAUT_DROIT)
        self.Plateau.grille[(9, 2)] = Cul_de_sac(ligne=2, colonne=9, taille=taille, orientation=HAUT)
        self.Plateau.grille[(9, 3)] = Cul_de_sac(ligne=3, colonne=9, taille=taille, orientation=GAUCHE)
        self.Plateau.grille[(9, 5)] = Cul_de_sac(ligne=5, colonne=9, taille=taille, orientation=BAS)
        self.Plateau.grille[(9, 6)] = Couloir_coin(ligne=6, colonne=9, taille=taille, orientation=COIN_BAS_DROIT)
        self.Plateau.grille[(9, 7)] = Cul_de_sac(ligne=7, colonne=9, taille=taille, orientation=GAUCHE)

        derniere_colonne = self.Plateau.get_nb_cellule_colonne() - 1
        self.Plateau.grille[(derniere_colonne, ligne_milieu)] = Tuille_arrivee(ligne=ligne_milieu,
                                                                               colonne=derniere_colonne,
                                                                               taille=taille)
        self.actualiser_pos_tuile_suivante()

        return 0, ligne_milieu