---
title: Backblaze 25Q3
---

Top 10 most populat disk models in Backblaze dataset as of 2025-09-30:

```sql top10_disks_per_model
select model, count from dwh.disks_per_model limit 10;
```

<BarChart 
    data={top10_disks_per_model}
    x=model
    y=count
/>
