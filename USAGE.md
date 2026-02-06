# Assignment Generator - Usage Examples

## Interactive Usage

### Example 1: Run Script with Interactive Prompts
```bash
$ python3 generate_assignment.py

╔════════════════════════════════════════════════════════════╗
║         Assignment Generator - Template Creator            ║
║     Creates Docker-based assignments automatically         ║
╚════════════════════════════════════════════════════════════╝

📋 Assignment Details:

Assignment name (e.g., 'Android XML'): Data Structures
Assignment ID (e.g., '164'): 201
Description (e.g., 'Change text to Hi Android'): Implement binary tree traversal algorithms
Build Docker image now? (y/n): y
Image name (default: assignment-x86): data_structures-x86

🚀 Generating Data Structures...

✅ Created directory: data_structures
✅ Created Dockerfile
✅ Created runner.sh
✅ Created enhance_json.py
✅ Created conftest.py
✅ Created pytest.ini
✅ Created docker-compose.yml
✅ Created test_assignment.py (template)
✅ Created startercode.zip and solution.zip
✅ Created ARCHITECTURE.md
✅ Created README.md

🔨 Building Docker image for amd64...
✅ Docker image built successfully

💾 Saving Docker image...
✅ Image saved: x86.tar (186.5 MB)

✅ Assignment generation complete!
📁 Location: data_structures

📝 Next steps:
   1. Edit test_assignment.py with your test cases
   2. Update startercode.zip and solution.zip with actual files
   3. Update ARCHITECTURE.md with specific details
   4. Run: docker buildx build --platform linux/amd64 -t data_structures-x86:latest data_structures/
   5. Run: docker save -o data_structures/x86.tar data_structures-x86:latest

============================================================
✨ Data Structures is ready for deployment!
============================================================
```

## Generated File Contents

### Generated test_assignment.py (Template)
```python
import pytest
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
```

**After Customization:**
```python
import pytest
from solution import BinaryTree, TreeNode

class TestBinaryTree:
    def test_create_empty_tree(self):
        """Test creating an empty tree"""
        tree = BinaryTree()
        assert tree.root is None
    
    def test_insert_single_node(self):
        """Test inserting single node"""
        tree = BinaryTree()
        tree.insert(10)
        assert tree.root.value == 10
    
    def test_inorder_traversal(self):
        """Test inorder traversal: left, root, right"""
        tree = BinaryTree()
        for val in [5, 3, 7, 2, 4, 6, 8]:
            tree.insert(val)
        result = tree.inorder()
        assert result == [2, 3, 4, 5, 6, 7, 8]
    
    def test_preorder_traversal(self):
        """Test preorder traversal: root, left, right"""
        tree = BinaryTree()
        for val in [5, 3, 7, 2, 4, 6, 8]:
            tree.insert(val)
        result = tree.preorder()
        assert result == [5, 3, 2, 4, 7, 6, 8]
    
    def test_postorder_traversal(self):
        """Test postorder traversal: left, right, root"""
        tree = BinaryTree()
        for val in [5, 3, 7, 2, 4, 6, 8]:
            tree.insert(val)
        result = tree.postorder()
        assert result == [2, 4, 3, 6, 8, 7, 5]

    def test_tree_height(self):
        """Test tree height calculation"""
        tree = BinaryTree()
        assert tree.height() == 0
        tree.insert(5)
        assert tree.height() == 1
        for val in [3, 7, 2, 4]:
            tree.insert(val)
        assert tree.height() == 3
```

## Workflow Examples

### Complete Android XML Assignment

#### Step 1: Generate
```bash
python3 generate_assignment.py
# Provide: "Android XML", "164", "Create centered TextView with 'Hi Android'"
# Choose: Build image now? y
# Results: android_xml/ folder with all files
```

#### Step 2: Edit test_assignment.py
```python
import pytest
import xml.etree.ElementTree as ET
from pathlib import Path

class TestAndroidXML:
    def test_xml_file_exists(self):
        """Test that main.xml exists"""
        xml_file = Path("/app/submission/activity_main.xml")
        assert xml_file.exists()
    
    def test_xml_is_valid(self):
        """Test that XML is well-formed"""
        tree = ET.parse("/app/submission/activity_main.xml")
        assert tree.getroot() is not None
    
    def test_has_linearlayout_root(self):
        """Test root is LinearLayout"""
        root = ET.parse("/app/submission/activity_main.xml").getroot()
        assert "LinearLayout" in root.tag
    
    def test_is_centered(self):
        """Test layout is centered"""
        root = ET.parse("/app/submission/activity_main.xml").getroot()
        assert root.get("{http://schemas.android.com/apk/res/android}gravity") == "center"
    
    def test_has_textview(self):
        """Test TextView exists"""
        root = ET.parse("/app/submission/activity_main.xml").getroot()
        textviews = root.findall(".//{http://schemas.android.com/apk/res/android}TextView")
        assert len(textviews) > 0
    
    def test_textview_text_is_correct(self):
        """Test TextView contains 'Hi Android'"""
        root = ET.parse("/app/submission/activity_main.xml").getroot()
        textviews = root.findall(".//{http://schemas.android.com/apk/res/android}TextView")
        assert any("Hi Android" in tv.get("{http://schemas.android.com/apk/res/android}text", "")
                   for tv in textviews)
```

#### Step 3: Create Zips
```bash
# Create starter code
mkdir -p temp_starter
cat > temp_starter/activity_main.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World" />
</LinearLayout>
EOF
zip android_xml/startercode.zip temp_starter/activity_main.xml

# Create solution
mkdir -p temp_solution
cat > temp_solution/activity_main.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hi Android" />
</LinearLayout>
EOF
zip android_xml/solution.zip temp_solution/activity_main.xml
```

#### Step 4: Build & Test
```bash
cd android_xml

# Build image
docker buildx build --platform linux/amd64 -t android_xml-x86:latest .

# Create test submission
mkdir -p src
cp <student_submission>/activity_main.xml src/

# Test locally
docker-compose up
# Expected output: JSON with stats showing 6/6 tests passed (marks: 1.0, percentage: 100.0)
```

#### Step 5: Deploy
```bash
# Save image
docker save -o x86.tar android_xml-x86:latest

# Send to platform
# - x86.tar (image)
# - docker-compose.yml (configuration)
```

### Python Algorithm Assignment

#### Generate
```bash
python3 generate_assignment.py
# Input: "Sorting Algorithms", "202", "Implement quicksort with specific requirements"
# Build: y
```

#### Custom Test File
```python
import pytest
from solution import quicksort

class TestQuicksort:
    def test_empty_list(self):
        assert quicksort([]) == []
    
    def test_single_element(self):
        assert quicksort([5]) == [5]
    
    def test_already_sorted(self):
        assert quicksort([1,2,3,4,5]) == [1,2,3,4,5]
    
    def test_reverse_sorted(self):
        assert quicksort([5,4,3,2,1]) == [1,2,3,4,5]
    
    def test_random_order(self):
        assert quicksort([3,1,4,1,5,9,2,6]) == [1,1,2,3,4,5,6,9]
    
    def test_with_duplicates(self):
        assert quicksort([5,2,8,2,9,1,5,5]) == [1,2,2,5,5,5,8,9]
    
    def test_large_list(self):
        import random
        data = list(range(1000))
        random.shuffle(data)
        result = quicksort(data)
        assert result == sorted(data)
    
    def test_in_place_behavior(self):
        """Verify if implementation modifies original"""
        data = [3,1,4,1,5]
        result = quicksort(data)
        # Depending on specification: either data is modified or not
        assert result is not None

class TestPerformance:
    def test_reasonable_performance(self):
        """Test completes in reasonable time"""
        import time
        data = list(range(1000, 0, -1))  # Worst case: reverse order
        start = time.time()
        quicksort(data)
        elapsed = time.time() - start
        assert elapsed < 1.0  # Should complete within 1 second
```

#### Zip Contents
```bash
# startercode.zip contains template with function signature
"""
def quicksort(arr):
    '''
    Sorts array using quicksort algorithm
    Args:
        arr: List of comparable elements
    Returns:
        Sorted list
    '''
    pass

if __name__ == "__main__":
    print(quicksort([3,1,4,1,5,9,2,6]))
"""

# solution.zip contains complete implementation
"""
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""
```

## Verification & Quality Checks

### Test Your Generated Assignment

```bash
#!/bin/bash
# Verification script

ASSIGNMENT=$1

echo "Verifying $ASSIGNMENT..."

# Check files exist
files=("Dockerfile" "runner.sh" "enhance_json.py" "conftest.py" "pytest.ini" "test_assignment.py" "docker-compose.yml")
for f in "${files[@]}"; do
    if [ ! -f "$ASSIGNMENT/$f" ]; then
        echo "❌ Missing: $f"
        exit 1
    fi
    echo "✅ Found: $f"
done

# Check directories
if [ ! -d "$ASSIGNMENT/src" ]; then
    echo "❌ Missing: src/ directory"
    exit 1
fi
echo "✅ Found: src/ directory"

# Check file permissions
if [ ! -x "$ASSIGNMENT/runner.sh" ]; then
    echo "❌ runner.sh is not executable"
    exit 1
fi
echo "✅ runner.sh is executable"

# Check Docker syntax
if ! docker build --dry-run "$ASSIGNMENT" > /dev/null 2>&1; then
    echo "❌ Dockerfile has syntax errors"
    exit 1
fi
echo "✅ Dockerfile syntax valid"

echo "✅ All checks passed!"
```

Usage:
```bash
bash verify_assignment.sh data_structures
```

## Command Reference

### Generate Assignment (Interactive)
```bash
python3 generate_assignment.py
```

### Build Docker Image
```bash
docker buildx build --platform linux/amd64 -t assignment-x86:latest .
```

### Test Locally
```bash
docker-compose up
```

### Save Image
```bash
docker save -o x86.tar assignment-x86:latest
```

### Load Image
```bash
docker load -i x86.tar
```

### Run Manual Test
```bash
docker run -v ./src:/app/submission:ro assignment-x86:latest
```

### View Image Details
```bash
docker image inspect assignment-x86:latest
```

### Clean Up
```bash
docker image rm assignment-x86:latest
docker system prune -a
```

