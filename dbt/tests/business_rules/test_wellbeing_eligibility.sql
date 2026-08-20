SELECT
    employee_id,
    nom,
    prenom,
    sport_pratique,
    nb_activities,
    eligible_wellbeing_days
FROM {{ ref('int_employee_benefits') }}
WHERE eligible_wellbeing_days = TRUE
  AND (
      sport_pratique IS NULL
      OR nb_activities < {{ var('min_activities') }}
  )