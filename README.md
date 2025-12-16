# Kubernetes Lab Environment

Personal lab environment for experimenting with data engineering / devops tools.

Right now in a process of migrating from k3s to Talos linux and from separate vms running postgres and clickhouse to running everything in kubernetes.

## Roadmap

### Deployments

- [ ] **Talos**
- [ ] **LGTM stack**
  - [ ] **Loki**
  - [ ] **Grafana**
  - [ ] **Tempo**
  - [ ] **Prometheus in place of Mimir**
  - [ ] **Alloy**
- [ ] **ArgoCD**
- [ ] **Longhorn**
- [ ] **Vault + Vault secrets operator**
- [ ] **Cloud Native PostgreSQL**
- [ ] **SeaweedFS**
- [ ] **Airflow**
- [ ] **Duck Lake**
- [ ] **ClickHouse**
- [ ] **JupyterHub**
- [ ] **OpenMetadata**
- [ ] **Trino/Presto**
- [ ] **PySpark (in kubernetes?)**
- [ ] **Hadoop (in kubernetes?)**

## Infra

```
AMD Ryzen 6600H Proxmox VE 9.1.2 Host / 6 Physical CPU Cores / 12 Virtual CPU Cores / 48GB RAM
│
└─── Talos ....
```
