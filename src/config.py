"""
Configuration globale du projet Sport Data Solution
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "docker" / ".env")

# ==========================================================
# Chemins du projet
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

# ==========================================================
# PostgreSQL
# ==========================================================

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sport_data")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")

DB_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

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

COMPANY_ADDRESS = "1362 Av. des Platanes, 34970 Lattes"

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")