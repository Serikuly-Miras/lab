# ArgoCD setup

## Purpose

Enabling GitOps workflows for continuous delivery and deployment.

## Setting up

Create a namespace for ArgoCD:

```bash
kubectl create namespace argocd
```

Install ArgoCD using the official manifests:

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

To allow insecure connections and resolve looping redirect via ingress HTTPS - patch the configmap:

```bash
kubectl patch configmap argocd-cmd-params-cm -n argocd \
        --type merge \
        -p '{"data":{"server.insecure":"true"}}'
```

Create tls secret manually then offload to vault secret provider later to acess webui via ingress:

```bash
kubectl create secret generic tls-secret \
  --from-file=ca.crt=/chain.pem \
  --from-file=tls.key=/privkey.pem \
  --from-file=tls.crt=/cert.pem -n <namespace>

kubectl apply -f ingress.yaml -n argocd
```

## Set up VSO (vault secrets operator) for ArgoCD to access TLS certs from vault

1. Enable kv-v2 secrets engine in vault
2. Enable and configure kubernetes auth method in vault
3. Create a policy that grants access to the certificate path
4. Add argocd role to authorize using kubernetes auth method
5. Apply resources needed -

```bash
kubectl apply -f argoc/custom-resources/
```

6. Verify secret syncing

```bash
kubectl describe vaultstaticsecret <secret-name> -n <namespace>
```
