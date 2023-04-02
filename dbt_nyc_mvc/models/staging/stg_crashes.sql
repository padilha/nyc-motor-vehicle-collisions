select
    collision_id,
    crash_datetime,
    borough,
    number_of_persons_injured,
    number_of_persons_killed,
    contributing_factor_vehicle_1,
    contributing_factor_vehicle_2,
    contributing_factor_vehicle_3,
    contributing_factor_vehicle_4,
    contributing_factor_vehicle_5
from {{ source('staging', 'crashes') }}
where date(crash_datetime) >= '2013-01-01'

{% if var('is_test_run', default=false) %}
    limit 100
{% endif %}