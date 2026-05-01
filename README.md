# Kubernetes Lab Environment

Repo designated for managing and documenting everything I am running.

## Servers Overview

```
AMD Ryzen5 6600H / Talos 1.12.6 baremetal
    ├── 6 CPU / 12 vCPU
    ├── 48GB DDR5 4800 RAM
    ├── 1TB NVMe SSD (200GB EPHEMERAL, 800GB local path provisioner)
    └── 500GB NVMe SSD (longhorn provisioner)

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
- [ ] **Loki** - Log aggregation
- [ ] **Alloy** - Telemetry collection

### Data Platform

- [x] **Cloud Native PostgreSQL (CNPG) operator** - PostgreSQL
- [x] **ClickHouse operator** - ClickHouse
- [x] **SeaweedFS** - Object storage / S3
- [x] **DuckLake** - SeaweedFS S3 + PostgreSQL backed Lakehouse
- [x] **Apache Airflow** - Workflow orchestration
- [x] **DBT/Astronomer cosmos** - Data transformation and orchestration
- [x] **ClickHouse** - OLAP database
- [x] **Trino** - Distributed SQL query engine
- [x] **Apache Iceberg/Delta Lake** - Alternative lakehouse
- [ ] **OpenMetadata** - Data discovery and governance

### Optional/Future

- [x] **Pi-Hole** - Tail'net-wide ad blocker / dns override
- [x] **Evidence blog** - s-miras.com (VPS)
- [x] **Hetzner Offsite S3** - longhorn backup target
- [ ] **Kubevirt** - VMs in Kubernetes

## Architecture

```mermaid
flowchart TD
    subgraph HW["Hardware"]
        NODE["Ryzen5 6600H · 12vCPU · 48GB DDR5\n1TB NVMe + 500GB NVMe · Baremetal"]
        VPS["CPX11 Hetzner VPS\n2vCPU · 2GB RAM · 40GB"]
    end

    subgraph OS["Operating System"]
        TALOS["Talos Linux 1.12.6"]
        UBUNTU["Ubuntu 24.04 LTS"]
    end

    subgraph K8S["Kubernetes"]
        ARGO["ArgoCD (GitOps)"]
    end

    subgraph STORAGE["Storage"]
        LONGHORN["Longhorn\nblock storage"]
        LPP["Local Path\nProvisioner"]
        SWFS["SeaweedFS\nS3 / object storage"]
        HETZ_S3["Hetzner S3\noffsite backup"]
    end

    subgraph SEC["Security & Networking"]
        VAULT["Vault"]
        ESO["External Secrets\nOperator"]
        CERT["cert-manager"]
        TRAEFIK["Traefik\ningress"]
        TS["Tailscale\noperator"]
        PIHOLE["Pi-Hole\nDNS"]
    end

    subgraph OBS["Observability"]
        PROM["Prometheus / Mimir\nmetrics"]
        TEMPO["Tempo\ntracing"]
        GRAFANA["Grafana\ndashboards"]
    end

    subgraph DB["Databases"]
        PG["PostgreSQL\nCNPG operator"]
        CH["ClickHouse\nOLAP"]
        KAFKA["Kafka\nStrimzi operator"]
    end

    subgraph LAKE["Lakehouse"]
        DUCKLAKE["DuckLake\nS3 + PG catalog"]
        ICEBERG["Iceberg / Delta Lake\nalternative format"]
        TRINO["Trino\ndistributed SQL"]
    end

    subgraph ORCH["Orchestration & Transformation"]
        AIRFLOW["Apache Airflow"]
        DBT["dbt / Astronomer Cosmos"]
    end

    subgraph WEB["Presentation"]
        EVIDENCE["Evidence\ns-miras.com"]
    end

    NODE --> TALOS --> ARGO
    VPS --> UBUNTU

    ARGO --> LONGHORN & LPP & SWFS
    LONGHORN --> HETZ_S3
    ARGO --> VAULT & CERT & TRAEFIK & TS & PIHOLE
    VAULT --> ESO

    ARGO --> PROM & TEMPO
    PROM & TEMPO --> GRAFANA

    ARGO --> PG & CH & KAFKA
    LPP & SWFS --> PG
    SWFS --> DUCKLAKE
    PG --> DUCKLAKE
    PG & CH --> ICEBERG

    DUCKLAKE & ICEBERG & CH --> TRINO

    TRINO & PG & KAFKA --> AIRFLOW
    AIRFLOW --> DBT
    DBT --> CH & DUCKLAKE

    TRINO & CH --> EVIDENCE
    UBUNTU --> EVIDENCE
```

## Directory Structure

```
lab/
├── dags/             # Airflow DAGs / Cosmos dbt projects
├── docs/             # Documentation
├── infra/            # Helm charts, ArgoCD apps, Talos conf files, etc.
└── web/              # s-miras.com evidence website / blog
```
