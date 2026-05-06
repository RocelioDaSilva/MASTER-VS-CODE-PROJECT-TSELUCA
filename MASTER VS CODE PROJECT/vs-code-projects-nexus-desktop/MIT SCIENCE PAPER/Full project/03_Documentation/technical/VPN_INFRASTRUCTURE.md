# VPN & Field Infrastructure Guide

Purpose: provide secure connectivity and data transfer patterns for field teams collecting survey and monitoring data.

Recommended approaches

- WireGuard (preferred): lightweight, performant, easy to deploy on field devices and small cloud gateways.
- OpenVPN: well-known alternative; use only if WireGuard is not possible.
- SFTP/SCP or HTTPS to a secure API endpoint for direct uploads from devices.
- Consider using an intermediary sync tool (rclone) to push to S3-compatible storage with server-side encryption.

WireGuard Quickstart (server)

1. Install WireGuard on your cloud gateway (Ubuntu example):

```bash
sudo apt update && sudo apt install -y wireguard
umask 077
wg genkey | tee server_private.key | wg pubkey > server_public.key
```

2. Create `/etc/wireguard/wg0.conf` with server private key and allowed IPs; enable forwarding and NAT.

3. Start and enable service:

```bash
sudo systemctl enable --now [email protected]
```
```

WireGuard Quickstart (device)

- Generate a keypair on each device and add peer entry on server with `AllowedIPs` = e.g. `10.10.0.2/32`.
- Use short-lived pre-shared keys for extra security.

Security & operational notes

- Use certificate/key rotation every 90 days.
- Limit permitted IPs and services exposed through the VPN (restrict to SFTP/API endpoints and DB admin subnet if necessary).
- Monitor connections and log unusual IPs.
- Use a bastion host + MFA for administrative RDP/SSH access.

Data transfer patterns

- Preferred: device -> secure API endpoint (HTTPS with client certs) -> backend ingestion queue
- Alternative: device -> SFTP to gateway -> periodic batch import (use `inotify` or cron to trigger ingestion)
- Use signed payloads and sequence numbers to detect replay or missing uploads.

Field device recommendations

- Use modern Android devices with automated `rclone` + WireGuard configuration.
- Keep local storage encrypted; enable remote wipe via MDM if available.
- Use retry/backoff logic on upload failures and persistent queueing.

Operational runbook (short)

- On data-loss: check device logs, verify last upload timestamp, run `scripts/db_restore.sh` if needed (DB admin only).
- On VPN outage: check server `wg show` and device logs; restart `wg-quick` and ensure NAT rules preserved.

Where to store secrets

- Do NOT store `PGPASSWORD`, private keys, or WireGuard private keys in source control.
- Use a secret manager (AWS Secrets Manager, Azure Key Vault) or an encrypted `.env` file kept out of repo.

If you want, I can generate example WireGuard configs per device and a server template, or prepare an Ansible playbook to provision the gateway and VPN users.