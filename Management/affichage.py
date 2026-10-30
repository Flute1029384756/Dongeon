
import math
import pygame
from Autres.Autre import (
    COLONNE,
    LIGNE,
    Color,
    RATIO_DECALAGE_COMBAT,
    DELAI_ACTION,
    SPRITE_COEUR_PLEIN,
    SPRITE_COEUR_VIDE,
    SPRITE_EPEE,
    SPRITES_AVENTURIER_IDLE,
    DELAI_ANIMATION_SPRITE,
    OPTIONS_MENU_DEBUT,
    OPTIONS_CHOIX_NIVEAU,
    RETOUR_MENU,
    TITRE,
)
from Classes_basiques.cellule import Textures
from Management.Management_Monstres_global import Manag_monstres_global
from Management.Management_Plateau import Manag_Plateau
from Management.Management_aventurier import Manag_aventurier


GLYPHES_PIXEL = {
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "001", "001", "001"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
    "/": ["001", "001", "010", "100", "100"],
    ":": ["000", "010", "000", "010", "000"],
    "-": ["000", "000", "111", "000", "000"],
    ">": ["100", "010", "001", "010", "100"],
    "<": ["001", "010", "100", "010", "001"],
    "A": ["010", "101", "111", "101", "101"],
    "B": ["110", "101", "110", "101", "110"],
    "C": ["111", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "G": ["111", "100", "101", "101", "111"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "J": ["001", "001", "001", "101", "111"],
    "K": ["101", "101", "110", "101", "101"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "101", "101", "101"],
    "N": ["101", "111", "111", "101", "101"],
    "O": ["111", "101", "101", "101", "111"],
    "P": ["111", "101", "111", "100", "100"],
    "Q": ["111", "101", "101", "111", "001"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["111", "100", "111", "001", "111"],
    "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "101", "111", "101"],
    "X": ["101", "101", "010", "101", "101"],
    "Y": ["101", "101", "010", "010", "010"],
    "Z": ["111", "001", "010", "100", "111"],
    ".": ["000", "000", "000", "000", "010"],
    " ": ["000", "000", "000", "000", "000"],
}


class Affichage:
    def _dessiner_texte_pixel(self, ecran, texte: str, x: int, y: int, taille_pixel: int = 3, couleur=Color.BLANC):
        curseur_x = x
        for caractere in texte.upper():
            motif = GLYPHES_PIXEL.get(caractere)
            if motif:
                for lig_idx, ligne in enumerate(motif):
                    for col_idx, bit in enumerate(ligne):
                        if bit == "1":
                            pygame.draw.rect(
                                ecran,
                                couleur,
                                (
                                    curseur_x + col_idx * taille_pixel,
                                    y + lig_idx * taille_pixel,
                                    taille_pixel,
                                    taille_pixel,
                                ),
                            )
            curseur_x += 4 * taille_pixel

    def _dessiner_icone_vitesse(self, ecran, cx: int, cy: int):
        # Symbole d'éclair doré pour représenter la vitesse d'attaque
        points_eclair = [
            (cx + 3, cy - 11),
            (cx - 7, cy + 1),
            (cx - 1, cy + 1),
            (cx - 4, cy + 11),
            (cx + 7, cy - 1),
            (cx + 1, cy - 1),
        ]
        pygame.draw.polygon(ecran, (255, 215, 70), points_eclair)
        pygame.draw.polygon(ecran, Color.BLANC, points_eclair, width=1)

    def _dessiner_cooldown_circulaire(self, ecran, cx: int, cy: int, rayon: int, ratio: float):
        ratio = max(0.0, min(1.0, ratio))
        pygame.draw.circle(ecran, (26, 22, 32), (cx, cy), rayon)

        if ratio >= 1.0:
            pygame.draw.circle(ecran, (70, 215, 120), (cx, cy), rayon - 2)
        elif ratio > 0.0:
            nb_segments = max(3, int(36 * ratio))
            angle_depart = -math.pi / 2
            points = [(cx, cy)]
            for i in range(nb_segments + 1):
                angle = angle_depart + (2 * math.pi * ratio) * (i / nb_segments)
                px = cx + (rayon - 2) * math.cos(angle)
                py = cy + (rayon - 2) * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(ecran, (65, 175, 245), points)

            angle_fin = angle_depart + 2 * math.pi * ratio
            x_aiguille = cx + (rayon - 2) * math.cos(angle_fin)
            y_aiguille = cy + (rayon - 2) * math.sin(angle_fin)
            pygame.draw.line(ecran, Color.BLANC, (cx, cy), (x_aiguille, y_aiguille), 2)

        pygame.draw.circle(ecran, Color.BLANC, (cx, cy), rayon, width=2)
        pygame.draw.circle(ecran, Color.BLANC, (cx, cy), 2)

    def _dessiner_barre_xp_minecraft(self, ecran, x: int, y: int, largeur: int, hauteur: int, ratio: float):
        ratio = max(0.0, min(1.0, ratio))
        rect_fond = pygame.Rect(x, y, largeur, hauteur)

        # Fond sombre style barre d'XP Minecraft
        pygame.draw.rect(ecran, (18, 30, 14), rect_fond, border_radius=3)

        if ratio > 0.0:
            largeur_interieure = max(2, int((largeur - 4) * ratio))
            rect_xp = pygame.Rect(x + 2, y + 2, largeur_interieure, hauteur - 4)
            pygame.draw.rect(ecran, (128, 255, 32), rect_xp, border_radius=2)

            # Reflet clair sur le haut et ombre verte en bas (effet pixel Minecraft)
            if largeur_interieure > 2:
                pygame.draw.rect(
                    ecran,
                    (190, 255, 120),
                    (x + 2, y + 2, largeur_interieure, max(2, (hauteur - 4) // 3)),
                )
                pygame.draw.rect(
                    ecran,
                    (70, 170, 18),
                    (x + 2, y + hauteur - 4, largeur_interieure, 2),
                )

        # Graduations verticales façon barre d'XP Minecraft
        nb_segments = 8
        for i in range(1, nb_segments):
            x_sep = x + int(i * largeur / nb_segments)
            pygame.draw.line(
                ecran,
                (18, 30, 14),
                (x_sep, y + 2),
                (x_sep, y + hauteur - 3),
                1,
            )

        pygame.draw.rect(ecran, (165, 220, 140), rect_fond, width=1, border_radius=3)

    def _dessiner_icone_endurance(self, ecran, cx: int, cy: int):
        # Symbole d'énergie / flamme d'endurance
        points_endurance = [
            (cx, cy - 10),
            (cx + 6, cy - 3),
            (cx + 7, cy + 3),
            (cx + 4, cy + 9),
            (cx, cy + 11),
            (cx - 4, cy + 9),
            (cx - 7, cy + 3),
            (cx - 6, cy - 3),
        ]
        pygame.draw.polygon(ecran, (245, 185, 45), points_endurance)
        pygame.draw.polygon(ecran, Color.BLANC, points_endurance, width=1)
        pygame.draw.circle(ecran, (255, 235, 140), (cx, cy + 2), 2)

    def _dessiner_barre_endurance(self, ecran, x: int, y: int, largeur: int, hauteur: int, endurance: int, endurance_max: int):
        endurance_max = max(1, endurance_max)
        ratio = max(0.0, min(1.0, max(0, endurance) / endurance_max))
        rect_fond = pygame.Rect(x, y, largeur, hauteur)

        pygame.draw.rect(ecran, (35, 25, 20), rect_fond, border_radius=4)

        if ratio > 0.0:
            if ratio > 0.35:
                couleur_barre = (245, 185, 45)
                couleur_reflet = (255, 230, 120)
            elif ratio > 0.15:
                couleur_barre = (235, 130, 35)
                couleur_reflet = (255, 180, 80)
            else:
                couleur_barre = (215, 55, 55)
                couleur_reflet = (250, 110, 110)

            largeur_remplie = max(3, int((largeur - 4) * ratio))
            rect_end = pygame.Rect(x + 2, y + 2, largeur_remplie, hauteur - 4)
            pygame.draw.rect(ecran, couleur_barre, rect_end, border_radius=3)

            reflet = pygame.Rect(x + 3, y + 3, max(0, largeur_remplie - 2), max(2, (hauteur - 4) // 3))
            pygame.draw.rect(ecran, couleur_reflet, reflet, border_radius=1)

        # Graduations par point d'endurance
        if 1 < endurance_max <= 20:
            for i in range(1, endurance_max):
                x_sep = x + int(i * largeur / endurance_max)
                pygame.draw.line(
                    ecran,
                    (25, 18, 15),
                    (x_sep, y + 2),
                    (x_sep, y + hauteur - 3),
                    1,
                )

        couleur_bord = Color.BLANC if endurance > 0 else (210, 80, 80)
        pygame.draw.rect(ecran, couleur_bord, rect_fond, width=1, border_radius=4)

    def dessiner_profil_entitee(
        self,
        ecran,
        entitee,
        x_zone: int,
        largeur_zone: int,
        y_depart: int = 16,
        taille_sprite: tuple[int, int] = (52, 68),
        retourner_gauche: bool = False,
    ):
        marge = 16
        largeur_panneau = max(200, largeur_zone - 2 * marge)
        hauteur_panneau = 248
        panneau_rect = pygame.Rect(x_zone + marge, y_depart, largeur_panneau, hauteur_panneau)

        # Fond et bordure du panneau de profil
        pygame.draw.rect(ecran, (28, 25, 32), panneau_rect, border_radius=8)
        pygame.draw.rect(ecran, (190, 180, 200), panneau_rect, width=2, border_radius=8)

        # Cadre de l'image de l'entité
        taille_cadre_avatar = 88
        cadre_avatar = pygame.Rect(
            panneau_rect.x + 12,
            panneau_rect.y + 12,
            taille_cadre_avatar,
            taille_cadre_avatar,
        )
        pygame.draw.rect(ecran, (48, 42, 54), cadre_avatar, border_radius=6)
        pygame.draw.rect(ecran, Color.BLANC, cadre_avatar, width=2, border_radius=6)

        img_profil = Textures.get_image(
            entitee.get_sprite(),
            taille_sprite,
            recadrer=True,
            retourner_gauche=retourner_gauche,
        )
        ecran.blit(img_profil, img_profil.get_rect(center=cadre_avatar.center))

        # Zone d'informations (Level, PV et barre de vie) à droite de l'avatar
        x_info = cadre_avatar.right + 14
        largeur_barre = panneau_rect.right - x_info - 14
        pv_actuels = max(0, entitee.get_pv())
        pv_max = max(1, entitee.get_pv_max())
        level = entitee.get_level()
        degat = entitee.get_degat_inflige()
        vitesse_ms = entitee.get_vitesse_frappe()
        ratio_cooldown = entitee.get_ratio_cooldown()
        ratio_pv = max(0.0, min(1.0, pv_actuels / pv_max))
        endurance = entitee.get_endurance() if hasattr(entitee, "get_endurance") else getattr(entitee, "endurance", 0)
        endurance_max = entitee.get_endurance_max() if hasattr(entitee, "get_endurance_max") else getattr(entitee, "endurance_max", 1)

        # Affichage du Level (et barre d'XP style Minecraft à côté si l'entité possède de l'XP)
        a_barre_xp = hasattr(entitee, "get_ratio_xp")
        if a_barre_xp:
            texte_level = f"LVL:{level}"
            taille_px_lvl = 2
            y_level = cadre_avatar.top + 4
            self._dessiner_texte_pixel(
                ecran,
                texte_level,
                x_info,
                y_level,
                taille_pixel=taille_px_lvl,
                couleur=(128, 255, 32),
            )
            largeur_texte_lvl = len(texte_level) * 4 * taille_px_lvl
            x_barre_xp = x_info + largeur_texte_lvl + 6
            largeur_barre_xp = max(30, panneau_rect.right - x_barre_xp - 14)
            self._dessiner_barre_xp_minecraft(
                ecran,
                x_barre_xp,
                cadre_avatar.top + 2,
                largeur_barre_xp,
                14,
                entitee.get_ratio_xp(),
            )
        else:
            texte_level = f"LVL : {level}"
            y_level = cadre_avatar.top + 2
            self._dessiner_texte_pixel(
                ecran,
                texte_level,
                x_info,
                y_level,
                taille_pixel=3,
                couleur=(255, 215, 80),
            )

        # Icône de coeur + texte PV
        sprite_coeur = SPRITE_COEUR_PLEIN if pv_actuels > 0 else SPRITE_COEUR_VIDE
        img_coeur = Textures.get_image(sprite_coeur, (22, 20))
        y_coeur = cadre_avatar.top + 28
        ecran.blit(img_coeur, (x_info, y_coeur))

        texte_pv = f"PV : {pv_actuels}/{pv_max}"
        espace_texte_dispo = largeur_barre - 28
        taille_pixel = 3 if len(texte_pv) * 4 * 3 <= espace_texte_dispo else 2
        decalage_y_texte = 3 if taille_pixel == 3 else 5
        self._dessiner_texte_pixel(
            ecran,
            texte_pv,
            x_info + 28,
            y_coeur + decalage_y_texte,
            taille_pixel=taille_pixel,
            couleur=Color.BLANC,
        )

        # Barre de vie
        hauteur_barre = 26
        y_barre = cadre_avatar.bottom - hauteur_barre - 2
        barre_fond_rect = pygame.Rect(x_info, y_barre, largeur_barre, hauteur_barre)
        pygame.draw.rect(ecran, (50, 20, 24), barre_fond_rect, border_radius=5)

        if ratio_pv > 0:
            if ratio_pv > 0.5:
                couleur_barre = (55, 200, 75)
                couleur_reflet = (110, 235, 125)
            elif ratio_pv > 0.25:
                couleur_barre = (230, 155, 35)
                couleur_reflet = (250, 195, 90)
            else:
                couleur_barre = (215, 45, 45)
                couleur_reflet = (245, 100, 100)

            largeur_remplie = max(4, int((largeur_barre - 4) * ratio_pv))
            barre_vie_rect = pygame.Rect(x_info + 2, y_barre + 2, largeur_remplie, hauteur_barre - 4)
            pygame.draw.rect(ecran, couleur_barre, barre_vie_rect, border_radius=4)

            reflet_rect = pygame.Rect(x_info + 4, y_barre + 4, max(0, largeur_remplie - 4), 5)
            if reflet_rect.width > 0:
                pygame.draw.rect(ecran, couleur_reflet, reflet_rect, border_radius=2)

        # Graduations par point de vie
        if 1 < pv_max <= 20:
            for i in range(1, pv_max):
                x_sep = x_info + int(i * largeur_barre / pv_max)
                pygame.draw.line(
                    ecran,
                    (28, 25, 32),
                    (x_sep, y_barre + 2),
                    (x_sep, y_barre + hauteur_barre - 3),
                    2,
                )

        pygame.draw.rect(ecran, Color.BLANC, barre_fond_rect, width=2, border_radius=5)

        # Case des dégâts avec symbole d'épée
        hauteur_case_degat = 36
        case_degat_rect = pygame.Rect(
            panneau_rect.x + 12,
            cadre_avatar.bottom + 10,
            largeur_panneau - 24,
            hauteur_case_degat,
        )
        pygame.draw.rect(ecran, (44, 38, 50), case_degat_rect, border_radius=6)
        pygame.draw.rect(ecran, (175, 165, 190), case_degat_rect, width=2, border_radius=6)

        img_epee = Textures.get_image(SPRITE_EPEE, (12, 26), recadrer=True)
        img_epee_inclinee = pygame.transform.rotate(img_epee, -45)
        ecran.blit(
            img_epee_inclinee,
            img_epee_inclinee.get_rect(center=(case_degat_rect.x + 22, case_degat_rect.centery)),
        )

        texte_degat = f"DEG : {degat}"
        self._dessiner_texte_pixel(
            ecran,
            texte_degat,
            case_degat_rect.x + 42,
            case_degat_rect.centery - 7,
            taille_pixel=3,
            couleur=Color.BLANC,
        )

        # Case de la vitesse d'attaque avec symbole et cooldown circulaire
        hauteur_case_vitesse = 38
        case_vitesse_rect = pygame.Rect(
            panneau_rect.x + 12,
            case_degat_rect.bottom + 8,
            largeur_panneau - 24,
            hauteur_case_vitesse,
        )
        pygame.draw.rect(ecran, (44, 38, 50), case_vitesse_rect, border_radius=6)
        pygame.draw.rect(ecran, (175, 165, 190), case_vitesse_rect, width=2, border_radius=6)

        self._dessiner_icone_vitesse(ecran, case_vitesse_rect.x + 22, case_vitesse_rect.centery)

        vitesse_sec = vitesse_ms / 1000
        texte_vitesse = (
            f"VIT : {int(vitesse_sec)}S"
            if vitesse_sec.is_integer()
            else f"VIT : {vitesse_sec:.1f}S"
        )
        self._dessiner_texte_pixel(
            ecran,
            texte_vitesse,
            case_vitesse_rect.x + 42,
            case_vitesse_rect.centery - 7,
            taille_pixel=3,
            couleur=Color.BLANC,
        )

        self._dessiner_cooldown_circulaire(
            ecran,
            case_vitesse_rect.right - 22,
            case_vitesse_rect.centery,
            rayon=13,
            ratio=ratio_cooldown,
        )

        # Case de l'endurance avec jauge d'énergie
        hauteur_case_endurance = 38
        case_endurance_rect = pygame.Rect(
            panneau_rect.x + 12,
            case_vitesse_rect.bottom + 8,
            largeur_panneau - 24,
            hauteur_case_endurance,
        )
        pygame.draw.rect(ecran, (44, 38, 50), case_endurance_rect, border_radius=6)
        bord_case_end = (175, 165, 190) if endurance > 0 else (210, 80, 80)
        pygame.draw.rect(ecran, bord_case_end, case_endurance_rect, width=2, border_radius=6)

        self._dessiner_icone_endurance(ecran, case_endurance_rect.x + 22, case_endurance_rect.centery)

        texte_end = f"END : {max(0, endurance)}/{endurance_max}"
        couleur_texte_end = Color.BLANC if endurance > 0 else (240, 90, 90)
        self._dessiner_texte_pixel(
            ecran,
            texte_end,
            case_endurance_rect.x + 40,
            case_endurance_rect.centery - 5,
            taille_pixel=2,
            couleur=couleur_texte_end,
        )

        x_barre_end = case_endurance_rect.x + 130
        largeur_barre_end = max(40, case_endurance_rect.right - x_barre_end - 12)
        self._dessiner_barre_endurance(
            ecran,
            x_barre_end,
            case_endurance_rect.centery - 8,
            largeur_barre_end,
            16,
            endurance,
            endurance_max,
        )

    def dessiner_profil_aventurier(self, ecran, aventurier, largeur_zone: int):
        self.dessiner_profil_entitee(
            ecran=ecran,
            entitee=aventurier,
            x_zone=0,
            largeur_zone=largeur_zone,
            y_depart=16,
            taille_sprite=(52, 68),
            retourner_gauche=False,
        )

    def dessiner_profil_monstres_combat(self, ecran, monstres_combattus: list, x_zone: int, largeur_zone: int):
        for idx, monstre in enumerate(monstres_combattus):
            self.dessiner_profil_entitee(
                ecran=ecran,
                entitee=monstre,
                x_zone=x_zone,
                largeur_zone=largeur_zone,
                y_depart=16 + idx * 262,
                taille_sprite=(58, 50),
                retourner_gauche=monstre.get_retourner_gauche(),
            )

    def dessiner_aide_placement_monstre(self, ecran, x_zone: int, largeur_zone: int, y_depart: int = 278):
        pygame.draw.line(
            ecran,
            (85, 76, 105),
            (x_zone + 28, y_depart),
            (x_zone + largeur_zone - 28, y_depart),
            2,
        )

        lignes_aide = [
            "FLECHE BAS :",
            "CHANGER DE MONSTRE",
        ]
        taille_px_aide = 3
        y_texte = y_depart + 14
        for ligne in lignes_aide:
            largeur_ligne = self._largeur_texte_pixel(ligne, taille_px_aide)
            x_texte = x_zone + (largeur_zone - largeur_ligne) // 2
            self._dessiner_texte_pixel(
                ecran,
                ligne,
                x_texte,
                y_texte,
                taille_pixel=taille_px_aide,
                couleur=(170, 160, 190),
            )
            y_texte += 5 * taille_px_aide + 9

    def dessiner(self, manag_Plateau: Manag_Plateau, manag_aventurier: Manag_aventurier,
                 manag_monstre: Manag_monstres_global, monstres_a_afficher: list = None):
        # fond cellule
        aventurier = manag_aventurier.get_aventurier()
        plateau = manag_Plateau.get_plateau()
        ecran = plateau.ecran
        taille_cellule = plateau.taille_cellule
        ecran.fill(Color.NOIR)
        for cellule in plateau.grille.values():
            cellule.dessiner(ecran)

        pos_aventurier = aventurier.get_position().get_position()
        pos_prec = aventurier.get_pos_precedente().get_position()
        dx_origine = pos_prec[COLONNE] - pos_aventurier[COLONNE]
        dy_origine = pos_prec[LIGNE] - pos_aventurier[LIGNE]
        if dx_origine == 0 and dy_origine == 0:
            dx_origine = -1

        monstres_combattus = [
            un_monstre
            for un_type in manag_monstre.get_list_monstre().values()
            for un_monstre in un_type
            if un_monstre.get_position() == pos_aventurier
        ]
        monstre_meme_case = bool(monstres_combattus)
        decalage_combat = taille_cellule * RATIO_DECALAGE_COMBAT

        if aventurier.en_deplacement_continu and DELAI_ACTION > 0:
            progression = min(1.0, (pygame.time.get_ticks() - aventurier.temps_debut_deplacement) / DELAI_ACTION)
        else:
            progression = 1.0

        if monstre_meme_case and progression >= 1.0:
            aventurier.activer_anim_idle()

        # aventurier
        x_depart = plateau.decalage_x + (pos_prec[COLONNE] + 1 / 2) * taille_cellule
        y_depart = plateau.decalage_y + (pos_prec[LIGNE] + 1 / 2) * taille_cellule
        x_cible = plateau.decalage_x + (pos_aventurier[COLONNE] + 1 / 2) * taille_cellule
        y_cible = plateau.decalage_y + (pos_aventurier[LIGNE] + 1 / 2) * taille_cellule
        retourner_aventurier = aventurier.get_retourner_gauche()
        if monstre_meme_case:
            x_cible += dx_origine * decalage_combat
            y_cible += dy_origine * decalage_combat
            if dx_origine > 0:
                retourner_aventurier = True

        x_aventurier = x_depart + (x_cible - x_depart) * progression
        y_aventurier = y_depart + (y_cible - y_depart) * progression

        img_aventurier = Textures.get_image(
            aventurier.get_sprite(),
            (int(taille_cellule * 0.35), int(taille_cellule * 0.45)),
            recadrer=True,
            retourner_gauche=retourner_aventurier,
        )
        ecran.blit(img_aventurier, img_aventurier.get_rect(center=(x_aventurier, y_aventurier)))

        # monstre
        for un_type in manag_monstre.get_list_monstre().values():
            for un_monstre in un_type:
                pos = un_monstre.get_position().get_position()
                x_monstre = plateau.decalage_x + (pos[COLONNE] + 1 / 2) * taille_cellule
                y_monstre = plateau.decalage_y + (pos[LIGNE] + 1 / 2) * taille_cellule
                retourner_monstre = un_monstre.get_retourner_gauche()
                if pos == pos_aventurier:
                    x_monstre -= dx_origine * decalage_combat * progression
                    y_monstre -= dy_origine * decalage_combat * progression
                    if dx_origine > 0:
                        retourner_monstre = False

                img_monstre = Textures.get_image(
                    un_monstre.get_sprite(),
                    (int(taille_cellule * 0.35), int(taille_cellule * 0.30)),
                    recadrer=True,
                    retourner_gauche=retourner_monstre,
                )
                ecran.blit(img_monstre, img_monstre.get_rect(center=(x_monstre, y_monstre)))

        # délimitation entre la grille (espace utilisable) et les zones d'affichage
        x_gauche = plateau.decalage_x
        x_droite = plateau.decalage_x + plateau.largeur
        pygame.draw.line(ecran, Color.BLANC, (x_gauche, 0), (x_gauche, plateau.hauteur_fenetre), 2)
        pygame.draw.line(ecran, Color.BLANC, (x_droite, 0), (x_droite, plateau.hauteur_fenetre), 2)

        # profil de l'aventurier en haut à gauche
        self.dessiner_profil_aventurier(ecran, aventurier, x_gauche)

        # profil du monstre combattu (ou sélectionné lors du placement) en haut à droite
        largeur_zone_droite = plateau.largeur_fenetre - x_droite
        monstres_droite = monstres_a_afficher if monstres_a_afficher is not None else monstres_combattus
        if monstres_droite:
            self.dessiner_profil_monstres_combat(
                ecran,
                monstres_droite,
                x_droite,
                largeur_zone_droite,
            )
            if monstres_a_afficher is not None:
                self.dessiner_aide_placement_monstre(
                    ecran,
                    x_droite,
                    largeur_zone_droite,
                )

        # update
        pygame.display.flip()

    def dessiner_curseur_pos(self, ecran, cellule_a_dessiner):
        cellule_a_dessiner.dessiner(ecran)
        pygame.display.flip()

    def _largeur_texte_pixel(self, texte: str, taille_pixel: int = 3) -> int:
        if not texte:
            return 0
        return len(texte) * 4 * taille_pixel - taille_pixel

    def _preparer_fond_menu(self, largeur: int, hauteur: int) -> pygame.Surface:
        fond = pygame.Surface((largeur, hauteur))
        taille_tuile = 64

        # 1. Sol pavé en dalles de pierre avec variations naturelles
        motifs_sol = ["floor_1", "floor_2", "floor_3", "floor_4", "floor_8"]
        for y in range(0, hauteur, taille_tuile):
            for x in range(0, largeur, taille_tuile):
                variante = motifs_sol[((x // taille_tuile) * 7 + (y // taille_tuile) * 13) % len(motifs_sol)]
                img_sol = Textures.get_image(variante, (taille_tuile, taille_tuile))
                fond.blit(img_sol, (x, y))

        # 2. Mur de pierre médiéval en haut
        for x in range(0, largeur, taille_tuile):
            fond.blit(Textures.get_image("wall_top_mid", (taille_tuile, taille_tuile)), (x, 0))
            fond.blit(Textures.get_image("wall_mid", (taille_tuile, taille_tuile)), (x, taille_tuile))

        # 3. Piliers et colonnes de donjon sur les côtés
        hauteur_colonne = 210
        largeur_colonne = 72
        colonne_img = Textures.get_image("column", (largeur_colonne, hauteur_colonne))
        fond.blit(colonne_img, (24, 100))
        fond.blit(colonne_img, (largeur - largeur_colonne - 24, 100))
        fond.blit(colonne_img, (24, 490))
        fond.blit(colonne_img, (largeur - largeur_colonne - 24, 490))

        # 4. Bannières royales suspendues aux murs
        banner_r = Textures.get_image("wall_banner_red", (56, 115))
        banner_b = Textures.get_image("wall_banner_blue", (56, 115))
        fond.blit(banner_r, (116, 120))
        fond.blit(banner_b, (largeur - 116 - 56, 120))
        fond.blit(banner_b, (116, 510))
        fond.blit(banner_r, (largeur - 116 - 56, 510))

        # 5. Coffres aux trésors et crânes au pied des piliers
        coffre = Textures.get_image("chest_full_open_anim_f0", (62, 62))
        skull = Textures.get_image("skull", (36, 36))
        fond.blit(coffre, (102, 340))
        fond.blit(coffre, (largeur - 102 - 62, 340))
        fond.blit(skull, (42, 330))
        fond.blit(skull, (largeur - 42 - 36, 330))

        # 6. Voile d'ambiance et vignette sombre (pour garder les boutons lisibles et l'atmosphère sombre)
        voile = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        voile.fill((10, 8, 14, 175))
        pygame.draw.rect(voile, (6, 5, 10, 130), (0, 0, largeur, hauteur), width=180)
        pygame.draw.rect(voile, (3, 2, 6, 190), (0, 0, largeur, hauteur), width=90)
        fond.blit(voile, (0, 0))

        return fond

    def dessiner_ecran_debut(self, ecran, selection: int, options: list[str] = OPTIONS_MENU_DEBUT):
        largeur_ecran, hauteur_ecran = ecran.get_size()
        temps = pygame.time.get_ticks()

        # Cache du fond d'écran texturé pour conserver 60 FPS
        if not hasattr(self, "_fond_menu_surface") or self._fond_menu_surface.get_size() != (largeur_ecran, hauteur_ecran):
            self._fond_menu_surface = self._preparer_fond_menu(largeur_ecran, hauteur_ecran)

        ecran.blit(self._fond_menu_surface, (0, 0))

        # Cadre central gothique / donjon
        largeur_cadre = 940
        hauteur_cadre = 580
        cadre_rect = pygame.Rect(
            (largeur_ecran - largeur_cadre) // 2,
            (hauteur_ecran - hauteur_cadre) // 2,
            largeur_cadre,
            hauteur_cadre,
        )

        # Fond du cadre central avec ombrage et bordure double pierre/or
        rect_ombre_cadre = cadre_rect.move(0, 8)
        pygame.draw.rect(ecran, (6, 5, 8), rect_ombre_cadre, border_radius=18)
        pygame.draw.rect(ecran, (24, 20, 30), cadre_rect, border_radius=18)
        pygame.draw.rect(ecran, (75, 68, 92), cadre_rect, width=3, border_radius=18)

        # Filet doré intérieur
        cadre_interieur = cadre_rect.inflate(-16, -16)
        pygame.draw.rect(ecran, (160, 130, 60), cadre_interieur, width=2, border_radius=12)

        # Rivets métalliques aux 4 coins du cadre
        for cx, cy in [
            (cadre_rect.left + 22, cadre_rect.top + 22),
            (cadre_rect.right - 22, cadre_rect.top + 22),
            (cadre_rect.left + 22, cadre_rect.bottom - 22),
            (cadre_rect.right - 22, cadre_rect.bottom - 22),
        ]:
            pygame.draw.circle(ecran, (15, 12, 18), (cx, cy), 8)
            pygame.draw.circle(ecran, (215, 180, 75), (cx, cy), 6)
            pygame.draw.circle(ecran, (255, 235, 140), (cx - 1, cy - 1), 2)

        # Bannière de titre en haut
        largeur_banniere = 660
        hauteur_banniere = 94
        banniere_rect = pygame.Rect(
            (largeur_ecran - largeur_banniere) // 2,
            cadre_rect.top + 24,
            largeur_banniere,
            hauteur_banniere,
        )
        pygame.draw.rect(ecran, (38, 32, 48), banniere_rect, border_radius=12)
        pygame.draw.rect(ecran, (255, 215, 80), banniere_rect, width=3, border_radius=12)

        # Épées dorées croisées en décoration de la bannière
        img_epee_or = Textures.get_image("weapon_golden_sword", (24, 52), recadrer=True)
        epee_or_g = pygame.transform.rotate(img_epee_or, -35)
        epee_or_d = pygame.transform.rotate(img_epee_or, 35)
        ecran.blit(epee_or_g, epee_or_g.get_rect(center=(banniere_rect.left + 40, banniere_rect.centery)))
        ecran.blit(epee_or_d, epee_or_d.get_rect(center=(banniere_rect.right - 40, banniere_rect.centery)))

        # Texte du titre en pixel art
        texte_titre = TITRE.upper()
        taille_px_titre = 8
        largeur_titre = self._largeur_texte_pixel(texte_titre, taille_px_titre)
        hauteur_titre = 5 * taille_px_titre
        x_titre = banniere_rect.centerx - largeur_titre // 2
        y_titre = banniere_rect.centery - hauteur_titre // 2

        # Ombre puis titre doré
        self._dessiner_texte_pixel(
            ecran,
            texte_titre,
            x_titre + 4,
            y_titre + 4,
            taille_pixel=taille_px_titre,
            couleur=(12, 10, 16),
        )
        self._dessiner_texte_pixel(
            ecran,
            texte_titre,
            x_titre,
            y_titre,
            taille_pixel=taille_px_titre,
            couleur=(255, 215, 80),
        )

        # Sprites animés : aventurier à gauche, monstre à droite
        indice_anim = (temps // DELAI_ANIMATION_SPRITE) % len(SPRITES_AVENTURIER_IDLE)
        sprite_aventurier = SPRITES_AVENTURIER_IDLE[indice_anim]
        img_aventurier = Textures.get_image(sprite_aventurier, (56, 72), recadrer=True, retourner_gauche=False)
        img_monstre = Textures.get_image("imp_idle_anim_f0", (52, 60), recadrer=True, retourner_gauche=True)
        ecran.blit(img_aventurier, img_aventurier.get_rect(center=(cadre_rect.left + 88, banniere_rect.centery)))
        ecran.blit(img_monstre, img_monstre.get_rect(center=(cadre_rect.right - 88, banniere_rect.centery)))

        # Agencement des boutons :
        # - Option 0 (Mode existant) : bouton long en haut
        # - Option 1 (Autre mode) : bouton long au milieu
        # - Option 2 (Quitter le jeu) : bouton en bas à gauche
        # - Option 3 (Sauvegarder config) : bouton en bas à droite
        largeur_long = 720
        largeur_court = 345
        hauteur_bouton = 74
        x_long = (largeur_ecran - largeur_long) // 2

        rects_boutons = [
            # 0 : Mode existant
            pygame.Rect(x_long, cadre_rect.top + 145, largeur_long, hauteur_bouton),
            # 1 : Autre mode
            pygame.Rect(x_long, cadre_rect.top + 245, largeur_long, hauteur_bouton),
            # 2 : Quitter le jeu (en bas à gauche)
            pygame.Rect(x_long, cadre_rect.top + 350, largeur_court, hauteur_bouton),
            # 3 : Sauvegarder config (en bas à droite)
            pygame.Rect(x_long + largeur_court + 30, cadre_rect.top + 350, largeur_court, hauteur_bouton),
        ]

        img_epee = Textures.get_image(SPRITE_EPEE, (16, 36), recadrer=True)
        epee_gauche = pygame.transform.rotate(img_epee, -90)
        epee_droite = pygame.transform.rotate(img_epee, 90)

        # Effet de pulsation dorée pour le bouton sélectionné
        lueur_or = int(215 + 40 * math.sin(temps * 0.006))
        couleur_bordure_selection = (255, lueur_or, 70)

        for idx, texte_option in enumerate(options):
            if idx >= len(rects_boutons):
                break
            rect_bouton = rects_boutons[idx]
            est_selectionne = idx == selection
            est_petit_bouton = rect_bouton.width < 500

            if est_selectionne:
                # Ombre portée prononcée et surbrillance du bouton actif
                rect_ombre = rect_bouton.move(0, 6)
                pygame.draw.rect(ecran, (8, 6, 12), rect_ombre, border_radius=12)
                pygame.draw.rect(ecran, (68, 56, 90), rect_bouton, border_radius=12)
                pygame.draw.rect(ecran, couleur_bordure_selection, rect_bouton, width=4, border_radius=12)

                # Reflet lumineux discret sur le haut du bouton
                pygame.draw.rect(
                    ecran,
                    (115, 98, 145),
                    (rect_bouton.x + 6, rect_bouton.y + 4, rect_bouton.width - 12, 4),
                    border_radius=2,
                )

                couleur_texte = (255, 240, 160)
                taille_px = 3 if est_petit_bouton else 5

                # Épées pointant vers le bouton sélectionné
                decalage_epee = 26 if est_petit_bouton else 42
                ecran.blit(
                    epee_gauche,
                    epee_gauche.get_rect(center=(rect_bouton.left + decalage_epee, rect_bouton.centery)),
                )
                ecran.blit(
                    epee_droite,
                    epee_droite.get_rect(center=(rect_bouton.right - decalage_epee, rect_bouton.centery)),
                )
            else:
                rect_ombre = rect_bouton.move(0, 3)
                pygame.draw.rect(ecran, (12, 10, 16), rect_ombre, border_radius=10)

                # Teinte subtilement différente pour Quitter (rougeâtre) et Sauvegarder (dorée)
                if idx == 2:
                    fond_bouton = (40, 26, 32)
                elif idx == 3:
                    fond_bouton = (32, 34, 44)
                else:
                    fond_bouton = (35, 30, 44)

                pygame.draw.rect(ecran, fond_bouton, rect_bouton, border_radius=10)
                pygame.draw.rect(ecran, (110, 100, 130), rect_bouton, width=2, border_radius=10)
                couleur_texte = (190, 182, 205)
                taille_px = 3 if est_petit_bouton else 4

            largeur_txt = self._largeur_texte_pixel(texte_option, taille_px)
            hauteur_txt = 5 * taille_px
            x_txt = rect_bouton.centerx - largeur_txt // 2
            y_txt = rect_bouton.centery - hauteur_txt // 2
            self._dessiner_texte_pixel(
                ecran,
                texte_option,
                x_txt,
                y_txt,
                taille_pixel=taille_px,
                couleur=couleur_texte,
            )

        # Ligne de séparation et aide clavier en bas
        y_separation = cadre_rect.bottom - 74
        pygame.draw.line(
            ecran,
            (85, 76, 105),
            (cadre_rect.left + 60, y_separation),
            (cadre_rect.right - 60, y_separation),
            2,
        )

        texte_aide = "FLECHES : CHOISIR   -   ENTREE : VALIDER   -   ECHAP : QUITTER"
        taille_px_aide = 3
        largeur_aide = self._largeur_texte_pixel(texte_aide, taille_px_aide)
        self._dessiner_texte_pixel(
            ecran,
            texte_aide,
            (largeur_ecran - largeur_aide) // 2,
            cadre_rect.bottom - 46,
            taille_pixel=taille_px_aide,
            couleur=(170, 160, 190),
        )

        pygame.display.flip()

    def dessiner_ecran_choix_niveau(self, ecran, selection: int, options: list[str] = OPTIONS_CHOIX_NIVEAU):
        largeur_ecran, hauteur_ecran = ecran.get_size()
        temps = pygame.time.get_ticks()

        if not hasattr(self, "_fond_menu_surface") or self._fond_menu_surface.get_size() != (largeur_ecran, hauteur_ecran):
            self._fond_menu_surface = self._preparer_fond_menu(largeur_ecran, hauteur_ecran)

        ecran.blit(self._fond_menu_surface, (0, 0))

        # Cadre central gothique / donjon
        largeur_cadre = 940
        hauteur_cadre = 580
        cadre_rect = pygame.Rect(
            (largeur_ecran - largeur_cadre) // 2,
            (hauteur_ecran - hauteur_cadre) // 2,
            largeur_cadre,
            hauteur_cadre,
        )

        rect_ombre_cadre = cadre_rect.move(0, 8)
        pygame.draw.rect(ecran, (6, 5, 8), rect_ombre_cadre, border_radius=18)
        pygame.draw.rect(ecran, (24, 20, 30), cadre_rect, border_radius=18)
        pygame.draw.rect(ecran, (75, 68, 92), cadre_rect, width=3, border_radius=18)

        cadre_interieur = cadre_rect.inflate(-16, -16)
        pygame.draw.rect(ecran, (160, 130, 60), cadre_interieur, width=2, border_radius=12)

        for cx, cy in [
            (cadre_rect.left + 22, cadre_rect.top + 22),
            (cadre_rect.right - 22, cadre_rect.top + 22),
            (cadre_rect.left + 22, cadre_rect.bottom - 22),
            (cadre_rect.right - 22, cadre_rect.bottom - 22),
        ]:
            pygame.draw.circle(ecran, (15, 12, 18), (cx, cy), 8)
            pygame.draw.circle(ecran, (215, 180, 75), (cx, cy), 6)
            pygame.draw.circle(ecran, (255, 235, 140), (cx - 1, cy - 1), 2)

        # Bannière de titre en haut
        largeur_banniere = 660
        hauteur_banniere = 94
        banniere_rect = pygame.Rect(
            (largeur_ecran - largeur_banniere) // 2,
            cadre_rect.top + 24,
            largeur_banniere,
            hauteur_banniere,
        )
        pygame.draw.rect(ecran, (38, 32, 48), banniere_rect, border_radius=12)
        pygame.draw.rect(ecran, (255, 215, 80), banniere_rect, width=3, border_radius=12)

        img_epee_or = Textures.get_image("weapon_golden_sword", (24, 52), recadrer=True)
        epee_or_g = pygame.transform.rotate(img_epee_or, -35)
        epee_or_d = pygame.transform.rotate(img_epee_or, 35)
        ecran.blit(epee_or_g, epee_or_g.get_rect(center=(banniere_rect.left + 40, banniere_rect.centery)))
        ecran.blit(epee_or_d, epee_or_d.get_rect(center=(banniere_rect.right - 40, banniere_rect.centery)))

        texte_titre = "CHOIX DU NIVEAU"
        taille_px_titre = 6
        largeur_titre = self._largeur_texte_pixel(texte_titre, taille_px_titre)
        hauteur_titre = 5 * taille_px_titre
        x_titre = banniere_rect.centerx - largeur_titre // 2
        y_titre = banniere_rect.centery - hauteur_titre // 2

        self._dessiner_texte_pixel(
            ecran,
            texte_titre,
            x_titre + 4,
            y_titre + 4,
            taille_pixel=taille_px_titre,
            couleur=(12, 10, 16),
        )
        self._dessiner_texte_pixel(
            ecran,
            texte_titre,
            x_titre,
            y_titre,
            taille_pixel=taille_px_titre,
            couleur=(255, 215, 80),
        )

        # Sprites animés : aventurier à gauche, monstre à droite
        indice_anim = (temps // DELAI_ANIMATION_SPRITE) % len(SPRITES_AVENTURIER_IDLE)
        sprite_aventurier = SPRITES_AVENTURIER_IDLE[indice_anim]
        img_aventurier = Textures.get_image(sprite_aventurier, (56, 72), recadrer=True, retourner_gauche=False)
        img_monstre = Textures.get_image("imp_idle_anim_f0", (52, 60), recadrer=True, retourner_gauche=True)
        ecran.blit(img_aventurier, img_aventurier.get_rect(center=(cadre_rect.left + 88, banniere_rect.centery)))
        ecran.blit(img_monstre, img_monstre.get_rect(center=(cadre_rect.right - 88, banniere_rect.centery)))

        # Grille 3x2 de boutons : Niveaux 1 à 5 + Retour
        largeur_total = 720
        largeur_bouton = 345
        hauteur_bouton = 74
        espacement_x = 30
        x_col_gauche = (largeur_ecran - largeur_total) // 2
        x_col_droite = x_col_gauche + largeur_bouton + espacement_x

        rects_boutons = [
            pygame.Rect(x_col_gauche, cadre_rect.top + 145, largeur_bouton, hauteur_bouton),
            pygame.Rect(x_col_droite, cadre_rect.top + 145, largeur_bouton, hauteur_bouton),
            pygame.Rect(x_col_gauche, cadre_rect.top + 245, largeur_bouton, hauteur_bouton),
            pygame.Rect(x_col_droite, cadre_rect.top + 245, largeur_bouton, hauteur_bouton),
            pygame.Rect(x_col_gauche, cadre_rect.top + 345, largeur_bouton, hauteur_bouton),
            pygame.Rect(x_col_droite, cadre_rect.top + 345, largeur_bouton, hauteur_bouton),
        ]

        img_epee = Textures.get_image(SPRITE_EPEE, (16, 36), recadrer=True)
        epee_gauche = pygame.transform.rotate(img_epee, -90)
        epee_droite = pygame.transform.rotate(img_epee, 90)

        lueur_or = int(215 + 40 * math.sin(temps * 0.006))
        couleur_bordure_selection = (255, lueur_or, 70)

        for idx, texte_option in enumerate(options):
            if idx >= len(rects_boutons):
                break
            rect_bouton = rects_boutons[idx]
            est_selectionne = idx == selection

            if est_selectionne:
                rect_ombre = rect_bouton.move(0, 6)
                pygame.draw.rect(ecran, (8, 6, 12), rect_ombre, border_radius=12)
                pygame.draw.rect(ecran, (68, 56, 90), rect_bouton, border_radius=12)
                pygame.draw.rect(ecran, couleur_bordure_selection, rect_bouton, width=4, border_radius=12)

                pygame.draw.rect(
                    ecran,
                    (115, 98, 145),
                    (rect_bouton.x + 6, rect_bouton.y + 4, rect_bouton.width - 12, 4),
                    border_radius=2,
                )

                couleur_texte = (255, 240, 160)
                taille_px = 4

                decalage_epee = 28
                ecran.blit(
                    epee_gauche,
                    epee_gauche.get_rect(center=(rect_bouton.left + decalage_epee, rect_bouton.centery)),
                )
                ecran.blit(
                    epee_droite,
                    epee_droite.get_rect(center=(rect_bouton.right - decalage_epee, rect_bouton.centery)),
                )
            else:
                rect_ombre = rect_bouton.move(0, 3)
                pygame.draw.rect(ecran, (12, 10, 16), rect_ombre, border_radius=10)

                fond_bouton = (40, 26, 32) if idx == RETOUR_MENU else (35, 30, 44)
                pygame.draw.rect(ecran, fond_bouton, rect_bouton, border_radius=10)
                pygame.draw.rect(ecran, (110, 100, 130), rect_bouton, width=2, border_radius=10)
                couleur_texte = (190, 182, 205)
                taille_px = 4

            largeur_txt = self._largeur_texte_pixel(texte_option, taille_px)
            hauteur_txt = 5 * taille_px
            x_txt = rect_bouton.centerx - largeur_txt // 2
            y_txt = rect_bouton.centery - hauteur_txt // 2
            self._dessiner_texte_pixel(
                ecran,
                texte_option,
                x_txt,
                y_txt,
                taille_pixel=taille_px,
                couleur=couleur_texte,
            )

        y_separation = cadre_rect.bottom - 74
        pygame.draw.line(
            ecran,
            (85, 76, 105),
            (cadre_rect.left + 60, y_separation),
            (cadre_rect.right - 60, y_separation),
            2,
        )

        texte_aide = "FLECHES : CHOISIR   -   ENTREE : VALIDER   -   ECHAP : RETOUR"
        taille_px_aide = 3
        largeur_aide = self._largeur_texte_pixel(texte_aide, taille_px_aide)
        self._dessiner_texte_pixel(
            ecran,
            texte_aide,
            (largeur_ecran - largeur_aide) // 2,
            cadre_rect.bottom - 46,
            taille_pixel=taille_px_aide,
            couleur=(170, 160, 190),
        )

        pygame.display.flip()




