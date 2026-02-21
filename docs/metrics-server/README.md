# Metrics Server on Talos

## Patch Talos Machine Configs

Refer to the [Sidero Labs documentation](https://docs.siderolabs.com/kubernetes-guides/monitoring-and-observability/deploy-metrics-server) for details on patching your Talos machine configs.

Apply the following manifests to your cluster:

```sh
# Install kubelet-serving-cert-approver
kubectl apply -f https://raw.githubusercontent.com/alex1989hu/kubelet-serving-cert-approver/main/deploy/standalone-install.yaml

# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
