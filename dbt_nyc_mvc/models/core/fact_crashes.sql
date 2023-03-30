{{ config(
    partition_by={
      "field": "crash_datetime",
      "data_type": "datetime",
      "granularity": "day"
    },
    cluster_by="borough"
)}}

select * from {{ ref('stg_crashes') }}