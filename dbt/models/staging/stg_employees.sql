SELECT
    "ID salarié"               AS employee_id,
    "Nom"                      AS nom,
    "Prénom"                   AS prenom,
    "Date de naissance"        AS date_naissance,
    "BU"                       AS bu,
    "Date d'embauche"          AS date_embauche,
    "Salaire brut"             AS salaire_brut,
    "Type de contrat"          AS type_contrat,
    "Nombre de jours de CP"    AS nb_jours_cp,
    "Adresse du domicile"      AS adresse_domicile,
    "Moyen de déplacement"     AS moyen_deplacement,
    "Pratique d'un sport"      AS sport_pratique
FROM {{ source('raw', 'employees_raw') }}