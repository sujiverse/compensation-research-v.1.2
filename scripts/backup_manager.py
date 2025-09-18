#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 Compensation Research System - Backup & Recovery Manager
Comprehensive backup and disaster recovery system
"""

import os
import sys
import json
import gzip
import shutil
import tarfile
import zipfile
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import subprocess
import hashlib
import time

class BackupManager:
    def __init__(self, config_file: str = "backup_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.setup_logging()

        # Backup destinations
        self.local_backup_dir = Path(self.config.get('local_backup_dir', 'backups'))
        self.cloud_backup_enabled = self.config.get('cloud_backup_enabled', False)

        # Ensure backup directory exists
        self.local_backup_dir.mkdir(parents=True, exist_ok=True)

    def setup_logging(self):
        """Setup backup logging"""
        os.makedirs('logs', exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - BACKUP - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/backup.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Load backup configuration"""
        default_config = {
            "local_backup_dir": "backups",
            "retention_days": 30,
            "compression_enabled": True,
            "incremental_backup": True,
            "cloud_backup_enabled": False,
            "cloud_provider": "aws_s3",
            "backup_schedule": {
                "full_backup_interval": "weekly",
                "incremental_interval": "daily"
            },
            "backup_targets": [
                "Compensation-Research-Vault",
                "logs",
                "cache",
                ".secrets.enc",
                ".encryption.key",
                "*.py",
                "*.yml",
                "*.yaml",
                "*.json",
                "*.md"
            ],
            "exclude_patterns": [
                "__pycache__",
                "*.pyc",
                ".git",
                "node_modules",
                "temp*",
                "*.tmp"
            ]
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")

        return default_config

    def create_full_backup(self, backup_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a complete system backup"""
        if not backup_name:
            backup_name = f"full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.logger.info(f"Starting full backup: {backup_name}")

        backup_info = {
            "backup_name": backup_name,
            "backup_type": "full",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "in_progress",
            "files_backed_up": 0,
            "total_size_bytes": 0,
            "backup_path": None,
            "checksum": None,
            "duration_seconds": 0
        }

        start_time = time.time()

        try:
            # Create backup directory
            backup_dir = self.local_backup_dir / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup files
            self._backup_files(backup_dir, backup_info)

            # Backup database (if configured)
            self._backup_database(backup_dir, backup_info)

            # Create compressed archive
            archive_path = self._create_archive(backup_dir, backup_name, backup_info)

            # Generate checksum
            backup_info["checksum"] = self._calculate_checksum(archive_path)

            # Upload to cloud (if enabled)
            if self.cloud_backup_enabled:
                self._upload_to_cloud(archive_path, backup_info)

            # Clean up temporary directory
            shutil.rmtree(backup_dir)

            backup_info["backup_path"] = str(archive_path)
            backup_info["duration_seconds"] = time.time() - start_time
            backup_info["status"] = "completed"

            self.logger.info(f"Full backup completed: {backup_name}")

            # Save backup metadata
            self._save_backup_metadata(backup_info)

            return backup_info

        except Exception as e:
            backup_info["status"] = "failed"
            backup_info["error"] = str(e)
            backup_info["duration_seconds"] = time.time() - start_time

            self.logger.error(f"Full backup failed: {e}")
            return backup_info

    def create_incremental_backup(self, reference_backup: Optional[str] = None) -> Dict[str, Any]:
        """Create an incremental backup"""
        backup_name = f"incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.logger.info(f"Starting incremental backup: {backup_name}")

        backup_info = {
            "backup_name": backup_name,
            "backup_type": "incremental",
            "reference_backup": reference_backup,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "in_progress",
            "files_backed_up": 0,
            "total_size_bytes": 0,
            "backup_path": None,
            "checksum": None,
            "duration_seconds": 0
        }

        start_time = time.time()

        try:
            # Find reference point for incremental backup
            if not reference_backup:
                reference_backup = self._find_latest_backup()

            reference_time = self._get_backup_timestamp(reference_backup)

            # Create backup directory
            backup_dir = self.local_backup_dir / backup_name
            backup_dir.mkdir(parents=True, exist_ok=True)

            # Backup only changed files
            self._backup_changed_files(backup_dir, reference_time, backup_info)

            # Create compressed archive
            archive_path = self._create_archive(backup_dir, backup_name, backup_info)

            # Generate checksum
            backup_info["checksum"] = self._calculate_checksum(archive_path)

            # Upload to cloud (if enabled)
            if self.cloud_backup_enabled:
                self._upload_to_cloud(archive_path, backup_info)

            # Clean up temporary directory
            shutil.rmtree(backup_dir)

            backup_info["backup_path"] = str(archive_path)
            backup_info["duration_seconds"] = time.time() - start_time
            backup_info["status"] = "completed"

            self.logger.info(f"Incremental backup completed: {backup_name}")

            # Save backup metadata
            self._save_backup_metadata(backup_info)

            return backup_info

        except Exception as e:
            backup_info["status"] = "failed"
            backup_info["error"] = str(e)
            backup_info["duration_seconds"] = time.time() - start_time

            self.logger.error(f"Incremental backup failed: {e}")
            return backup_info

    def _backup_files(self, backup_dir: Path, backup_info: Dict[str, Any]):
        """Backup files according to configuration"""
        files_backed_up = 0
        total_size = 0

        for target in self.config["backup_targets"]:
            for file_path in self._find_files(target):
                if self._should_exclude(file_path):
                    continue

                try:
                    # Create relative path structure
                    rel_path = os.path.relpath(file_path)
                    backup_file_path = backup_dir / rel_path
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file
                    shutil.copy2(file_path, backup_file_path)

                    files_backed_up += 1
                    total_size += os.path.getsize(file_path)

                except Exception as e:
                    self.logger.warning(f"Failed to backup file {file_path}: {e}")

        backup_info["files_backed_up"] = files_backed_up
        backup_info["total_size_bytes"] = total_size

    def _backup_changed_files(self, backup_dir: Path, reference_time: datetime, backup_info: Dict[str, Any]):
        """Backup only files changed since reference time"""
        files_backed_up = 0
        total_size = 0

        for target in self.config["backup_targets"]:
            for file_path in self._find_files(target):
                if self._should_exclude(file_path):
                    continue

                try:
                    # Check if file was modified since reference time
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

                    if file_mtime > reference_time:
                        # Create relative path structure
                        rel_path = os.path.relpath(file_path)
                        backup_file_path = backup_dir / rel_path
                        backup_file_path.parent.mkdir(parents=True, exist_ok=True)

                        # Copy file
                        shutil.copy2(file_path, backup_file_path)

                        files_backed_up += 1
                        total_size += os.path.getsize(file_path)

                except Exception as e:
                    self.logger.warning(f"Failed to backup changed file {file_path}: {e}")

        backup_info["files_backed_up"] = files_backed_up
        backup_info["total_size_bytes"] = total_size

    def _backup_database(self, backup_dir: Path, backup_info: Dict[str, Any]):
        """Backup database if configured"""
        db_url = os.environ.get('POSTGRES_URL')
        if not db_url:
            return

        try:
            # Extract database connection info
            import urllib.parse
            parsed = urllib.parse.urlparse(db_url)

            db_backup_file = backup_dir / "database_dump.sql"

            # Use pg_dump to create database backup
            cmd = [
                'pg_dump',
                '--host', parsed.hostname,
                '--port', str(parsed.port or 5432),
                '--username', parsed.username,
                '--dbname', parsed.path[1:],  # Remove leading slash
                '--file', str(db_backup_file),
                '--verbose'
            ]

            env = os.environ.copy()
            env['PGPASSWORD'] = parsed.password

            result = subprocess.run(cmd, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info("Database backup completed")
                backup_info["database_backed_up"] = True
            else:
                self.logger.error(f"Database backup failed: {result.stderr}")
                backup_info["database_backed_up"] = False

        except Exception as e:
            self.logger.error(f"Database backup error: {e}")
            backup_info["database_backed_up"] = False

    def _create_archive(self, backup_dir: Path, backup_name: str, backup_info: Dict[str, Any]) -> Path:
        """Create compressed archive of backup"""
        if self.config.get("compression_enabled", True):
            archive_path = self.local_backup_dir / f"{backup_name}.tar.gz"

            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(backup_dir, arcname=backup_name)
        else:
            archive_path = self.local_backup_dir / f"{backup_name}.tar"

            with tarfile.open(archive_path, 'w') as tar:
                tar.add(backup_dir, arcname=backup_name)

        backup_info["compressed"] = self.config.get("compression_enabled", True)
        backup_info["archive_size_bytes"] = os.path.getsize(archive_path)

        return archive_path

    def _find_files(self, pattern: str) -> List[str]:
        """Find files matching pattern"""
        import glob

        if os.path.isfile(pattern):
            return [pattern]
        elif os.path.isdir(pattern):
            files = []
            for root, dirs, filenames in os.walk(pattern):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            return files
        else:
            return glob.glob(pattern, recursive=True)

    def _should_exclude(self, file_path: str) -> bool:
        """Check if file should be excluded from backup"""
        import fnmatch

        for pattern in self.config["exclude_patterns"]:
            if fnmatch.fnmatch(file_path, pattern) or pattern in file_path:
                return True
        return False

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file"""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    def _upload_to_cloud(self, archive_path: Path, backup_info: Dict[str, Any]):
        """Upload backup to cloud storage"""
        cloud_provider = self.config.get("cloud_provider", "aws_s3")

        try:
            if cloud_provider == "aws_s3":
                self._upload_to_s3(archive_path, backup_info)
            elif cloud_provider == "azure_blob":
                self._upload_to_azure(archive_path, backup_info)
            elif cloud_provider == "gcp_storage":
                self._upload_to_gcp(archive_path, backup_info)
            else:
                self.logger.warning(f"Unsupported cloud provider: {cloud_provider}")

        except Exception as e:
            self.logger.error(f"Cloud upload failed: {e}")
            backup_info["cloud_upload_failed"] = str(e)

    def _upload_to_s3(self, archive_path: Path, backup_info: Dict[str, Any]):
        """Upload to AWS S3"""
        try:
            import boto3

            s3_client = boto3.client('s3')
            bucket = os.environ.get('BACKUP_BUCKET')

            if not bucket:
                raise ValueError("BACKUP_BUCKET environment variable not set")

            key = f"compensation-research/{archive_path.name}"

            s3_client.upload_file(str(archive_path), bucket, key)

            backup_info["cloud_location"] = f"s3://{bucket}/{key}"
            backup_info["cloud_uploaded"] = True

            self.logger.info(f"Backup uploaded to S3: s3://{bucket}/{key}")

        except ImportError:
            self.logger.error("boto3 not installed. Cannot upload to S3.")
        except Exception as e:
            self.logger.error(f"S3 upload failed: {e}")
            raise

    def restore_backup(self, backup_name: str, restore_path: Optional[str] = None) -> Dict[str, Any]:
        """Restore from backup"""
        self.logger.info(f"Starting restore from backup: {backup_name}")

        restore_info = {
            "backup_name": backup_name,
            "restore_timestamp": datetime.utcnow().isoformat(),
            "status": "in_progress",
            "files_restored": 0,
            "duration_seconds": 0
        }

        start_time = time.time()

        try:
            # Find backup file
            backup_file = self._find_backup_file(backup_name)
            if not backup_file:
                raise ValueError(f"Backup file not found: {backup_name}")

            # Verify checksum
            if not self._verify_backup_integrity(backup_file):
                raise ValueError("Backup integrity check failed")

            # Extract backup
            if not restore_path:
                restore_path = "."

            self._extract_backup(backup_file, restore_path, restore_info)

            restore_info["status"] = "completed"
            restore_info["duration_seconds"] = time.time() - start_time

            self.logger.info(f"Restore completed: {backup_name}")

            return restore_info

        except Exception as e:
            restore_info["status"] = "failed"
            restore_info["error"] = str(e)
            restore_info["duration_seconds"] = time.time() - start_time

            self.logger.error(f"Restore failed: {e}")
            return restore_info

    def _extract_backup(self, backup_file: Path, restore_path: str, restore_info: Dict[str, Any]):
        """Extract backup archive"""
        files_restored = 0

        if backup_file.suffix == '.gz':
            with tarfile.open(backup_file, 'r:gz') as tar:
                tar.extractall(restore_path)
                files_restored = len(tar.getnames())
        else:
            with tarfile.open(backup_file, 'r') as tar:
                tar.extractall(restore_path)
                files_restored = len(tar.getnames())

        restore_info["files_restored"] = files_restored

    def cleanup_old_backups(self) -> Dict[str, Any]:
        """Clean up old backups based on retention policy"""
        retention_days = self.config.get("retention_days", 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        cleanup_info = {
            "cutoff_date": cutoff_date.isoformat(),
            "files_deleted": 0,
            "space_freed_bytes": 0,
            "deleted_backups": []
        }

        for backup_file in self.local_backup_dir.glob("*.tar*"):
            try:
                file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)

                if file_mtime < cutoff_date:
                    file_size = backup_file.stat().st_size
                    backup_file.unlink()

                    cleanup_info["files_deleted"] += 1
                    cleanup_info["space_freed_bytes"] += file_size
                    cleanup_info["deleted_backups"].append(backup_file.name)

                    self.logger.info(f"Deleted old backup: {backup_file.name}")

            except Exception as e:
                self.logger.error(f"Failed to delete backup {backup_file}: {e}")

        return cleanup_info

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        backups = []

        # List local backups
        for backup_file in sorted(self.local_backup_dir.glob("*.tar*")):
            try:
                stat = backup_file.stat()
                backup_info = {
                    "name": backup_file.stem,
                    "file_path": str(backup_file),
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": "incremental" if "incremental" in backup_file.name else "full"
                }

                # Try to load metadata
                metadata = self._load_backup_metadata(backup_file.stem)
                if metadata:
                    backup_info.update(metadata)

                backups.append(backup_info)

            except Exception as e:
                self.logger.error(f"Error processing backup {backup_file}: {e}")

        return backups

    def _save_backup_metadata(self, backup_info: Dict[str, Any]):
        """Save backup metadata"""
        metadata_file = self.local_backup_dir / f"{backup_info['backup_name']}.metadata.json"

        with open(metadata_file, 'w') as f:
            json.dump(backup_info, f, indent=2, default=str)

    def _load_backup_metadata(self, backup_name: str) -> Optional[Dict[str, Any]]:
        """Load backup metadata"""
        metadata_file = self.local_backup_dir / f"{backup_name}.metadata.json"

        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load metadata for {backup_name}: {e}")

        return None

    def _find_backup_file(self, backup_name: str) -> Optional[Path]:
        """Find backup file by name"""
        for backup_file in self.local_backup_dir.glob(f"{backup_name}.*"):
            if backup_file.suffix in ['.tar', '.gz'] and backup_file.is_file():
                return backup_file
        return None

    def _verify_backup_integrity(self, backup_file: Path) -> bool:
        """Verify backup file integrity"""
        metadata = self._load_backup_metadata(backup_file.stem)

        if not metadata or 'checksum' not in metadata:
            self.logger.warning(f"No checksum available for {backup_file.name}")
            return True  # Assume OK if no checksum

        calculated_checksum = self._calculate_checksum(backup_file)
        stored_checksum = metadata['checksum']

        if calculated_checksum == stored_checksum:
            self.logger.info(f"Backup integrity verified: {backup_file.name}")
            return True
        else:
            self.logger.error(f"Backup integrity check failed: {backup_file.name}")
            return False

    def _find_latest_backup(self) -> Optional[str]:
        """Find the latest backup for incremental reference"""
        backups = self.list_backups()

        if not backups:
            return None

        # Sort by creation time and return latest
        latest = max(backups, key=lambda x: x['created'])
        return latest['name']

    def _get_backup_timestamp(self, backup_name: Optional[str]) -> datetime:
        """Get backup timestamp for incremental reference"""
        if not backup_name:
            return datetime.min

        metadata = self._load_backup_metadata(backup_name)

        if metadata and 'timestamp' in metadata:
            return datetime.fromisoformat(metadata['timestamp'])

        # Fallback to file modification time
        backup_file = self._find_backup_file(backup_name)
        if backup_file:
            return datetime.fromtimestamp(backup_file.stat().st_mtime)

        return datetime.min

def main():
    """Main backup management interface"""
    if len(sys.argv) < 2:
        print("Usage: python backup_manager.py <command> [args]")
        print("Commands:")
        print("  full-backup [name]     - Create full backup")
        print("  incremental-backup     - Create incremental backup")
        print("  restore <backup_name>  - Restore from backup")
        print("  list                   - List all backups")
        print("  cleanup                - Clean up old backups")
        print("  verify <backup_name>   - Verify backup integrity")
        sys.exit(1)

    manager = BackupManager()
    command = sys.argv[1]

    if command == "full-backup":
        backup_name = sys.argv[2] if len(sys.argv) > 2 else None
        result = manager.create_full_backup(backup_name)
        print(json.dumps(result, indent=2, default=str))

    elif command == "incremental-backup":
        result = manager.create_incremental_backup()
        print(json.dumps(result, indent=2, default=str))

    elif command == "restore" and len(sys.argv) > 2:
        backup_name = sys.argv[2]
        restore_path = sys.argv[3] if len(sys.argv) > 3 else None
        result = manager.restore_backup(backup_name, restore_path)
        print(json.dumps(result, indent=2, default=str))

    elif command == "list":
        backups = manager.list_backups()
        print("Available backups:")
        for backup in backups:
            print(f"  - {backup['name']} ({backup['size_mb']} MB, {backup['type']}, {backup['created']})")

    elif command == "cleanup":
        result = manager.cleanup_old_backups()
        print(f"Cleanup completed: {result['files_deleted']} files deleted, {result['space_freed_bytes']} bytes freed")

    elif command == "verify" and len(sys.argv) > 2:
        backup_name = sys.argv[2]
        backup_file = manager._find_backup_file(backup_name)
        if backup_file:
            is_valid = manager._verify_backup_integrity(backup_file)
            print(f"Backup {backup_name}: {'VALID' if is_valid else 'INVALID'}")
        else:
            print(f"Backup not found: {backup_name}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()