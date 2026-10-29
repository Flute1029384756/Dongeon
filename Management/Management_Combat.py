from Classes_basiques.Monstres import Monstres
from Management.Management_Monstres_global import Manag_monstres_global
from Management.Management_aventurier import Manag_aventurier
from Autres.Autre import Etat_entitee

class Manag_combat:
    def __init__(self, manag_aventurier:Manag_aventurier, manag_monstre_global:Manag_monstres_global):
        self.manag_aventurier = manag_aventurier
        self.manag_monstre_global = manag_monstre_global

    def combat(self):
        pos_combat = self.manag_aventurier.get_aventurier().get_position()
        degat_inflige_par_aventurier = self.manag_aventurier.get_degat_inflige()
        degat_inflige_par_monstre, nb_monstre_frappe, nb_monstre_tue = self.manag_monstre_global.return_degat_infligee(pos=pos_combat,
                                                                                                    degat_infligee=degat_inflige_par_aventurier)

        self.manag_aventurier.gagner_experience(nb_monstre_frappe, nb_monstre_tue)


        if self.manag_aventurier.perte_de_vie(quantitee=degat_inflige_par_monstre) == Etat_entitee.MORT:
            return Etat_entitee.MORT

        return Etat_entitee.VIVANT
