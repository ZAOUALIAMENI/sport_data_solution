"""
Calcul des distances domicile → entreprise via Google Maps

Le script :

- lit les salariés depuis stg_employees
- calcule la distance et la durée du trajet
- insère les résultats dans commute_distances_raw

Aucune règle métier n'est appliquée ici.
"""

import googlemaps
import pandas as pd
from datetime import datetime

from sqlalchemy import text

from database import engine
from config import COMPANY_ADDRESS, GOOGLE_MAPS_API_KEY


# ==========================================================
# Client Google Maps
# ==========================================================

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


# ==========================================================
# Lecture des salariés
# ==========================================================

def load_employees():
    """
    Charge les salariés.
    """

    query = """
        SELECT
            employee_id,
            adresse_domicile,
            moyen_deplacement
        FROM stg_employees
    """

    return pd.read_sql(query, engine)


# ==========================================================
# Mapping des modes de déplacement
# ==========================================================

def get_google_mode(mode):
    """
    Convertit le mode RH vers le mode Google Maps.
    """

    mapping = {
        "Marche/running": "walking",
        "Vélo/Trottinette/Autres": "bicycling",
        "Véhicule thermique/électrique": "driving",
        "Transports en commun": "transit",
    }

    return mapping.get(mode, "driving")


# ==========================================================
# Calcul du trajet
# ==========================================================

def compute_commute(origin, mode):
    """
    Retourne la distance et la durée du trajet.
    """

    try:

        result = gmaps.distance_matrix(
            origins=[origin],
            destinations=[COMPANY_ADDRESS],
            mode=mode,
            units="metric",
        )

        element = result["rows"][0]["elements"][0]

        status = element["status"]

        if status != "OK":

            return {
                "distance_meters": None,
                "duration_seconds": None,
                "api_status": status,
            }

        return {
            "distance_meters": element["distance"]["value"],
            "duration_seconds": element["duration"]["value"],
            "api_status": status,
        }

    except Exception as e:

        print(e)
        
        return {
            "distance_meters": None,
            "duration_seconds": None,
            "api_status": "ERROR",
        }


# ==========================================================
# Génération des résultats
# ==========================================================

def generate_distances(employees):

    rows = []

    for employee in employees.itertuples(index=False):

        google_mode = get_google_mode(
            employee.moyen_deplacement
        )

        commute = compute_commute(
            employee.adresse_domicile,
            google_mode,
        )

        rows.append({

            "employee_id": employee.employee_id,

            "origin_address": employee.adresse_domicile,

            "destination_address": COMPANY_ADDRESS,

            "travel_mode": google_mode,

            "distance_meters": commute["distance_meters"],

            "duration_seconds": commute["duration_seconds"],

            "api_status": commute["api_status"],

            "calculation_date": datetime.now()

        })

    return pd.DataFrame(rows)


# ==========================================================
# Insertion PostgreSQL
# ==========================================================

def insert_distances(df):

    with engine.begin() as conn:

        conn.execute(
            text(
                """
                TRUNCATE TABLE commute_distances_raw
                RESTART IDENTITY CASCADE
                """
            )
        )

    df.to_sql(
        "commute_distances_raw",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("CALCUL DES DISTANCES DOMICILE → ENTREPRISE")
    print("=" * 60)

    employees = load_employees()

    print(f"{len(employees)} salariés trouvés.")

    df = generate_distances(employees)

    insert_distances(df)

    print()
    print("Simulation terminée")
    print(f"Trajets calculés : {len(df)}")


if __name__ == "__main__":
    main()