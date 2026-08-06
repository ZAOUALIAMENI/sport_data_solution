SELECT

    e.employee_id,

    e.nom,

    e.prenom,

    e.moyen_deplacement,

    d.distance_meters,

    ROUND(d.distance_meters / 1000.0, 2) AS distance_km,

    CASE

        WHEN e.moyen_deplacement = 'Marche/running'
             AND (d.distance_meters / 1000.0) > {{ var('max_walk_km') }}
        THEN TRUE

        WHEN e.moyen_deplacement = 'Vélo/Trottinette/Autres'
             AND (d.distance_meters / 1000.0) > {{ var('max_bike_km') }}
        THEN TRUE

        ELSE FALSE

    END AS incoherent_commute

FROM {{ ref('stg_employees') }} e

LEFT JOIN {{ ref('stg_commute_distances') }} d
       ON e.employee_id = d.employee_id