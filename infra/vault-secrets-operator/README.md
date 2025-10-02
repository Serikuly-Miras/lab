# Vault secrets operator

Used to manage secrets and certificates in Kubernetes using HashiCorp Vault.

## Prerequisites outside of yaml config files

### Enable kv-v2 secrets engine in Vault (if not already enabled):

```sh
~ vault secrets enable -path=kvv2 kv-v2
```

### Create a policy for the operator to access specific secrets (adjust paths as needed):

```sh
~ vault policy write lab-acl - <<EOF
path "kvv2/data/seaweedfs" {
capabilities = ["read"]
}
path "kvv2/metadata/seaweedfs" {
capabilities = ["read"]
}
EOF
```

### Enable Kubernetes authentication method, dont forget to configure:

```sh
~ vault auth enable -path=vso kubernetes
```

### Apply files (sa, va, vc) and everything should work

### Create secret and see events to debug if it isnt syncing properly

```yaml
# example secret
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: sw-s3-static-secret
  namespace: lab
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
spec:
  vaultAuthRef: vault-auth
  mount: kvv2
  type: kv-v2
  path: seaweedfs
  destination:
    create: true
    name: sw-s3-auth-secret
  refreshAfter: 10s
```

```
kubectl describe vaultstaticsecretsw-s3-static-secret -n lab
```
