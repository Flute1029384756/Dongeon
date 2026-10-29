from pathlib import Path

# Coordonnées
COLONNE = 0
LIGNE = 1

# Dimensions et fenêtre
LARGEUR_GRILLE = 1000
HAUTEUR_GRILLE = 800
LARGEUR = LARGEUR_GRILLE
HAUTEUR = HAUTEUR_GRILLE
LARGEUR_FENETRE = 1600
HAUTEUR_FENETRE = 800
DECALAGE_X = (LARGEUR_FENETRE - LARGEUR_GRILLE) // 2
DECALAGE_Y = (HAUTEUR_FENETRE - HAUTEUR_GRILLE) // 2
TAILLE_GRILLE_MAX = 10
TITRE = "Test Donjon"
DELAI_ACTION = 500
RATIO_DECALAGE_COMBAT = 0.30

# Tileset et sprites
DOSSIER_TILESET = Path(__file__).resolve().parent.parent / "Tileset"
DOSSIER_FRAMES = DOSSIER_TILESET / "0x72_DungeonTilesetII_v1.7" / "frames"
NB_SOUS_TUILES = 4
DELAI_ANIMATION_SPRITE = 150
SPRITE_SOL = "floor_1"
SPRITE_MUR = "wall_mid"
SPRITE_BORD_MUR = "wall_top_mid"
SPRITE_DEPART = "floor_ladder"
SPRITE_ARRIVEE = "floor_stairs"
SPRITE_COEUR_PLEIN = "ui_heart_full"
SPRITE_COEUR_DEMI = "ui_heart_half"
SPRITE_COEUR_VIDE = "ui_heart_empty"
SPRITE_EPEE = "weapon_knight_sword"
SPRITE_ENTITEE_DEFAUT = "knight_m_idle_anim_f0"
SPRITES_AVENTURIER_IDLE = [
    "knight_m_idle_anim_f0",
    "knight_m_idle_anim_f1",
    "knight_m_idle_anim_f2",
    "knight_m_idle_anim_f3",
]
SPRITES_AVENTURIER_RUN = [
    "knight_m_run_anim_f0",
    "knight_m_run_anim_f1",
    "knight_m_run_anim_f2",
    "knight_m_run_anim_f3",
]
SPRITES_AVENTURIER_HIT = [
    "knight_m_hit_anim_f0",
]
SPRITE_AVENTURIER = SPRITES_AVENTURIER_IDLE
SPRITE_MONSTRE_DEFAUT = "imp_idle_anim_f0"
SPRITES_ARAIGNEE = [
    "SpiderPack/IdleOrange2/SpiderIdleSide1",
    "SpiderPack/IdleOrange2/SpiderIdleSide2",
    "SpiderPack/IdleOrange2/SpiderIdleSide3",
    "SpiderPack/IdleOrange2/SpiderIdleSide4",
]

# Identifiants des managers
MANAG_AVENTURIER = 0
MANAG_PLATEAU = 1
MANAG_PHASE1 = 2
MANAG_PHASE2 = 3
MANAG_MONSTRES_GLOBAL = 4
MANAG_COMBAT = 5

# Options du menu de début
MODE_EXISTANT = 0
AUTRE_MODE = 1
QUITTER_JEU = 2
SAUVEGARDER_CONFIG = 3
OPTIONS_MENU_DEBUT = [
    "MODE EXISTANT",
    "AUTRE MODE",
    "QUITTER LE JEU",
    "SAUVEGARDER CONFIG",
]

# Options et types de pièces
NB_OPTION_MAX = 8
NB_PIECE_MAX = 7
DEPART = 0
ARRIVEE = 1
COULOIR_HORIZONTAL = 2
COULOIR_VERTICAL = 3
COIN = 4
TRIANGLE = 5
CUL_DE_SAC = 6
CELLULE_VIDE = 7

# Orientations des tuiles
COIN_HAUT_GAUCHE, TRIANGLE_HAUT, HAUT = 0, 0, 0
COIN_HAUT_DROIT, TRIANGLE_DROIT, DROIT = 1, 1, 1
COIN_BAS_DROIT, TRIANGLE_BAS, BAS = 2, 2, 2
COIN_BAS_GAUCHE, TRIANGLE_GAUCHE, GAUCHE = 3, 3, 3

# Types de monstres
ARAIGNEE = 0

# Statistiques de base des entités
PV_AVENTURIER_DEFAUT = 10
LEVEL_AVENTURIER_DEFAUT = 1
TAILLE_AVENTURIER_DEFAUT = 20
DEGAT_AVENTURIER_DEFAUT = 2
VITESSE_FRAPPE_AVENTURIER_DEFAUT = 1000

STAT_PV = 0
STAT_DEGAT = 1
STAT_VITESSE_FRAPPE = 2

PV_ARAIGNEE_DEFAUT = 12
TAILLE_ARAIGNEE_DEFAUT = 5
DEGAT_ARAIGNEE_DEFAUT = 3
VITESSE_FRAPPE_ARAIGNEE_DEFAUT = 1500

class Position:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def changer_pos(self, x=None, y=None, pos=None):
        if pos:
            self.x = pos[0]
            self.y = pos[1]
            return
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return (self.x, self.y) == (other.x, other.y)
        if isinstance(other, tuple) and len(other) == 2:
            return (self.x, self.y) == other
        return False

    def __hash__(self):
        return hash((self.x, self.y))


class Color:
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    LIME_GREEN = (50, 205, 50)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

class Var_global:
    CONTINUE = 0
    FIN_REUSSITE_AVENTURIER = 1
    FIN_ESCAPE = 2
    FIN_PHASE_1 = 3
    QUIT = 4

class Etat_entitee:
    # Etat entitée
    MORT = 0
    VIVANT = 1
    LEVEL_UP = 2
    RIEN_ANORMAL = 3

class Action_aventurier:
    DEPLACEMENT = 0
    FRAPER = 1
    TUER_MONSTRE = 2
    MOURIR = 3