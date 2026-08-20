SELECT
    employee_id,
    nom,
    prenom,
    moyen_deplacement,
    distance_km,
    incoherent_commute
FROM {{ ref('int_employee_commute') }}
WHERE moyen_deplacement = 'Vélo/Trottinette/Autres'
  AND distance_km > {{ var('max_bike_km') }}