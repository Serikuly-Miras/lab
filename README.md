# Kubernetes Lab Environment

Repo designated for managing home lab Kubernetes cluster and personal website.

## Architecture Overview

```
AMD Ryzen 5 6600H / Proxmox VE 9.1.4
├── 6 CPU / 12 vCPU
├── 48GB DDR5 5600 RAM
├── 1TB Fast NVMe SSD (SSD1) / 1TB Slower NVMe SSD (SSD2)
│
└─── Talos 1.12.0 Cluster (K8s Rev: v1.35.0)
     ├── Control Plane Nodes (1x)
     │   └── 2 CPU / 8GB RAM / 100GB SSD1
     │
     └── Worker Nodes (3x)
         ├─── 4 CPU / 16GB RAM / 350GB SSD1
         ├─── 4 CPU / 12GB RAM / 350GB SSD1
         └─── 2 CPU /  8GB RAM / 600GB SSD2

```

## Roadmap

### Infrastructure & Platform

- [x] **Talos Linux** - Immutable Kubernetes OS
- [x] **ArgoCD** - GitOps continuous deployment
- [x] **Longhorn** - Distributed block storage
- [x] **Vault + External Secrets Operator** - Secret management

### Observability (LGTM Stack)

- [ ] **Loki** - Log aggregation
- [x] **Grafana** - Visualization and dashboards
- [x] **Tempo** - Distributed tracing
- [x] **Mimir/Prometheus** - Metrics storage and querying
- [ ] **Alloy** - Telemetry collection

### Data Platform

- [ ] **Cloud Native PostgreSQL (CNPG)** - PostgreSQL
- [ ] **ClickHouse** - OLAP database
- [x] **SeaweedFS** - Object storage / S3
- [ ] **Apache Airflow** - Workflow orchestration
- [ ] **Apache Iceberg/Delta Lake** - Data lakehouse formats
- [ ] **Trino** - Distributed SQL query engine
- [ ] **DuckLake** - S3 + PostgreSQL backed Lakehouse
- [ ] **OpenMetadata** - Data discovery and governance

### Optional/Future

- [x] **Pi-Hole** - Tail'net-wide ad blocker / dns override

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs
├── docs/             # Documentation
├── infra/            # Helm charts, ArgoCD apps etc.
├── notebooks/        # Jupyter notebooks
├── talos/            # Talos Linux configs
└── web/              # s-miras.com website
```
