import struct
import zlib
from pathlib import Path
import pygame
from Autres.Autre import (
    Color,
    DECALAGE_X,
    DECALAGE_Y,
    COIN_HAUT_GAUCHE,
    COIN_HAUT_DROIT,
    COIN_BAS_DROIT,
    COIN_BAS_GAUCHE,
    TRIANGLE_HAUT,
    TRIANGLE_DROIT,
    TRIANGLE_BAS,
    TRIANGLE_GAUCHE,
    HAUT,
    DROIT,
    BAS,
    GAUCHE,
    DOSSIER_TILESET,
    DOSSIER_FRAMES,
    NB_SOUS_TUILES,
    SPRITE_SOL,
    SPRITE_MUR,
    SPRITE_BORD_MUR,
    SPRITE_DEPART,
    SPRITE_ARRIVEE,
)


class Textures:
    _cache_images = {}
    _cache_tuiles = {}

    @staticmethod
    def _charger_png(chemin: Path) -> pygame.Surface:
        if pygame.image.get_extended():
            return pygame.image.load(str(chemin))

        donnees = chemin.read_bytes()
        pos = 8
        largeur = hauteur = 0
        color_type = 6
        idat = bytearray()
        while pos < len(donnees):
            longueur, type_chunk = struct.unpack(">I4s", donnees[pos:pos + 8])
            contenu = donnees[pos + 8:pos + 8 + longueur]
            pos += 12 + longueur
            if type_chunk == b"IHDR":
                largeur, hauteur, _, color_type = struct.unpack(">IIBB", contenu[:10])
            elif type_chunk == b"IDAT":
                idat.extend(contenu)
            elif type_chunk == b"IEND":
                break

        brut = zlib.decompress(bytes(idat))
        bpp = 3 if color_type == 2 else 4
        mode_couleur = "RGB" if color_type == 2 else "RGBA"
        stride = largeur * bpp
        pixels = bytearray(hauteur * stride)
        i = 0
        for y in range(hauteur):
            filtre = brut[i]
            i += 1
            ligne_debut = y * stride
            for x in range(stride):
                val = brut[i]
                i += 1
                a = pixels[ligne_debut + x - bpp] if x >= bpp else 0
                b = pixels[ligne_debut - stride + x] if y > 0 else 0
                c = pixels[ligne_debut - stride + x - bpp] if (x >= bpp and y > 0) else 0
                if filtre == 1:
                    val = (val + a) & 0xFF
                elif filtre == 2:
                    val = (val + b) & 0xFF
                elif filtre == 3:
                    val = (val + ((a + b) >> 1)) & 0xFF
                elif filtre == 4:
                    p = a + b - c
                    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                    pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                    val = (val + pr) & 0xFF
                pixels[ligne_debut + x] = val

        return pygame.image.frombytes(bytes(pixels), (largeur, hauteur), mode_couleur)

    @classmethod
    def get_image(cls, nom: str, taille: tuple[int, int], recadrer: bool = False,
                  retourner_gauche: bool = False) -> pygame.Surface:
        cle = (nom, taille, recadrer, retourner_gauche)
        if cle not in cls._cache_images:
            chemin = DOSSIER_FRAMES / f"{nom}.png"
            if not chemin.is_file():
                chemin = DOSSIER_TILESET / f"{nom}.png"
            image = cls._charger_png(chemin)
            if retourner_gauche:
                image = pygame.transform.flip(image, True, False)
            if recadrer:
                bbox = image.get_bounding_rect()
                if bbox.width > 0 and bbox.height > 0:
                    image = image.subsurface(bbox).copy()
            if pygame.display.get_surface() is not None:
                image = image.convert_alpha()
            cls._cache_images[cle] = pygame.transform.scale(image, taille)
        return cls._cache_images[cle]

    @classmethod
    def get_surface_tuile(cls, taille: int, ouvertures: tuple[bool, bool, bool, bool],
                          sprite_centre: str = None, couleur_cadre=None) -> pygame.Surface:
        cle = (taille, ouvertures, sprite_centre, couleur_cadre)
        if cle in cls._cache_tuiles:
            return cls._cache_tuiles[cle]

        ouvert_haut, ouvert_droit, ouvert_bas, ouvert_gauche = ouvertures
        nb = NB_SOUS_TUILES
        sous_taille = taille // nb

        surface = pygame.Surface((taille, taille), pygame.SRCALPHA)

        img_sol = cls.get_image(SPRITE_SOL, (sous_taille, sous_taille))
        img_mur = cls.get_image(SPRITE_MUR, (sous_taille, sous_taille)).copy()
        # Assombrit légèrement la brique du mur pour bien la distinguer du sol
        img_mur.fill((150, 150, 150, 255), special_flags=pygame.BLEND_RGBA_MULT)

        bord_bas = cls.get_image(SPRITE_BORD_MUR, (sous_taille, sous_taille))
        bord_haut = pygame.transform.flip(bord_bas, False, True)
        bord_droit = pygame.transform.rotate(bord_bas, 90)
        bord_gauche = pygame.transform.rotate(bord_bas, -90)

        def est_sol(gx: int, gy: int) -> bool:
            if gx in (1, 2) and gy in (1, 2):
                return True
            if gy == 0 and gx in (1, 2) and ouvert_haut:
                return True
            if gy == 3 and gx in (1, 2) and ouvert_bas:
                return True
            if gx == 0 and gy in (1, 2) and ouvert_gauche:
                return True
            if gx == 3 and gy in (1, 2) and ouvert_droit:
                return True
            return False

        for gy in range(nb):
            for gx in range(nb):
                pos_px = (gx * sous_taille, gy * sous_taille)
                if est_sol(gx, gy):
                    surface.blit(img_sol, pos_px)
                else:
                    surface.blit(img_mur, pos_px)
                    if gy + 1 < nb and est_sol(gx, gy + 1):
                        surface.blit(bord_bas, pos_px)
                    if gy - 1 >= 0 and est_sol(gx, gy - 1):
                        surface.blit(bord_haut, pos_px)
                    if gx + 1 < nb and est_sol(gx + 1, gy):
                        surface.blit(bord_droit, pos_px)
                    if gx - 1 >= 0 and est_sol(gx - 1, gy):
                        surface.blit(bord_gauche, pos_px)

        if sprite_centre is not None:
            img_centre = cls.get_image(sprite_centre, (sous_taille * 2, sous_taille * 2))
            surface.blit(img_centre, (sous_taille, sous_taille))

        if couleur_cadre is not None:
            pygame.draw.rect(surface, couleur_cadre, surface.get_rect(), 3)
        else:
            pygame.draw.rect(surface, (40, 35, 35), surface.get_rect(), 1)

        cls._cache_tuiles[cle] = surface
        return surface


class Cellule:
    def __init__(self, ligne, colonne, taille, couleur_fond=Color.NOIR, couleur_bord=Color.BLANC,
                 decalage_x=DECALAGE_X, decalage_y=DECALAGE_Y):
        self.taille = taille
        self.couleur_fond = couleur_fond
        self.couleur_bord = couleur_bord
        self.colonne = colonne
        self.ligne = ligne
        self.decalage_x = decalage_x
        self.decalage_y = decalage_y
        self.bloquee = False
        self.pos_tuile_suivante = []
        self.surface = None
        self.rect = pygame.Rect(
            self.decalage_x + colonne * taille,
            self.decalage_y + ligne * taille,
            taille,
            taille,
        )

    def get_ouvertures(self) -> tuple[bool, bool, bool, bool]:
        if not self.pos_tuile_suivante:
            return False, False, False, False
        return (
            (self.colonne, self.ligne - 1) in self.pos_tuile_suivante,
            (self.colonne + 1, self.ligne) in self.pos_tuile_suivante,
            (self.colonne, self.ligne + 1) in self.pos_tuile_suivante,
            (self.colonne - 1, self.ligne) in self.pos_tuile_suivante,
        )

    def construire_surface(self, sprite_centre: str = None, couleur_cadre=None):
        self.surface = Textures.get_surface_tuile(
            taille=self.taille,
            ouvertures=self.get_ouvertures(),
            sprite_centre=sprite_centre,
            couleur_cadre=couleur_cadre,
        )

    def dessiner(self, ecran):
        if self.surface is not None:
            ecran.blit(self.surface, self.rect)
        else:
            pygame.draw.rect(ecran, self.couleur_fond, self.rect)

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = []

    def changer_pos(self, pos: list):
        self.colonne = pos[0]
        self.ligne = pos[1]
        self.rect = pygame.Rect(
            self.decalage_x + self.colonne * self.taille,
            self.decalage_y + self.ligne * self.taille,
            self.taille,
            self.taille,
        )


class Cellule_vide(Cellule):
    def __init__(self, ligne, colonne, taille):
        super().__init__(ligne, colonne, taille)
        self.bloquee = True

    def dessiner(self, ecran):
        pass


class Tuile_depart(Cellule):
    def __init__(self, ligne, colonne, taille):
        super().__init__(ligne, colonne, taille)
        self.definir_pos_liee_f_orientation()
        self.construire_surface(sprite_centre=SPRITE_DEPART)

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = [
            (self.colonne + 1, self.ligne),
            (self.colonne - 1, self.ligne),
            (self.colonne, self.ligne + 1),
            (self.colonne, self.ligne - 1),
        ]


class Tuile_arrivee(Cellule):
    def __init__(self, ligne, colonne, taille):
        super().__init__(ligne, colonne, taille)
        self.definir_pos_liee_f_orientation()
        self.construire_surface(sprite_centre=SPRITE_ARRIVEE)

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = None

    def get_ouvertures(self) -> tuple[bool, bool, bool, bool]:
        return (True, True, True, True)


class Couloir_horizontal(Cellule):
    def __init__(self, ligne, colonne, taille):
        super().__init__(ligne, colonne, taille)
        self.definir_pos_liee_f_orientation()
        self.espacement_bord = 5
        self.construire_surface()

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = [
            (self.colonne + 1, self.ligne),
            (self.colonne - 1, self.ligne),
        ]


class Couloir_vertical(Cellule):
    def __init__(self, ligne, colonne, taille):
        super().__init__(ligne, colonne, taille)
        self.definir_pos_liee_f_orientation()
        self.espacement_bord = 5
        self.construire_surface()

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = [
            (self.colonne, self.ligne + 1),
            (self.colonne, self.ligne - 1),
        ]


class Couloir_coin(Cellule):
    def __init__(self, ligne, colonne, taille, orientation):
        super().__init__(ligne, colonne, taille)
        self.orientation = orientation
        self.espacement_bord = 5
        self.definir_pos_liee_f_orientation()
        self.construire_surface()

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = []
        if self.orientation == COIN_HAUT_GAUCHE:
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        elif self.orientation == COIN_HAUT_DROIT:
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
        elif self.orientation == COIN_BAS_DROIT:
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
        elif self.orientation == COIN_BAS_GAUCHE:
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        else:
            print("Error, coin non reconnu")
            exit()


class Couloir_triangle(Cellule):
    def __init__(self, ligne, colonne, taille, orientation):
        super().__init__(ligne, colonne, taille)
        self.orientation = orientation
        self.espacement_bord = 5
        self.definir_pos_liee_f_orientation()
        self.construire_surface()

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = []
        if self.orientation == TRIANGLE_HAUT:
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        elif self.orientation == TRIANGLE_DROIT:
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
        elif self.orientation == TRIANGLE_BAS:
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        elif self.orientation == TRIANGLE_GAUCHE:
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        else:
            print("Error, triangle non reconnu")
            exit()


class Cul_de_sac(Cellule):
    def __init__(self, ligne, colonne, taille, orientation):
        super().__init__(ligne, colonne, taille)
        self.orientation = orientation
        self.espacement_bord = 5
        self.definir_pos_liee_f_orientation()
        self.construire_surface()

    def definir_pos_liee_f_orientation(self):
        self.pos_tuile_suivante = []
        if self.orientation == HAUT:
            self.pos_tuile_suivante.append((self.colonne, self.ligne - 1))
        elif self.orientation == DROIT:
            self.pos_tuile_suivante.append((self.colonne + 1, self.ligne))
        elif self.orientation == BAS:
            self.pos_tuile_suivante.append((self.colonne, self.ligne + 1))
        elif self.orientation == GAUCHE:
            self.pos_tuile_suivante.append((self.colonne - 1, self.ligne))
        else:
            print("Error, cul de sac non reconnu")
            exit()
