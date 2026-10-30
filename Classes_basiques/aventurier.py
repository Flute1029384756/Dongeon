import pygame
from Autres.Autre import (
    Color,
    SPRITES_AVENTURIER_IDLE,
    SPRITES_AVENTURIER_RUN,
    SPRITES_AVENTURIER_HIT,
    PV_AVENTURIER_DEFAUT,
    LEVEL_AVENTURIER_DEFAUT,
    TAILLE_AVENTURIER_DEFAUT,
    DEGAT_AVENTURIER_DEFAUT,
    VITESSE_FRAPPE_AVENTURIER_DEFAUT, Position, Etat_entitee,
)
from Classes_basiques.Entitee import Entitee


class Aventurier(Entitee):
    def __init__(self, colonne:int, ligne:int, list_xp_pour_level:list[int], level_max:int):
        super().__init__(
            PV_AVENTURIER_DEFAUT,
            LEVEL_AVENTURIER_DEFAUT,
            TAILLE_AVENTURIER_DEFAUT,
            colonne,
            ligne,
            Color.BLANC,
            degat_inflige=DEGAT_AVENTURIER_DEFAUT,
            vitesse_frappe=VITESSE_FRAPPE_AVENTURIER_DEFAUT,
            endurance=5,
            consommation_arme=1
        )
        self.sprite = SPRITES_AVENTURIER_IDLE
        self.xp = 0
        self.list_xp_pour_level = list_xp_pour_level
        self.level_max = level_max
        self.pos_origine = Position(x=colonne, y=ligne)

    def activer_anim_idle(self):
        self.sprite = SPRITES_AVENTURIER_IDLE

    def activer_anim_run(self):
        self.sprite = SPRITES_AVENTURIER_RUN

    def activer_anim_hit(self):
        self.sprite = SPRITES_AVENTURIER_HIT

    def gagner_experience(self, xp):
        self.xp += xp
        if self.level < self.level_max and self.xp > self.list_xp_pour_level[self.level-1]:
            self.level += 1
            self.xp = 0
            return Etat_entitee.LEVEL_UP

        return Etat_entitee.RIEN_ANORMAL

    def get_ratio_xp(self):
        if self.level >= self.level_max or not self.list_xp_pour_level:
            return 1.0
        indice = max(0, min(self.level - 1, len(self.list_xp_pour_level) - 1))
        seuil_suivant = max(1, self.list_xp_pour_level[indice])
        return max(0.0, min(1.0, self.xp / seuil_suivant))

    def regeneration(self):
        self.pv = self.pv_max
        self.vitesse_frappe = self.meilleur_vitesse_frappe
        self.endurance = self.endurance_max
        self.temps_derniere_recup_endurance = pygame.time.get_ticks()

    def augmenter_statistique(self, pv_rajoute:int=0, degat:int=0, vitesse_frappe:int=0):
        self.pv += pv_rajoute
        self.pv_max += pv_rajoute

        self.degat_inflige += degat

        self.vitesse_frappe = self.meilleur_vitesse_frappe
        self.vitesse_frappe += vitesse_frappe
        self.meilleur_vitesse_frappe += vitesse_frappe
        self.vitesse_frappe_epuisement = self.vitesse_frappe * 1.5

        self.endurance = self.endurance_max
        self.temps_derniere_recup_endurance = pygame.time.get_ticks()