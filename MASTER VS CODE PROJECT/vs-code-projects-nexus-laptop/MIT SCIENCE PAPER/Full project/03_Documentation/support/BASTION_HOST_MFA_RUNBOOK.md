# 🔐 Bastion Host & MFA Setup Runbook

**Version**: 1.0 | **Date**: February 2026  
**Purpose**: Harden administrative access to GEESP-Angola infrastructure using bastion host + MFA  
**Audience**: DevOps engineers, system administrators

---

## **Table of Contents**

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Bastion Host Setup](#bastion-host-setup)
4. [MFA Configuration (TOTP)](#mfa-configuration-totp)
5. [User Provisioning](#user-provisioning)
6. [Access & Login Flow](#access--login-flow)
7. [Audit Logging](#audit-logging)
8. [Troubleshooting](#troubleshooting)

---

## **Architecture Overview**

```
Developer/Admin
       ↓
   [Internet]
       ↓
Bastion Host (SSH)
   ├─ MFA/TOTP gate
   ├─ Audit logging
   └─ Key forwarding
       ↓
App Servers (Internal Network)
   ├─ PostgreSQL
   ├─ Redis
   └─ API Servers
```

**Key Security Principles:**
- **Bastion**: Single entry point, hardened, no direct database access
- **MFA**: TOTP (Time-based One-Time Password) adds second factor
- **Logging**: All admin activities recorded for compliance
- **Key Forwarding**: Admin keys never stored on bastion; forwarded from local machine

---

## **Prerequisites**

### **On Your Local Machine**
```bash
# macOS
brew install openssh

# Ubuntu/Debian
sudo apt-get install openssh-client openssh-server

# Windows (use OpenSSH client or PuTTY)
# https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
```

### **Required Software**
- SSH key pair (ED25519 recommended)
- TOTP authenticator app:
  - Google Authenticator
  - Authy
  - Microsoft Authenticator
  - FreeOTP
  - 1Password

### **Network**
- Bastion host must be internet-accessible (public IP or cloud)
- Application servers behind NAT/firewall (accessible only from bastion)

---

## **Bastion Host Setup**

### **Step 1: Spin up bastion VM**

**AWS:**
```bash
# Launch t3.micro Ubuntu 22.04 LTS
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.micro \
  --key-name my-keypair \
  --security-groups bastion-sg
```

**Azure:**
```bash
az vm create \
  --resource-group geesp-infra \
  --name geesp-bastion \
  --image UbuntuLTS \
  --size Standard_B1s \
  --ssh-key-values ./my-key.pub
```

**DigitalOcean:**
```bash
doctl compute droplet create geesp-bastion \
  --region sfo3 \
  --size s-1vcpu-512mb-10gb \
  --image ubuntu-22-04-x64 \
  --ssh-keys my-key-id
```

### **Step 2: Initial SSH (first login with key)**

```bash
# Connect as root initially
ssh -i ~/.ssh/id_ed25519 root@<bastion-ip>

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Set hostname
sudo hostnamectl set-hostname geesp-bastion
```

### **Step 3: Create admin user (non-root)**

```bash
# Create user
sudo useradd -m -G sudo geespadmin
sudo bash -c 'echo "geespadmin ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/geespadmin'

# Switch to new user
sudo su - geespadmin
```

### **Step 4: Setup SSH hardening**

```bash
# Backup original config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Edit SSH config
sudo nano /etc/ssh/sshd_config
```

**Critical SSH settings:**
```ini
# Disable root login
PermitRootLogin no

# Disable password auth (key only)
PasswordAuthentication no
PubkeyAuthentication yes

# Disable X11 forwarding
X11Forwarding no

# Restrict SSH to specific users
AllowUsers geespadmin

# Set SSH port (optional, change from 22)
Port 22

# Disable empty passwords
PermitEmptyPasswords no

# Limit login retries
MaxAuthTries 3

# Kill idle sessions
ClientAliveInterval 300
ClientAliveCountMax 2
```

**Apply changes:**
```bash
# Test syntax before applying
sudo sshd -t

# Restart SSH
sudo systemctl restart ssh

# Verify it's running
sudo systemctl status ssh
```

### **Step 5: Configure firewall (UFW)**

```bash
# Enable firewall
sudo ufw enable

# Allow SSH (port 22)
sudo ufw allow 22/tcp

# Access to internal services via SSH tunneling only
# (don't expose app ports directly)
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Verify rules
sudo ufw status
```

---

## **MFA Configuration (TOTP)**

### **Step 1: Install PAM module**

```bash
sudo apt-get install -y libpam-google-authenticator

# Test installation
which google-authenticator
```

### **Step 2: Configure PAM for MFA**

```bash
# Edit PAM SSH config
sudo nano /etc/pam.d/sshd
```

**Add these lines at the top (before @include common-auth):**
```ini
auth required pam_google_authenticator.so

# Optional: Require MFA only for certain users/groups
# auth [success=done new_authtok_reqd=done default=ignore] pam_unix.so nullok try_first_pass yescrypt
# auth requisite pam_deny.so
# auth required pam_permit.so
```

### **Step 3: Update SSH to use keyboard-interactive auth**

```bash
# Edit sshd_config
sudo nano /etc/ssh/sshd_config
```

**Add/update:**
```ini
# Enable keyboard-interactive for MFA
KbdInteractiveAuthentication yes

# Use MFA with public key
PubkeyAuthentication yes
```

**Restart SSH:**
```bash
sudo sshd -t
sudo systemctl restart ssh
```

### **Step 4: User enrolls in MFA**

**Each user runs this once:**
```bash
google-authenticator
```

**Interactive setup:**
```
Do you want authentication tokens to be time-based (y/n) y

┌──────────────────────────────────────┐
│ You can share this secret with other │
│                                      │
│     █████████████████████           │
│     █                           █   │  ← SCAN WITH PHONE
│     █     SECRET KEY HERE       █   │
│     █                           █   │
│     █████████████████████           │
│                                      │
│ Your new secret key is: XXXX XXXX X │
│ Enter code from authenticator: ____│ ← ENTER 6-DIGIT CODE
└──────────────────────────────────────┘
```

**Important responses:**
```
Do you want me to update your "/home/geespadmin/.google_authenticator" file? y

Do you want to disallow multiple uses of the same authentication
token? This restricts you to one login every 30s, but it increases
your chances to notice or even prevent man-in-the-middle attacks (y/n) y

By default, the Google Authenticator time window is 30 seconds.
If you experience problems with poor time synchronization, you can
increase the window from its default size of 3 permitted windows
(by 1 past and 1 future) to 17 permitted windows (by 8 past and 8
future). Do you want to do so? (y/n) y

If the computer that you are logging into does not have the current
time, then the one-time password (OTP) will not be correct. In order to
account for possible time-skew, we allow an extra token before and after
the correct time. This will permit for a time skew of up to 30 seconds
backward or forward. Do you want to enable this? (y/n) y
```

**Save backup codes:**
```
Your emergency scratch codes are:
12345678
87654321
...
```

⚠️ **SAVE THESE OFFLINE** - only works if phone is lost!

---

## **User Provisioning**

### **Automated User Onboarding Script**

**File:** `/root/add_mfa_user.sh`

```bash
#!/bin/bash
# Add new admin user with MFA support
# Usage: ./add_mfa_user.sh username email

set -euo pipefail

USERNAME=${1:-}
EMAIL=${2:-}

if [ -z "$USERNAME" ]; then
    echo "Usage: $0 <username> <email>"
    exit 1
fi

echo "=== Adding MFA-enabled admin user: $USERNAME ==="

# Create user
sudo useradd -m -G sudo "$USERNAME"
echo "✓ User created"

# Add to sudoers (no password)
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/"$USERNAME" > /dev/null
sudo chmod 0440 /etc/sudoers.d/"$USERNAME"
echo "✓ Sudo access granted"

# Create SSH directory
sudo mkdir -p /home/"$USERNAME"/.ssh
sudo chmod 700 /home/"$USERNAME"/.ssh
echo "✓ SSH directory created"

# Wait for user to provide public key
echo ""
echo "ACTION REQUIRED:"
echo "1. Provide your SSH public key (e.g., from 'cat ~/.ssh/id_ed25519.pub')"
read -p "Paste public key: " pubkey

echo "$pubkey" | sudo tee /home/"$USERNAME"/.ssh/authorized_keys > /dev/null
sudo chmod 600 /home/"$USERNAME"/.ssh/authorized_keys
sudo chown -R "$USERNAME:$USERNAME" /home/"$USERNAME"/.ssh
echo "✓ SSH key installed"

# Setup MFA
echo ""
echo "Next: SSH to bastion and run: google-authenticator"
echo ""
echo "ssh -i ~/.ssh/id_ed25519 $USERNAME@<bastion-ip>"
echo ""
echo "Then share setup details with user."
echo "✓ User provisioning complete"
```

**Usage:**
```bash
sudo /root/add_mfa_user.sh alice alice@geesp-angola.org
```

### **SSH Key Rotation (90-day policy)**

```bash
# Create rotation script: /root/rotate_ssh_keys.sh

#!/bin/bash
echo "=== SSH Key Rotation Reminder ==="
echo "Your SSH keys should be rotated every 90 days"
echo ""
echo "To rotate:"
echo "1. Generate new key: ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new"
echo "2. Copy old: cp ~/.ssh/id_ed25519 ~/.ssh/id_ed25519_backup_$(date +%Y%m%d)"
echo "3. Request admin to add new public key to authorized_keys"
echo "4. Test login: ssh -i ~/.ssh/id_ed25519_new user@bastion"
echo "5. Once verified, delete old key: rm ~/.ssh/id_ed25519"

# Schedule rotation reminder
sudo crontab -e
# Add: 0 0 1 */3 * /root/rotate_ssh_keys.sh
```

---

## **Access & Login Flow**

### **First Login (With SSH Agent Forwarding)**

```bash
# Step 1: SSH to bastion with key forwarding
ssh -A -i ~/.ssh/id_ed25519 geespadmin@<bastion-ip>

# Step 2: Authenticator app shows (press refresh if needed)
# Enter the 6-digit code from TOTP app when prompted

# Once authenticated:
geespadmin@geesp-bastion:~$
```

### **Accessing Internal Services from Bastion**

**Option A: SSH Tunnel to App Server**
```bash
# Create local SSH tunnel to internal app server
ssh -J geespadmin@<bastion-ip> ec2-user@<app-server-internal-ip>

# Or using ProxyJump in ~/.ssh/config:
# Host geesp-app
#     HostName 10.0.1.50
#     User ec2-user
#     ProxyJump geespadmin@<bastion-ip>

# Then: ssh geesp-app
```

**Option B: Port Forward for Database Access**
```bash
# Forward local 5432 → app server 5432 (PostgreSQL)
ssh -L 5432:app-server:5432 geespadmin@<bastion-ip>

# In another terminal:
psql -h localhost -U admin -d geesp_db
```

**Option C: SOCKS Proxy (for multiple services)**
```bash
# Create SOCKS proxy through bastion
ssh -D 1080 geespadmin@<bastion-ip>

# Configure apps to use localhost:1080 as SOCKS proxy
```

### **~/.ssh/config for Easy Access**

```ini
# Bastion host
Host geesp-bastion
    HostName <bastion-public-ip>
    User geespadmin
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
    StrictHostKeyChecking accept-new

# Internal app server (accessed via bastion)
Host geesp-app
    HostName <app-internal-ip>
    User ec2-user
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump geesp-bastion
    StrictHostKeyChecking accept-new

# Database via tunnel
Host geesp-db
    HostName <db-internal-ip>
    User postgres
    ProxyJump geesp-bastion
    LocalForward 5432 <db-internal-ip>:5432
```

**Now use simple commands:**
```bash
ssh geesp-bastion              # SSH to bastion
ssh geesp-app                  # SSH to app (via bastion)
ssh geesp-db                   # Port forward to DB
```

---

## **Audit Logging**

### **Enable Comprehensive Logging**

```bash
# All admin commands logged to /var/log/auth.log
grep "geespadmin" /var/log/auth.log

# SSH connections
cat /var/log/auth.log | grep "sshd\[" | tail -20

# Failed login attempts
grep "Failed password" /var/log/auth.log

# Google Authenticator failures
grep "google_authenticator" /var/log/auth.log
```

### **Setup Centralized Logging (Optional)**

```bash
# Install rsyslog (usually pre-installed)
sudo apt-get install rsyslog

# Create log rule: /etc/rsyslog.d/30-bastion.conf
:programname, isequal, "sshd" /var/log/bastion-sshd.log
:programname, isequal, "sudo" /var/log/bastion-sudo.log

# Rotate logs weekly
sudo nano /etc/logrotate.d/bastion
```

**Logrotate config:**
```ini
/var/log/bastion-sshd.log
/var/log/bastion-sudo.log
{
    weekly
    rotate 12
    compress
    delaycompress
    notifempty
    create 0640 root adm
}
```

### **Audit Trail Query (for compliance)**

```bash
#!/bin/bash
# Generate audit report for compliance

REPORT_DATE=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="audit_report_$REPORT_DATE.txt"

{
    echo "=== BASTION AUDIT REPORT ==="
    echo "Generated: $(date)"
    echo ""
    
    echo "=== ACTIVE USERS ==="
    who
    
    echo ""
    echo "=== RECENT SSH LOGINS (last 20) ==="
    grep sshd /var/log/auth.log | grep "Accepted publickey" | tail -20
    
    echo ""
    echo "=== FAILED LOGIN ATTEMPTS (last day) ==="
    grep "Failed password" /var/log/auth.log | grep "$(date +%b\ %d)"
    
    echo ""
    echo "=== SUDO ACTIVITY (last 20) ==="
    grep sudo /var/log/auth.log | tail -20
    
} > "$REPORT_FILE"

echo "Report saved to: $REPORT_FILE"
```

---

## **Troubleshooting**

### **Issue: "MFA code invalid"**

**Check 1: Time synchronization**
```bash
# On bastion
ntpstat
# or
timedatectl status

# Sync if needed
sudo ntpdate -u ntp.ubuntu.com
```

**Check 2: TOTP code expired**
- Codes valid for 30 seconds only
- Try new code immediately after refresh

**Check 3: Re-enroll if lost**
```bash
# Delete old configs (as user)
rm ~/.google_authenticator

# Re-run setup
google-authenticator

# Save new backup codes!
```

### **Issue: "Permission denied (publickey,keyboard-interactive)"**

**Check 1: SSH key permissions**
```bash
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

**Check 2: Bastion has public key**
```bash
# On bastion (as your user)
cat ~/.ssh/authorized_keys | grep "$(cat ~/.ssh/id_ed25519.pub)"
```

**Check 3: Enable SSH debug**
```bash
ssh -vvv -i ~/.ssh/id_ed25519 geespadmin@bastion-ip
```

### **Issue: "MFA module failed"**

```bash
# Check PAM config
sudo cat /etc/pam.d/sshd | grep google

# Check TOTP file exists and is readable
ls -la ~/.google_authenticator

# Re-test PAM
sudo pamtester -v sshd geespadmin authenticate
```

### **Issue: "SSH-Agent not forwarding"**

```bash
# On local machine
# 1. Start SSH agent
eval "$(ssh-agent)"

# 2. Add key
ssh-add ~/.ssh/id_ed25519

# 3. Connect with -A flag
ssh -A geespadmin@bastion-ip

# 4. On bastion, test forwarding
echo $SSH_AUTH_SOCK        # Should show socket path
ssh-add -l                 # Should list your key
```

### **Issue: "Too many authentication failures"**

```bash
# SSH is rejecting after 3 failed attempts
# Wait 30-60 seconds before retrying

# Or increase limit on bastion:
# Edit /etc/ssh/sshd_config:
# MaxAuthTries 5
# sudo systemctl restart ssh
```

---

## **Maintenance Checklist**

- [ ] Weekly: Review auth.log for suspicious activity
- [ ] Monthly: Verify all user accounts still active (disable unused)
- [ ] Quarterly: Rotate admin SSH keys (90-day policy)
- [ ] Quarterly: Update system packages (`sudo apt-get update && upgrade`)
- [ ] Semi-annually: Test disaster recovery (can you SSH if key is lost?)
- [ ] Annually: Security audit external (penetration test bastion)

---

## **Compliance & Security Standards**

**This setup aligns with:**
- ✅ NIST 800-53 (AC-2, AC-3, AC-11: Account & Access Control)
- ✅ CIS Controls (v8 Controls 5 & 6: PAM & MFA)
- ✅ ISO 27001 (A.9.2: User Access Management)
- ✅ SOC 2 (Logical Access Controls)

---

**Questions?** Contact: infra-support@geesp-angola.org
