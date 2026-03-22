---
title: Backblaze
---

```sql backblaze_per_model_summary
select
  "date"::text as "date",
  manufacturer,
  sum(sum_capacity_bytes) / 1024**4 as sum_capacity_tb
from dwh.backblaze_per_model_summary
group by "date", manufacturer
order by "date" asc
```

<BarChart 
    data={backblaze_per_model_summary}
    x=date
    y=sum_capacity_tb
    series=manufacturer
    title="Capacity by Manufacturer"
    sort=false
/>
