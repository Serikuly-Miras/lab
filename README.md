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
- [x] **Airflow**: Workflow orchestration
- [ ] **Argo Workflows**: Kubernetes-native workflow engine
- [ ] **Data Lake**: Delta Lake or DuckLake implementation
- [ ] **Harbor**: Self-hosted container registry
- [ ] **ETL Pipeline**: Data processing with Polars/Pandas/DuckDB over SeaweedFS S3
- [ ] **TodoApp**: Sample application for testing deployments/harbor/vault etc.

### Future Improvements

- [x] Integrate Vault as certificate provider (replace manual k8s secrets)
- [ ] Enhanced monitoring and observability
- [ ] Headscale migration (replace Tailscale)
- [ ] Postgres backup automation to S3
- [ ] Postgres read replicas
- [ ] Automated etcd backups and disaster recovery procedures

### Some intresting topics to explore

- [ ] 1brc. billion rows challenge
  - [x] Load txt and parquet files into S3 (see notebooks)
  - [ ] Load into delta lake or duck lake
  - [ ] Use airflow to orchestrate processing
  - [ ] Use argo workflows to orchestrate processing
  - [ ] Run and collect benchmarks with visualization
