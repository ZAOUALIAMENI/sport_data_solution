SELECT

    e.employee_id,

    e.nom,

    e.prenom,

    e.salaire_brut,

    e.moyen_deplacement,

    e.sport_pratique,

    COALESCE(a.nb_activities, 0) AS nb_activities,

    c.distance_km,

    c.incoherent_commute,

    -- ==========================================================
    -- Prime sportive
    -- ==========================================================

    CASE

        WHEN e.moyen_deplacement IN (
            'Marche/running',
            'Vélo/Trottinette/Autres'
        )
        AND c.incoherent_commute = FALSE

        THEN TRUE

        ELSE FALSE

    END AS eligible_sport_bonus,

    CASE

        WHEN e.moyen_deplacement IN (
            'Marche/running',
            'Vélo/Trottinette/Autres'
        )
        AND c.incoherent_commute = FALSE

        THEN ROUND(
            e.salaire_brut * {{ var('sport_bonus_rate') }},
            2
        )

        ELSE 0

    END AS sport_bonus,

    -- ==========================================================
    -- Jours bien-être
    -- ==========================================================

    CASE

        WHEN e.sport_pratique IS NOT NULL
        AND COALESCE(a.nb_activities, 0) >= {{ var('min_activities') }}

        THEN TRUE

        ELSE FALSE

    END AS eligible_wellbeing_days,

    CASE

        WHEN e.sport_pratique IS NOT NULL
        AND COALESCE(a.nb_activities, 0) >= {{ var('min_activities') }}

        THEN {{ var('wellbeing_days') }}

        ELSE 0

    END AS wellbeing_days

FROM {{ ref('stg_employees') }} e

LEFT JOIN {{ ref('int_employee_activity_summary') }} a
       ON e.employee_id = a.employee_id

LEFT JOIN {{ ref('int_employee_commute') }} c
       ON e.employee_id = c.employee_id