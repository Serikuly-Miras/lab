---
title: Backblaze
---

## Introduction

Thanks [Backblaze](https://www.backblaze.com) for providing this amazing dataset.

More details can be found on their designated page for this dataset:
https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data

## Overview

This is a simple dashboard to showcase the data pipeline: from CSV files processed by an Airflow DAG, to a data-raw bucket inside SeaweedFS, then ingested into a CNPG database, transformed with the Airflow Cosmos dbt pipeline, queried and cached by Evidence, and finally visualized in your browser right here.

More on the setup: [lab](https://github.com/Serikuly-Miras/lab)

## Dashboard

```sql backblaze_datacenters_timerange_covered
  select
    first_date,
    last_date,
    first_date::date::text || ' - ' || last_date::date::text as timerange_covered_months
  from backblaze_datacenters_timerange_covered
```

<BigValue 
  data={backblaze_datacenters_timerange_covered} 
  value=timerange_covered_months
  title="Time range covered by feched part of the dataset"
/>

```sql backblaze_datacenters_capacity
  select
    city,
    longitude,
    latitude,
    (capacity_bytes / 1024**5)::int::text as capacity_PiB
  from dwh.backblaze_datacenters_capacity
```

<PointMap 
    data={backblaze_datacenters_capacity} 
    lat=latitude
    long=longitude  
    pointName=city 
    tooltipType=hover
    title="Backblaze datacenters on a map"
    value=city
    valueSuffix=" PiB"
/>

```sql backblaze_month_over_month_agg
  select
    capacity_change_percentage,
    current_month_capacity_bytes / 1024**5 as current_month_capacity_PiB,
    current_month_drives_count,
    drives_change_count
  from dwh.backblaze_month_over_month_agg
```

```sql backblaze_dataset_row_count
  select
    total_rows // 1000**2 as total_rows_millions
  from dwh.backblaze_dataset_row_count
```

<Grid cols=3>
<BigValue 
  data={backblaze_month_over_month_agg} 
  value=current_month_capacity_PiB
  comparison=capacity_change_percentage
  comparisonTitle="% from last month"
  title="Current capacity (PiB)"
/>

<BigValue 
  data={backblaze_month_over_month_agg} 
  value=current_month_drives_count
  comparison=drives_change_count
  comparisonTitle=" from last month"
  title="Current drives count"
/>

<BigValue
  data={backblaze_dataset_row_count}
  value=total_rows_millions
  title="Total rows in the dataset (millions)"
/>
</Grid>

<!-- ## Failure rates

row >
failure rates by manufacturer for the last month in the dataset
failure rates by manufacturer for the last 3 months in the dataset

row >
failure rates by datacenter for the last month in the dataset
failure rates by datacenter for the last 3 months in the dataset -->
