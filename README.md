# Kubernetes Lab Environment

Repo designated for managing and documenting everything I am running.

## Servers Overview

```
AMD Ryzen5 6600H / Talos 1.12.6 baremetal
    ├── 6 CPU / 12 vCPU
    ├── 48GB DDR5 4800 RAM
    ├── 1TB NVMe SSD (200GB EPHEMERAL, 800GB local path provisioner)
    └── 500GB NVMe SSD (longhorn provisioner)
```

## Architecture Overview

### Storage

#### Foundation

- [x] **Local Path Provisioner** - Local storage for stateful workloads
- [x] **Longhorn** - Distributed block storage
- [x] **SeaweedFS** - Object storage / S3

#### Data Platform

- [x] **Cloud Native PostgreSQL (CNPG) operator** - PostgreSQL
- [x] **ClickHouse operator** - ClickHouse
- [x] **Starrocks operator** - Starrocks
- [x] **Apache Iceberg** - Alternative lakehouse
- [ ] **OpenMetadata** - Data discovery and governance

### Orchestration & Workflow

- [x] **Apache Airflow** - Workflow orchestration
- [x] **DBT/Astronomer cosmos** - Data transformation and orchestration
- [x] **Trino** - Distributed SQL query engine

### Must-have

- [x] **ArgoCD** - GitOps continuous deployment
- [x] **Vault + External Secrets Operator** - Secret management
- [x] **Prometheus** - Metrics storage and querying
- [x] **Grafana** - Visualization and dashboards
- [x] **Tempo** - Distributed tracing
- [ ] **Loki** - Log aggregation
- [ ] **Alloy** - Telemetry collection

### Nice-to-have

- [x] **Pi-Hole** - Tail'net-wide ad blocker / dns override
- [ ] **Kubevirt** - VMs in Kubernetes

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs / Cosmos dbt projects
├── docs/             # Documentation
└── infra/            # Helm charts, ArgoCD apps, Talos conf files, etc.
```
