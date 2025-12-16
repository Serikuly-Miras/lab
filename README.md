# Kubernetes Lab Environment

Personal lab environment for experimenting with data engineering / devops tools.

## Roadmap

### Deployments

- [x] **Proxmox + k3s (1 master / 2 workers)**: Simple Kubernetes environment
- [x] **Postgres 18**: Database for upcoming projects
- [x] **ArgoCD**: GitOps continuous deployment
- [x] **Longhorn**: Distributed block storage
- [x] **Vault + Vault secrets operator**: Secret and certificate management
- [x] **Grafana + Prometheus**: Monitoring and observability stack
- [x] **SeaweedFS**: Distributed object storage with S3 compatibility
- [x] **Airflow 3**: Workflow orchestration
- [x] **GitLab + container registry**: Self-hosted git and container registry
- [x] **Data Lake**: Delta Lake or DuckLake implementation
- [x] **ClickHouse**: Columnar database for analytics
- [ ] **Argo Workflows**: Kubernetes-native workflow engine

### Future Improvements

- [x] Integrate Vault as certificate provider (replace manual k8s secrets)
- [x] Postgres read replicas
- [ ] Migrate to Talos linux for improved security and manageability

### Some interesting topics to explore

- [ ] Backblaze hard drive data analysis
  - [x] Load slice of data into Postgres and DuckDB (see notebooks)
  - [ ] Compare query performance between Postgres, DuckDB and ClickHouse
  - [ ] Visualize trends and patterns in hard drive performance and failures

## Infra

```
AMD Ryzen 6600H Proxmox VE 9.0 Host / 6 Physical CPU Cores / 12 Virtual CPU Cores / 48GB RAM
│
└─── K3S single node kubernetes cluster
    ├── CPU: 6 vCPU (3 CPU limit)
    ├── Memory: 16GB
    ├── Storage: 100GB
    │
    └── ArgoCD app of apps
        ├── Longhorn
        ├── HashiCorp Vault
        ├── HashiCorp Vault Secrets Operator
        ├── Kube Prometheus Stack
        ├── Postgres Prometheus Exporter
        ├── SeaweedFS
        └── JupyterHub

```
