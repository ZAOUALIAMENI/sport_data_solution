"""
Génération des activités sportives

- Lecture des salariés sportifs depuis stg_employees
- Attribution d'un profil
- Génération d'un historique sur 12 mois
- Insertion dans activities_raw

Les règles métier seront réalisées dans DBT.
"""

import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import text

from config import (
    HISTORY_DAYS,
    PROFILE_CONFIG,
    SPORT_CONFIG,
    SPORTS_WITHOUT_DISTANCE,
    COMMENTS,
)
from database import engine


# ==========================================================
# Lecture des employés
# ==========================================================

def load_employees():

    query = """
        SELECT
            employee_id,
            nom,
            prenom,
            sport_pratique
        FROM stg_employees
        WHERE sport_pratique IS NOT NULL
          AND TRIM(sport_pratique) <> ''
    """

    return pd.read_sql(query, engine)


# ==========================================================
# Attribution d'un profil
# ==========================================================

def assign_profile():

    profiles = list(PROFILE_CONFIG.keys())

    probabilities = [
        PROFILE_CONFIG[p][0]
        for p in profiles
    ]

    return random.choices(
        profiles,
        weights=probabilities,
        k=1
    )[0]


# ==========================================================
# Nombre d'activités
# ==========================================================

def get_activity_count(profile):

    _, minimum, maximum = PROFILE_CONFIG[profile]

    return random.randint(minimum, maximum)


# ==========================================================
# Génération des dates
# ==========================================================

def generate_dates(count, history=False):

    end_date = datetime.now()

    if history:
        start_date = end_date - timedelta(days=HISTORY_DAYS)
    else:
        start_date = end_date

    dates = []

    for _ in range(count):

        if history:
            delta = random.randint(
                0,
                (end_date - start_date).days - 1
            )

            activity_date = start_date + timedelta(days=delta)

        else:
            activity_date = end_date

        activity_date = activity_date.replace(
            hour=random.randint(6, 21),
            minute=random.randint(0, 59),
            second=0,
            microsecond=0,
        )

        dates.append(activity_date)

    dates.sort()

    return dates


# ==========================================================
# Génération d'une activité
# ==========================================================

def generate_activity(employee_id, sport, start):

    if sport in SPORT_CONFIG:

        duration_min, duration_max = SPORT_CONFIG[sport]["duration"]
        speed_min, speed_max = SPORT_CONFIG[sport]["speed"]

    else:

        duration_min, duration_max = (1800, 7200)
        speed_min, speed_max = (4, 8)

    duration = random.randint(duration_min, duration_max)

    end = start + timedelta(seconds=duration)

    if sport in SPORTS_WITHOUT_DISTANCE:
        distance = None
    else:
        speed = random.uniform(speed_min, speed_max)
        distance = int(speed * (duration / 3600) * 1000)

    return {
        "ID salarié": employee_id,
        "Date de début": start,
        "Date de fin": end,
        "Type d'activité": sport,
        "Distance (m)": distance,
        "Temps écoulé (s)": duration,
        "Commentaire": random.choice(COMMENTS),
    }


# ==========================================================
# Activités d'un salarié
# ==========================================================

def generate_employee_activities(employee, history=False):

    profile = assign_profile()

    count = get_activity_count(profile)

    dates = generate_dates(
        count,
        history=history
    )

    return [
        generate_activity(
            employee.employee_id,
            employee.sport_pratique,
            date,
        )
        for date in dates
    ]


# ==========================================================
# Sauvegarde
# ==========================================================

def insert_activities(activities):

    df = pd.DataFrame(activities)

    df.to_sql(
        "activities_raw",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

# ==========================================================
# Détection du premier chargement
# ==========================================================

def is_initial_load():

    query = """
        SELECT COUNT(*)
        FROM activities_raw
    """

    with engine.connect() as conn:
        count = conn.execute(text(query)).scalar()

    return count == 0

# ==========================================================
# Main
# ==========================================================

def main():

    initial_load = is_initial_load()
    employees = load_employees()

    all_activities = []

    if initial_load:

        # Génération de l'historique sur 12 mois
        for employee in employees.itertuples(index=False):
            all_activities.extend(
                generate_employee_activities(
                    employee,
                    history=True
                )
            )

    else:

        # Génération de quelques nouvelles activités pour aujourd'hui
        daily_employees = employees.sample(
            n=min(5, len(employees))
        )

        for employee in daily_employees.itertuples(index=False):
            all_activities.append(
                generate_activity(
                    employee.employee_id,
                    employee.sport_pratique,
                    generate_dates(1, history=False)[0],
                )
            )

    insert_activities(all_activities)

    print("=" * 50)
    print("Simulation terminée")
    print("=" * 50)
    print(f"Employés sportifs : {len(employees)}")
    print(f"Activités générées : {len(all_activities)}")

if __name__ == "__main__":
    main()