import heapq
import pygame

from Classes_basiques.aventurier import Aventurier
from Management.Management_Plateau import Manag_Plateau, Tuille_arrivee
from Autres.Autre import Var_global, Etat_entitee, Action_aventurier


class Manag_aventurier:
    def __init__(self):
        level_max = 4
        list_augmentation_level = [10*x for x in range(1, level_max)]
        print(list_augmentation_level)
        self.dict_acion_xp_gagne = {
            Action_aventurier.DEPLACEMENT: 1,
            Action_aventurier.FRAPER: 1,
            Action_aventurier.TUER_MONSTRE: 2,
        }
        self.aventurier = Aventurier(colonne=0, ligne=0,
                                     list_xp_pour_level=list_augmentation_level,
                                     level_max=level_max)

    def get_aventurier(self):
        return self.aventurier

    def retour_spawn(self):
        self.aventurier.regeneration()
        self.placer_aventurier_pos(pos=self.aventurier.pos_origine.get_position())

    def placer_aventurier_pos(self, pos:tuple, teleportation:bool=True, pos_origine:bool=False):
        if teleportation:
            self.aventurier.get_pos_precedente().changer_pos(pos=pos)
            self.aventurier.en_deplacement_continu = False
            if pos_origine:
                self.aventurier.pos_origine.changer_pos(x=pos[0], y=pos[1])
        else:
            self.aventurier.temps_debut_deplacement = pygame.time.get_ticks()
            self.aventurier.en_deplacement_continu = True
        self.aventurier.get_position().changer_pos(pos=pos)

    def dijkstra(self, manag_plateau: Manag_Plateau):
        grille = manag_plateau.get_plateau().grille
        depart = self.aventurier.get_position().get_position()

        distances = {depart: 0}
        predecesseurs = {depart: None}
        file_priorite = [(0, depart)]
        visites = set()
        arrivee = None

        while file_priorite:
            dist_actuelle, pos_actuelle = heapq.heappop(file_priorite)

            if pos_actuelle in visites:
                continue
            visites.add(pos_actuelle)

            tuile_actuelle = grille.get(pos_actuelle)
            if tuile_actuelle is None:
                continue

            if isinstance(tuile_actuelle, Tuille_arrivee):
                arrivee = pos_actuelle
                break

            if not tuile_actuelle.pos_tuile_suivante:
                continue

            for voisin in tuile_actuelle.pos_tuile_suivante:
                if voisin in grille and not grille[voisin].bloquee and voisin not in visites:
                    tuile_voisine = grille[voisin]
                    if not isinstance(tuile_voisine, Tuille_arrivee) and (
                        not tuile_voisine.pos_tuile_suivante or pos_actuelle not in tuile_voisine.pos_tuile_suivante
                    ):
                        continue
                    nouvelle_dist = dist_actuelle + 1
                    if nouvelle_dist < distances.get(voisin, float('inf')):
                        distances[voisin] = nouvelle_dist
                        predecesseurs[voisin] = pos_actuelle
                        heapq.heappush(file_priorite, (nouvelle_dist, voisin))

        if arrivee is None:
            return []

        chemin = []
        courant = arrivee
        while courant is not None:
            chemin.append(courant)
            courant = predecesseurs[courant]
        chemin.reverse()
        return chemin

    def deplacer_aventurier(self, manag_plateau:Manag_Plateau, teleportation:bool=False):
        tuille_actuelle = manag_plateau.get_plateau().grille[self.aventurier.get_position()]
        if isinstance(tuille_actuelle, Tuille_arrivee):
            self.aventurier.activer_anim_idle()
            self.aventurier.en_deplacement_continu = False
            return Var_global.FIN_REUSSITE_AVENTURIER

        chemin = self.dijkstra(manag_plateau)
        if len(chemin) > 1:
            pos_actuelle = self.aventurier.get_position().get_position()
            prochaine_pos = chemin[1]
            if prochaine_pos[0] < pos_actuelle[0]:
                self.aventurier.retourner_gauche = True
            elif prochaine_pos[0] > pos_actuelle[0]:
                self.aventurier.retourner_gauche = False
            self.aventurier.activer_anim_run()
            self.aventurier.get_pos_precedente().changer_pos(pos=pos_actuelle)
            self.placer_aventurier_pos(prochaine_pos, teleportation=teleportation)

        self.aventurier.gagner_experience(self.dict_acion_xp_gagne[Action_aventurier.DEPLACEMENT])

        return Var_global.CONTINUE

    def perte_de_vie(self, quantitee=None, pourcentage=None):
        if not self.aventurier.perte_de_vie(quantitee, pourcentage):
            print("impossible aucun degat infligé à l'aventurier car pas de parametre")

        if self.aventurier.verifier_mort() == Etat_entitee.MORT:
            print("l'aventurier est mort")
            return Etat_entitee.MORT

        return Etat_entitee.VIVANT

    def get_degat_inflige(self):
        if pygame.time.get_ticks() - self.aventurier.time_dernier_coup >= self.aventurier.vitesse_frappe:
            self.aventurier.time_dernier_coup = pygame.time.get_ticks()
            return self.aventurier.get_degat_inflige()
        else:
            return 0

    def gagner_experience(self, nb_monstre_frappe, nb_monstre_tue):
        self.aventurier.gagner_experience(self.dict_acion_xp_gagne[Action_aventurier.FRAPER] * nb_monstre_frappe)
        self.aventurier.gagner_experience(self.dict_acion_xp_gagne[Action_aventurier.TUER_MONSTRE] * nb_monstre_tue)