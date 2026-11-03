import pygame

from Classes_basiques.Monstres import Araignee, Gobelin, Araignee_venimeuse
from Autres.Autre import ARAIGNEE, Etat_entitee, GOBELIN, ARAIGNEE_VENIMEUSE


class Manag_monstres_global:
    def __init__(self):
        self.ens_monstres_crees = {
            ARAIGNEE: [],
            GOBELIN: [],
            ARAIGNEE_VENIMEUSE: [],
        }

    def creer_objet_monstre(self, numero: int, x: int = 0, y: int = 0):
        if numero == ARAIGNEE:
            return Araignee(x=x, y=y, level=1)
        elif numero == GOBELIN:
            return Gobelin(x=x, y=y, level=1)
        elif numero == ARAIGNEE_VENIMEUSE:
            return Araignee_venimeuse(x=x, y=y, level=1)
        print("monstre non reconnu")
        return None

    def creation_nouveau_monstre(self, numero:int, x:int, y:int):
        monstre = self.creer_objet_monstre(numero=numero, x=x, y=y)
        if monstre is None:
            return False

        self.ens_monstres_crees[numero].append(monstre)
        return len(self.ens_monstres_crees[numero]) - 1

    def placer_monstre(self, type_monstre, nouvelle_pos, indice=None, ancienne_pos=None):
        if indice is not None:
            self.ens_monstres_crees[type_monstre][indice].get_position().changer_pos(pos=nouvelle_pos)
        else:
            for un_type in self.ens_monstres_crees.values():
                for un_monstre in un_type:
                    if un_monstre.get_position() == ancienne_pos:
                        un_monstre.get_position().changer_pos(pos=nouvelle_pos)

    def supprimer_monstre(self, type_monstre=None, indice=None, pos=None, monstre=None):
        if type_monstre is not None and indice is not None:
            del self.ens_monstres_crees[type_monstre][indice]
            return

        for un_type in self.ens_monstres_crees.values():
            for un_monstre in list(un_type):
                if un_monstre is monstre or (pos is not None and un_monstre.get_position() == pos):
                    un_type.remove(un_monstre)

    def end_of_monster(self):
        for un_type in self.ens_monstres_crees.values():
            un_type.clear()

    def get_list_monstre(self):
        return self.ens_monstres_crees

    def verif_case_occupee_par_monstre(self, pos):
        monstre_sur_pos = []
        for un_type, list_monstre in self.ens_monstres_crees.items():
            for un_monstre in list_monstre:
                if un_monstre.get_position() == pos:
                    monstre_sur_pos.append(un_monstre)

        return monstre_sur_pos

    def return_degat_infligee(self, pos, degat_infligee):
        degat_inflige_par_monstre = 0
        nb_monstre_frappe = 0
        nb_monstre_tue = 0
        for un_monstre in self.verif_case_occupee_par_monstre(pos=pos):
            un_monstre.perte_de_vie(quantitee=degat_infligee)
            if degat_infligee > 0:
                nb_monstre_frappe += 1

            # le monstre meurt
            if un_monstre.verifier_mort() == Etat_entitee.MORT:
                self.supprimer_monstre(monstre=un_monstre)
                nb_monstre_tue += 1

            # le monstre a eu le temps de recharger sa frappe
            elif pygame.time.get_ticks() - un_monstre.time_dernier_coup >= un_monstre.vitesse_frappe:
                    un_monstre.time_dernier_coup = pygame.time.get_ticks()
                    degat_inflige_par_monstre += un_monstre.get_degat_inflige()
                    un_monstre.diminution_endurance()

            # le monstre ne fait rien
            else:
                degat_inflige_par_monstre += 0

        return degat_inflige_par_monstre, nb_monstre_frappe, nb_monstre_tue

    def retour_spawn(self):
        for un_type, list_type in self.ens_monstres_crees.items():
            for un_monstre in list_type:
                un_monstre.regeneration()
