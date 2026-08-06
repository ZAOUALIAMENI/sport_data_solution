SELECT

    employee_id,

    origin_address,

    destination_address,

    travel_mode,

    distance_meters,

    duration_seconds,

    api_status,

    calculation_date

FROM {{ source('raw', 'commute_distances_raw') }}