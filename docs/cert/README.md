# SSL Certificate Generation with Let's Encrypt

## Purpose

Generate SSL certificates for lab environment usage from a trusted CA fo ease of use locally.
Requires having a domain and access to its DNS settings.

## Prerequisites

Install certbot:

```bash
sudo apt update && sudo apt install certbot
```

## Generate Wildcard Certificate

Run certbot with manual DNS challenge:

```bash
sudo certbot certonly \
  --manual \
  --preferred-challenges dns \
  --email <your-email@example.com> \
  --server https://acme-v02.api.letsencrypt.org/directory \
  --agree-tos \
  -d <your-domain.com> \
  -d *.<your-domain.com> \
  -d *.lab.<your-domain.com>
```

## DNS Configuration

When prompted, add the TXT DNS records to your domain's DNS settings.

## Certificate Location

Certificates will be saved to:

```
/etc/letsencrypt/live/<your-domain.com>/
```

**Note:** Replace `<your-email@example.com>` and `<your-domain.com>` with your actual email and domain.

## Creating Kubernetes Secret

When bootstrapping create secret manually, then offload that tasks to vault secret provider.

```bash
kubectl create secret generic tls-secret \
  --from-file=ca.crt=/chain.pem \
  --from-file=tls.key=/privkey.pem \
  --from-file=tls.crt=/cert.pem -n <namespace>
```

# Auto certificate provisioning/renewal with Tailscale Magic DNS and Traefik

## Nothing here for now
