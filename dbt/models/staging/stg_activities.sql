SELECT
    "ID salarié"          AS employee_id,
    "Date de début"       AS date_debut,
    "Date de fin"         AS date_fin,
    "Type d'activité"     AS sport_type,
    "Distance (m)"        AS distance_metres,
    "Temps écoulé (s)"    AS temps_ecoule_sec,
    "Commentaire"         AS commentaire
FROM {{ source('raw', 'activities_raw') }}