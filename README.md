# Kubernetes Lab Environment

Repo designated for managing and documenting everything I am running.

## Servers Overview

```
AMD Ryzen5 6600H / Talos 1.12.6 baremetal
    ├── 6 CPU / 12 vCPU
    ├── 48GB DDR5 4800 RAM
    ├── 1TB NVMe SSD (200GB EPHEMERAL, 800GB local path provisioner)
    └── 500GB NVMe SSD (longhorn provisioner)

HETZNER S3 Object Storage (Offsite backups)
```

## Architecture Overview

### Storage

#### Foundation

- [x] **Local Path Provisioner** - Local storage for stateful workloads
- [x] **Longhorn** - Distributed block storage
- [x] **SeaweedFS** - Object storage / S3

#### Data Platforms

- [x] **Cloud Native PostgreSQL (CNPG) operator** - PostgreSQL
- [x] **Starrocks** - Starrocks (main OLAP database)
- [x] **Apache Iceberg** - Open table format for data lakes
- [ ] **OpenMetadata** - Data discovery and governance

#### Streaming

- [x] **Strimzi Kafka operator** - Kafka and Kafka Connect
- [x] **Postgresql CDC source** - Debezium connector for PostgreSQL
- [x] **Starrocks sink** - Starrocks sink connector for Kafka Connect

### Orchestration & Workflow

- [x] **Apache Airflow** - Workflow orchestration
- [x] **DBT/Astronomer cosmos** - Data transformation and orchestration

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
- [ ] **Gitea** - Self-hosted Git server (mirroring GitHub)

### Was deployed but removed for not having use rn

- [ ] **ClickHouse** - ClickHouse (secondary OLAP database)
- [ ] **Trino** - Distributed SQL query engine
- [ ] **DuckLake** - New lakehouse platform built on top of oltp + s3

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs / Cosmos dbt projects
├── docs/             # Documentation
└── infra/            # Helm charts, ArgoCD apps, Talos conf files, etc.
```
