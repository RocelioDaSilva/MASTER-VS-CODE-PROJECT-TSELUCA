#!/usr/bin/env python3
"""
Email Alert Integration for GEESP-Angola Monitoring
Sends email notifications when critical thresholds are exceeded.

Configuration:
    See monitoring/alertmanager.yml for alert rules
    Email config stored in environment variables or .env file

Environment Variables Required:
    ALERT_EMAIL_FROM (sender, e.g., alerts@geesp-angola.org)
    ALERT_EMAIL_SMTP_HOST (e.g., smtp.gmail.com, smtp.sendgrid.net)
    ALERT_EMAIL_SMTP_PORT (typically 587 for TLS)
    ALERT_EMAIL_USERNAME (SMTP login)
    ALERT_EMAIL_PASSWORD (SMTP password or API key)
    ALERT_EMAIL_TO_LIST (comma-separated recipients for critical alerts)
    ALERT_EMAIL_CC_PM (PM email for critical issues)

Usage:
    python scripts/monitoring_email_alerts.py --config monitoring/alertmanager.yml

Or as a scheduled task (cron):
    0 * * * * python /path/to/scripts/monitoring_email_alerts.py >> /var/log/alerts.log 2>&1
"""

import os
import sys
import json
import smtplib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse

# Configure logging
try:
    from logging_config import get_script_logger
except ImportError:
    from .logging_config import get_script_logger

logger = get_script_logger("monitoring_alerts", log_file="monitoring_alerts.log")


class EmailAlertSender:
    """Send email notifications for monitoring alerts"""
    
    def __init__(self):
        self.smtp_host = os.getenv('ALERT_EMAIL_SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('ALERT_EMAIL_SMTP_PORT', '587'))
        self.sender_email = os.getenv('ALERT_EMAIL_FROM', 'alerts@geesp-angola.org')
        self.sender_password = os.getenv('ALERT_EMAIL_PASSWORD', '')
        self.recipient_list = os.getenv('ALERT_EMAIL_TO_LIST', '').split(',')
        self.cc_pm = os.getenv('ALERT_EMAIL_CC_PM', '')
        
        if not self.sender_password:
            logger.warning("ALERT_EMAIL_PASSWORD not set. Email alerts disabled.")
            self.enabled = False
        else:
            self.enabled = True
    
    def send_alert(
        self,
        alert_name: str,
        severity: str,  # "critical", "warning", "info"
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send alert email
        
        Args:
            alert_name: Name of the alert (e.g., "HighDiskUsage")
            severity: Alert severity level
            message: Human-readable message
            details: Optional dict with additional context
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning(f"Email alerts disabled. Skipping: {alert_name}")
            return False
        
        try:
            # Compose email
            subject = f"[{severity.upper()}] GEESP-Angola Alert: {alert_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # HTML email body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #1976d2; color: white; padding: 10px; }}
                    .severity-critical {{ background-color: #d32f2f; }}
                    .severity-warning {{ background-color: #f57c00; }}
                    .severity-info {{ background-color: #0288d1; }}
                    .content {{ padding: 15px; }}
                    .details {{ background-color: #f5f5f5; padding: 10px; margin-top: 15px; border-left: 4px solid #1976d2; }}
                    .footer {{ font-size: 12px; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="header severity-{severity.lower()}">
                    <h2>{alert_name}</h2>
                    <p>Severity: <strong>{severity.upper()}</strong> | Time: {datetime.utcnow().isoformat()}</p>
                </div>
                
                <div class="content">
                    <h3>Alert Details</h3>
                    <p>{message}</p>
                    
                    {"<div class='details'>" + self._format_details(details) + "</div>" if details else ""}
                    
                    <h3>Recommended Actions</h3>
                    <ul>
                        <li>Review the alert in the monitoring dashboard: https://monitoring.geesp-angola.org/</li>
                        <li>Check recent log files in /var/log/geesp/</li>
                        <li>Contact IT team if issue persists</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This is an automated alert from GEESP-Angola Monitoring System.</p>
                    <p>To modify alert rules, contact: monitoring@geesp-angola.org</p>
                </div>
            </body>
            </html>
            """
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_list)
            if self.cc_pm:
                msg['CC'] = self.cc_pm
            
            # Attach plain text and HTML
            text_part = MIMEText(message, 'plain')
            html_part = MIMEText(html_body, 'html')
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send via SMTP
            logger.info(f"Connecting to SMTP: {self.smtp_host}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                
                all_recipients = self.recipient_list + ([self.cc_pm] if self.cc_pm else [])
                server.sendmail(self.sender_email, all_recipients, msg.as_string())
            
            logger.info(f"✓ Alert email sent: {alert_name} ({severity})")
            return True
            
        except smtplib.SMTPException as e:
            logger.error(f"✗ SMTP error sending alert '{alert_name}': {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Error sending alert: {e}")
            return False
    
    @staticmethod
    def _format_details(details: Dict[str, Any]) -> str:
        """Format details dict as HTML"""
        html = "<strong>Details:</strong><br>"
        for key, value in details.items():
            html += f"<strong>{key}:</strong> {value}<br>"
        return html


class MonitoringAlertChecker:
    """Check monitoring metrics and trigger alerts"""
    
    def __init__(self, email_sender: EmailAlertSender):
        self.sender = email_sender
        self.checks_passed = 0
        self.checks_failed = 0
    
    def check_disk_usage(self, threshold_percent: float = 85.0) -> bool:
        """Check disk usage on critical partitions"""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            usage_percent = (used / total) * 100
            
            if usage_percent > threshold_percent:
                logger.warning(f"High disk usage: {usage_percent:.1f}%")
                self.sender.send_alert(
                    alert_name="HighDiskUsage",
                    severity="critical",
                    message=f"Root partition disk usage at {usage_percent:.1f}%, threshold: {threshold_percent}%",
                    details={
                        "Usage": f"{usage_percent:.1f}%",
                        "Used": f"{used / (1024**3):.1f} GB",
                        "Free": f"{free / (1024**3):.1f} GB",
                        "Total": f"{total / (1024**3):.1f} GB"
                    }
                )
                self.checks_failed += 1
                return False
            else:
                logger.info(f"✓ Disk usage OK: {usage_percent:.1f}%")
                self.checks_passed += 1
                return True
                
        except Exception as e:
            logger.error(f"Error checking disk usage: {e}")
            return True  # Non-blocking
    
    def check_database_connectivity(self, host: str = "localhost", port: int = 5432) -> bool:
        """Check PostgreSQL database connectivity"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=os.getenv('DB_USER', 'geesp'),
                password=os.getenv('DB_PASSWORD', ''),
                database='geesp_data',
                connect_timeout=5
            )
            conn.close()
            logger.info(f"✓ Database connectivity OK ({host}:{port})")
            self.checks_passed += 1
            return True
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            self.sender.send_alert(
                alert_name="DatabaseUnavailable",
                severity="critical",
                message=f"Cannot connect to PostgreSQL at {host}:{port}",
                details={
                    "Host": host,
                    "Port": port,
                    "Error": str(e)
                }
            )
            self.checks_failed += 1
            return False
    
    def check_api_health(self, url: str = "http://localhost:8000/health") -> bool:
        """Check REST API health endpoint"""
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✓ API health OK ({url})")
                self.checks_passed += 1
                return True
            else:
                raise Exception(f"Status {response.status_code}")
                
        except Exception as e:
            logger.error(f"API health check error: {e}")
            self.sender.send_alert(
                alert_name="APIUnhealthy",
                severity="warning",
                message=f"API health check failed: {url}",
                details={
                    "URL": url,
                    "Error": str(e)
                }
            )
            self.checks_failed += 1
            return False
    
    def check_data_freshness(self, max_age_hours: int = 24) -> bool:
        """Check if latest data is fresh"""
        try:
            data_dir = Path("data/processed")
            if not data_dir.exists():
                logger.warning("Data directory not found")
                return True  # Non-blocking
            
            metadata_file = data_dir / "datasets_metadata.json"
            if not metadata_file.exists():
                logger.warning("No metadata file found")
                return True
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            last_update_str = metadata.get('timestamp')
            if not last_update_str:
                logger.warning("No timestamp in metadata")
                return True
            
            last_update = datetime.fromisoformat(last_update_str)
            age_hours = (datetime.now() - last_update).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                logger.warning(f"Data is stale: {age_hours:.1f} hours old")
                self.sender.send_alert(
                    alert_name="DataStale",
                    severity="warning",
                    message=f"Latest data is {age_hours:.1f} hours old (threshold: {max_age_hours} hours)",
                    details={
                        "Last Update": last_update_str,
                        "Age (hours)": f"{age_hours:.1f}",
                        "Threshold": f"{max_age_hours} hours"
                    }
                )
                self.checks_failed += 1
                return False
            else:
                logger.info(f"✓ Data freshness OK (age: {age_hours:.1f} hours)")
                self.checks_passed += 1
                return True
                
        except Exception as e:
            logger.error(f"Error checking data freshness: {e}")
            return True
    
    def run_all_checks(self) -> bool:
        """Run all monitoring checks"""
        logger.info("=" * 70)
        logger.info("Running Health Checks")
        logger.info("=" * 70)
        
        self.check_disk_usage(threshold_percent=85.0)
        self.check_database_connectivity()
        self.check_api_health()
        self.check_data_freshness(max_age_hours=24)
        
        logger.info("=" * 70)
        logger.info(f"Health Check Summary: {self.checks_passed} passed, {self.checks_failed} failed")
        logger.info("=" * 70)
        
        return self.checks_failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Run monitoring checks and send email alerts if issues found"
    )
    parser.add_argument(
        "--config",
        default="monitoring/alertmanager.yml",
        help="Path to AlertManager configuration file"
    )
    parser.add_argument(
        "--disk-threshold",
        type=float,
        default=85.0,
        help="Disk usage threshold (%) for alert"
    )
    parser.add_argument(
        "--data-age-threshold",
        type=int,
        default=24,
        help="Data freshness threshold (hours)"
    )
    
    args = parser.parse_args()
    
    # Initialize email sender
    sender = EmailAlertSender()
    
    # Run checks
    checker = MonitoringAlertChecker(sender)
    success = checker.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
