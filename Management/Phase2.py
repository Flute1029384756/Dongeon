import pygame
from Autres.Autre import (
    Var_global,
    MANAG_AVENTURIER,
    MANAG_PLATEAU,
    MANAG_MONSTRES_GLOBAL,
    DELAI_ACTION,
    Etat_entitee
)
from Management.Management_Combat import Manag_combat


class Manag_phase2:
    def __init__(self, affichage, manag_aventurier, manag_monstre_global):
        self.affichage = affichage
        self.Manag_combat = Manag_combat(manag_aventurier=manag_aventurier,
                                         manag_monstre_global=manag_monstre_global)



    def jeu(self, Management_secondaire):
        horloge = pygame.time.Clock()
        dernier_tour = pygame.time.get_ticks()

        en_cours = True
        while en_cours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    return Var_global.QUIT
                if evenement.type == pygame.KEYUP and evenement.key == pygame.K_ESCAPE:
                    return Var_global.FIN_ESCAPE

            Management_secondaire[MANAG_AVENTURIER].actualiser_endurance()

            self.affichage.dessiner(manag_Plateau=Management_secondaire[MANAG_PLATEAU],
                                    manag_aventurier=Management_secondaire[MANAG_AVENTURIER],
                                    manag_monstre=Management_secondaire[MANAG_MONSTRES_GLOBAL])

            maintenant = pygame.time.get_ticks()
            if maintenant - dernier_tour >= DELAI_ACTION:
                dernier_tour = maintenant

                if len(Management_secondaire[MANAG_MONSTRES_GLOBAL].verif_case_occupee_par_monstre(Management_secondaire[MANAG_AVENTURIER].get_aventurier().get_position())) > 0:
                    if self.Manag_combat.combat() == Etat_entitee.MORT:
                        self.affichage.dessiner(manag_Plateau=Management_secondaire[MANAG_PLATEAU],
                                                manag_aventurier=Management_secondaire[MANAG_AVENTURIER],
                                                manag_monstre=Management_secondaire[MANAG_MONSTRES_GLOBAL])
                        return Var_global.FIN_DEFAITE_AVENTURIER
                else:
                    res = Management_secondaire[MANAG_AVENTURIER].deplacer_aventurier(
                        Management_secondaire[MANAG_PLATEAU])
                    if res == Var_global.FIN_REUSSITE_AVENTURIER:
                        print("L'aventurier a atteint la dernière case !")
                        en_cours = False

            horloge.tick(60)

        return Var_global.FIN_REUSSITE_AVENTURIER