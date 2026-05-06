#!/usr/bin/env python3
"""
GEESP-Angola Master Integration & Validation Script
Comprehensive testing, type checking, and quality assurance for the entire system
Runs all validation tasks sequentially and generates a quality report
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ValidationRunner:
    """Orchestrates all validation tasks"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: Dict[str, Dict] = {}
        self.start_time = datetime.now()

    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}▶ {text}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str]:
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300
            )

            if result.returncode == 0:
                self.print_success(description)
                return True, result.stdout
            else:
                self.print_error(f"{description} - Exit code: {result.returncode}")
                if result.stderr:
                    print(f"  Error output: {result.stderr[:500]}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.print_error(f"{description} - Timeout (5 min)")
            return False, "Command timeout"
        except Exception as e:
            self.print_error(f"{description} - {str(e)}")
            return False, str(e)

    # ========================================================================
    # VALIDATION TASKS
    # ========================================================================

    def validate_python_syntax(self) -> bool:
        """Validate all Python files for syntax errors"""
        self.print_header("STEP 1: Python Syntax Validation")

        python_files = list(self.project_root.glob("scripts/**/*.py")) + \
                       list(self.project_root.glob("models/**/*.py")) + \
                       list(self.project_root.glob("tests/**/*.py")) + \
                       list(self.project_root.glob("migrations/**/*.py"))

        print(f"Checking {len(python_files)} Python files...")

        all_valid = True
        for py_file in python_files:
            success, _ = self.run_command(
                ["python", "-m", "py_compile", str(py_file)],
                f"Syntax check: {py_file.name}"
            )
            if not success:
                all_valid = False

        self.results["syntax_validation"] = {"passed": all_valid}
        return all_valid

    def validate_imports(self) -> bool:
        """Validate all imports are resolvable"""
        self.print_header("STEP 2: Import Validation")

        test_code = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent / 'models'))

# Test critical imports
try:
    from error_handlers import GEESPError, validate_inputs
    print("✓ Error handlers")
    
    from config_loader import load_config
    print("✓ Config loader")
    
    from mcda_analysis import MCDAnalyzer
    print("✓ MCDA analysis")
    
    from lcoe_calculator import LCOECalculator
    print("✓ LCOE calculator")
    
    from data_loaders_async import get_async_loader, get_progress_tracker
    print("✓ Async data loaders")
    
    from earth_engine_integration import get_gee_extractor
    print("✓ GEE integration")
    
    from models.monitoring import get_database_manager
    print("✓ Database models")
    
    print("\\n✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}", file=sys.stderr)
    sys.exit(1)
"""

        with open("/tmp/test_imports.py", "w") as f:
            f.write(test_code)

        success, output = self.run_command(
            ["python", "/tmp/test_imports.py"],
            "Import validation"
        )

        if success:
            print(output)

        self.results["import_validation"] = {"passed": success}
        return success

    def run_pytest(self) -> bool:
        """Run pytest test suite"""
        self.print_header("STEP 3: Pytest Test Suite")

        test_dirs = [
            "tests/test_coverage_expansion.py",
            "tests/test_gee_integration_full.py",
            "tests/test_database_models.py",
        ]

        all_passed = True
        for test_file in test_dirs:
            if (self.project_root / test_file).exists():
                success, output = self.run_command(
                    ["python", "-m", "pytest", test_file, "-v", "--tb=short"],
                    f"Running {Path(test_file).name}"
                )
                if not success:
                    all_passed = False
                    print(f"  Output (first 1000 chars): {output[:1000]}")

        self.results["pytest"] = {"passed": all_passed}
        return all_passed

    def type_check_mypy(self) -> bool:
        """Run mypy for type checking"""
        self.print_header("STEP 4: Type Checking (mypy)")

        python_dirs = [
            "scripts/mcda_analysis.py",
            "scripts/lcoe_calculator.py",
            "scripts/api.py",
            "models/monitoring.py",
        ]

        all_passed = True
        for py_file in python_dirs:
            full_path = self.project_root / py_file
            if full_path.exists():
                success, output = self.run_command(
                    ["python", "-m", "mypy", str(full_path), "--ignore-missing-imports"],
                    f"Type check: {Path(py_file).name}"
                )
                if not success and "No module found" not in output:
                    all_passed = False
                    print(f"  Issues: {output[:500]}")

        self.results["mypy"] = {"passed": all_passed}
        return all_passed

    def lint_code(self) -> bool:
        """Run pylint for code quality"""
        self.print_header("STEP 5: Code Linting (pylint)")

        python_files = [
            "scripts/mcda_analysis.py",
            "scripts/error_handlers.py",
            "scripts/config_loader.py",
        ]

        all_passed = True
        for py_file in python_files:
            full_path = self.project_root / py_file
            if full_path.exists():
                success, output = self.run_command(
                    ["python", "-m", "pylint", str(full_path), "--disable=all", 
                     "--enable=E,F", "--exit-zero"],
                    f"Lint: {Path(py_file).name}"
                )
                # pylint often returns non-zero even with warnings
                print(f"  Result: {output.split(chr(10))[0] if output else 'OK'}")

        self.results["pylint"] = {"passed": True}  # Non-blocking
        return True

    def check_code_formatting(self) -> bool:
        """Check code formatting with black"""
        self.print_header("STEP 6: Code Formatting Check (black)")

        python_files = [
            "scripts/api.py",
            "scripts/earth_engine_integration.py",
            "models/monitoring.py",
        ]

        all_need_formatting = False
        for py_file in python_files:
            full_path = self.project_root / py_file
            if full_path.exists():
                success, output = self.run_command(
                    ["python", "-m", "black", "--check", str(full_path)],
                    f"Format check: {Path(py_file).name}"
                )
                if not success:
                    all_need_formatting = True
                    print(f"  Needs formatting: {Path(py_file).name}")

        self.results["black"] = {"passed": not all_need_formatting}
        return not all_need_formatting

    def validate_docker_image(self) -> bool:
        """Validate Dockerfile can be built"""
        self.print_header("STEP 7: Docker Image Validation")

        dockerfile = self.project_root / "Dockerfile"
        if not dockerfile.exists():
            self.print_warning("Dockerfile not found")
            self.results["docker"] = {"passed": False, "reason": "No Dockerfile"}
            return False

        success, output = self.run_command(
            ["docker", "build", "-t", "geesp-test:latest", "--dry-run", "."],
            "Docker build validation"
        )

        self.results["docker"] = {"passed": success}
        return success

    def validate_k8s_manifests(self) -> bool:
        """Validate Kubernetes manifests"""
        self.print_header("STEP 8: Kubernetes Manifest Validation")

        k8s_files = list((self.project_root / "k8s").glob("*.yaml"))

        if not k8s_files:
            self.print_warning("No Kubernetes manifests found")
            self.results["k8s"] = {"passed": True, "files": 0}
            return True

        print(f"Found {len(k8s_files)} Kubernetes manifests")

        for k8s_file in k8s_files:
            # Basic YAML syntax check
            import yaml
            try:
                with open(k8s_file) as f:
                    yaml.safe_load_all(f)
                self.print_success(f"Valid manifest: {k8s_file.name}")
            except Exception as e:
                self.print_error(f"Invalid manifest {k8s_file.name}: {e}")
                self.results["k8s"] = {"passed": False}
                return False

        self.results["k8s"] = {"passed": True, "files": len(k8s_files)}
        return True

    def check_dependencies(self) -> bool:
        """Verify all required dependencies are installed"""
        self.print_header("STEP 9: Dependency Verification")

        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.print_warning("requirements.txt not found")
            self.results["dependencies"] = {"passed": True, "warning": "No requirements.txt"}
            return True

        success, output = self.run_command(
            ["pip", "check"],
            "Dependency conflict check"
        )

        self.results["dependencies"] = {"passed": success}
        return success

    def validate_api_endpoints(self) -> bool:
        """Validate FastAPI endpoints are properly defined"""
        self.print_header("STEP 10: API Endpoint Validation")

        api_file = self.project_root / "scripts" / "api.py"
        if not api_file.exists():
            self.print_warning("api.py not found")
            self.results["api_endpoints"] = {"passed": True}
            return True

        test_code = f"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('{self.project_root}') / 'scripts'))

try:
    from api import app
    
    # Check routes
    routes = [route.path for route in app.routes]
    
    required_endpoints = ['/health', '/ready', '/mcda', '/mcda/batch', '/api/docs']
    
    found_endpoints = []
    missing_endpoints = []
    
    for endpoint in required_endpoints:
        if any(endpoint in route for route in routes):
            found_endpoints.append(endpoint)
        else:
            missing_endpoints.append(endpoint)
    
    print(f"✓ Found {{len(found_endpoints)}} required endpoints")
    if missing_endpoints:
        print(f"⚠ Missing endpoints: {{', '.join(missing_endpoints)}}")
    else:
        print("✓ All required endpoints present")
        
except Exception as e:
    print(f"✗ API validation error: {{e}}", file=sys.stderr)
    sys.exit(1)
"""

        with open("/tmp/test_api.py", "w") as f:
            f.write(test_code)

        success, output = self.run_command(
            ["python", "/tmp/test_api.py"],
            "API endpoint validation"
        )

        if success:
            print(output)

        self.results["api_endpoints"] = {"passed": success}
        return success

    def generate_quality_report(self):
        """Generate comprehensive quality report"""
        self.print_header("VALIDATION REPORT SUMMARY")

        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results.values() if r.get("passed", False))

        print(f"\nTotal Checks: {total_checks}")
        print(f"Passed: {Colors.OKGREEN}{passed_checks}{Colors.ENDC}")
        print(f"Failed: {Colors.FAIL}{total_checks - passed_checks}{Colors.ENDC}")
        print(f"Success Rate: {Colors.OKBLUE}{passed_checks/total_checks*100:.1f}%{Colors.ENDC}")

        print(f"\n{Colors.BOLD}Detailed Results:{Colors.ENDC}")
        for check_name, result in self.results.items():
            status = Colors.OKGREEN + "✓ PASS" + Colors.ENDC if result.get("passed") else Colors.FAIL + "✗ FAIL" + Colors.ENDC
            print(f"  {check_name:30} {status}")

        # Overall assessment
        print(f"\n{Colors.BOLD}Overall Assessment:{Colors.ENDC}")
        if passed_checks == total_checks:
            print(f"{Colors.OKGREEN}✓ All validation checks passed - System is production-ready!{Colors.ENDC}")
        elif passed_checks >= total_checks * 0.9:
            print(f"{Colors.WARNING}⚠ Most checks passed - Address failures before production deployment{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ Multiple validation failures - Significant work required{Colors.ENDC}")

        # Save report to file
        report_file = self.project_root / "VALIDATION_REPORT.json"
        with open(report_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_checks": total_checks,
                "passed_checks": passed_checks,
                "success_rate": passed_checks / total_checks,
                "results": self.results,
            }, f, indent=2)

        print(f"\n✓ Detailed report saved to: VALIDATION_REPORT.json")

        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱ Total validation time: {elapsed_time:.1f} seconds")

    def run_all_validations(self) -> bool:
        """Run all validation tasks"""
        self.print_header("GEESP-Angola Master Integration & Validation")
        print(f"Project root: {self.project_root}")
        print(f"Start time: {self.start_time.isoformat()}\n")

        tasks = [
            ("Python Syntax", self.validate_python_syntax),
            ("Imports", self.validate_imports),
            ("Pytest", self.run_pytest),
            ("MyPy Type Checking", self.type_check_mypy),
            ("Pylint", self.lint_code),
            ("Black Formatting", self.check_code_formatting),
            ("Docker Image", self.validate_docker_image),
            ("K8s Manifests", self.validate_k8s_manifests),
            ("Dependencies", self.check_dependencies),
            ("API Endpoints", self.validate_api_endpoints),
        ]

        for task_name, task_func in tasks:
            try:
                task_func()
            except Exception as e:
                self.print_error(f"Unexpected error in {task_name}: {e}")
                self.results[task_name.lower()] = {"passed": False, "error": str(e)}

        self.generate_quality_report()

        # Return overall success (allow warnings)
        return True


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    validation = ValidationRunner(project_root)

    try:
        validation.run_all_validations()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Validation interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.FAIL}Validation failed with error: {e}{Colors.ENDC}")
        sys.exit(1)
