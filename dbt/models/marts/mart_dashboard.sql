SELECT

    -- ==========================================================
    -- Informations salarié
    -- ==========================================================

    e.employee_id,

    e.nom,

    e.prenom,

    e.bu,

    e.type_contrat,

    e.salaire_brut,

    e.sport_pratique,

    CASE
        WHEN e.sport_pratique IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS sportif,

    e.moyen_deplacement,

    -- ==========================================================
    -- Activités sportives
    -- ==========================================================

    COALESCE(a.nb_activities, 0) AS nb_activities,

    ROUND(
        COALESCE(a.total_distance_metres, 0) / 1000.0,
        2
    ) AS total_distance_sport_km,

    ROUND(
        COALESCE(a.total_duration_seconds, 0) / 60.0,
        1
    ) AS total_duree_sport_minutes,

    a.first_activity,

    a.last_activity,

    a.last_activity_sport,

    a.last_activity_comment,

    -- ==========================================================
    -- Déplacements domicile → entreprise
    -- ==========================================================

    COALESCE(c.distance_km, 0) AS distance_domicile_entreprise_km,

    c.incoherent_commute,

    CASE
        WHEN c.incoherent_commute THEN 'Incohérent'
        ELSE 'Cohérent'
    END AS commute_status,

    -- ==========================================================
    -- Avantages salariés
    -- ==========================================================

    b.eligible_sport_bonus,

    ROUND(b.sport_bonus, 2) AS sport_bonus,

    b.eligible_wellbeing_days,

    b.wellbeing_days

FROM {{ ref('stg_employees') }} e

LEFT JOIN {{ ref('int_employee_activity_summary') }} a
       ON e.employee_id = a.employee_id

LEFT JOIN {{ ref('int_employee_commute') }} c
       ON e.employee_id = c.employee_id

LEFT JOIN {{ ref('int_employee_benefits') }} b
       ON e.employee_id = b.employee_id