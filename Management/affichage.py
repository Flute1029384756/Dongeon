
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
    "P": ["111", "101", "111", "100", "100"],
    "V": ["101", "101", "101", "101", "010"],
    "L": ["100", "100", "100", "100", "111"],
    "E": ["111", "100", "110", "100", "111"],
    "N": ["101", "111", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "D": ["110", "101", "101", "101", "110"],
    "G": ["111", "100", "101", "101", "111"],
    "A": ["010", "101", "111", "101", "101"],
    "T": ["111", "010", "010", "010", "010"],
    "S": ["111", "100", "111", "001", "111"],
    ".": ["000", "000", "000", "000", "010"],
    " ": ["000", "000", "000", "000", "000"],
}


class Affichage:
    def _dessiner_texte_pixel(self, ecran, texte: str, x: int, y: int, taille_pixel: int = 3, couleur=Color.BLANC):
        curseur_x = x
        for caractere in texte:
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
        hauteur_panneau = 202
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
                y_depart=16 + idx * 216,
                taille_sprite=(58, 50),
                retourner_gauche=monstre.get_retourner_gauche(),
            )

    def dessiner(self, manag_Plateau: Manag_Plateau, manag_aventurier: Manag_aventurier,
                 manag_monstre:Manag_monstres_global):
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

        # profil du monstre combattu en haut à droite (uniquement si un combat est en cours)
        if monstres_combattus:
            self.dessiner_profil_monstres_combat(
                ecran,
                monstres_combattus,
                x_droite,
                plateau.largeur_fenetre - x_droite,
            )

        # update
        pygame.display.flip()

    def dessiner_curseur_pos(self, ecran, cellule_a_dessiner):
        cellule_a_dessiner.dessiner(ecran)
        pygame.display.flip()

