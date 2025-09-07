# SSL Certificate Generation with Let's Encrypt

## Purpose

Generate SSL certificates for lab environment usage, enabling secure HTTPS connections for services like ArgoCD (argocd.lab.s-miras.com) when mapping domains to local infrastructure instead of VPS hosting.

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
  -d "*.your-domain.com"
```

## DNS Configuration

When prompted, add the TXT DNS records to your domain's DNS settings.

## Certificate Location

Certificates will be saved to:

```
/etc/letsencrypt/live/<your-domain.com>/
```

**Note:** Replace `<your-email@example.com>` and `<your-domain.com>` with your actual email and domain.
