DROP TABLE IF EXISTS activities_raw CASCADE;
DROP TABLE IF EXISTS employees_raw CASCADE;

-- ==========================================================
-- EMPLOYEES_RAW
-- ==========================================================

CREATE TABLE employees_raw (

    id SERIAL PRIMARY KEY,

    "ID salarié" INTEGER,
    "Nom" VARCHAR(100),
    "Prénom" VARCHAR(100),
    "Date de naissance" DATE,
    "BU" VARCHAR(50),
    "Date d'embauche" DATE,
    "Salaire brut" NUMERIC(10,2),
    "Type de contrat" VARCHAR(20),
    "Nombre de jours de CP" INTEGER,
    "Adresse du domicile" TEXT,
    "Moyen de déplacement" VARCHAR(50),
    "Pratique d'un sport" VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- ACTIVITIES_RAW
-- ==========================================================

CREATE TABLE activities_raw (

    id SERIAL PRIMARY KEY,

    "ID salarié" INTEGER,
    "Date de début" TIMESTAMP,
    "Date de fin" TIMESTAMP,
    "Type d'activité" VARCHAR(50),
    "Distance (m)" INTEGER,
    "Temps écoulé (s)" INTEGER,
    "Commentaire" TEXT,
    slack_sent_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS commute_distances_raw;

CREATE TABLE commute_distances_raw (
    employee_id INTEGER PRIMARY KEY,
    origin_address TEXT,
    destination_address TEXT,
    travel_mode TEXT,
    distance_meters INTEGER,
    duration_seconds INTEGER,
    api_status TEXT,
    calculation_date TIMESTAMP
);