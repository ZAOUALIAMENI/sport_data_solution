-- Durée positive
SELECT *
FROM {{ ref('stg_activities') }}
WHERE temps_ecoule_sec <= 0

UNION ALL

-- Dates cohérentes
SELECT *
FROM {{ ref('stg_activities') }}
WHERE date_fin <= date_debut

UNION ALL

-- Distance positive
SELECT *
FROM {{ ref('stg_activities') }}
WHERE distance_metres < 0

UNION ALL

-- Sports sans distance
SELECT *
FROM {{ ref('stg_activities') }}
WHERE sport_type IN ('Yoga', 'Pilates', 'Musculation', 'Escalade')
  AND distance_metres IS NOT NULL

UNION ALL

-- Sports avec distance
SELECT *
FROM {{ ref('stg_activities') }}
WHERE sport_type NOT IN ('Yoga', 'Pilates', 'Musculation', 'Escalade')
  AND distance_metres IS NULL