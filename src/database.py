"""
Connexion PostgreSQL
"""

from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# ==========================================================
# Chargement des variables d'environnement
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "docker" / ".env")

# ==========================================================
# Variables
# ==========================================================

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# ==========================================================
# URL PostgreSQL
# ==========================================================

DB_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================================
# Engine SQLAlchemy
# ==========================================================

engine = create_engine(DB_URL)