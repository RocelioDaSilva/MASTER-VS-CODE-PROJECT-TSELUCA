# Ansible Vault Examples for GEESP-Angola

This guide shows how to use Ansible Vault to encrypt secrets (passwords, API keys, database credentials) for safe storage in version control.

## Quick Start

### 1. Create a Vault-Encrypted File

```bash
# Create a new vault file with interactive prompt
ansible-vault create secrets/prod_db_credentials.yml

# Enter a strong vault password (>16 chars recommended)
# Then type your secrets:
db_postgres_password: "your_secure_postgres_password_here"
db_user: "app_user"
api_key: "your_api_key_here"
```

### 2. View Vault-Protected File

```bash
# Decrypt on-screen (prompts for vault password)
ansible-vault view secrets/prod_db_credentials.yml
```

### 3. Edit Vault-Protected File

```bash
# Edit encrypted file in-place
ansible-vault edit secrets/prod_db_credentials.yml
```

### 4. Encrypt Existing File

```bash
# Convert plain file to vault-protected
ansible-vault encrypt secrets/database.yml
```

## Use Vault Secrets in Playbooks

### Example Playbook: `deploy_app.yml`

```yaml
---
- name: Deploy GEESP-Angola App with Secrets
  hosts: production
  vars_files:
    - secrets/prod_db_credentials.yml  # Vault-encrypted file
    - secrets/api_keys.yml              # Another vault file
  vars:
    app_version: "{{ app_version | default('latest') }}"
  
  tasks:
    - name: Create .env file with secrets
      template:
        src: .env.j2
        dest: /opt/geesp/app/.env
        owner: appuser
        group: appgroup
        mode: '0600'
      vars:
        # Use variables from vault
        postgres_password: "{{ db_postgres_password }}"
        api_key: "{{ api_key }}"
    
    - name: Deploy Docker container with secrets
      docker_container:
        name: geesp-app
        image: geesp-app:{{ app_version }}
        env:
          POSTGRES_PASSWORD: "{{ db_postgres_password }}"
          DATABASE_URL: "postgresql://{{ db_user }}:{{ db_postgres_password }}@db:5432/geesp"
          API_KEY: "{{ api_key }}"
          STREAMLIT_SERVER_PORT: "8501"
        ports:
          - "8501:8501"
        restart_policy: always
```

## Run Playbook with Vault Password

### Option A: Interactive Prompt

```bash
ansible-playbook deploy_app.yml --ask-vault-pass
# Enter vault password when prompted
```

### Option B: Vault Password File

```bash
# Create a password file (don't commit to git!)
echo "your_vault_password_here" > ~/.vault_password

# Restrict permissions
chmod 600 ~/.vault_password

# Run playbook with password file
ansible-playbook deploy_app.yml --vault-password-file=~/.vault_password
```

### Option C: Environment Variable (CI/CD)

```bash
# In CI/CD pipeline, set password as environment variable
export VAULT_PASS="your_vault_password"

# Run with environment variable
ansible-playbook deploy_app.yml --vault-password-file=/dev/stdin < <(echo $VAULT_PASS)
```

## Vault File Organization Best Practices

```
geesp-angola/
├── playbooks/
│   ├── deploy_prod.yml
│   ├── deploy_staging.yml
│   └── maintenance.yml
├── inventory/
│   ├── production.ini
│   ├── staging.ini
│   └── development.ini
└── secrets/                    # ← Add to .gitignore
    ├── prod_db_credentials.yml (vault-encrypted)
    ├── staging_db_credentials.yml (vault-encrypted)
    ├── api_keys.yml            (vault-encrypted)
    └── tls_certificates/       (vault-encrypted files)
```

### gitignore Entry

```bash
# .gitignore
secrets/*.yml
secrets/*/
!secrets/*.template.yml      # Include templates (without real secrets)
.vault_password
```

## Example Vault-Encrypted Variables File

### File: `secrets/prod_db_credentials.yml`
```yaml
# Encrypted with ansible-vault
# Content (when decrypted):
db_postgres_password: "P@ssw0rd!Secure#2026"
db_user: "geesp_app_prod"
db_host: "postgres.prod.internal"
db_port: 5432
db_name: "geesp_production"
api_key: "sk-proj-abc123xyz789..."
redis_password: "RedisP@ss#Secure"
jwt_secret: "long_random_jwt_secret_key_here"
```

## CI/CD Integration (GitHub Actions Example)

```yaml
name: Deploy to Production
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Ansible
        run: pip install ansible
      
      - name: Create vault password file from secret
        env:
          VAULT_PASS: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}
        run: echo "$VAULT_PASS" > /tmp/.vault_pass && chmod 600 /tmp/.vault_pass
      
      - name: Run deployment playbook
        run: |
          ansible-playbook playbooks/deploy_prod.yml \
            --vault-password-file=/tmp/.vault_pass \
            -i inventory/production.ini
      
      - name: Clean up vault password
        if: always()
        run: rm -f /tmp/.vault_pass
```

## Rotating Vault Passwords

```bash
# Change the vault encryption password
ansible-vault rekey secrets/prod_db_credentials.yml
# Prompts for old password, then new password

# Rekey all vault files at once
for file in secrets/*.yml; do ansible-vault rekey "$file"; done
```

## Troubleshooting

**Error: "Decryption failed"**
- Check that vault password is correct
- Verify file is vault-encrypted: `head -1 secrets/file.yml` should show `$ANSIBLE_VAULT;1.1;`

**Error: "vault identity open(...) returned empty"**
- Check file permissions: vault password file must have mode `0600`
- Try `--ask-vault-pass` to verify password works interactively

**Error: "File is not a vault-encrypted file"**
- File may have been accidentally committed unencrypted
- Encrypt it: `ansible-vault encrypt secrets/file.yml`
- Change git history if sensitive data was exposed

## Additional Resources

- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [Ansible Best Practices - Secrets Management](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
