# Test Donjon

Un jeu de stratégie et de construction de donjon en 2D réalisé en **Python** avec **Pygame**.  
Le joueur conçoit un donjon ou y place des monstres avec un budget limité afin d'empêcher un aventurier d'atteindre la sortie.

---

## Modes de jeu

* **Mode Création** : construis ton propre donjon case par case (départ, arrivée, couloirs, coins, intersections en triangle, culs-de-sac) ou teste des donjons prédéfinis, puis lance l'aventurier à travers le parcours.
* **Mode Jeu Classique** : sélectionne un niveau, gère ton budget en pièces pour acheter et positionner des monstres sur le plateau, puis observe l'aventurier tenter de traverser le donjon.
* **Sauvegarder Config** : affiche dans le terminal la configuration actuelle du plateau sous forme de dictionnaire réutilisable.

---

## Mécaniques principales

* **Aventurier autonome** : se déplace dans le donjon vers la tuile d'arrivée, combat les monstres rencontrés, gagne de l'expérience (XP) et monte de niveau.
* **Monstres disponibles** :
  * **Gobelin** (coût : 1)
  * **Araignée** (coût : 4)
  * **Araignée venimeuse** (coût : 6)
* **Combat & Endurance** : chaque entité possède des points de vie (PV), des dégâts, une vitesse de frappe et une jauge d'endurance qui se régénère dans le temps.

---

## Contrôles

### Menu principal & choix de niveau
* **Flèches directionnelles** : naviguer entre les options
* **Entrée** : valider
* **Échap** : revenir en arrière / quitter

### Mode Création (Phase 1)
* **Flèches directionnelles** : déplacer le curseur sur la grille
* **`P`** : changer de type de tuile
* **`M`** : faire pivoter la tuile (orientation)
* **Entrée** : placer la tuile sélectionnée
* **`A`** : charger / cycler entre des donjons prédéfinis
* **`Espace`** : valider le plateau et lancer l'aventurier (Phase 2)
* **`Échap`** : retourner au menu principal

---

## Structure du projet

```text
.
├── main.py                        # Point d'entrée du jeu
├── Autres/
│   └── Autre.py                   # Constantes, statistiques, chemins de sprites et enums
├── Classes_basiques/
│   ├── Entitee.py                 # Classe de base des entités (PV, dégâts, endurance, combat)
│   ├── aventurier.py              # Classe Aventurier (XP, niveaux, animations)
│   ├── Monstres.py                # Classes Monstres (Araignée, Araignée venimeuse, Gobelin)
│   ├── cellule.py                 # Tuiles du donjon et gestion des textures
│   └── Plateau.py                 # Grille de jeu et fenêtre Pygame
├── Management/
│   ├── Management_général.py      # Boucle principale et menus (Root)
│   ├── Phase1.py                  # Phase de construction du donjon
│   ├── Phase_placement_monstre.py # Sélection de niveau et placement des monstres
│   ├── Phase2.py                  # Phase d'exploration et de combat
│   ├── Management_Plateau.py      # Logique du plateau et donjons prédéfinis
│   ├── Management_aventurier.py   # Déplacements et état de l'aventurier
│   ├── Management_Monstres_global.py # Gestion globale des monstres sur le plateau
│   ├── Management_Combat.py       # Résolution des combats
│   └── affichage.py               # Rendu graphique, HUD, barres de vie/XP et menus
└── Tileset/                       # Sprites et tilesets (0x72 DungeonTileset II, SpiderPack)
```

---

## Prérequis et lancement

1. **Installer Python 3** et **Pygame** :
   ```bash
   pip install pygame
   ```
2. **Lancer le jeu** depuis la racine du dépôt :
   ```bash
   python main.py
   ```

---

## Assets graphiques

* [0x72 DungeonTileset II v1.7](Tileset/0x72_DungeonTilesetII_v1.7/)
* [SpiderPack](Tileset/SpiderPack/)
