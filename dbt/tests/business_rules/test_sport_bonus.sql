SELECT
    employee_id,
    nom,
    prenom,
    moyen_deplacement,
    incoherent_commute,
    eligible_sport_bonus
FROM {{ ref('int_employee_benefits') }}
WHERE eligible_sport_bonus = TRUE
  AND (
      moyen_deplacement NOT IN (
          'Marche/running',
          'Vélo/Trottinette/Autres'
      )
      OR incoherent_commute != FALSE
  )