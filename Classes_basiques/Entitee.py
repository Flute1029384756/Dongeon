import pygame
from Autres.Autre import (
    Color,
    Position,
    SPRITE_ENTITEE_DEFAUT,
    DELAI_ANIMATION_SPRITE,
    Etat_entitee,
    DELAI_RECUP_ENDURANCE,
)

class Entitee:
    def __init__(self, pv:int, level:int, x:int, y:int,
                 degat_inflige:int, vitesse_frappe:int, endurance:int, consommation_arme:int,
                 delai_recup_endurance:int=DELAI_RECUP_ENDURANCE,
                 sprite=SPRITE_ENTITEE_DEFAUT):
        self.pv = pv
        self.pv_max = pv
        self.level = level
        self.xp = level
        self.position = Position(x, y)
        self.pos_precedente = Position(x, y)
        self.sprite = sprite
        self.retourner_gauche = False
        self.temps_debut_deplacement = 0
        self.en_deplacement_continu = False
        self.degat_inflige = degat_inflige

        self.vitesse_frappe = vitesse_frappe
        self.meilleur_vitesse_frappe = vitesse_frappe
        self.vitesse_frappe_epuisement = vitesse_frappe * 1.5

        self.time_dernier_coup = 0
        self.endurance_max = endurance
        self.endurance = endurance
        self.consommation_arme = consommation_arme
        self.delai_recup_endurance = delai_recup_endurance
        self.temps_derniere_recup_endurance = 0

    def get_pv(self):
        return self.pv

    def get_pv_max(self):
        return self.pv_max

    def get_level(self):
        return self.level

    def get_position(self):
        return self.position

    def get_pos_precedente(self):
        return self.pos_precedente

    def get_sprite(self):
        if isinstance(self.sprite, list):
            indice = (pygame.time.get_ticks() // DELAI_ANIMATION_SPRITE) % len(self.sprite)
            return self.sprite[indice]
        return self.sprite

    def set_sprite(self, sprite):
        self.sprite = sprite

    def get_retourner_gauche(self):
        return self.retourner_gauche

    def perte_de_vie(self, quantitee=None, pourcentage=None):
        if quantitee is not None:
            self.pv -= quantitee
        elif pourcentage is not None:
            self.pv = self.pv * pourcentage/100
        else:
            return False

        return True

    def get_degat_inflige(self):
        if self.endurance <= 0:
            return self.degat_inflige // 2
        else:
            return self.degat_inflige

    def get_vitesse_frappe(self):
        return self.vitesse_frappe

    def get_endurance(self):
        return self.endurance

    def get_endurance_max(self):
        return self.endurance_max

    def get_ratio_cooldown(self):
        if self.vitesse_frappe <= 0 or self.time_dernier_coup <= 0:
            return 1.0
        temps_ecoule = pygame.time.get_ticks() - self.time_dernier_coup
        return max(0.0, min(1.0, temps_ecoule / self.vitesse_frappe))

    def verifier_mort(self):
        if self.pv <= 0:
            return Etat_entitee.MORT
        else:
            return Etat_entitee.VIVANT

    def diminution_endurance(self, endurance_diminuee=None, pourcentage=None):
        if endurance_diminuee is not None:
            self.endurance -= endurance_diminuee
        elif pourcentage is not None:
            self.endurance = self.endurance * pourcentage/100
        else:
            self.endurance -= self.consommation_arme

        if self.endurance <= 0:
            self.vitesse_frappe = self.vitesse_frappe_epuisement
            if self.endurance < 0:
                self.endurance = 0

    def recuperer_endurance(self, quantite: int = 1):
        if self.endurance < self.endurance_max:
            self.endurance = min(self.endurance_max, self.endurance + quantite)
            if self.endurance > 0:
                self.vitesse_frappe = self.meilleur_vitesse_frappe

    def actualiser_recuperation_endurance(self, maintenant=None):
        if maintenant is None:
            maintenant = pygame.time.get_ticks()

        if self.endurance >= self.endurance_max:
            self.temps_derniere_recup_endurance = maintenant
            return

        if self.temps_derniere_recup_endurance == 0:
            self.temps_derniere_recup_endurance = maintenant
            return

        if maintenant - self.temps_derniere_recup_endurance >= self.delai_recup_endurance:
            nb_points = (maintenant - self.temps_derniere_recup_endurance) // self.delai_recup_endurance
            self.recuperer_endurance(nb_points)
            self.temps_derniere_recup_endurance += nb_points * self.delai_recup_endurance

    def regeneration(self):
        self.pv = self.pv_max
        self.vitesse_frappe = self.meilleur_vitesse_frappe
        self.endurance = self.endurance_max
        self.temps_derniere_recup_endurance = pygame.time.get_ticks()