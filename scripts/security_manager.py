#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 Compensation Research System - Security Manager
Comprehensive security management and monitoring system
"""

import os
import sys
import json
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    def __init__(self):
        self.setup_logging()
        self.secrets_file = Path('.secrets.enc')
        self.key_file = Path('.encryption.key')
        self.audit_log = Path('logs/security_audit.log')
        self.fernet = self._initialize_encryption()

    def setup_logging(self):
        """Setup security logging"""
        os.makedirs('logs', exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SECURITY - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/security.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_encryption(self) -> Fernet:
        """Initialize encryption system"""
        if self.key_file.exists():
            # Load existing key
            key = self.key_file.read_bytes()
        else:
            # Generate new key
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            os.chmod(self.key_file, 0o600)  # Restrict permissions
            self.logger.info("Generated new encryption key")

        return Fernet(key)

    def encrypt_secret(self, value: str) -> str:
        """Encrypt a secret value"""
        if not value:
            return ""

        encrypted = self.fernet.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_secret(self, encrypted_value: str) -> str:
        """Decrypt a secret value"""
        if not encrypted_value:
            return ""

        try:
            encrypted_bytes = base64.b64decode(encrypted_value.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Failed to decrypt secret: {e}")
            return ""

    def store_secret(self, key: str, value: str) -> bool:
        """Store an encrypted secret"""
        try:
            # Load existing secrets
            secrets_data = self.load_secrets()

            # Encrypt and store
            encrypted_value = self.encrypt_secret(value)
            secrets_data[key] = {
                'value': encrypted_value,
                'created': datetime.utcnow().isoformat(),
                'last_accessed': datetime.utcnow().isoformat()
            }

            # Save to encrypted file
            secrets_json = json.dumps(secrets_data, indent=2)
            encrypted_content = self.fernet.encrypt(secrets_json.encode())
            self.secrets_file.write_bytes(encrypted_content)
            os.chmod(self.secrets_file, 0o600)

            self.audit_log_event('SECRET_STORED', {'key': key})
            self.logger.info(f"Secret stored: {key}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store secret {key}: {e}")
            return False

    def get_secret(self, key: str) -> Optional[str]:
        """Retrieve and decrypt a secret"""
        try:
            secrets_data = self.load_secrets()

            if key not in secrets_data:
                return None

            # Update last accessed time
            secrets_data[key]['last_accessed'] = datetime.utcnow().isoformat()
            self._save_secrets(secrets_data)

            encrypted_value = secrets_data[key]['value']
            decrypted_value = self.decrypt_secret(encrypted_value)

            self.audit_log_event('SECRET_ACCESSED', {'key': key})
            return decrypted_value

        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {key}: {e}")
            return None

    def load_secrets(self) -> Dict[str, Any]:
        """Load secrets from encrypted file"""
        if not self.secrets_file.exists():
            return {}

        try:
            encrypted_content = self.secrets_file.read_bytes()
            decrypted_content = self.fernet.decrypt(encrypted_content)
            return json.loads(decrypted_content.decode())
        except Exception as e:
            self.logger.error(f"Failed to load secrets: {e}")
            return {}

    def _save_secrets(self, secrets_data: Dict[str, Any]):
        """Save secrets to encrypted file"""
        secrets_json = json.dumps(secrets_data, indent=2)
        encrypted_content = self.fernet.encrypt(secrets_json.encode())
        self.secrets_file.write_bytes(encrypted_content)

    def list_secrets(self) -> List[str]:
        """List all stored secret keys (not values)"""
        secrets_data = self.load_secrets()
        return list(secrets_data.keys())

    def delete_secret(self, key: str) -> bool:
        """Delete a stored secret"""
        try:
            secrets_data = self.load_secrets()

            if key in secrets_data:
                del secrets_data[key]
                self._save_secrets(secrets_data)
                self.audit_log_event('SECRET_DELETED', {'key': key})
                self.logger.info(f"Secret deleted: {key}")
                return True
            else:
                self.logger.warning(f"Secret not found for deletion: {key}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to delete secret {key}: {e}")
            return False

    def rotate_encryption_key(self) -> bool:
        """Rotate the encryption key and re-encrypt all secrets"""
        try:
            # Load current secrets
            current_secrets = self.load_secrets()

            # Decrypt all current values
            decrypted_data = {}
            for key, data in current_secrets.items():
                decrypted_value = self.decrypt_secret(data['value'])
                decrypted_data[key] = {
                    'value': decrypted_value,
                    'created': data['created'],
                    'last_accessed': data['last_accessed']
                }

            # Generate new encryption key
            new_key = Fernet.generate_key()
            new_fernet = Fernet(new_key)

            # Re-encrypt all secrets with new key
            new_secrets = {}
            for key, data in decrypted_data.items():
                encrypted_value = base64.b64encode(
                    new_fernet.encrypt(data['value'].encode())
                ).decode()
                new_secrets[key] = {
                    'value': encrypted_value,
                    'created': data['created'],
                    'last_accessed': data['last_accessed']
                }

            # Backup old key
            backup_key_file = Path(f'.encryption.key.backup.{int(datetime.utcnow().timestamp())}')
            self.key_file.rename(backup_key_file)
            os.chmod(backup_key_file, 0o600)

            # Save new key and secrets
            self.key_file.write_bytes(new_key)
            os.chmod(self.key_file, 0o600)

            self.fernet = new_fernet
            self._save_secrets(new_secrets)

            self.audit_log_event('ENCRYPTION_KEY_ROTATED', {})
            self.logger.info("Encryption key rotated successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to rotate encryption key: {e}")
            return False

    def audit_log_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for auditing"""
        os.makedirs('logs', exist_ok=True)

        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'details': details,
            'user': os.environ.get('USER', 'unknown'),
            'process_id': os.getpid()
        }

        with open(self.audit_log, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

    def validate_api_key(self, api_key: str, service: str) -> bool:
        """Validate API key format and basic security"""
        if not api_key:
            return False

        # Basic validation rules
        validations = {
            'openai': lambda k: k.startswith('sk-') and len(k) > 40,
            'github': lambda k: k.startswith('ghp_') or k.startswith('gho_'),
            'slack': lambda k: k.startswith('xox'),
            'discord': lambda k: 'discord.com' in k or len(k) > 50
        }

        if service.lower() in validations:
            is_valid = validations[service.lower()](api_key)

            if is_valid:
                self.audit_log_event('API_KEY_VALIDATED', {'service': service, 'status': 'valid'})
            else:
                self.audit_log_event('API_KEY_VALIDATION_FAILED', {'service': service, 'status': 'invalid'})

            return is_valid

        # Generic validation for unknown services
        return len(api_key) >= 16 and api_key.isprintable()

    def scan_for_leaked_secrets(self) -> Dict[str, List[str]]:
        """Scan codebase for potential secret leaks"""
        secret_patterns = {
            'api_keys': [
                r'api[_-]?key[_-]?=\s*["\']([^"\']+)["\']',
                r'key[_-]?=\s*["\']([a-zA-Z0-9_-]{20,})["\']'
            ],
            'tokens': [
                r'token[_-]?=\s*["\']([^"\']+)["\']',
                r'auth[_-]?token[_-]?=\s*["\']([^"\']+)["\']'
            ],
            'passwords': [
                r'password[_-]?=\s*["\']([^"\']+)["\']',
                r'passwd[_-]?=\s*["\']([^"\']+)["\']'
            ],
            'github_tokens': [
                r'ghp_[a-zA-Z0-9]{36}',
                r'gho_[a-zA-Z0-9]{36}'
            ],
            'slack_tokens': [
                r'xox[baprs]-[a-zA-Z0-9-]+'
            ]
        }

        findings = {}
        scan_paths = ['.', 'scripts/', 'logs/']

        import re

        for path in scan_paths:
            if not os.path.exists(path):
                continue

            for root, dirs, files in os.walk(path):
                # Skip sensitive directories
                dirs[:] = [d for d in dirs if not d.startswith('.git') and d != '__pycache__']

                for file in files:
                    if file.endswith(('.py', '.yml', '.yaml', '.json', '.env', '.txt')):
                        file_path = os.path.join(root, file)

                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()

                            for category, patterns in secret_patterns.items():
                                for pattern in patterns:
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    if matches:
                                        if category not in findings:
                                            findings[category] = []
                                        findings[category].extend([
                                            f"{file_path}: {match[:10]}..."
                                            for match in matches
                                        ])

                        except Exception as e:
                            self.logger.warning(f"Could not scan file {file_path}: {e}")

        if findings:
            self.audit_log_event('SECRET_LEAK_DETECTED', {'findings_count': len(findings)})

        return findings

    def check_file_permissions(self) -> Dict[str, Any]:
        """Check file permissions for security"""
        sensitive_files = [
            '.env', '.secrets.enc', '.encryption.key',
            'logs/security.log', 'logs/security_audit.log'
        ]

        results = {}

        for file_path in sensitive_files:
            if os.path.exists(file_path):
                stat_info = os.stat(file_path)
                permissions = oct(stat_info.st_mode)[-3:]

                # Check if file is readable by others
                is_secure = not (int(permissions[1]) > 0 or int(permissions[2]) > 0)

                results[file_path] = {
                    'permissions': permissions,
                    'is_secure': is_secure,
                    'owner_readable': int(permissions[0]) >= 4,
                    'owner_writable': int(permissions[0]) >= 6
                }

                if not is_secure:
                    self.audit_log_event('INSECURE_FILE_PERMISSIONS', {
                        'file': file_path,
                        'permissions': permissions
                    })

        return results

    def generate_secure_password(self, length: int = 32) -> str:
        """Generate a cryptographically secure password"""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        self.audit_log_event('SECURE_PASSWORD_GENERATED', {'length': length})
        return password

    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for storage"""
        salt = secrets.token_bytes(32)
        hasher = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100000)
        return base64.b64encode(salt + hasher).decode()

    def verify_hashed_data(self, data: str, hashed: str) -> bool:
        """Verify hashed data"""
        try:
            decoded = base64.b64decode(hashed.encode())
            salt = decoded[:32]
            stored_hash = decoded[32:]

            new_hash = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100000)
            return secrets.compare_digest(stored_hash, new_hash)
        except Exception:
            return False

    def security_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive security health check"""
        health_report = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }

        # Check 1: File permissions
        health_report['checks']['file_permissions'] = self.check_file_permissions()

        # Check 2: Secret leaks
        leaks = self.scan_for_leaked_secrets()
        health_report['checks']['secret_leaks'] = {
            'status': 'secure' if not leaks else 'vulnerable',
            'findings': leaks
        }

        # Check 3: Encryption key status
        health_report['checks']['encryption'] = {
            'key_exists': self.key_file.exists(),
            'secrets_file_exists': self.secrets_file.exists(),
            'can_encrypt': True,
            'can_decrypt': True
        }

        try:
            # Test encryption/decryption
            test_data = "security_test"
            encrypted = self.encrypt_secret(test_data)
            decrypted = self.decrypt_secret(encrypted)
            health_report['checks']['encryption']['can_encrypt'] = True
            health_report['checks']['encryption']['can_decrypt'] = (decrypted == test_data)
        except Exception as e:
            health_report['checks']['encryption']['can_encrypt'] = False
            health_report['checks']['encryption']['can_decrypt'] = False
            health_report['checks']['encryption']['error'] = str(e)

        # Check 4: Secret inventory
        secrets_list = self.list_secrets()
        health_report['checks']['secrets_inventory'] = {
            'total_secrets': len(secrets_list),
            'secrets': secrets_list
        }

        # Determine overall status
        if leaks:
            health_report['overall_status'] = 'vulnerable'
        elif not health_report['checks']['encryption']['can_decrypt']:
            health_report['overall_status'] = 'degraded'

        return health_report

def main():
    """Main security management interface"""
    if len(sys.argv) < 2:
        print("Usage: python security_manager.py <command> [args]")
        print("Commands:")
        print("  store <key> <value>  - Store encrypted secret")
        print("  get <key>           - Retrieve secret")
        print("  list                - List all secret keys")
        print("  delete <key>        - Delete secret")
        print("  rotate-key          - Rotate encryption key")
        print("  scan-leaks          - Scan for secret leaks")
        print("  health-check        - Security health check")
        print("  generate-password   - Generate secure password")
        sys.exit(1)

    manager = SecurityManager()
    command = sys.argv[1]

    if command == "store" and len(sys.argv) == 4:
        key, value = sys.argv[2], sys.argv[3]
        if manager.store_secret(key, value):
            print(f"Secret '{key}' stored successfully")
        else:
            print(f"Failed to store secret '{key}'")

    elif command == "get" and len(sys.argv) == 3:
        key = sys.argv[2]
        value = manager.get_secret(key)
        if value is not None:
            print(value)
        else:
            print(f"Secret '{key}' not found")

    elif command == "list":
        secrets = manager.list_secrets()
        print("Stored secrets:")
        for secret in secrets:
            print(f"  - {secret}")

    elif command == "delete" and len(sys.argv) == 3:
        key = sys.argv[2]
        if manager.delete_secret(key):
            print(f"Secret '{key}' deleted")
        else:
            print(f"Failed to delete secret '{key}'")

    elif command == "rotate-key":
        if manager.rotate_encryption_key():
            print("Encryption key rotated successfully")
        else:
            print("Failed to rotate encryption key")

    elif command == "scan-leaks":
        leaks = manager.scan_for_leaked_secrets()
        if leaks:
            print("⚠️  Potential secret leaks found:")
            for category, findings in leaks.items():
                print(f"\n{category}:")
                for finding in findings[:5]:  # Limit output
                    print(f"  - {finding}")
        else:
            print("✅ No secret leaks detected")

    elif command == "health-check":
        report = manager.security_health_check()
        print(f"Security Health: {report['overall_status'].upper()}")
        print(json.dumps(report, indent=2))

    elif command == "generate-password":
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 32
        password = manager.generate_secure_password(length)
        print(password)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()