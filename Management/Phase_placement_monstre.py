import pygame
from Autres.Autre import (
    Var_global,
    OPTIONS_CHOIX_NIVEAU,
    RETOUR_MENU, ARAIGNEE, GOBELIN, ARAIGNEE_VENIMEUSE,
)
from Classes_basiques.cellule import Tuile_depart, Tuile_arrivee, Cellule_vide
from Management.Management_Monstres_global import Manag_monstres_global
from Management.Management_Plateau import Manag_Plateau
from Management.Management_aventurier import Manag_aventurier


class Manag_phase_1_placement_monstre:
    def __init__(self, affichage, manag_plateau:Manag_Plateau, manag_aventurier:Manag_aventurier, manag_monstre:Manag_monstres_global):
        self.affichage = affichage
        self.manag_plateau = manag_plateau
        self.manag_aventurier = manag_aventurier
        self.manag_monstre = manag_monstre
        self.level = 1
        self.ens_carte_possible = {
            1: [ARAIGNEE, GOBELIN, ARAIGNEE_VENIMEUSE],
            2: [ARAIGNEE]
        }

    def ecran_choix_niveau(self):
        horloge = pygame.time.Clock()
        ecran = self.manag_plateau.get_plateau().ecran
        selection = 0
        nb_options = len(OPTIONS_CHOIX_NIVEAU)

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return Var_global.QUIT
                if evenement.type == pygame.KEYUP:
                    if evenement.key == pygame.K_UP:
                        selection = (selection - 2) % nb_options
                    elif evenement.key == pygame.K_DOWN:
                        selection = (selection + 2) % nb_options
                    elif evenement.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        selection = selection - 1 if selection % 2 == 1 else selection + 1
                    elif evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if selection == RETOUR_MENU:
                            return Var_global.FIN_ESCAPE
                        self.level = selection + 1
                        return self.level
                    elif evenement.key == pygame.K_ESCAPE:
                        return Var_global.FIN_ESCAPE

            self.affichage.dessiner_ecran_choix_niveau(
                ecran=ecran,
                selection=selection,
                options=OPTIONS_CHOIX_NIVEAU,
            )
            horloge.tick(60)

    def selection_carte_placer(self):
        horloge = pygame.time.Clock()
        placement = False
        tirage = False

        ens_carte = self.ens_carte_possible[self.level]

        if len(ens_carte) == 0:
            return Var_global.CONTINUE

        selection = 0
        indice_monstre = None
        cartes_monstres = [self.manag_monstre.creer_objet_monstre(numero=num) for num in ens_carte]
        monstre_selectionne = cartes_monstres[selection]
        plateau = self.manag_plateau.get_plateau()
        grille = plateau.grille
        tuiles_interdites = (Cellule_vide, Tuile_depart, Tuile_arrivee)

        pos_carte = None
        for pos, case_tuile in grille.items():
            if not isinstance(case_tuile, tuiles_interdites) and len(self.manag_monstre.verif_case_occupee_par_monstre(pos)) == 0:
                pos_carte = list(pos)
                break
        if pos_carte is None:
            for pos, case_tuile in grille.items():
                if not isinstance(case_tuile, tuiles_interdites):
                    pos_carte = list(pos)
                    break

        if len(ens_carte) == 1:
            placement = True
            indice_monstre = self.manag_monstre.creation_nouveau_monstre(
                numero=ens_carte[selection],
                x=pos_carte[0],
                y=pos_carte[1],
            )
            monstre_selectionne = self.manag_monstre.get_list_monstre()[ens_carte[selection]][indice_monstre]

        deplacements = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
        }

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return Var_global.QUIT
                if evenement.type == pygame.KEYUP:
                    if not tirage:
                        if evenement.key == pygame.K_m:
                            tirage = True
                        if evenement.key == pygame.K_ESCAPE:
                            return Var_global.FIN_ESCAPE
                    elif not placement and tirage:
                        if evenement.key == pygame.K_m:
                            tirage = False
                        if evenement.key == pygame.K_ESCAPE:
                            tirage = False
                        if evenement.key == pygame.K_RETURN:
                            if pos_carte is None:
                                return Var_global.FIN_ESCAPE
                            indice_monstre = self.manag_monstre.creation_nouveau_monstre(
                                numero=ens_carte[selection],
                                x=pos_carte[0],
                                y=pos_carte[1],
                            )
                            monstre_selectionne = self.manag_monstre.get_list_monstre()[ens_carte[selection]][indice_monstre]
                            placement = True
                        if evenement.key == pygame.K_RIGHT:
                            selection = (selection + 1) % len(ens_carte)
                            monstre_selectionne = cartes_monstres[selection]
                        if evenement.key == pygame.K_LEFT:
                            selection = (selection - 1) % len(ens_carte)
                            monstre_selectionne = cartes_monstres[selection]
                    elif placement and tirage:
                        if evenement.key == pygame.K_ESCAPE:
                            self.manag_monstre.supprimer_monstre(monstre=monstre_selectionne)
                            monstre_selectionne = cartes_monstres[selection]
                            placement = False
                            break
                        if evenement.key in deplacements:
                            dx, dy = deplacements[evenement.key]
                            x_courant, y_courant = pos_carte[0] + dx, pos_carte[1] + dy
                            pos_trouvee = None

                            while 0 <= x_courant < plateau.nb_cellule_colonne and 0 <= y_courant < plateau.nb_cellule_ligne:
                                pos_test = (x_courant, y_courant)
                                case = grille.get(pos_test)
                                monstres_sur_case = [
                                    m for m in self.manag_monstre.verif_case_occupee_par_monstre(pos_test)
                                    if m is not monstre_selectionne
                                ]
                                if (case is not None
                                        and not isinstance(case, tuiles_interdites)
                                        and len(monstres_sur_case) == 0):
                                    pos_trouvee = pos_test
                                    break
                                x_courant += dx
                                y_courant += dy

                            if pos_trouvee is not None:
                                pos_carte[0], pos_carte[1] = pos_trouvee
                                self.manag_monstre.placer_monstre(
                                    type_monstre=ens_carte[selection],
                                    nouvelle_pos=pos_carte,
                                    indice=indice_monstre,
                                )
                        if evenement.key in (pygame.K_RETURN, pygame.K_SPACE):
                            return Var_global.CONTINUE

            self.affichage.dessiner(
                manag_Plateau=self.manag_plateau,
                manag_aventurier=self.manag_aventurier,
                manag_monstre=self.manag_monstre,
                monstres_a_afficher=[monstre_selectionne] if monstre_selectionne else None,
                cartes_selection=cartes_monstres if not placement and tirage else None,
                indice_carte_selectionnee=selection,
                afficher_touche_m=True,
            )
            horloge.tick(60)


    def creation_plateau(self, ):
        if self.level == 1:
            dict_nouveau_donjon = {(0, 0): (7, 0), (0, 1): (7, 0), (0, 2): (7, 0), (0, 3): (7, 0), (0, 4): (0, 0), (0, 5): (7, 0), (0, 6): (7, 0), (0, 7): (7, 0), (1, 0): (7, 0), (1, 1): (7, 0), (1, 2): (7, 0), (1, 3): (7, 0), (1, 4): (2, 0), (1, 5): (7, 0), (1, 6): (7, 0), (1, 7): (7, 0), (2, 0): (7, 0), (2, 1): (7, 0), (2, 2): (7, 0), (2, 3): (7, 0), (2, 4): (2, 0), (2, 5): (7, 0), (2, 6): (7, 0), (2, 7): (7, 0), (3, 0): (7, 0), (3, 1): (7, 0), (3, 2): (7, 0), (3, 3): (7, 0), (3, 4): (2, 0), (3, 5): (7, 0), (3, 6): (7, 0), (3, 7): (7, 0), (4, 0): (7, 0), (4, 1): (7, 0), (4, 2): (7, 0), (4, 3): (7, 0), (4, 4): (2, 0), (4, 5): (7, 0), (4, 6): (7, 0), (4, 7): (7, 0), (5, 0): (7, 0), (5, 1): (7, 0), (5, 2): (7, 0), (5, 3): (7, 0), (5, 4): (2, 0), (5, 5): (7, 0), (5, 6): (7, 0), (5, 7): (7, 0), (6, 0): (7, 0), (6, 1): (7, 0), (6, 2): (7, 0), (6, 3): (7, 0), (6, 4): (2, 0), (6, 5): (7, 0), (6, 6): (7, 0), (6, 7): (7, 0), (7, 0): (7, 0), (7, 1): (7, 0), (7, 2): (7, 0), (7, 3): (7, 0), (7, 4): (2, 0), (7, 5): (7, 0), (7, 6): (7, 0), (7, 7): (7, 0), (8, 0): (7, 0), (8, 1): (7, 0), (8, 2): (7, 0), (8, 3): (7, 0), (8, 4): (2, 0), (8, 5): (7, 0), (8, 6): (7, 0), (8, 7): (7, 0), (9, 0): (7, 0), (9, 1): (7, 0), (9, 2): (7, 0), (9, 3): (7, 0), (9, 4): (1, 0), (9, 5): (7, 0), (9, 6): (7, 0), (9, 7): (7, 0)}

        else:
            dict_nouveau_donjon = {}
        res = self.manag_plateau.creation_dongeon_personnalise(dict_dongeon=dict_nouveau_donjon)

        if len(res) == 2:
            self.manag_aventurier.placer_aventurier_pos(res, pos_origine=True)


    def mode_creation(self, level):
        self.level = level

        self.creation_plateau()

        return self.selection_carte_placer()


