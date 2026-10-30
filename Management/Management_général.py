import pygame
from Management.affichage import Affichage
from Management.Management_Plateau import Manag_Plateau
from Management.Management_aventurier import Manag_aventurier
from Management.Phase1 import Manag_phase1
from Management.Phase2 import Manag_phase2
from Management.Phase_placement_monstre import Manag_phase_1_placement_monstre
from Management.Management_Monstres_global import Manag_monstres_global
from Autres.Autre import (
    MANAG_AVENTURIER,
    MANAG_PLATEAU,
    MANAG_PHASE1,
    MANAG_PHASE2,
    MANAG_MONSTRES_GLOBAL,
    MANAG_PHASE1_MONSTRE,
    MODE_EXISTANT,
    AUTRE_MODE,
    QUITTER_JEU,
    SAUVEGARDER_CONFIG,
    OPTIONS_MENU_DEBUT, Var_global,
)

class Root:
    def __init__(self):
        self.affichage = Affichage()
        self.Management_secondaire = {
            MANAG_AVENTURIER: Manag_aventurier(),
            MANAG_PLATEAU: Manag_Plateau(),
            MANAG_MONSTRES_GLOBAL: Manag_monstres_global(),
            }

        self.Management_secondaire[MANAG_PHASE1] = Manag_phase1(self.affichage,
                                                                self.Management_secondaire[MANAG_PLATEAU].get_plateau().taille_cellule)

        self.Management_secondaire[MANAG_PHASE1_MONSTRE] = Manag_phase_1_placement_monstre(
            affichage=self.affichage,
            manag_plateau=self.Management_secondaire[MANAG_PLATEAU],
            manag_aventurier=self.Management_secondaire[MANAG_AVENTURIER],
            manag_monstre=self.Management_secondaire[MANAG_MONSTRES_GLOBAL]
        )

        self.Management_secondaire[MANAG_PHASE2] = Manag_phase2(affichage=self.affichage,
                                                                manag_aventurier=self.Management_secondaire[MANAG_AVENTURIER],
                                                                manag_monstre_global=self.Management_secondaire[MANAG_MONSTRES_GLOBAL])

    def reinitialiser_partie(self):
        self.Management_secondaire[MANAG_PLATEAU].reinitialisation_plateau()
        self.Management_secondaire[MANAG_MONSTRES_GLOBAL].end_of_monster()
        self.Management_secondaire[MANAG_AVENTURIER].reinitialiser_aventurier()

    def sauvegarder_config(self):
        config = self.Management_secondaire[MANAG_PLATEAU].sauvegarder_config()
        print("\n================ CONFIGURATION DU PLATEAU ================")
        nb_pieces = 0
        for pos, info in sorted(config.items(), key=lambda item: (item[0][1], item[0][0])):
            if info[0] != 7:  # Différent de Cellule_vide
                nb_pieces += 1
                print(f"  Case {pos} -> Type pièce: {info[0]}, Orientation: {info[1]}")
        print(f"Total pièces non vides : {nb_pieces}")
        print("Dictionnaire complet de sauvegarde :")
        print(config)
        print("===========================================================\n")
        return config

    def ecran_debut(self):
        horloge = pygame.time.Clock()
        ecran = self.Management_secondaire[MANAG_PLATEAU].get_plateau().ecran
        selection = MODE_EXISTANT

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return QUITTER_JEU
                if evenement.type == pygame.KEYUP:
                    if evenement.key == pygame.K_UP:
                        if selection == MODE_EXISTANT:
                            selection = QUITTER_JEU
                        elif selection == AUTRE_MODE:
                            selection = MODE_EXISTANT
                        elif selection in (QUITTER_JEU, SAUVEGARDER_CONFIG):
                            selection = AUTRE_MODE
                    elif evenement.key == pygame.K_DOWN:
                        if selection == MODE_EXISTANT:
                            selection = AUTRE_MODE
                        elif selection == AUTRE_MODE:
                            selection = QUITTER_JEU
                        elif selection in (QUITTER_JEU, SAUVEGARDER_CONFIG):
                            selection = MODE_EXISTANT
                    elif evenement.key == pygame.K_LEFT:
                        if selection == SAUVEGARDER_CONFIG:
                            selection = QUITTER_JEU
                        elif selection == QUITTER_JEU:
                            selection = SAUVEGARDER_CONFIG
                    elif evenement.key == pygame.K_RIGHT:
                        if selection == QUITTER_JEU:
                            selection = SAUVEGARDER_CONFIG
                        elif selection == SAUVEGARDER_CONFIG:
                            selection = QUITTER_JEU
                    elif evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        return selection
                    elif evenement.key == pygame.K_ESCAPE:
                        return QUITTER_JEU

            self.affichage.dessiner_ecran_debut(
                ecran=ecran,
                selection=selection,
                options=OPTIONS_MENU_DEBUT,
            )
            horloge.tick(60)

    def jeu(self):
        while True:
            choix = self.ecran_debut()

            if choix == QUITTER_JEU:
                return False

            if choix == MODE_EXISTANT:
                self.reinitialiser_partie()
                res = self.Management_secondaire[MANAG_PHASE1].creation_plateau(self.Management_secondaire)
                if res == Var_global.QUIT:
                    print("Fin sans continuité du jeu")
                    return False
                elif res == Var_global.FIN_ESCAPE:
                    continue

                if not self.Management_secondaire[MANAG_PHASE2].jeu(self.Management_secondaire):
                    return False

            elif choix == AUTRE_MODE:
                self.reinitialiser_partie()
                res = self.Management_secondaire[MANAG_PHASE1_MONSTRE].mode_creation()
                if res == Var_global.QUIT:
                    print("Fin sans continuité du jeu")
                    return False
                elif res == Var_global.FIN_ESCAPE:
                    continue
                elif res == Var_global.CONTINUE:
                    if not self.Management_secondaire[MANAG_PHASE2].jeu(self.Management_secondaire):
                        return False

            elif choix == SAUVEGARDER_CONFIG:
                self.sauvegarder_config()

