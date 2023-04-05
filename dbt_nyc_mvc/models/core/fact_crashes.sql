{{
    config(
        partition_by={
            "field": "crash_datetime",
            "data_type": "datetime",
            "granularity": "day"
        },
        cluster_by=["borough", "contributing_factor_vehicle_1"]
    )
}}

select * from {{ ref('stg_crashes') }}

{% if var('is_test_run', default=false) %}
    limit 100
{% endif %}