"""
Chargement des données RH et Sport
Ingestion des données brutes dans PostgreSQL (RAW)
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================================
# Configuration
# ==========================================================

from config import DB_URL, DATA_DIR

RH_FILE = DATA_DIR / "RH.xlsx"
SPORT_FILE = DATA_DIR / "Sportive.xlsx"

# ==========================================================
# Lecture des fichiers
# ==========================================================

print("Chargement des fichiers...")

df_rh = pd.read_excel(RH_FILE)
df_sport = pd.read_excel(SPORT_FILE)

print(f"RH : {len(df_rh)} lignes")
print(f"Sport : {len(df_sport)} lignes")

# ==========================================================
# Fusion des données
# ==========================================================

df = df_rh.merge(
    df_sport,
    on="ID salarié",
    how="left"
)

# ==========================================================
# Chargement PostgreSQL
# ==========================================================

engine = create_engine(DB_URL)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE employees_raw RESTART IDENTITY CASCADE"))

df.to_sql(
    "employees_raw",
    engine,
    if_exists="append",
    index=False
)

with engine.connect() as conn:
    nb = conn.execute(
        text("SELECT COUNT(*) FROM employees_raw")
    ).scalar()

print(f"\n{nb} employés importés avec succès.")