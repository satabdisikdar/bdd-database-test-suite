#!/usr/bin/env python3
"""
Test runner script for BDD Database Test Automation Suite
Provides easy command-line interface for running tests with different configurations
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0, result.stdout, result.stderr

def setup_environment():
    """Set up the test environment"""
    print("Setting up test environment...")
    
    # Create required directories
    directories = ['reports', 'reports/junit', 'data']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Check if virtual environment exists
    venv_path = Path('venv')
    if not venv_path.exists():
        print("Creating virtual environment...")
        success, _, _ = run_command(f"{sys.executable} -m venv venv")
        if not success:
            print("Failed to create virtual environment")
            return False
    
    # Install dependencies
    pip_cmd = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip.exe"
    print("Installing dependencies...")
    success, _, _ = run_command(f"{pip_cmd} install -r requirements.txt")
    if not success:
        print("Failed to install dependencies")
        return False
    
    print("Environment setup complete!")
    return True

def run_tests(args):
    """Run the BDD tests with specified configuration"""
    
    # Build behave command
    behave_cmd = "behave"
    
    # Add profile if specified
    if args.profile:
        behave_cmd += f" -D profile={args.profile}"
    
    # Add database driver if specified
    if args.db_driver:
        behave_cmd += f" -D db_driver={args.db_driver}"
    
    # Add timeout if specified
    if args.timeout:
        behave_cmd += f" -D timeout={args.timeout}"
    
    # Add specific feature file if specified
    if args.feature:
        behave_cmd += f" features/{args.feature}"
    
    # Add scenario name if specified
    if args.scenario:
        behave_cmd += f" -n '{args.scenario}'"
    
    # Add tags if specified
    if args.tags:
        behave_cmd += f" --tags={args.tags}"
    
    # Add format options
    if args.format:
        behave_cmd += f" --format={args.format}"
    
    # Add output file if specified
    if args.output:
        behave_cmd += f" --outfile={args.output}"
    
    # Add JUnit reporting if requested
    if args.junit:
        behave_cmd += " --junit --junit-directory=reports/junit"
    
    # Add other options
    if args.dry_run:
        behave_cmd += " --dry-run"
    
    if args.stop_on_failure:
        behave_cmd += " --stop"
    
    if args.verbose:
        behave_cmd += " --verbose"
    
    if args.no_capture:
        behave_cmd += " --no-capture"
    
    # Run the tests
    print(f"Running tests with command: {behave_cmd}")
    success, stdout, stderr = run_command(behave_cmd)
    
    if success:
        print("Tests completed successfully!")
    else:
        print("Tests failed!")
        return False
    
    # Generate reports if requested
    if args.generate_reports:
        generate_reports()
    
    return True

def generate_reports():
    """Generate additional test reports"""
    print("Generating additional reports...")
    
    # Generate HTML report
    html_cmd = "behave --format=html --outfile=reports/results.html"
    run_command(html_cmd)
    
    # Generate JSON report
    json_cmd = "behave --format=json --outfile=reports/results.json"
    run_command(json_cmd)
    
    print("Reports generated in reports/ directory")

def list_scenarios():
    """List all available test scenarios"""
    print("Available test scenarios:")
    
    # Use behave dry-run to list scenarios
    cmd = "behave --dry-run --no-summary"
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print(stdout)
    else:
        print("Failed to list scenarios")

def validate_setup():
    """Validate that the test environment is properly set up"""
    print("Validating test environment setup...")
    
    # Check if required files exist
    required_files = [
        'requirements.txt',
        'behave.ini',
        'config/database_config.py',
        'config/test_config.py',
        'utils/database_utils.py',
        'features/database_operations.feature',
        'features/performance_testing.feature',
        'features/steps/database_steps.py',
        'features/environment.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    # Check if behave is installed
    try:
        import behave
        print(f"Behave version: {behave.__version__}")
    except ImportError:
        print("Behave not installed. Run with --setup first.")
        return False
    
    # Check if database utilities can be imported
    try:
        from utils.database_utils import db_manager
        print("Database utilities imported successfully")
    except ImportError as e:
        print(f"Failed to import database utilities: {e}")
        return False
    
    print("Environment validation complete!")
    return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="BDD Database Test Automation Suite Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                                    # Run all tests
  python run_tests.py --profile=staging                 # Run with staging profile
  python run_tests.py --feature=database_operations.feature  # Run specific feature
  python run_tests.py --scenario="Create a new user"    # Run specific scenario
  python run_tests.py --tags=@performance              # Run performance tests only
  python run_tests.py --setup                          # Set up environment
  python run_tests.py --list                           # List available scenarios
  python run_tests.py --validate                       # Validate setup
        """
    )
    
    # Configuration options
    parser.add_argument('--profile', choices=['local', 'ci', 'staging', 'production'],
                       help='Configuration profile to use')
    parser.add_argument('--db-driver', choices=['sqlite', 'postgresql', 'mysql'],
                       help='Database driver to use')
    parser.add_argument('--timeout', type=int, help='Test timeout in seconds')
    
    # Test selection options
    parser.add_argument('--feature', help='Specific feature file to run')
    parser.add_argument('--scenario', help='Specific scenario to run')
    parser.add_argument('--tags', help='Tags to filter tests (e.g., @performance)')
    
    # Output options
    parser.add_argument('--format', choices=['pretty', 'plain', 'json', 'html'],
                       default='pretty', help='Output format')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--junit', action='store_true', help='Generate JUnit XML reports')
    parser.add_argument('--generate-reports', action='store_true',
                       help='Generate additional HTML/JSON reports')
    
    # Execution options
    parser.add_argument('--dry-run', action='store_true',
                       help='Dry run (validate scenarios without executing)')
    parser.add_argument('--stop-on-failure', action='store_true',
                       help='Stop execution on first failure')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--no-capture', action='store_true',
                       help='Don\'t capture stdout/stderr')
    
    # Utility options
    parser.add_argument('--setup', action='store_true',
                       help='Set up test environment')
    parser.add_argument('--list', action='store_true',
                       help='List available test scenarios')
    parser.add_argument('--validate', action='store_true',
                       help='Validate test environment setup')
    
    args = parser.parse_args()
    
    # Handle utility commands
    if args.setup:
        return setup_environment()
    
    if args.list:
        list_scenarios()
        return True
    
    if args.validate:
        return validate_setup()
    
    # Run tests
    return run_tests(args)

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 