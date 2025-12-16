# Kubernetes Lab Environment

Personal lab environment for experimenting with data engineering and DevOps tools.

Currently migrating from k3s to Talos Linux and from separate VMs running PostgreSQL and ClickHouse to running everything in Kubernetes.

## Architecture Overview

```
AMD Ryzen 5 6600H / Proxmox VE 9.1.2
├── 6 Physical CPU Cores / 12 Virtual CPU Cores
├── 48GB RAM
│
└── Talos Linux Cluster ( in progress... )
    ├── Control Plane Nodes (1x)
    └── Worker Nodes (1x)
```

## Roadmap

### Infrastructure & Platform

- [ ] **Talos Linux** - Immutable Kubernetes OS
- [ ] **ArgoCD** - GitOps continuous deployment
- [ ] **Longhorn** - Distributed block storage
- [ ] **Vault + External Secrets Operator** - Secret management

### Observability (LGTM Stack)

- [ ] **Loki** - Log aggregation
- [ ] **Grafana** - Visualization and dashboards
- [ ] **Tempo** - Distributed tracing
- [ ] **Mimir/Prometheus** - Metrics storage and querying
- [ ] **Alloy** - Telemetry collection

### Data Platform

- [ ] **Cloud Native PostgreSQL (CNPG)** - PostgreSQL
- [ ] **ClickHouse** - OLAP database
- [ ] **SeaweedFS** - Object storage / S3
- [ ] **Apache Airflow** - Workflow orchestration
- [ ] **Apache Iceberg/Delta Lake** - Data lakehouse formats
- [ ] **Trino** - Distributed SQL query engine
- [ ] **DuckLake** - S3 + PostgreSQL backed Lakehouse

### Analytics & ML

- [ ] **JupyterHub** - Interactive notebooks
- [ ] **Apache Spark** - Big data processing
- [ ] **OpenMetadata** - Data discovery and governance

### Optional/Future

- [ ] **Apache Hadoop** - Distributed storage and processing

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs
├── infra/            # Talos configs, Helm charts, ArgoCD apps
├── docs/             # Documentation
└── notebooks/        # Jupyter notebooks
```
