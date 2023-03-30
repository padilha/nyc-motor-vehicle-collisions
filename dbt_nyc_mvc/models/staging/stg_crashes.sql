select
    collision_id,
    crash_datetime,
    borough,
    latitude,
    longitude,
    number_of_persons_injured,
    number_of_persons_killed,
    contributing_factor_vehicle_1
from {{ source('staging', 'crashes') }}
where borough is not null 

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}
    limit 100
{% endif %}