SELECT
    employee_id,
    nom,
    prenom,
    salaire_brut,
    sport_bonus,
    ROUND(
        salaire_brut * {{ var('sport_bonus_rate') }},
        2
    ) AS expected_bonus
FROM {{ ref('int_employee_benefits') }}
WHERE eligible_sport_bonus = TRUE
  AND sport_bonus != ROUND(
      salaire_brut * {{ var('sport_bonus_rate') }},
      2
  )