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
- [ ] **ClickHouse**: Columnar database for analytics
- [ ] **Argo Workflows**: Kubernetes-native workflow engine

### Future Improvements

- [x] Integrate Vault as certificate provider (replace manual k8s secrets)
- [ ] Postgres read replicas
- [ ] Migrate to Talos linux for improved security and manageability

### Some interesting topics to explore

- [ ] Backblaze hard drive data analysis
  - [x] Load slice of data into Postgres and DuckDB (see notebooks)
  - [ ] Compare query performance between Postgres, DuckDB and ClickHouse
  - [ ] Visualize trends and patterns in hard drive performance and failures

### Commit message format

`<type>(<scope>): <description>`

#### `<type>`:

- **feat**: A new feature
- **fix**: A bug fix
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

### Schema

<div style="background-color: white; width: 400px; margin: auto; padding: 10px;">
  <div style="text-align: center; border: 1px solid black; margin: auto;">
      <div style="border-bottom: 1px solid black; padding: 10px;">
        <div style="color: black; font-weight: bold;">Proxmox VE 9</div>
        <div style="color: black; font-weight: bold;">Ryzen 6600H, 48GB RAM</div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px;">
          <!-- K3S Single Node -->
          <div style="border: 1px solid black; padding: 10px; background-color: black; color: white; text-align: center;">
              <div>K3S Single Node</div>
              <div style="font-size: 0.9em; color: gray;">CPU: 3, RAM: 16GB</div>
          </div>
          <!-- ClickHouse Node -->
          <div style="border: 1px solid black; padding: 10px; background-color: black; color: white; text-align: center;">
              <div>ClickHouse Node</div>
              <div style="font-size: 0.9em; color: gray;">CPU: 1, RAM: 4GB</div>
          </div>
          <!-- Postgres Master -->
          <div style="border: 1px solid black; padding: 10px; background-color: black; color: white; text-align: center;">
              <div>Postgres Master</div>
              <div style="font-size: 0.9em; color: gray;">CPU: 1, RAM: 4GB</div>
          </div>
          <!-- Postgres Replica -->
          <div style="border: 1px solid black; padding: 10px; background-color: black; color: white; text-align: center;">
              <div>Postgres Replica</div>
              <div style="font-size: 0.9em; color: gray;">CPU: 1, RAM: 4GB</div>
          </div>
      </div>
  </div>
</div>
