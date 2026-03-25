---
title: PG and CNPG
---

## Introduction

After starting a simple HomeLab, I became really interested in running everything inside Kubernetes and using cloud-native solutions for everything. For my database needs, I decided to go with Cloud Native PostgreSQL (CNPG). Ever since, I have been interested in how much overhead CNPG adds on top of regular PostgreSQL and how it performs in general. So, I decided to do some benchmarks to compare the two and share the results here.

## Warnings

Please do not draw any conclusions based on these benchmarks/results. This is not a scientific benchmark, and there are a lot of factors that can affect the results. This is just a fun experiment to see how CNPG performs in a simple setup and to share my thoughts on it.

Look at it more like a case study in a vacuum. And if you are interested, check out these related links:

- [CNPG | Benchmarking page](https://cloudnative-pg.io/docs/1.28/benchmarking)
- [CNPG | FAQ](https://cloudnative-pg.io/docs/1.28/faq)
- [Kubernetes | Local Persistent Volumes GA](https://kubernetes.io/blog/2019/04/04/kubernetes-1.14-local-persistent-volumes-ga/)
- [EDB | Why EDB Chose Immutable Application Containers](https://www.enterprisedb.com/blog/why-edb-chose-immutable-application-containers)

## Repo

All the code for this experiment can be found in this repo:
[pg_and_cnpg](https://github.com/Serikuly-Miras/pg_and_cnpg)

## Setup

For servers, I utilized a simple Terraform project to set up 4 VMs on Hetzner Cloud with the following specs:

- 3x ccx33 (8 dedicated vCPU, 32GB RAM, 240GB SSD) for the k3s worker nodes, PostgreSQL node, and a pgbench client
- 1x cpx32 (4 shared vCPU, 8GB RAM, 160GB SSD) for the k3s control-plane node

All nodes are running Ubuntu 22.04 and are located in the same datacenter (nbg1).

### Postgres / Pgbench

Installation is pretty straightforward: just a simple Ansible playbook to install PostgreSQL 18 from https://www.postgresql.org/download/linux/ubuntu/ and apply some tuning from https://pgtune.leopard.in.ua/.

### K3s

This is also pretty straightforward. The playbook aligns with the official quick start guide https://docs.k3s.io/quick-start, although I would recommend something more production-ready like this [Ansible repo](https://github.com/k3s-io/k3s-ansible) or using Talos (highly recommend trying it).

On top of it, the setup installs Helm, Longhorn, the CNPG operator, and finally our cluster manifest with the same pgtune overrides.

I only tested local path and longhorn as csi drivers for CNPG expecting to see a slightly more overhead from longhorn.

## Results

The results are not very surprising, after all we only add latency and work by running PostgreSQL with CNPG. But it is interesting to see the numbers and how they compare to regular PostgreSQL. Also maybe there is something wrong with how much overhead longhorn adds, which i will be investigating in the future.

```sql benchmarks
select
    'read-only pgbench' as benchmark,
    'PG' as system,
    40819.319622::int as tps
union all
select
    'read-write pgbench' as benchmark,
    'PG' as system,
    8176.927887::int as tps
union all
select
    'read-only pgbench' as benchmark,
    'CNPG + longhorn' as system,
    8562.530432::int as tps
union all
select
    'read-write pgbench' as benchmark,
    'CNPG + longhorn' as system,
    2497.811928::int as tps
union all
select
    'read-only pgbench' as benchmark,
    'CNPG + local path' as system,
    37963.010676::int as tps
union all
select
    'read-write pgbench' as benchmark,
    'CNPG + local path' as system,
    7269.751636::int as tps
```

<BarChart
    data={benchmarks}
    x=benchmark
    y=tps
    series=system
    type=grouped
    title="PG vs CNPG benchmarks"
    yAxisTitle="TPS"
    xAxisTitle="Benchmark type"
    valueSuffix=" TPS"
    labels=true
    yFmt=num1k
/>

## Conclusion

It is too early to draw any conclusions from these results, but it is clear that there is an overhead when running PostgreSQL in Kubernetes with CNPG. This is not necessarily a bad thing, as CNPG provides a lot of benefits in terms of scalability, availability, and manageability.

For myself, I have already decided that CNPG is amazing—super simple and easy to use. But it is not a solution for every use case, and it is important to evaluate the trade-offs before choosing to run PostgreSQL in Kubernetes with CNPG. For future experiments, I will be adding:

- Testing with different storage solutions
- Investigating the overhead of longhorn and how to optimize it
- Testing with different Kubernetes distributions (like k8s or Talos)
- Testing with different PostgreSQL versions (like 17 or 19 when it comes out)
- Testing with different workloads (like OLTP or OLAP)
