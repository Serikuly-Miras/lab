# Kubernetes Lab Environment

Repo designated for managing and documenting everything I am running.

## Servers Overview

```
AMD 6600H / Proxmox VE 9.1.6 (Mini PC)
    ├── 6 CPU / 12 vCPU
    ├── 48GB DDR5 5600 RAM
    ├── 1TB Fast NVMe SSD (SSD1) / 1TB Slower NVMe SSD (SSD2)
    │
    └─── Talos 1.12.4 Cluster (K8s Rev: v1.35.0)
        ├── Control Plane Nodes
        │   └── 2 CPU / 4GB RAM / 100GB SSD1
        │
        └── Worker Nodes
            ├─── 4 CPU / 16GB RAM / 350GB SSD1
            ├─── 4 CPU / 16GB RAM / 350GB SSD1
            └─── 2 CPU /  8GB RAM / 600GB SSD2

AMD CPX11 / Ubuntu 24.04.4 LTS (Hetzner VPS)
    ├── 2 vCPU
    ├── 2GB RAM
    └── 40GB Disk
```

## Roadmap

Tools and technologies I am currently running or plan to run in the lab environment.

### Infrastructure & Platform

- [x] **Talos Linux** - Immutable Kubernetes OS
- [x] **ArgoCD** - GitOps continuous deployment
- [x] **Longhorn** - Distributed block storage
- [x] **Vault + External Secrets Operator** - Secret management
- [ ] **VPA** - Vertical Pod Autoscaler for resource optimization
- [ ] **HPA** - Horizontal Pod Autoscaler example
- [ ] **KEDA** - Kubernetes Event-Driven Autoscaling example

### Observability (LGTM Stack)

- [x] **Grafana** - Visualization and dashboards
- [x] **Tempo** - Distributed tracing
- [x] **Mimir/Prometheus** - Metrics storage and querying
- [ ] **Alloy** - Telemetry collection
- [ ] **Loki** - Log aggregation

### Data Platform

- [x] **Cloud Native PostgreSQL (CNPG)** - PostgreSQL
- [x] **SeaweedFS** - Object storage / S3
- [x] **Apache Airflow** - Workflow orchestration
- [x] **DuckLake** - S3 + PostgreSQL backed Lakehouse
- [x] **DBT/Astronomer cosmos** - Data transformation and orchestration
- [ ] **ClickHouse** - OLAP database
- [ ] **Trino** - Distributed SQL query engine
- [ ] **OpenMetadata** - Data discovery and governance
- [ ] **Apache Iceberg/Delta Lake** - Data lakehouse formats
- [ ] **Kubeflow** - Machine learning platform on Kubernetes

### Optional/Future

- [x] **Pi-Hole** - Tail'net-wide ad blocker / dns override
- [x] **Evidence blog** - s-miras.com (VPS)
- [ ] **Cool 3d printed case and rack** - For the mini PC and future hardware additions

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs / Cosmos dbt projects
├── docs/             # Documentation
├── infra/            # Helm charts, ArgoCD apps, Talos conf files, etc.
└── web/              # s-miras.com evidence website / blog
```
