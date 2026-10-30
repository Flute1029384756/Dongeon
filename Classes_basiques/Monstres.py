from Autres.Autre import (
    SPRITES_GOBLIN,
    SPRITE_MONSTRE_DEFAUT,
    SPRITES_ARAIGNEE,
    PV_GOBELIN_DEFAUT,
    PV_ARAIGNEE_DEFAUT,
    DEGAT_GOBELIN_DEFAUT,
    DEGAT_ARAIGNEE_DEFAUT,
    VITESSE_FRAPPE_ARAIGNEE_DEFAUT,
    VITESSE_FRAPPE_GOBELIN_DEFAUT,
)
from Classes_basiques.Entitee import Entitee

class Monstres(Entitee):
    def __init__(self, pv:int, level:int, x:int, y:int,
                 degat_inflige:int, vitesse_frappe:int, endurance:int, consommation_arme:int):
        super().__init__(pv, level, x, y,
                         degat_inflige=degat_inflige, vitesse_frappe=vitesse_frappe, endurance=endurance, consommation_arme=consommation_arme)
        self.sprite = SPRITE_MONSTRE_DEFAUT

class Araignee(Monstres):
    def __init__(self, x:int, y:int, level:int):
        super().__init__(
            pv=PV_ARAIGNEE_DEFAUT,
            level=level,
            x=x,
            y=y,
            degat_inflige=DEGAT_ARAIGNEE_DEFAUT,
            vitesse_frappe=VITESSE_FRAPPE_ARAIGNEE_DEFAUT,
            endurance=10,
            consommation_arme=1
        )
        self.sprite = SPRITES_ARAIGNEE
        self.retourner_gauche = True

class Gobelin(Monstres):
    def __init__(self, x:int, y:int, level:int):
        super().__init__(
            pv=PV_GOBELIN_DEFAUT,
            level=level,
            x=x,
            y=y,
            degat_inflige=DEGAT_GOBELIN_DEFAUT,
            vitesse_frappe=VITESSE_FRAPPE_GOBELIN_DEFAUT,
            endurance=3,
            consommation_arme=1
            )
        self.sprite = SPRITES_GOBLIN
        self.retourner_gauche = True