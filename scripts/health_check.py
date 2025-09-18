#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔬 Compensation Research System - Health Check
Comprehensive system health monitoring and validation
"""

import sys
import os
import json
import time
import psutil
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HealthChecker:
    def __init__(self):
        self.health_status = {
            "overall": "unknown",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {},
            "metrics": {},
            "warnings": [],
            "errors": []
        }

        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/health_check.log', mode='a')
            ]
        )
        self.logger = logging.getLogger(__name__)

    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource availability"""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory Usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)

            # Disk Usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)

            # Network
            network = psutil.net_io_counters()

            result = {
                "status": "healthy",
                "cpu": {
                    "usage_percent": cpu_percent,
                    "status": "healthy" if cpu_percent < 80 else "warning" if cpu_percent < 95 else "critical"
                },
                "memory": {
                    "usage_percent": memory_percent,
                    "available_gb": round(memory_available_gb, 2),
                    "status": "healthy" if memory_percent < 80 else "warning" if memory_percent < 95 else "critical"
                },
                "disk": {
                    "usage_percent": disk_percent,
                    "free_gb": round(disk_free_gb, 2),
                    "status": "healthy" if disk_percent < 80 else "warning" if disk_percent < 95 else "critical"
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "status": "healthy"
                }
            }

            # Overall system status
            if any(comp["status"] == "critical" for comp in [result["cpu"], result["memory"], result["disk"]]):
                result["status"] = "critical"
            elif any(comp["status"] == "warning" for comp in [result["cpu"], result["memory"], result["disk"]]):
                result["status"] = "warning"

            return result

        except Exception as e:
            self.logger.error(f"System resource check failed: {e}")
            return {"status": "error", "error": str(e)}

    def check_dependencies(self) -> Dict[str, Any]:
        """Check Python dependencies and imports"""
        required_modules = [
            'requests', 'unidecode', 'schedule', 'pandas', 'numpy',
            'nltk', 'spacy', 'redis', 'sqlalchemy', 'prometheus_client'
        ]

        result = {
            "status": "healthy",
            "modules": {},
            "missing": [],
            "outdated": []
        }

        for module in required_modules:
            try:
                __import__(module)
                result["modules"][module] = "available"
            except ImportError:
                result["modules"][module] = "missing"
                result["missing"].append(module)
                result["status"] = "error"

        return result

    def check_file_system(self) -> Dict[str, Any]:
        """Check file system structure and permissions"""
        required_dirs = [
            'logs', 'cache', 'backups',
            'Compensation-Research-Vault',
            'Compensation-Research-Vault/00-Templates',
            'Compensation-Research-Vault/01-Papers',
            'Compensation-Research-Vault/08-Meta'
        ]

        result = {
            "status": "healthy",
            "directories": {},
            "permissions": {},
            "missing_dirs": []
        }

        for dir_path in required_dirs:
            path = Path(dir_path)
            if path.exists():
                result["directories"][dir_path] = "exists"
                result["permissions"][dir_path] = {
                    "readable": os.access(path, os.R_OK),
                    "writable": os.access(path, os.W_OK)
                }

                if not (os.access(path, os.R_OK) and os.access(path, os.W_OK)):
                    result["status"] = "warning"

            else:
                result["directories"][dir_path] = "missing"
                result["missing_dirs"].append(dir_path)

                # Try to create missing directories
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    result["directories"][dir_path] = "created"
                except Exception as e:
                    result["status"] = "error"
                    self.logger.error(f"Failed to create directory {dir_path}: {e}")

        return result

    def check_network_connectivity(self) -> Dict[str, Any]:
        """Check network connectivity to external services"""
        test_urls = [
            ("OpenAlex API", "https://api.openalex.org/works", 5),
            ("GitHub API", "https://api.github.com", 5),
            ("Google DNS", "https://8.8.8.8", 3)
        ]

        result = {
            "status": "healthy",
            "endpoints": {},
            "failed_endpoints": []
        }

        for name, url, timeout in test_urls:
            try:
                import requests
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    result["endpoints"][name] = {
                        "status": "reachable",
                        "response_time": response.elapsed.total_seconds()
                    }
                else:
                    result["endpoints"][name] = {
                        "status": "unreachable",
                        "status_code": response.status_code
                    }
                    result["failed_endpoints"].append(name)

            except Exception as e:
                result["endpoints"][name] = {
                    "status": "error",
                    "error": str(e)
                }
                result["failed_endpoints"].append(name)

        if result["failed_endpoints"]:
            result["status"] = "warning" if len(result["failed_endpoints"]) < len(test_urls) else "error"

        return result

    def check_application_components(self) -> Dict[str, Any]:
        """Check application-specific components"""
        components = [
            'paper_screener.py',
            'why_analyzer.py',
            'node_connector.py',
            'obsidian_generator.py',
            'compensation_research_system.py'
        ]

        result = {
            "status": "healthy",
            "components": {},
            "missing_components": []
        }

        for component in components:
            if os.path.exists(component):
                try:
                    # Try to import and validate
                    module_name = component.replace('.py', '')
                    if module_name == 'compensation_research_system':
                        # Skip full import for main system to avoid circular imports
                        result["components"][component] = "available"
                    else:
                        __import__(module_name)
                        result["components"][component] = "available"

                except Exception as e:
                    result["components"][component] = f"import_error: {str(e)}"
                    result["status"] = "warning"
            else:
                result["components"][component] = "missing"
                result["missing_components"].append(component)
                result["status"] = "error"

        return result

    def check_configuration(self) -> Dict[str, Any]:
        """Check configuration and environment variables"""
        result = {
            "status": "healthy",
            "environment": {},
            "configuration": {}
        }

        # Check environment variables
        env_vars = [
            "PYTHONPATH", "PATH", "HOME", "USER"
        ]

        for var in env_vars:
            result["environment"][var] = os.environ.get(var, "not_set")

        # Check optional configuration
        optional_vars = [
            "OPENAI_API_KEY", "RESEARCH_CONFIG", "SLACK_WEBHOOK",
            "DISCORD_WEBHOOK", "AWS_ACCESS_KEY_ID"
        ]

        for var in optional_vars:
            value = os.environ.get(var)
            result["configuration"][var] = "configured" if value else "not_configured"

        return result

    def run_performance_test(self) -> Dict[str, Any]:
        """Run basic performance tests"""
        result = {
            "status": "healthy",
            "tests": {}
        }

        # File I/O Test
        try:
            start_time = time.time()
            test_file = Path("temp_health_test.txt")
            test_file.write_text("Health check test data" * 1000)
            content = test_file.read_text()
            test_file.unlink()

            file_io_time = time.time() - start_time
            result["tests"]["file_io"] = {
                "duration_seconds": round(file_io_time, 3),
                "status": "healthy" if file_io_time < 1.0 else "warning"
            }

        except Exception as e:
            result["tests"]["file_io"] = {"status": "error", "error": str(e)}
            result["status"] = "warning"

        # Memory allocation test
        try:
            start_time = time.time()
            test_data = [i for i in range(100000)]
            del test_data

            memory_test_time = time.time() - start_time
            result["tests"]["memory_allocation"] = {
                "duration_seconds": round(memory_test_time, 3),
                "status": "healthy" if memory_test_time < 0.5 else "warning"
            }

        except Exception as e:
            result["tests"]["memory_allocation"] = {"status": "error", "error": str(e)}
            result["status"] = "warning"

        return result

    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        self.logger.info("Starting comprehensive health check...")

        checks = {
            "system_resources": self.check_system_resources,
            "dependencies": self.check_dependencies,
            "file_system": self.check_file_system,
            "network": self.check_network_connectivity,
            "application": self.check_application_components,
            "configuration": self.check_configuration,
            "performance": self.run_performance_test
        }

        for check_name, check_func in checks.items():
            try:
                self.logger.info(f"Running {check_name} check...")
                self.health_status["checks"][check_name] = check_func()

                # Collect warnings and errors
                check_result = self.health_status["checks"][check_name]
                if check_result["status"] == "warning":
                    self.health_status["warnings"].append(f"{check_name}: {check_result.get('error', 'Warning condition detected')}")
                elif check_result["status"] in ["error", "critical"]:
                    self.health_status["errors"].append(f"{check_name}: {check_result.get('error', 'Error condition detected')}")

            except Exception as e:
                self.logger.error(f"Check {check_name} failed: {e}")
                self.health_status["checks"][check_name] = {
                    "status": "error",
                    "error": str(e)
                }
                self.health_status["errors"].append(f"{check_name}: {str(e)}")

        # Determine overall health status
        if self.health_status["errors"]:
            self.health_status["overall"] = "unhealthy"
        elif self.health_status["warnings"]:
            self.health_status["overall"] = "degraded"
        else:
            self.health_status["overall"] = "healthy"

        self.logger.info(f"Health check completed. Overall status: {self.health_status['overall']}")
        return self.health_status

    def save_health_report(self):
        """Save health report to file"""
        os.makedirs('logs', exist_ok=True)

        report_file = f"logs/health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.health_status, f, indent=2, default=str)

        # Also save as latest
        with open('health_status.txt', 'w') as f:
            f.write(self.health_status['overall'])

        with open('logs/health_latest.json', 'w') as f:
            json.dump(self.health_status, f, indent=2, default=str)

        self.logger.info(f"Health report saved to {report_file}")

def main():
    """Main health check execution"""
    checker = HealthChecker()

    try:
        # Run all health checks
        health_status = checker.run_all_checks()

        # Save report
        checker.save_health_report()

        # Print summary
        print(f"🔬 Health Check Summary")
        print(f"Overall Status: {health_status['overall'].upper()}")
        print(f"Timestamp: {health_status['timestamp']}")

        if health_status['warnings']:
            print(f"\n⚠️  Warnings ({len(health_status['warnings'])}):")
            for warning in health_status['warnings']:
                print(f"  - {warning}")

        if health_status['errors']:
            print(f"\n❌ Errors ({len(health_status['errors'])}):")
            for error in health_status['errors']:
                print(f"  - {error}")

        # Exit with appropriate code
        if health_status['overall'] == 'unhealthy':
            sys.exit(1)
        elif health_status['overall'] == 'degraded':
            sys.exit(2)
        else:
            sys.exit(0)

    except Exception as e:
        logging.error(f"Health check failed: {e}")
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()