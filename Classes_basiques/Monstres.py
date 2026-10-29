from Autres.Autre import (
    Color,
    SPRITE_MONSTRE_DEFAUT,
    SPRITES_ARAIGNEE,
    PV_ARAIGNEE_DEFAUT,
    TAILLE_ARAIGNEE_DEFAUT,
    DEGAT_ARAIGNEE_DEFAUT,
    VITESSE_FRAPPE_ARAIGNEE_DEFAUT,
)
from Classes_basiques.Entitee import Entitee

class Monstres(Entitee):
    def __init__(self, pv:int, level:int, taille:int, x:int, y:int, color:Color, degat_inflige:int, vitesse_frappe:int):
        super().__init__(pv, level, taille, x, y, couleur=color, degat_inflige=degat_inflige, vitesse_frappe=vitesse_frappe)
        self.sprite = SPRITE_MONSTRE_DEFAUT

class Araignee(Monstres):
    def __init__(self, x:int, y:int, level:int):
        super().__init__(
            pv=PV_ARAIGNEE_DEFAUT,
            level=level,
            taille=TAILLE_ARAIGNEE_DEFAUT,
            x=x,
            y=y,
            color=Color.BLUE,
            degat_inflige=DEGAT_ARAIGNEE_DEFAUT,
            vitesse_frappe=VITESSE_FRAPPE_ARAIGNEE_DEFAUT,
        )
        self.sprite = SPRITES_ARAIGNEE
        self.retourner_gauche = True