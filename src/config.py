"""
Configuration de la simulation
"""

# ==========================================================
# Historique
# ==========================================================

HISTORY_DAYS = 365

# ==========================================================
# Profils sportifs
# probability, min activités, max activités
# ==========================================================

PROFILE_CONFIG = {
    "occasionnel": (0.50, 4, 12),
    "regulier": (0.35, 13, 25),
    "intensif": (0.15, 26, 60),
}

# ==========================================================
# Paramètres des sports
# durée (secondes) + vitesse (km/h)
# ==========================================================

SPORT_CONFIG = {
    "Marche": {
        "duration": (1800, 7200),
        "speed": (4, 6),
    },
    "Running": {
        "duration": (1800, 7200),
        "speed": (8, 16),
    },
    "Vélo": {
        "duration": (3600, 14400),
        "speed": (15, 30),
    },
    "Randonnée": {
        "duration": (7200, 21600),
        "speed": (3, 5),
    },
    "Natation": {
        "duration": (1800, 5400),
        "speed": (2, 4),
    },
}

# ==========================================================
# Sports sans distance
# ==========================================================

SPORTS_WITHOUT_DISTANCE = {
    "Escalade",
    "Musculation",
    "Yoga",
    "Pilates",
}

# ==========================================================
# Commentaires
# ==========================================================

COMMENTS = [
    "",
    "",
    "",
    "Belle séance !",
    "Très bonnes sensations.",
    "Objectif atteint.",
    "Sortie agréable.",
    "Reprise du sport.",
]

# ==========================================================
# Google Maps
# ==========================================================

import os

COMPANY_ADDRESS = "1362 Av. des Platanes, 34970 Lattes"

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")