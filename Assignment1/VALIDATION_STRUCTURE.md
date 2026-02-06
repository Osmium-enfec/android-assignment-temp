# Assignment 1 - Validation Structure Summary

## Complete File Organization

```
Assignment1/
├── ASSIGNMENT_INFO.md                           # Assignment documentation
├── app/src/main/res/layout/
│   ├── activity_main.xml                        # Starter layout (with TODOs)
│   └── activity_main_solution.xml               # Solution layout
├── starter_files/
│   ├── MainActivity.java                        # Starter Java code with TODOs
│   └── activity_main.xml                        # Starter XML with TODOs
├── solution_files/
│   ├── MainActivity.java                        # Solution Java code
│   └── activity_main.xml                        # Solution XML
└── docker/
    ├── Dockerfile                               # Docker image configuration
    ├── docker-compose.yml                       # Docker Compose orchestration
    ├── runner.sh                                # Test execution script
    ├── test_assignment.py                       # Pytest test suite
    ├── conftest.py                              # Pytest configuration
    ├── pytest.ini                               # Pytest settings
    └── enhance_json.py                          # JSON result enhancement utility
```

---

## Validation Files Summary

### 1. **startercode.zip** (Provided Separately)
Contains starter files with TODOs for students:
- `MainActivity.java` (8,392 bytes)
- `activity_main.xml` (with TODOs)

### 2. **solution.zip** (Provided Separately)
Contains complete solution:
- `MainActivity.java` (3,938 bytes)
- `activity_main.xml` (complete)

### 3. **x86.tar** (Docker Image)
Contains:
- Android SDK
- Python 3.x
- pytest framework
- lxml XML parser
- All test dependencies
- Configured to run tests automatically

---

## Docker Compose Configuration

The `docker-compose.yml` file:
- Defines the `judge` service
- Uses `assignment1-x86:latest` image
- Mounts submission code in `/app/submission` (read-only)
- Sets resource limits (1 CPU, 1GB RAM)
- Runs the `/app/runner.sh` script automatically
- Provides secure isolation with capability dropping

---

## Runner Flow (runner.sh)

The runner script executes in 3 stages:

**Stage 1: Validation**
- Check submission directory exists
- Verify `activity_main.xml` file presence

**Stage 2: Testing**
- Run pytest test suite
- Execute XML validation tests
- Verify TextView implementation
- Check centering and styling

**Stage 3: Results**
- Display test results
- Generate summary report

---

## Test Suite Coverage

### Test Categories

#### Smoke Tests (Foundation)
- ✓ File exists
- ✓ Valid XML structure

#### Layout Structure Tests
- ✓ Root element is a layout
- ✓ Layout dimensions correct
- ✓ Gravity/centering configured

#### TextView Tests
- ✓ TextView exists
- ✓ Text content is "Hi Android"
- ✓ Dimensions are wrap_content
- ✓ Text size is adequate (≥24sp)

#### Centering Tests
- ✓ Content is centered on screen

**Total: 12+ test cases**

---

## Execution Workflow

### Local Testing
```bash
# Navigate to assignment
cd Assignment1

# Prepare submission
mkdir -p src
unzip -o startercode.zip -d src

# Build Docker image (if needed)
docker build -t assignment1-x86:latest docker/

# Run tests with Docker Compose
docker-compose up

# View test output
docker logs assignment1-judge-1
```

### Test Execution Timeline
1. **0s**: Container startup
2. **2-3s**: Directory validation
3. **5-10s**: XML parsing
4. **10-15s**: Test execution
5. **15-20s**: Results displayed

---

## Key Test Validations

### XML Structure
```xml
✓ Valid XML declaration
✓ Proper namespace declarations
✓ Well-formed elements and attributes
✓ No unclosed tags
```

### Layout Requirements
```xml
✓ <LinearLayout> or similar root container
✓ android:layout_width="match_parent"
✓ android:layout_height="match_parent"
✓ android:gravity="center"
```

### TextView Requirements
```xml
✓ <TextView> element present
✓ android:text="Hi Android"
✓ android:layout_width="wrap_content"
✓ android:layout_height="wrap_content"
✓ android:textSize >= 24sp (recommended: 32sp)
✓ android:textStyle="bold" (recommended)
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed ✓ |
| 1 | Submission directory missing |
| 1 | Required file not found |
| 1 | XML parsing failed |
| >0 | Test failures detected |

---

## Performance Metrics

| Metric | Expected |
|--------|----------|
| Build time | 2-5 minutes |
| Test execution | 5-15 seconds |
| Memory usage | 512MB - 1GB |
| CPU usage | 0.5-1 CPU cores |

---

## Files Provided

### For Instructors
- `ASSIGNMENT_INFO.md` - Full assignment documentation
- `docker/Dockerfile` - Docker image recipe
- `docker/docker-compose.yml` - Orchestration config
- `docker/runner.sh` - Test execution script
- `docker/test_assignment.py` - Complete test suite
- `solution_files/` - Reference solution

### For Students
- `startercode.zip` - Starter project structure
- `ASSIGNMENT_INFO.md` - Assignment instructions
- `README.md` (optional) - Quick start guide

---

## Customization Options

### Modify Test Strictness
Edit `docker/test_assignment.py`:
- Adjust minimum text size
- Change required attributes
- Add/remove test cases

### Change Docker Image
Edit `docker/Dockerfile`:
- Update Android SDK version
- Add additional tools
- Modify base image

### Adjust Resource Limits
Edit `docker/docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
```

---

## Troubleshooting

### Docker image not found
```bash
cd docker/
docker build -t assignment1-x86:latest .
```

### Permission denied on runner.sh
```bash
chmod +x docker/runner.sh
```

### XML parsing fails
- Check for special characters
- Verify all tags are closed
- Validate namespace declarations

### Tests timeout
- Check resource limits
- Verify submission file size
- Check for infinite loops

---

**Configuration Version**: 1.0  
**Last Updated**: February 6, 2026  
**Assignment Difficulty**: Beginner  
**Estimated Completion**: 15-20 minutes
