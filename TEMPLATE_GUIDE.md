# Assignment Template Generator - Comprehensive Guide

## Overview

The Assignment Template Generator is an automated system for creating Docker-based programming assignments with built-in testing infrastructure. It eliminates repetitive setup work and ensures consistency across all assignments.

## Why Use This Generator?

### Problems It Solves
- **Manual Repetition**: No more copying Dockerfiles, scripts, or configuration
- **Consistency**: Every assignment follows the same proven architecture
- **Time Savings**: Generate complete assignment packages in minutes
- **Reliability**: Uses tested patterns from working Assignment1
- **Scalability**: Build 10s or 100s of assignments without overhead

### What You Get
- Complete Docker setup (amd64 architecture for web platforms)
- Pytest testing framework with JSON output
- Automated test report enhancement (adds marks/percentage stats)
- Docker Compose configuration
- Starter code and solution templates
- Complete documentation
- Ready-to-deploy packages

## Installation & Setup

### Prerequisites
- Python 3.7+
- Docker with buildx support
- macOS, Linux, or WSL on Windows

### Installation
No installation required. The script is standalone:
```bash
python3 generate_assignment.py
```

## Quick Start

### 1. Run the Generator
```bash
python3 generate_assignment.py
```

### 2. Answer the Interactive Prompts
```
Assignment name (e.g., 'Android XML'): My Assignment
Assignment ID (e.g., '164'): 201
Description (e.g., 'Change text to Hi Android'): Implement sorting algorithm
Build Docker image now? (y/n): n
Image name (default: assignment-x86): my_assignment
```

### 3. Generated Structure
```
my_assignment/
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Compose configuration
├── runner.sh                  # Entry point script
├── enhance_json.py            # JSON report processor
├── conftest.py                # Pytest configuration
├── pytest.ini                 # Pytest settings
├── test_assignment.py         # TEST CASES (edit this!)
├── startercode.zip            # Starter template (edit this!)
├── solution.zip               # Solution template (edit this!)
├── README.md                  # Quick reference
├── ARCHITECTURE.md            # System documentation
└── src/                       # Student submissions go here
```

### 4. Customize Your Assignment

#### Edit test_assignment.py
```python
import pytest

class TestMyAssignment:
    def test_basic_functionality(self):
        # Your test here
        assert True
    
    def test_edge_case(self):
        # Test edge cases
        assert True
```

#### Update Zip Files
Replace starter and solution zips with actual content:
```bash
# Create startercode.zip with template files
zip startercode.zip starter_file.py

# Create solution.zip with complete solution
zip solution.zip solution_file.py
```

### 5. Build Docker Image
```bash
cd my_assignment
docker buildx build --platform linux/amd64 -t my_assignment-x86:latest .
```

### 6. Test Locally
```bash
docker-compose up
```

### 7. Save for Deployment
```bash
docker save -o x86.tar my_assignment-x86:latest
```

## Architecture & Components

### File Purposes

#### Dockerfile
- Base image: `python:3.11-slim`
- Installs: pytest, pytest-json-report, lxml
- Copies: test files, runner script, enhancement script
- Platform: linux/amd64
- Working directory: /app

#### runner.sh
```bash
#!/bin/bash
set +e  # Don't exit on errors
export PYTHONPATH=/app/submission:/app:$PYTHONPATH
pytest /app/test_assignment.py --json-report --json-report-file=/tmp/report.json -v
python3 /app/enhance_json.py /tmp/report.json
exit 0  # ALWAYS exit 0
```

**Key Design Decisions:**
- `set +e`: Ignore errors so script continues
- Export PYTHONPATH: Makes student code importable
- JSON output: Machine-readable results
- Always exit 0: Errors reported in JSON, not via exit codes

#### enhance_json.py
```python
# Reads /tmp/report.json from pytest
# Adds 'stats' section:
{
    "stats": {
        "total_tests": 10,
        "passed": 9,
        "failed": 1,
        "marks": 0.9,      # passed/total
        "percentage": 90.0  # marks * 100
    }
}
# Always outputs valid JSON
# Always exits 0
```

#### conftest.py
```python
# Pytest configuration
# Adds /app/submission to sys.path
# Allows imports from student submission
import sys
sys.path.insert(0, '/app/submission')
```

#### test_assignment.py
Your test suite goes here. Uses standard pytest:
```python
def test_something():
    assert expected == actual

class TestGroup:
    def test_grouped_test(self):
        assert True
```

#### docker-compose.yml
- Service name: `judge`
- Image: Your assignment image
- Volumes: `./src:/app/submission:ro` (read-only)
- Platform: `linux/amd64`
- Resources: 1 CPU max, 512M RAM max
- stdin/tty: enabled for interactive output

## Testing & Validation

### Local Testing Workflow

1. **Create test submission**:
   ```bash
   mkdir -p my_assignment/src
   cp my_solution.py my_assignment/src/
   ```

2. **Run tests**:
   ```bash
   cd my_assignment
   docker-compose up
   ```

3. **Check output**:
   - Verify JSON is printed
   - Check `stats` section exists
   - Verify marks/percentage are correct
   - Confirm exit code is 0

### Expected JSON Output
```json
{
  "created": "2024-01-15T10:30:45Z",
  "duration": 0.456,
  "summary": {
    "passed": 10,
    "failed": 0,
    "total": 10,
    "collected": 10
  },
  "stats": {
    "total_tests": 10,
    "passed": 10,
    "failed": 0,
    "marks": 1.0,
    "percentage": 100.0
  }
}
```

## Advanced Configuration

### Custom Base Image
Edit the Dockerfile:
```dockerfile
FROM node:18-slim  # Change base image
RUN npm install    # Install Node packages instead
```

### Custom Dependencies
```dockerfile
RUN pip install requests pandas numpy  # Add more Python packages
```

### Custom Python Version
```dockerfile
FROM python:3.10-slim  # or 3.9, 3.12, etc.
```

### Different Test Framework
Edit conftest.py and test_assignment.py to use unittest, nose, etc.

## Troubleshooting

### Image Won't Build
**Problem**: `docker buildx build` fails
**Solution**:
- Verify Docker is running: `docker ps`
- Install buildx: `docker buildx create --name mybuilder && docker buildx use mybuilder`
- Check Dockerfile syntax
- Check Python version availability

### Tests Don't Run
**Problem**: No test output, JSON shows `failed: 1`
**Solution**:
- Check test_assignment.py syntax: `python3 test_assignment.py`
- Verify pytest installed: `pip list | grep pytest`
- Check imports work: try importing in Python shell

### Wrong Architecture
**Problem**: Image built for arm64 instead of amd64
**Solution**:
```bash
# CORRECT: Always use platform flag
docker buildx build --platform linux/amd64 -t image:latest .

# WRONG: Don't use docker build
docker build -t image:latest .

# Verify:
docker image inspect image:latest | grep Architecture
```

### Exit Code Not 0
**Problem**: Exit code is 1 or 127
**Solution**:
- Check that both runner.sh and enhance_json.py have `exit 0`
- Verify runner.sh is executable: `chmod +x runner.sh`
- Check PYTHONPATH is exported before running tests

### No JSON Output
**Problem**: Docker runs but no JSON output
**Solution**:
- Verify pytest generates JSON: run pytest manually
- Check /tmp/report.json exists in running container
- Verify enhance_json.py is reading the correct path
- Check enhance_json.py has read permissions

## Performance & Optimization

### Build Time
- First build: 2-3 minutes (downloads base image)
- Subsequent builds: 10-30 seconds (uses cache)
- Clean build: `docker system prune`

### Runtime
- Small test suites: < 1 second
- Large suites (100+ tests): 5-10 seconds
- Memory limit: 512M (configurable in docker-compose.yml)

### Image Size
- Base python:3.11-slim: ~150MB
- With dependencies: ~200MB
- After save: ~100MB (compressed)

## Security Considerations

### Docker Compose Settings
```yaml
security_opt:
  - no-new-privileges:true  # Prevent privilege escalation
cap_drop:
  - ALL                      # Drop all capabilities
tmpfs:
  - /tmp:rw,noexec,nosuid    # Tmpfs without execution
volumes:
  - ./src:/app/submission:ro # Read-only submission
```

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '1'              # Max 1 CPU
      memory: 512M           # Max 512MB RAM
```

## Deployment Pipeline

### Step-by-Step Deployment

1. **Generate**: `python3 generate_assignment.py`
2. **Customize**: Edit test_assignment.py, update zips
3. **Build**: `docker buildx build --platform linux/amd64 ...`
4. **Test**: `docker-compose up` with test submissions
5. **Save**: `docker save -o x86.tar assignment-x86:latest`
6. **Deploy**: Send x86.tar + docker-compose.yml to platform
7. **Load**: `docker load -i x86.tar` on deployment server
8. **Run**: `docker-compose up` with student submission

### Deployment Checklist
- ✓ Image built with `--platform linux/amd64`
- ✓ docker-compose.yml uses correct image name
- ✓ x86.tar file is present (~100-200MB)
- ✓ Test files included in image
- ✓ stdin_open: true in docker-compose.yml
- ✓ tty: true in docker-compose.yml
- ✓ JSON output confirmed locally
- ✓ Exit code always 0

## Examples

### Example 1: Android XML Assignment
```
Name: Android XML
ID: 164
Description: Modify activity_main.xml to change greeting text to "Hi Android"

Test cases:
- Verify XML parses correctly
- Check for LinearLayout root
- Verify TextView exists
- Check text content matches "Hi Android"
```

### Example 2: Python Functions
```
Name: Python Functions
ID: 165
Description: Implement sorting and searching functions

Test cases:
- Test sort function with various inputs
- Test search function edge cases
- Verify performance requirements
- Check output format
```

### Example 3: Web Development
```
Name: Web Development
ID: 166
Description: Create responsive web page with CSS Grid

Test cases:
- Verify HTML structure
- Check CSS Grid layout
- Test responsiveness breakpoints
- Validate accessibility
```

## FAQ

**Q: Can I use a different testing framework?**
A: Yes, edit conftest.py and test_assignment.py to use unittest, nose, doctest, etc.

**Q: Can I use a different language?**
A: Yes, change Dockerfile base image to appropriate language (node, go, rust, etc.)

**Q: How do I get exit code 1?**
A: You shouldn't - the system always returns 0. Errors are in JSON stats.

**Q: Can I test locally without Docker?**
A: Yes, run tests directly with Python:
```bash
export PYTHONPATH=/path/to/submission:$PYTHONPATH
pytest test_assignment.py
```

**Q: How often should I rebuild the image?**
A: Every time you modify test_assignment.py, Dockerfile, or dependencies.

**Q: Can I use external APIs?**
A: Yes, add to dependencies in Dockerfile: `RUN pip install requests ...`

**Q: How do I update existing assignments?**
A: Edit files in the assignment folder and rebuild:
```bash
docker buildx build --platform linux/amd64 -t image:latest .
docker save -o x86.tar image:latest
```

## Best Practices

1. **Always use `--platform linux/amd64`** when building
2. **Keep test_assignment.py organized** into logical test classes
3. **Use meaningful test names** (test_parsing, test_validation, etc.)
4. **Test edge cases** (empty input, large input, invalid input)
5. **Document expected behavior** in test docstrings
6. **Keep dependencies minimal** to reduce image size
7. **Use read-only volumes** for submissions (`./src:/app/submission:ro`)
8. **Always verify locally** before deployment
9. **Version your images** (use tags like `v1.0`, `v1.1`)
10. **Keep configuration in docker-compose.yml** not in Dockerfile

## Support & Troubleshooting

### Check System Requirements
```bash
docker --version          # Should be recent
docker buildx version     # Should exist
python3 --version         # Should be 3.7+
```

### Test Docker Setup
```bash
docker buildx create --name testbuilder
docker buildx use testbuilder
docker buildx build --platform linux/amd64 --help
```

### Validate Assignment Structure
```bash
# Check all required files exist
ls -la my_assignment/
# Should show: Dockerfile, runner.sh, test_assignment.py, etc.

# Check file permissions
stat my_assignment/runner.sh
# Should show -rwxr-xr-x (executable)
```

## Contributing Improvements

If you find issues or improvements:
1. Document the problem clearly
2. Test the solution locally
3. Create a new assignment template with the fix
4. Share feedback for continuous improvement

## Version History

- **v1.0** (2024): Initial release with Python 3.11-slim, pytest, amd64 support
- Uses proven Assignment1 architecture
- 100% JSON output reliability
- Exit code 0 guaranteed

