from Classes_basiques.cellule import *
from Autres.Autre import (
    MANAG_AVENTURIER,
    MANAG_PLATEAU,
    MANAG_MONSTRES_GLOBAL,
    NB_OPTION_MAX,
    NB_PIECE_MAX,
    ARAIGNEE,
)

class Manag_phase1:
    def __init__(self, affichage, taille):
        self.affichage = affichage
        self.ens_piece_existante = [Tuile_depart(ligne=0, colonne=0, taille=taille),
                                    Tuile_arrivee(ligne=0, colonne=0, taille=taille),
                                    Couloir_horizontal(ligne=0, colonne=0, taille=taille),
                                    Couloir_vertical(ligne=0, colonne=0, taille=taille),
                                    [Couloir_coin(ligne=0, colonne=0, taille=taille, orientation=0),
                                Couloir_coin(ligne=0, colonne=0, taille=taille, orientation=1),
                                Couloir_coin(ligne=0, colonne=0, taille=taille, orientation=2),
                                Couloir_coin(ligne=0, colonne=0, taille=taille, orientation=3)],
                                    [Couloir_triangle(ligne=0, colonne=0, taille=taille, orientation=0),
                                Couloir_triangle(ligne=0, colonne=0, taille=taille, orientation=1),
                                Couloir_triangle(ligne=0, colonne=0, taille=taille, orientation=2),
                                Couloir_triangle(ligne=0, colonne=0, taille=taille, orientation=3)],
                                    [Cul_de_sac(ligne=0, colonne=0, taille=taille, orientation=0),
                                Cul_de_sac(ligne=0, colonne=0, taille=taille, orientation=1),
                                Cul_de_sac(ligne=0, colonne=0, taille=taille, orientation=2),
                                Cul_de_sac(ligne=0, colonne=0, taille=taille, orientation=3)]
                                    ]

    def creation_plateau(self, Management_secondaire):
        horloge = pygame.time.Clock()
        numero_option = 0
        pos_piece = [0, 0]
        orientation = 0
        self.update_pos(pos_piece)

        mode_ecriture = True
        selection_piece = 0
        res = ()

        en_cours = True
        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return False
                if evenement.type == pygame.KEYUP and evenement.key == pygame.K_SPACE:
                    if Management_secondaire[MANAG_PLATEAU].verifier_plateau():
                        if len(res) == 2:
                            Management_secondaire[MANAG_AVENTURIER].placer_aventurier_pos(res, pos_origine=True)
                        return True
                if evenement.type == pygame.KEYUP and evenement.key == pygame.K_a:
                    Management_secondaire[MANAG_PLATEAU].reinitialisation_plateau()
                    Management_secondaire[MANAG_MONSTRES_GLOBAL].end_of_monster()
                    mode_ecriture = False

                    if numero_option == 5:
                        res = Management_secondaire[MANAG_PLATEAU].creation_couloir_vertical()
                    elif numero_option == 1:
                        res = Management_secondaire[MANAG_PLATEAU].creation_couloir_zigzag()
                    elif numero_option == 2:
                        res = Management_secondaire[MANAG_PLATEAU].creation_long_couloir()
                    elif numero_option == 3:
                        res = Management_secondaire[MANAG_PLATEAU].creation_couloir_triangle()
                    elif numero_option == 4:
                        res = Management_secondaire[MANAG_PLATEAU].creation_couloir_cul_de_sac()
                    elif numero_option == 0:
                        res = Management_secondaire[MANAG_PLATEAU].creation_couloir_horizontal()
                        for x in [2, 4, 6, 7]:
                            Management_secondaire[MANAG_MONSTRES_GLOBAL].creation_nouveau_monstre(numero=ARAIGNEE,
                                                                                                  x=res[0] + x,
                                                                                                  y=res[1])
                    elif numero_option == 6:
                        dict_nouveau_donjon = {(0, 0): (4, 0), (0, 1): (3, 0), (0, 2): (3, 0), (0, 3): (0, 0), (0, 4): (3, 0), (0, 5): (3, 0), (0, 6): (3, 0), (0, 7): (4, 3), (1, 0): (5, 0), (1, 1): (6, 0), (1, 2): (6, 1), (1, 3): (2, 0), (1, 4): (4, 0), (1, 5): (4, 3), (1, 6): (6, 2), (1, 7): (5, 2), (2, 0): (5, 0), (2, 1): (6, 0), (2, 2): (2, 0), (2, 3): (2, 0), (2, 4): (2, 0), (2, 5): (2, 0), (2, 6): (6, 2), (2, 7): (5, 2), (3, 0): (5, 0), (3, 1): (6, 0), (3, 2): (2, 0), (3, 3): (2, 0), (3, 4): (2, 0), (3, 5): (2, 0), (3, 6): (6, 2), (3, 7): (5, 2), (4, 0): (5, 0), (4, 1): (6, 0), (4, 2): (7, 0), (4, 3): (2, 0), (4, 4): (2, 0), (4, 5): (2, 0), (4, 6): (6, 2), (4, 7): (5, 2), (5, 0): (5, 0), (5, 1): (6, 0), (5, 2): (2, 0), (5, 3): (2, 0), (5, 4): (2, 0), (5, 5): (2, 0), (5, 6): (6, 2), (5, 7): (5, 2), (6, 0): (5, 0), (6, 1): (6, 0), (6, 2): (2, 0), (6, 3): (2, 0), (6, 4): (2, 0), (6, 5): (2, 0), (6, 6): (6, 2), (6, 7): (5, 2), (7, 0): (5, 0), (7, 1): (6, 0), (7, 2): (6, 3), (7, 3): (2, 0), (7, 4): (2, 0), (7, 5): (6, 3), (7, 6): (6, 2), (7, 7): (5, 2), (8, 0): (5, 0), (8, 1): (4, 3), (8, 2): (6, 1), (8, 3): (2, 0), (8, 4): (2, 0), (8, 5): (6, 1), (8, 6): (4, 0), (8, 7): (5, 2), (9, 0): (1, 0), (9, 1): (1, 0), (9, 2): (1, 0), (9, 3): (1, 0), (9, 4): (1, 0), (9, 5): (1, 0), (9, 6): (1, 0), (9, 7): (1, 0)}
                        res = Management_secondaire[MANAG_PLATEAU].creation_dongeon_personnalise(dict_dongeon=dict_nouveau_donjon)
                    else:
                        mode_ecriture = True
                        selection_piece = 0
                        res = ()

                    numero_option = (numero_option+1)%NB_OPTION_MAX

                    if len(res) == 2:
                        Management_secondaire[MANAG_AVENTURIER].placer_aventurier_pos(res, pos_origine=True)

                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_p:
                    selection_piece = (selection_piece + 1)%NB_PIECE_MAX

                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_UP:
                    pos_piece[1] -= 1
                    if pos_piece[1] < 0:
                        pos_piece[1] = 0
                    self.update_pos(pos_piece)
                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_DOWN:
                    pos_piece[1] += 1
                    if pos_piece[1] >= Management_secondaire[MANAG_PLATEAU].Plateau.nb_cellule_ligne:
                        pos_piece[1] = Management_secondaire[MANAG_PLATEAU].Plateau.nb_cellule_ligne - 1

                    self.update_pos(pos_piece)
                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_LEFT:
                    pos_piece[0] -= 1
                    if pos_piece[0] < 0:
                        pos_piece[0] = 0
                    self.update_pos(pos_piece)
                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_RIGHT:
                    pos_piece[0] += 1
                    if pos_piece[0] >= Management_secondaire[MANAG_PLATEAU].Plateau.nb_cellule_colonne:
                        pos_piece[0] = Management_secondaire[MANAG_PLATEAU].Plateau.nb_cellule_colonne - 1
                    self.update_pos(pos_piece)

                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_m:
                    orientation = (orientation+1)%4

                if mode_ecriture and evenement.type == pygame.KEYUP and evenement.key == pygame.K_RETURN:
                    Management_secondaire[MANAG_PLATEAU].placement_piece(numero=selection_piece,
                                                                         orientation=orientation,
                                                                         pos=pos_piece)
                    if selection_piece == 0:
                        res = tuple(pos_piece)
                        if len(res) == 2:
                            Management_secondaire[MANAG_AVENTURIER].placer_aventurier_pos(res, pos_origine=True)
                    if len(res) == 2:
                        Management_secondaire[MANAG_PLATEAU].completer_tuile_depart()

            self.affichage.dessiner(manag_Plateau=Management_secondaire[MANAG_PLATEAU],
                                    manag_aventurier=Management_secondaire[MANAG_AVENTURIER],
                                    manag_monstre=Management_secondaire[MANAG_MONSTRES_GLOBAL]
                                    )
            if mode_ecriture:

                cellule_a_dessiner = self.ens_piece_existante[selection_piece]

                if isinstance(cellule_a_dessiner, list):
                    cellule_a_dessiner = cellule_a_dessiner[orientation]
                self.affichage.dessiner_curseur_pos(ecran=Management_secondaire[MANAG_PLATEAU].get_plateau().ecran,
                                                    cellule_a_dessiner=cellule_a_dessiner)

            horloge.tick(60)

        if len(res) == 2:
            Management_secondaire[MANAG_AVENTURIER].placer_aventurier_pos(res, pos_origine=True)

        return True

    def update_pos(self, pos):
        for une_piece in self.ens_piece_existante:
            if isinstance(une_piece, list):
                for une_vrai_piece in une_piece:
                    une_vrai_piece.changer_pos(pos=pos)
            else:
                une_piece.changer_pos(pos=pos)