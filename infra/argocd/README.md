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
