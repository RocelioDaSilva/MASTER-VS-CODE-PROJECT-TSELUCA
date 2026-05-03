# Production Secret Management Guide for GEESP-Angola

## Overview

Secure secret management is critical for protecting:
- Database credentials (PostgreSQL, Redis)
- API keys and authentication tokens
- TLS certificates and private keys
- Third-party service credentials (email, Slack, etc.)

This guide covers best practices and implementation patterns for GEESP-Angola.

## Secret Types and Storage

| Secret Type | Where | How | Rotation |
|-------------|-------|-----|----------|
| Database passwords | Ansible Vault / K8s Secrets | Encrypted at rest | 90 days |
| API keys | Environment / CI/CD secrets | Encrypted transit | 180 days |
| Private keys (TLS) | File + permissions | Encrypted file + 0600 mode | 365 days |
| OAuth tokens | Redis (transient) | In-memory, short TTL | As per OAuth provider |
| Service account creds | Vault / sealed secrets | Encrypted backend | 30 days |

## Implementation Patterns

### Pattern 1: Environment Variables (Development)

```bash
# .env file (never commit)
POSTGRES_PASSWORD=dev_password_only
REDIS_PASSWORD=redis_dev_pass
API_KEY=dev_key_only

# .env.example (committed, no real values)
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-change_me}
REDIS_PASSWORD=${REDIS_PASSWORD:-change_me}
API_KEY=${API_KEY:-change_me}

# Load and run
set -a
source .env
set +a
docker-compose up
```

### Pattern 2: Ansible Vault (Staging/Production)

```bash
# Create vault file with secrets
ansible-vault create secrets/prod_credentials.yml

# Content:
db_password: "P@ssw0rd!Secure#2026"
api_key: "sk-proj-abc123xyz789..."
redis_password: "Redis#Secure2026"

# Use in playbook
- name: Deploy with secrets
  hosts: production
  vars_files:
    - secrets/prod_credentials.yml
  tasks:
    - name: Set environment variables
      environment:
        POSTGRES_PASSWORD: "{{ db_password }}"
        API_KEY: "{{ api_key }}"
      docker_container:
        name: geesp-app
        ...
```

### Pattern 3: Container Orchestration Secrets (Kubernetes)

```bash
# Create K8s secrets from files
kubectl create secret generic geesp-db-credentials \
  --from-literal=username=geesp_user \
  --from-literal=password=secure_password

# Or from YAML
kubectl apply -f secrets.yaml

# Reference in deployment
spec:
  containers:
  - name: geesp-app
    env:
    - name: POSTGRES_PASSWORD
      valueFrom:
        secretKeyRef:
          name: geesp-db-credentials
          key: password
```

### Pattern 4: Docker Secret (Swarm)

```bash
# Create secret (only available to services that need it)
echo "secure_password" | docker secret create db_password -

# Use in service
docker service create \
  --secret db_password \
  --env POSTGRES_PASSWORD_FILE=/run/secrets/db_password \
  geesp-app
```

### Pattern 5: HashiCorp Vault (Enterprise)

```bash
# Write secret to Vault
vault write secret/geesp/prod \
  db_password="secure_password" \
  api_key="sk-proj-abc123..."

# Authenticate and retrieve in application
vault login -method=approle
export POSTGRES_PASSWORD=$(vault read -field=db_password secret/geesp/prod)
```

## Secret Rotation Best Practices

### Automated Rotation Script

```bash
#!/bin/bash
# scripts/rotate_secrets.sh
# Rotate secrets every N days (e.g., 90 days for DB passwords)

ROTATION_INTERVAL_DAYS=90
LAST_ROTATION_FILE=".last_rotation"

check_rotation_needed() {
    if [ ! -f "$LAST_ROTATION_FILE" ]; then
        return 0  # First time
    fi
    
    LAST_ROTATION=$(cat "$LAST_ROTATION_FILE")
    CURRENT_TIME=$(date +%s)
    DIFF=$((($CURRENT_TIME - $LAST_ROTATION) / 86400))  # Convert to days
    
    if [ $DIFF -ge $ROTATION_INTERVAL_DAYS ]; then
        return 0  # Rotation needed
    fi
    return 1
}

rotate_database_password() {
    local NEW_PASSWORD=$(openssl rand -base64 32)
    
    # Update in PostgreSQL
    PGPASSWORD=$POSTGRES_PASSWORD psql \
        -h localhost -U postgres \
        -c "ALTER USER geesp_app WITH PASSWORD '$NEW_PASSWORD';"
    
    # Update in Vault / Ansible Vault / K8s Secret
    # Example for Ansible Vault:
    ansible-vault encrypt_string "$NEW_PASSWORD" \
        --name db_password > secrets/prod_credentials.yml.new
    
    # Backup old secret
    cp secrets/prod_credentials.yml "secrets/prod_credentials.yml.bak.$(date +%s)"
    
    # Update and redeploy
    mv secrets/prod_credentials.yml.new secrets/prod_credentials.yml
    
    # Record rotation time
    date +%s > "$LAST_ROTATION_FILE"
    
    echo "Database password rotated successfully"
}

rotate_api_keys() {
    # Similar pattern for API keys
    # Call provider-specific endpoint to revoke old key and generate new one
    curl -X POST "https://api.provider.com/keys/revoke" \
        -H "Authorization: Bearer $OLD_API_KEY"
    
    NEW_API_KEY=$(curl -X POST "https://api.provider.com/keys/create")
    
    # Update in secret store
    ansible-vault edit secrets/prod_credentials.yml
}

if check_rotation_needed; then
    echo "Rotating secrets..."
    rotate_database_password
    rotate_api_keys
else
    echo "Secrets are still fresh"
fi
```

## CI/CD Integration for Secrets

### GitHub Actions

```yaml
name: Deploy with Secrets
on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Create vault password from GitHub secret
      - name: Create Ansible vault password
        env:
          VAULT_PASS: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}
        run: echo "$VAULT_PASS" > /tmp/.vault_pass && chmod 600 /tmp/.vault_pass
      
      # Decrypt secrets for use in deployment
      - name: Decrypt secrets
        run: >
          ansible-vault view 
          --vault-password-file=/tmp/.vault_pass
          secrets/prod_credentials.yml > /tmp/decrypted_secrets
      
      # Build and push image with credentials
      - name: Build and push Docker image
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u $ --password-stdin
          docker build -t $REGISTRY/geesp-app:latest .
          docker push $REGISTRY/geesp-app:latest
      
      # Deploy with decrypted secrets (CI has access to files)
      - name: Deploy to production
        run: |
          ansible-playbook deploy.yml \
            --vault-password-file=/tmp/.vault_pass
      
      # Clean up sensitive files
      - name: Clean up secrets
        if: always()
        run: |
          rm -f /tmp/.vault_pass /tmp/decrypted_secrets
          history -c  # Clear bash history with secrets
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  script:
    # Create vault password file from CI/CD variable
    - echo "$VAULT_PASSWORD" > ~/.vault_password
    - chmod 600 ~/.vault_password
    
    # Decrypt and use secrets
    - ansible-vault view --vault-password-file=~/.vault_password secrets/prod_credentials.yml
    
    # Run deployment
    - ansible-playbook deploy.yml --vault-password-file=~/.vault_password
  after_script:
    # Always clean up
    - rm -f ~/.vault_password
  only:
    - main
```

## Secret Audit and Monitoring

### Audit Trail

```bash
# Log all secret access
ansible-vault view --audit-log secrets/prod_credentials.yml

# Monitor unauthorized access attempts
grep "FAILED.*vault" /var/log/secure
grep "vault.*unauthorized" /var/log/audit.log

# Track who rotated secrets and when
git log --all --oneline -- secrets/ | head -20
```

### Secrets Scanning

```bash
# Prevent accidental commits of secrets
pip install detect-secrets

# Add pre-commit hook
detect-secrets scan --all-files

# Scan for exposed API keys in code
git log -p --all | grep -i "api[_-]key"

# Use tools like GitGuardian for automated scanning
# Configure webhook in GitHub: https://dashboard.gitguardian.com/
```

## Incident Response: Compromised Secret

If a secret is compromised:

1. **Immediately revoke** the secret at the source
2. **Rotate** to a new secret
3. **Audit logs** for misuse during exposure window
4. **Notify stakeholders** (team, users if needed)
5. **Update deployments** with new secret
6. **Document incident** for compliance/review

```bash
#!/bin/bash
# scripts/emergency_secret_rotation.sh

COMPROMISED_SECRET="api_key"
NEW_SECRET=$(openssl rand -base64 32)

# 1. Revoke old secret with API provider
curl -X POST "https://api.provider.com/revoke" \
    -H "Authorization: Bearer $COMPROMISED_SECRET"

# 2. Update secret in all locations
ansible-vault edit secrets/prod_credentials.yml  # Update manually or via script

# 3. Redeploy with new secret
ansible-playbook deploy.yml -e "quick_redeploy=true"

# 4. Verify new secret is in use
curl -H "Authorization: Bearer $NEW_SECRET" https://api.provider.com/verify

# 5. Log incident
echo "$(date): Emergency rotation of $COMPROMISED_SECRET" >> incidents.log
```

## Checklist: Secret Management Setup

- [ ] All secrets moved out of code and environment variables
- [ ] Ansible Vault configured with strong password (>16 chars)
- [ ] Vault password file not committed to git (added to .gitignore)
- [ ] Pre-commit hooks installed to prevent secret leaks
- [ ] Secret rotation schedule established (90/180/365 days per type)
- [ ] Audit logging enabled for all secret access
- [ ] CI/CD pipeline uses GitHub Secrets / GitLab Variables
- [ ] Production deployments use Ansible Vault or K8s Secrets
- [ ] Emergency rotation procedures documented
- [ ] Team trained on secret management practices
- [ ] Regular audit of who has access to secrets

## References

- [OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [CIS Docker Benchmark: Secret Management](https://www.cisecurity.org/benchmark/docker)
- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
