WITH ranked_activities AS (

    SELECT

        employee_id,

        date_debut,

        sport_type,

        commentaire,

        ROW_NUMBER() OVER (
            PARTITION BY employee_id
            ORDER BY date_debut DESC
        ) AS rn

    FROM {{ ref('stg_activities') }}

),

activity_summary AS (

    SELECT

        employee_id,

        COUNT(*) AS nb_activities,

        COALESCE(SUM(distance_metres), 0) AS total_distance_metres,

        COALESCE(SUM(temps_ecoule_sec), 0) AS total_duration_seconds,

        MIN(date_debut) AS first_activity,

        MAX(date_debut) AS last_activity

    FROM {{ ref('stg_activities') }}

    GROUP BY employee_id

)

SELECT

    s.employee_id,

    s.nb_activities,

    s.total_distance_metres,

    s.total_duration_seconds,

    s.first_activity,

    s.last_activity,

    r.sport_type AS last_activity_sport,

    r.commentaire AS last_activity_comment

FROM activity_summary s

LEFT JOIN ranked_activities r
       ON s.employee_id = r.employee_id
      AND r.rn = 1