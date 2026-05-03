#!/usr/bin/env python3
"""
Automated Cron-based Data Synchronization & ETL Trigger
Runs scheduled data ingestion and synchronization from remote sources.

Usage as cron job:
    # Daily at 02:00 AM
    0 2 * * * /usr/bin/python3 /path/to/scripts/cron_data_sync.py >> /var/log/geesp_cron.log 2>&1
    
    # Every 6 hours
    0 */6 * * * /usr/bin/python3 /path/to/scripts/cron_data_sync.py >> /var/log/geesp_cron.log 2>&1
    
    # Weekly on Monday at 03:00 AM
    0 3 * * 1 /usr/bin/python3 /path/to/scripts/cron_data_sync.py --full >> /var/log/geesp_cron.log 2>&1

Schedule recommendation:
    - Quick sync (free datasets): Daily 02:00 AM (30 min)
    - Full sync (Earth Engine + free datasets): Weekly Monday 03:00 AM (1-2 hours)
    - Database backup: Daily 01:00 AM
"""

import os
import sys
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Setup logging
log_dir = Path("logs") if Path("logs").exists() else Path("/var/log")
log_file = log_dir / "geesp_cron.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("cron_data_sync")

# Find project root
PROJECT_ROOT = Path(__file__).parent.parent
if not (PROJECT_ROOT / "Coding parts" / "geesp-angola").exists():
    PROJECT_ROOT = Path.cwd()

SCRIPTS_DIR = PROJECT_ROOT / "scripts"
GEESP_DIR = PROJECT_ROOT / "Coding parts" / "geesp-angola"


class DataSyncOrchestrator:
    """Orchestrates automated data synchronization tasks"""
    
    def __init__(self, full_sync: bool = False, skip_earth_engine: bool = False):
        self.full_sync = full_sync
        self.skip_earth_engine = skip_earth_engine
        self.start_time = datetime.now()
        self.results = {}
    
    def run_etl_pipeline(self) -> bool:
        """Run free datasets ETL pipeline"""
        logger.info("=" * 70)
        logger.info("STARTING ETL PIPELINE (Free Datasets)")
        logger.info("=" * 70)
        
        try:
            cmd = [
                sys.executable,
                str(SCRIPTS_DIR / "data_ingestion_etl.py"),
                "--free-datasets",
                "--output", str(GEESP_DIR / "data" / "processed")
            ]
            
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            
            logger.info("ETL Pipeline Output:")
            if result.stdout:
                logger.info(result.stdout)
            if result.stderr:
                logger.warning(result.stderr)
            
            if result.returncode == 0:
                logger.info("✓ ETL Pipeline completed successfully")
                self.results['etl'] = 'success'
                return True
            else:
                logger.error(f"✗ ETL Pipeline failed with code {result.returncode}")
                self.results['etl'] = f'failed: {result.returncode}'
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("✗ ETL Pipeline exceeded 10 minute timeout")
            self.results['etl'] = 'timeout'
            return False
        except Exception as e:
            logger.error(f"✗ Error running ETL: {e}")
            self.results['etl'] = f'error: {str(e)}'
            return False
    
    def run_earth_engine_fetch(self) -> bool:
        """Run Earth Engine data fetching (requires authentication)"""
        if self.skip_earth_engine:
            logger.info("Skipping Earth Engine fetch (as requested)")
            return True
        
        logger.info("=" * 70)
        logger.info("STARTING EARTH ENGINE DATA FETCH")
        logger.info("=" * 70)
        
        try:
            cmd = [
                sys.executable,
                str(SCRIPTS_DIR / "data_ingestion_etl.py"),
                "--earth-engine",
                "--output", str(GEESP_DIR / "data" / "processed")
            ]
            
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=1200  # 20 minutes max for GEE
            )
            
            logger.info("Earth Engine Output:")
            if result.stdout:
                logger.info(result.stdout)
            if result.stderr:
                logger.warning(result.stderr)
            
            if result.returncode == 0:
                logger.info("✓ Earth Engine fetch completed successfully")
                self.results['earth_engine'] = 'success'
                return True
            else:
                logger.error(f"✗ Earth Engine fetch failed with code {result.returncode}")
                self.results['earth_engine'] = f'failed: {result.returncode}'
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("✗ Earth Engine fetch exceeded 20 minute timeout")
            self.results['earth_engine'] = 'timeout'
            return False
        except Exception as e:
            logger.error(f"✗ Error running Earth Engine: {e}")
            self.results['earth_engine'] = f'error: {str(e)}'
            return False
    
    def backup_database(self) -> bool:
        """Create backup of PostgreSQL database"""
        logger.info("=" * 70)
        logger.info("BACKING UP DATABASE")
        logger.info("=" * 70)
        
        try:
            script = SCRIPTS_DIR / "db_backup.sh"
            if not script.exists():
                logger.warning(f"Backup script not found: {script}")
                self.results['backup'] = 'skipped: script not found'
                return True
            
            cmd = ["bash", str(script)]
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.stdout:
                logger.info(result.stdout)
            if result.stderr and result.returncode != 0:
                logger.warning(result.stderr)
            
            if result.returncode == 0:
                logger.info("✓ Database backup completed successfully")
                self.results['backup'] = 'success'
                return True
            else:
                logger.error(f"✗ Database backup failed with code {result.returncode}")
                self.results['backup'] = f'failed: {result.returncode}'
                return True  # Non-blocking failure
                
        except subprocess.TimeoutExpired:
            logger.error("✗ Database backup exceeded 10 minute timeout")
            self.results['backup'] = 'timeout'
            return True
        except Exception as e:
            logger.error(f"✗ Error running backup: {e}")
            self.results['backup'] = f'error: {str(e)}'
            return True
    
    def run_validation_checks(self) -> bool:
        """Run data quality validation"""
        logger.info("=" * 70)
        logger.info("RUNNING DATA VALIDATION CHECKS")
        logger.info("=" * 70)
        
        try:
            output_dir = GEESP_DIR / "data" / "processed"
            if not output_dir.exists():
                logger.warning(f"Output directory doesn't exist: {output_dir}")
                self.results['validation'] = 'skipped: no data'
                return True
            
            # Check for required raster files
            required_files = [
                "mapa_irradiacao.npy",
                "mapa_populacao.npy",
                "mapa_distanciarede.npy",
                "mapa_declividade.npy",
                "mapa_ndvi.npy"
            ]
            
            missing = []
            for fname in required_files:
                fpath = output_dir / fname
                if not fpath.exists():
                    missing.append(fname)
                    logger.warning(f"Missing: {fname}")
            
            if missing:
                logger.error(f"✗ Missing {len(missing)} required raster files")
                self.results['validation'] = f'failed: {len(missing)} files missing'
                return False
            else:
                logger.info("✓ All required raster files present")
                self.results['validation'] = 'success'
                return True
                
        except Exception as e:
            logger.error(f"✗ Error during validation: {e}")
            self.results['validation'] = f'error: {str(e)}'
            return False
    
    def send_completion_summary(self):
        """Log final summary"""
        elapsed = datetime.now() - self.start_time
        logger.info("=" * 70)
        logger.info(f"CRON JOB COMPLETED - Duration: {elapsed}")
        logger.info("=" * 70)
        logger.info("Task Results:")
        for task, result in self.results.items():
            status_icon = "✓" if isinstance(result, str) and result == 'success' else "✗"
            logger.info(f"  {status_icon} {task}: {result}")
        logger.info("=" * 70)
    
    def execute(self) -> int:
        """Execute full sync orchestration"""
        logger.info(f"Starting cron data sync (full_sync={self.full_sync})")
        
        success_count = 0
        
        # Always run validation first
        if self.run_validation_checks():
            success_count += 1
        
        # Run ETL pipeline
        if self.run_etl_pipeline():
            success_count += 1
        
        # Run Earth Engine if full sync
        if self.full_sync or not self.skip_earth_engine:
            if self.run_earth_engine_fetch():
                success_count += 1
        
        # Run backup
        if self.backup_database():
            success_count += 1
        
        self.send_completion_summary()
        
        # Return non-zero exit code if any critical task failed
        return 0 if success_count >= 2 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Automated data synchronization and ETL trigger for GEESP-Angola",
        epilog="Example: python cron_data_sync.py --full --skip-earth-engine"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full sync including Earth Engine (default: quick sync only)"
    )
    parser.add_argument(
        "--skip-earth-engine",
        action="store_true",
        help="Skip Earth Engine data fetch (useful if GEE auth is not configured)"
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="Skip database backup step"
    )
    
    args = parser.parse_args()
    
    orchestrator = DataSyncOrchestrator(
        full_sync=args.full,
        skip_earth_engine=args.skip_earth_engine
    )
    
    exit_code = orchestrator.execute()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
