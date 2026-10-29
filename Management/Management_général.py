from Management.affichage import Affichage
from Management.Management_Plateau import Manag_Plateau
from Management.Management_aventurier import Manag_aventurier
from Management.Phase1 import Manag_phase1
from Management.Phase2 import Manag_phase2
from Management.Management_Monstres_global import Manag_monstres_global
from Autres.Autre import (
    MANAG_AVENTURIER,
    MANAG_PLATEAU,
    MANAG_PHASE1,
    MANAG_PHASE2,
    MANAG_MONSTRES_GLOBAL,
    MANAG_COMBAT,
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

        self.Management_secondaire[MANAG_PHASE2] = Manag_phase2(affichage=self.affichage,
                                                                manag_aventurier=self.Management_secondaire[MANAG_AVENTURIER],
                                                                manag_monstre_global=self.Management_secondaire[MANAG_MONSTRES_GLOBAL])



    def jeu(self):
        if not self.Management_secondaire[MANAG_PHASE1].creation_plateau(self.Management_secondaire):
            print("Fin sans continuité du jeu")
            return False

        return self.Management_secondaire[MANAG_PHASE2].jeu(self.Management_secondaire)
