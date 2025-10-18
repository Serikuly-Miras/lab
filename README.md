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
- [ ] **Argo Workflows**: Kubernetes-native workflow engine
- [ ] **ETL Pipeline**: Data processing with Polars/Pandas/DuckDB over SeaweedFS S3
- [ ] **TodoApp**: Sample application for testing deployments/container registry/vault etc.

### Future Improvements (no order)

- [x] Integrate Vault as certificate provider (replace manual k8s secrets)
- [ ] Enhanced monitoring and observability (setup Grafana dashboards)
- [ ] Headscale migration (replace Tailscale)
- [ ] Postgres backup automation to S3
- [ ] Postgres read replicas
- [ ] Automated etcd backups and disaster recovery procedures
- [ ] Migrate to Talos linux for improved security and manageability

### Some interesting topics to explore

- [ ] 1brc. billion rows challenge

  - [ ] Load data into Postgres and DuckDB
  - [ ] Compare query performance between Postgres and DuckDB
  - [ ] Add simple viz of query/required space per solution

- [ ] Backblaze hard drive data analysis

  - [x] Load data into Postgres and DuckDB (see notebooks)
  - [ ] Compare query performance between Postgres and DuckDB
  - [ ] Visualize trends and patterns in hard drive performance and failures

### Commit message format

`<type>(<scope>): <description>`

#### `<type>`:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation-only changes
- **style**: Changes that do not affect the meaning of the code (e.g., white-space, formatting)
- **refactor/update**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding or correcting tests
- **chore**: Changes to the build process or auxiliary tools and libraries (e.g., documentation generation)

#### `<scope>`:

- **infra**: Changes related to infrastructure setup or configuration
- **db**: Changes related to database schema, queries, or optimizations
- **notebooks**: Changes related to Jupyter notebooks or data analysis scripts
- **ci/cd**: Changes related to continuous integration and deployment pipelines
- **docs**: Changes related to documentation files
