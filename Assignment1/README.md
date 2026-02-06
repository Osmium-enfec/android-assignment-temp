# Assignment 1: Hello Android - Complete Setup

## Quick Start

### For Students

1. **Download Starter Code**
   - Extract `startercode.zip`
   - Open the project in Android Studio
   - Navigate to `app/src/main/res/layout/activity_main.xml`

2. **Complete the Task**
   - Follow the TODOs in the layout file
   - Add a TextView with text "Hi Android"
   - Center the text on the screen
   - Use appropriate styling

3. **Test Your Solution**
   - Package your solution as `solution.zip`
   - Submit to the platform
   - View automated test results

### For Instructors

1. **Build Docker Image**
   ```bash
   cd Assignment1/docker
   docker build -t assignment1-x86:latest .
   ```

2. **Run Tests**
   ```bash
   cd Assignment1
   docker-compose up
   ```

3. **View Results**
   - Check container logs
   - Review test output
   - Analyze student submissions

---

## Assignment Structure

### Main Files

| File | Purpose |
|------|---------|
| `ASSIGNMENT_INFO.md` | Complete assignment documentation |
| `VALIDATION_STRUCTURE.md` | Test and validation setup guide |
| `app/src/main/res/layout/activity_main.xml` | Original starter layout |
| `starter_files/` | Starter code files |
| `solution_files/` | Reference solution |
| `docker/` | Docker configuration and tests |

### Docker Components

| Component | File | Purpose |
|-----------|------|---------|
| Image | `Dockerfile` | Docker image recipe |
| Orchestration | `docker-compose.yml` | Container setup |
| Tests | `test_assignment.py` | Pytest test suite |
| Runner | `runner.sh` | Test execution script |
| Config | `pytest.ini` | Test configuration |

---

## Key Features

### ✓ Comprehensive Testing
- 12+ test cases covering all requirements
- Smoke tests for basic validation
- Structure tests for layout correctness
- Content tests for TextView implementation
- Style tests for formatting

### ✓ Automatic Evaluation
- Docker-based isolated environment
- Secure sandboxing
- Resource limitations
- Automated test execution
- Structured result reporting

### ✓ Clear Documentation
- Detailed assignment instructions
- Example code and explanations
- Troubleshooting guide
- Learning objectives
- Resource references

### ✓ Flexible Customization
- Modifiable test suite
- Configurable Docker image
- Adjustable resource limits
- Extensible test framework

---

## Assignment Content

### Learning Objectives
Students will learn:
1. Android Activity lifecycle basics
2. XML layout file creation
3. LinearLayout configuration
4. TextView widget usage
5. View positioning and centering
6. Android resource system

### Requirements
Create an XML layout that:
- Uses LinearLayout as root container
- Contains a centered TextView
- Displays text "Hi Android"
- Uses appropriate text styling
- Maintains proper view dimensions

### Test Coverage
All requirements are validated by:
- XML structure tests
- Layout centering tests
- TextView content tests
- Text styling tests
- Dimension validation

---

## File Deliverables

### startercode.zip
Contains:
- `MainActivity.java` (with TODOs)
- `activity_main.xml` (with TODOs)
- Project structure
- Required configuration files

**Size**: ~8KB (extracted)

### solution.zip
Contains:
- Complete `MainActivity.java`
- Complete `activity_main.xml`
- All required elements properly configured

**Size**: ~4KB

### x86.tar
Docker image containing:
- Android SDK 30+
- Python 3.x runtime
- pytest framework
- XML validation tools
- All dependencies pre-installed

**Size**: ~2-3GB (compressed)

---

## Testing Workflow

### Test Execution Steps

```
1. Container Startup (1-2s)
   ↓
2. File Validation (1s)
   ├─ Check /app/submission exists
   └─ Verify activity_main.xml present
   ↓
3. XML Parsing (1-2s)
   ├─ Load XML file
   └─ Parse with lxml
   ↓
4. Pytest Execution (5-10s)
   ├─ Run smoke tests
   ├─ Run structure tests
   ├─ Run content tests
   ├─ Run styling tests
   └─ Generate report
   ↓
5. Results Output (1-2s)
   ├─ Summary statistics
   ├─ Pass/fail details
   └─ Exit code return
```

### Test Results Example

```
================================
Assignment 1 - Runner Script
================================

[1/3] Validating submission structure...
✓ activity_main.xml found

[2/3] Running XML validation tests...
test_file_exists PASSED
test_file_is_valid_xml PASSED
test_has_root_layout PASSED
test_layout_has_match_parent_dimensions PASSED
test_has_textview PASSED
test_textview_displays_hi_android PASSED
test_textview_has_wrap_content_dimensions PASSED
test_textview_has_adequate_text_size PASSED
test_layout_is_centered PASSED

[3/3] Test execution completed

================================
All checks passed!
================================
```

---

## Commands Reference

### Build Docker Image
```bash
cd Assignment1/docker
docker build -t assignment1-x86:latest .
```

### Run with Docker Compose
```bash
cd Assignment1
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Run Tests Directly
```bash
cd Assignment1/docker
python3 -m pytest test_assignment.py -v
```

### Validate XML
```bash
python3 -m lxml activity_main.xml
```

---

## Troubleshooting

### Issue: Docker image not found
**Solution**: Build the image first
```bash
cd Assignment1/docker && docker build -t assignment1-x86:latest .
```

### Issue: Permission denied on runner.sh
**Solution**: Make script executable
```bash
chmod +x Assignment1/docker/runner.sh
```

### Issue: XML parsing error
**Solution**: Check for:
- Unclosed tags
- Missing namespace declarations
- Invalid characters
- Proper XML structure

### Issue: Tests timeout
**Solution**:
- Check resource availability
- Verify submission file integrity
- Check for infinite loops in code

### Issue: All tests pass locally, fail in Docker
**Solution**:
- Verify exact file paths match
- Check file permissions
- Validate XML against strict schema
- Test in Docker container directly

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Test Cases | 12+ |
| Smoke Tests | 2 |
| Structure Tests | 3 |
| Content Tests | 4 |
| Styling Tests | 3+ |
| Expected Pass Rate | ~95% for correct implementations |
| Execution Time | 10-20 seconds |
| Memory Usage | ~512MB |

---

## Additional Resources

### Official Documentation
- [Android Developers Guide](https://developer.android.com/guide)
- [Android Layout Documentation](https://developer.android.com/guide/topics/ui/declaring-layout)
- [TextView API Reference](https://developer.android.com/reference/android/widget/TextView)

### Tools
- [Android Studio](https://developer.android.com/studio)
- [Android Emulator](https://developer.android.com/studio/run/emulator)
- [XML Validator](https://www.xmlvalidation.com/)

### Learning
- [Android Fundamentals Course](https://developer.android.com/courses)
- [Kotlin for Android](https://developer.android.com/kotlin)
- [Material Design Guide](https://material.io/design)

---

## Support

### For Students
- Review `ASSIGNMENT_INFO.md` for detailed instructions
- Check `VALIDATION_STRUCTURE.md` for test details
- Examine `solution_files/` for reference implementation

### For Instructors
- Customize tests in `docker/test_assignment.py`
- Modify Docker image in `docker/Dockerfile`
- Adjust resource limits in `docker/docker-compose.yml`

---

**Assignment Version**: 1.0  
**Platform**: Android (API Level 30+)  
**Difficulty**: Beginner  
**Estimated Time**: 15-20 minutes  
**Prerequisites**: Basic XML knowledge, Android Studio  

---

**Last Updated**: February 6, 2026  
**Created for**: Assignment Android Course  
**Status**: Ready for Distribution
