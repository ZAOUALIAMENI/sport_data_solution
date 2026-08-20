SELECT
    employee_id,
    nom,
    prenom,
    nb_activities,
    eligible_wellbeing_days,
    wellbeing_days
FROM {{ ref('int_employee_benefits') }}
WHERE
    (
        eligible_wellbeing_days = TRUE
        AND wellbeing_days != {{ var('wellbeing_days') }}
    )
    OR
    (
        eligible_wellbeing_days = FALSE
        AND wellbeing_days != 0
    )