#!/usr/bin/env python3
"""
Assignment Generator Script
Automates creation of Docker-based assignments with testing infrastructure
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

class AssignmentGenerator:
    def __init__(self, assignment_name, assignment_id, description):
        self.assignment_name = assignment_name
        self.assignment_id = assignment_id
        self.description = description
        self.base_dir = Path(assignment_name.replace(" ", "_").lower())
        self.src_dir = self.base_dir / "src"
        
    def create_directory_structure(self):
        """Create base directory structure"""
        self.base_dir.mkdir(exist_ok=True)
        self.src_dir.mkdir(exist_ok=True)
        print(f"✅ Created directory: {self.base_dir}")
        
    def create_dockerfile(self, base_image="python:3.11-slim", dependencies="pytest pytest-json-report lxml"):
        """Create Dockerfile"""
        dockerfile_content = f"""FROM {base_image}

USER root

WORKDIR /app

RUN pip install {dependencies}

COPY conftest.py /app/conftest.py
COPY pytest.ini /app/pytest.ini
COPY test_assignment.py /app/test_assignment.py
COPY runner.sh /app/runner.sh
COPY enhance_json.py /app/enhance_json.py

RUN chmod +x /app/runner.sh /app/enhance_json.py

CMD ["/bin/sh", "-c", "export PYTHONPATH=/app/submission:/app:$PYTHONPATH && /app/runner.sh"]
"""
        dockerfile_path = self.base_dir / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        print(f"✅ Created Dockerfile")
        
    def create_runner_sh(self):
        """Create runner.sh script"""
        runner_content = """#!/bin/bash
set +e

export PYTHONPATH=/app/submission:/app:$PYTHONPATH

pytest /app/test_assignment.py --json-report --json-report-file=/tmp/report.json -v > /dev/null 2>&1

python3 /app/enhance_json.py /tmp/report.json

exit 0
"""
        runner_path = self.base_dir / "runner.sh"
        runner_path.write_text(runner_content)
        runner_path.chmod(0o755)
        print(f"✅ Created runner.sh")
        
    def create_enhance_json(self):
        """Create enhance_json.py"""
        enhance_content = '''#!/usr/bin/env python3

import json
import sys
import os

os.environ['PYTHONUNBUFFERED'] = '1'

def enhance_report(report_file):
    # ALWAYS output valid JSON, even on error
    try:
        if not os.path.exists(report_file):
            raise FileNotFoundError(f"Report file {report_file} not found")
        
        with open(report_file, 'r') as f:
            content = f.read()
        
        data = json.loads(content)
        
        summary = data.get('summary', {})
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        total = summary.get('total', 0)
        
        if total > 0:
            marks = passed / total
        else:
            marks = 0
        
        data['stats'] = {
            'total_tests': total,
            'passed': passed,
            'failed': failed,
            'marks': round(marks, 2),
            'percentage': round(marks * 100, 2)
        }
        
        output = json.dumps(data, indent=2)
        sys.stdout.write(output)
        sys.stdout.write('\\n')
        sys.stdout.flush()
        
    except Exception as e:
        # Output error JSON with stats
        error_data = {
            'error': str(e),
            'stats': {
                'total_tests': 0,
                'passed': 0,
                'failed': 1,
                'marks': 0.0,
                'percentage': 0.0
            }
        }
        output = json.dumps(error_data, indent=2)
        sys.stdout.write(output)
        sys.stdout.write('\\n')
        sys.stdout.flush()
    
    return 0  # ALWAYS return success

if __name__ == '__main__':
    if len(sys.argv) < 2:
        error_output = json.dumps({'error': 'Missing report file argument', 'stats': {'total_tests': 0, 'passed': 0, 'failed': 1, 'marks': 0.0, 'percentage': 0.0}})
        sys.stdout.write(error_output)
        sys.stdout.write('\\n')
        sys.stdout.flush()
        sys.exit(0)  # ALWAYS exit 0
    
    enhance_report(sys.argv[1])
    sys.exit(0)  # ALWAYS exit 0
'''
        enhance_path = self.base_dir / "enhance_json.py"
        enhance_path.write_text(enhance_content)
        enhance_path.chmod(0o755)
        print(f"✅ Created enhance_json.py")
        
    def create_conftest(self):
        """Create conftest.py"""
        conftest_content = '''import sys
from pathlib import Path

# Add submission directory to Python path
submission_path = Path("/app/submission").resolve()
if submission_path not in [Path(p).resolve() for p in sys.path]:
    sys.path.insert(0, str(submission_path))
'''
        conftest_path = self.base_dir / "conftest.py"
        conftest_path.write_text(conftest_content)
        print(f"✅ Created conftest.py")
        
    def create_pytest_ini(self):
        """Create pytest.ini"""
        pytest_content = """[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    layout: Layout related tests
    textview: TextView related tests
    smoke: Smoke tests
"""
        pytest_path = self.base_dir / "pytest.ini"
        pytest_path.write_text(pytest_content)
        print(f"✅ Created pytest.ini")
        
    def create_docker_compose(self, image_name="assignment1-x86"):
        """Create docker-compose.yml"""
        compose_content = f"""version: '3.8'

services:
  judge:
    image: {image_name}:latest
    platform: linux/amd64
    working_dir: /app
    
    volumes:
      - ./src:/app/submission:ro
    
    networks:
      - judge-network
    
    security_opt:
      - no-new-privileges:true
    
    cap_drop:
      - ALL
    
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=50m
    
    stdin_open: true
    tty: true
    
    command: /bin/sh -c "export PYTHONPATH=/app/submission:/app:$PYTHONPATH && /app/runner.sh"

networks:
  judge-network:
    driver: bridge
"""
        compose_path = self.base_dir / "docker-compose.yml"
        compose_path.write_text(compose_content)
        print(f"✅ Created docker-compose.yml")
        
    def create_test_template(self):
        """Create a template test file"""
        test_content = '''import pytest
import sys
from pathlib import Path

# Your test cases go here
# Example:
# def test_example():
#     assert True

# Create placeholder test
class TestTemplate:
    def test_placeholder(self):
        """Placeholder test - replace with actual tests"""
        assert True
'''
        test_path = self.base_dir / "test_assignment.py"
        test_path.write_text(test_content)
        print(f"✅ Created test_assignment.py (template)")
        
    def create_zips(self, starter_content="TODO: Complete this assignment", 
                    solution_content="Assignment completed"):
        """Create startercode.zip and solution.zip"""
        import zipfile
        
        # Create starter zip
        starter_path = self.base_dir / "startercode.zip"
        with zipfile.ZipFile(starter_path, 'w') as zf:
            zf.writestr("README.md", starter_content)
        
        # Create solution zip
        solution_path = self.base_dir / "solution.zip"
        with zipfile.ZipFile(solution_path, 'w') as zf:
            zf.writestr("README.md", solution_content)
        
        print(f"✅ Created startercode.zip and solution.zip")
        
    def create_architecture_doc(self):
        """Create ARCHITECTURE.md documentation"""
        arch_doc = f"""# {self.assignment_name} - Architecture

## Overview
{self.description}

## File Structure
```
{self.assignment_name}/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Container orchestration
├── runner.sh              # Main entry point script
├── enhance_json.py        # JSON report enhancement
├── test_assignment.py     # Test suite
├── conftest.py            # Pytest configuration
├── pytest.ini             # Pytest settings
├── startercode.zip        # Starter template for students
├── solution.zip           # Complete solution
└── src/                   # Student submission directory
    └── (files to be submitted)
```

## How It Works

### Execution Flow
1. Docker container starts with `runner.sh` as entry point
2. `runner.sh` exports PYTHONPATH and runs pytest
3. Pytest generates JSON report at `/tmp/report.json`
4. `enhance_json.py` reads the report and adds statistics
5. Enhanced JSON is output to stdout
6. Exit code always 0 (errors reported in JSON)

### Key Components

**runner.sh**
- Sets PYTHONPATH to include submission and app directories
- Runs pytest with `--json-report` flag
- Calls enhance_json.py to format results
- Always exits with code 0

**enhance_json.py**
- Reads pytest JSON report
- Adds `stats` section with:
  - `total_tests`: Total number of tests
  - `passed`: Number of passing tests
  - `failed`: Number of failing tests
  - `marks`: Normalized score (0-1)
  - `percentage`: Score percentage (0-100)
- Outputs valid JSON to stdout

**test_assignment.py**
- Contains all test cases
- Tests are organized into classes
- Each test validates specific requirements

## Configuration

### Docker
- Base image: `python:3.11-slim`
- Dependencies: pytest, pytest-json-report, lxml
- Platform: linux/amd64

### Testing
- Framework: pytest
- Report format: JSON
- Output capture: Enhanced JSON with statistics

## Deployment

### Building
```bash
docker buildx build --platform linux/amd64 -t {self.assignment_name.lower()}-x86:latest .
```

### Saving Image
```bash
docker save -o x86.tar {self.assignment_name.lower()}-x86:latest
```

### Running Locally
```bash
docker-compose up
```

## Deliverables
- `x86.tar`: Docker image (amd64 architecture)
- `startercode.zip`: Template for students
- `solution.zip`: Complete solution
- `docker-compose.yml`: Ready for web platform

## Response Format

### Success Response (JSON)
```json
{{
  "created": <timestamp>,
  "duration": <seconds>,
  "summary": {{
    "passed": <count>,
    "total": <count>,
    "collected": <count>
  }},
  "stats": {{
    "total_tests": <count>,
    "passed": <count>,
    "failed": <count>,
    "marks": <0-1>,
    "percentage": <0-100>
  }}
}}
```

## Notes
- All exit codes are 0 (errors reported in JSON)
- PYTHONPATH includes both submission and app directories
- Tests can access files from `/app/submission/`
- JSON output always present, even on errors
"""
        arch_path = self.base_dir / "ARCHITECTURE.md"
        arch_path.write_text(arch_doc)
        print(f"✅ Created ARCHITECTURE.md")
        
    def create_readme(self):
        """Create README.md"""
        readme_content = f"""# {self.assignment_name}

{self.description}

## Quick Start

### Build Docker Image
```bash
docker buildx build --platform linux/amd64 -t {self.assignment_name.lower()}-x86:latest .
```

### Save for Deployment
```bash
docker save -o x86.tar {self.assignment_name.lower()}-x86:latest
```

### Test Locally
```bash
docker-compose up
```

## Files
- **Dockerfile**: Container definition
- **runner.sh**: Main execution script
- **enhance_json.py**: JSON report enhancement
- **test_assignment.py**: Test cases
- **docker-compose.yml**: Compose configuration
- **startercode.zip**: Starter template
- **solution.zip**: Solution template

## Requirements
- Docker with buildx support
- Python 3.11+
- pytest, pytest-json-report, lxml

## Output
Returns JSON with test results and statistics.
"""
        readme_path = self.base_dir / "README.md"
        readme_path.write_text(readme_content)
        print(f"✅ Created README.md")
        
    def build_docker_image(self, image_name="assignment1-x86"):
        """Build Docker image for amd64 architecture"""
        print(f"\n🔨 Building Docker image for amd64...")
        cmd = f"cd {self.base_dir} && docker buildx build --platform linux/amd64 -t {image_name}:latest ."
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker image built successfully")
            return True
        else:
            print(f"❌ Build failed:\n{result.stderr}")
            return False
            
    def save_image(self, image_name="assignment1-x86"):
        """Save Docker image as x86.tar for deployment"""
        print(f"\n💾 Saving Docker image as x86.tar...")
        # First ensure image exists
        cmd_check = f"docker image inspect {image_name}:latest > /dev/null 2>&1"
        check = subprocess.run(cmd_check, shell=True)
        
        if check.returncode != 0:
            print(f"❌ Image {image_name}:latest not found")
            return False
        
        # Save the image
        cmd = f"cd {self.base_dir} && docker save -o x86.tar {image_name}:latest"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                tar_size = (self.base_dir / "x86.tar").stat().st_size / (1024*1024)
                print(f"✅ Image saved: x86.tar ({tar_size:.1f} MB)")
                return True
            except Exception as e:
                print(f"❌ Error reading tar file: {e}")
                return False
        else:
            print(f"❌ Save failed: {result.stderr}")
            return False
            
    def generate(self, build_image=False, image_name="assignment1-x86"):
        """Generate all files and optionally build Docker image with tar"""
        print(f"\n🚀 Generating {self.assignment_name}...\n")
        
        self.create_directory_structure()
        self.create_dockerfile()
        self.create_runner_sh()
        self.create_enhance_json()
        self.create_conftest()
        self.create_pytest_ini()
        self.create_docker_compose(image_name)
        self.create_test_template()
        self.create_zips()
        self.create_architecture_doc()
        self.create_readme()
        
        if build_image:
            build_success = self.build_docker_image(image_name)
            if build_success:
                self.save_image(image_name)
            else:
                print("⚠️  Skipping tar file generation due to build failure")
        
        print(f"\n✅ Assignment generation complete!")
        print(f"📁 Location: {self.base_dir}")
        print(f"\n📝 Next steps:")
        print(f"   1. Edit test_assignment.py with your test cases")
        print(f"   2. Update startercode.zip and solution.zip with actual files")
        print(f"   3. Update ARCHITECTURE.md with specific details")
        print(f"   4. Run: docker buildx build --platform linux/amd64 -t {image_name}:latest {self.base_dir}/")
        print(f"   5. Run: docker save -o {self.base_dir}/x86.tar {image_name}:latest")


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║         Assignment Generator - Template Creator            ║
║     Creates Docker-based assignments automatically         ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Get user input
    print("📋 Assignment Details:\n")
    assignment_name = input("Assignment name (e.g., 'Android XML'): ").strip()
    assignment_id = input("Assignment ID (e.g., '164'): ").strip()
    description = input("Description (e.g., 'Change text to Hi Android'): ").strip()
    
    build = input("\nBuild Docker image now? (y/n): ").strip().lower() == 'y'
    image_name = input("Image name (default: assignment-x86): ").strip() or "assignment-x86"
    
    # Generate
    gen = AssignmentGenerator(assignment_name, assignment_id, description)
    gen.generate(build_image=build, image_name=image_name)
    
    print("\n" + "="*60)
    print(f"✨ {assignment_name} is ready for deployment!")
    print("="*60)


if __name__ == "__main__":
    main()
