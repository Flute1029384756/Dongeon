import pygame
from Autres.Autre import Color, Position, SPRITE_ENTITEE_DEFAUT, DELAI_ANIMATION_SPRITE, Etat_entitee

class Entitee:
    def __init__(self, pv:int, level:int, taille:int, x:int, y:int, couleur:Color, degat_inflige:int, vitesse_frappe:int, sprite=SPRITE_ENTITEE_DEFAUT):
        self.pv = pv
        self.pv_max = pv
        self.level = level
        self.xp = level
        self.taille = taille
        self.couleur = couleur
        self.position = Position(x, y)
        self.pos_precedente = Position(x, y)
        self.sprite = sprite
        self.retourner_gauche = False
        self.temps_debut_deplacement = 0
        self.en_deplacement_continu = False
        self.degat_inflige = degat_inflige
        self.vitesse_frappe = vitesse_frappe
        self.time_dernier_coup = 0

    def get_pv(self):
        return self.pv

    def get_pv_max(self):
        return self.pv_max

    def get_level(self):
        return self.level

    def get_taille(self):
        return self.taille

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
        return self.degat_inflige

    def get_vitesse_frappe(self):
        return self.vitesse_frappe

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