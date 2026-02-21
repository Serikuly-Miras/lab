# Kubernetes Lab Environment

Repo designated for managing and documenting everything I am running (s-miras.com + experiments on a homelab).

## Architecture Overview

```
│
├─── AMD 6600H / Proxmox VE 9.1.4 (Mini PC)
│    ├── 6 CPU / 12 vCPU
│    ├── 48GB DDR5 5600 RAM
│    ├── 1TB Fast NVMe SSD (SSD1) / 1TB Slower NVMe SSD (SSD2)
│    │
│    └─── Talos 1.12.0 Cluster (K8s Rev: v1.35.0)
│        ├── Control Plane Nodes
│        │   └── 2 CPU / 8GB RAM / 100GB SSD1
│        │
│        └── Worker Nodes (3x)
│            ├─── 4 CPU / 16GB RAM / 350GB SSD1
│            ├─── 4 CPU / 12GB RAM / 350GB SSD1
│            └─── 2 CPU /  8GB RAM / 600GB SSD2
│
├─── INTEL 8750H / Ubuntu 24.04.4 LTS (Old Legion Laptop)
│    ├── 6 CPU / 12 vCPU
│    ├── 32GB DDR4 2667 RAM
│    ├── 500GB NVMe SSD
│    │
│    └─── ClickHouse 26.1.3 (Single Node)
│
└─── AMD CPX11 / Ubuntu 24.04.4 LTS (Hetzner VPS)
     ├── 2 vCPU
     ├── 2GB RAM
     └── 40GB Disk
```

## Roadmap

### Infrastructure & Platform

- [x] **Talos Linux** - Immutable Kubernetes OS
- [x] **ArgoCD** - GitOps continuous deployment
- [x] **Longhorn** - Distributed block storage
- [x] **Vault + External Secrets Operator** - Secret management

### Observability (LGTM Stack)

- [x] **Grafana** - Visualization and dashboards
- [x] **Tempo** - Distributed tracing
- [x] **Mimir/Prometheus** - Metrics storage and querying
- [ ] **Alloy** - Telemetry collection
- [ ] **Loki** - Log aggregation

### Data Platform

- [x] **Cloud Native PostgreSQL (CNPG)** - PostgreSQL
- [x] **ClickHouse** - OLAP database
- [x] **SeaweedFS** - Object storage / S3
- [x] **Apache Airflow** - Workflow orchestration
- [x] **DuckLake** - S3 + PostgreSQL backed Lakehouse
- [ ] **Trino** - Distributed SQL query engine
- [ ] **OpenMetadata** - Data discovery and governance
- [ ] **Apache Iceberg/Delta Lake** - Data lakehouse formats

### Optional/Future

- [x] **Pi-Hole** - Tail'net-wide ad blocker / dns override

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs
├── docs/             # Documentation
├── infra/            # Helm charts, ArgoCD apps etc.
├── talos/            # Talos Linux configs
└── web/              # s-miras.com website
```
