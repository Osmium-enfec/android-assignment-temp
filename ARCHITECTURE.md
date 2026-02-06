# Assignment Template Guide

This guide explains how to create assignments using the JSON configuration system.

---

## Overview

The assignment generator creates all necessary files from a single JSON configuration file:
- Starter code (with TODOs)
- Solution code
- Test files
- Docker image for automated testing
- Documentation

---

## JSON Configuration Structure

### Basic Template

```json
{
    "assignment_number": 1,
    "title": "Episode 1 - Assignment 1: Your Topic Here",
    "topics": [
        "Topic 1",
        "Topic 2",
        "Topic 3"
    ],
    "functions": [
        {
            "name": "function_name",
            "description": "What this function does",
            "params": "param1, param2",
            "args": [
                {"name": "param1", "type": "str", "desc": "Description of param1"},
                {"name": "param2", "type": "int", "desc": "Description of param2"}
            ],
            "returns": "str: What the function returns",
            "example": "function_name('hello', 5) -> 'result'",
            "solution": "return param1 * param2",
            "test_call": "function_name('hello', 5)",
            "expected": "'result'",
            "tests": [
                {"name": "test_case1", "input": "'hello', 5", "expected": "'result'"},
                {"name": "test_case2", "input": "'a', 3", "expected": "'aaa'"}
            ]
        }
    ]
}
```

---

## Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `assignment_number` | Yes | Integer (e.g., 1, 2, 3). Used for folder name `Assignment{N}` and image name `assignment{N}-x86` |
| `title` | Yes | Full title shown in documentation |
| `topics` | Yes | Array of topic strings covered in assignment |
| `functions` | Yes | Array of function definitions |

### Function Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Function name (snake_case) |
| `description` | Yes | Brief description of function purpose |
| `params` | Yes | Parameter list as string (e.g., `"a, b, c"`) |
| `args` | No | Array of argument details for docstring |
| `returns` | No | Return type and description |
| `example` | No | Example usage shown in docs |
| `solution` | Yes | The actual implementation code |
| `test_call` | Yes | Example call for main block |
| `expected` | Yes | Expected result for documentation |
| `tests` | Yes | Array of test cases |

### Test Case Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Test method name (e.g., `test_positive`) |
| `input` | Yes | Input arguments as string |
| `expected` | Yes | Expected output |

---

## Usage

```bash
cd /Users/enfec/Desktop/Assignment_Python
python3 generate_assignment.py your_config.json
```

This generates:
```
Assignment{N}/
├── assignment.py      # Starter code with TODOs
├── solution.py        # Complete solution
├── startercode.zip    # For distribution
├── solution.zip       # For testing
├── x86.tar           # Docker image
├── ASSIGNMENT_INFO.md # Documentation
└── x86/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── test_assignment.py
    ├── conftest.py
    ├── pytest.ini
    ├── runner.sh
    └── enhance_json.py
```

---

## Testing

```bash
cd Assignment{N}
rm -rf src && mkdir -p src && unzip -o solution.zip -d src
docker run --rm --platform linux/amd64 \
  -v "$(pwd)/src:/app/submission:ro" \
  assignment{N}-x86:latest /app/runner.sh
```

---

# Adapting for XML Assignments

To create XML assignments, you'll need a **separate generator** since the current one is Python-specific. Here's what you need:

## XML Assignment Structure

For XML assignments, you would typically test:
- XML syntax validity
- Schema validation (XSD)
- XPath queries
- XSLT transformations

## Recommended XML Config Template

```json
{
    "assignment_number": 1,
    "title": "XML Assignment 1: Basic XML Structure",
    "language": "xml",
    "topics": [
        "XML declaration",
        "Elements and attributes",
        "Nesting and hierarchy",
        "Well-formed XML rules"
    ],
    "tasks": [
        {
            "name": "task1_catalog",
            "description": "Create a catalog XML with at least 3 books",
            "requirements": [
                "Root element must be <catalog>",
                "Each book must have <title>, <author>, <price> elements",
                "Each book must have an 'id' attribute"
            ],
            "starter_template": "<?xml version=\"1.0\"?>\n<catalog>\n  <!-- Add your books here -->\n</catalog>",
            "validation": {
                "type": "xpath",
                "checks": [
                    {"xpath": "/catalog", "expected": "exists"},
                    {"xpath": "count(/catalog/book)", "expected": ">=3"},
                    {"xpath": "/catalog/book/@id", "expected": "exists"},
                    {"xpath": "/catalog/book/title", "expected": "exists"},
                    {"xpath": "/catalog/book/author", "expected": "exists"},
                    {"xpath": "/catalog/book/price", "expected": "exists"}
                ]
            }
        },
        {
            "name": "task2_schema",
            "description": "Create XML that validates against provided XSD schema",
            "schema_file": "books.xsd",
            "validation": {
                "type": "xsd",
                "schema": "books.xsd"
            }
        }
    ]
}
```

## XML Validation Types

| Type | Description | Tools |
|------|-------------|-------|
| `wellformed` | Check if XML is well-formed | `xmllint` |
| `xpath` | Validate using XPath expressions | `xmllint --xpath`, `lxml` |
| `xsd` | Validate against XML Schema | `xmllint --schema` |
| `dtd` | Validate against DTD | `xmllint --dtdvalid` |
| `xslt` | Check XSLT transformation output | `xsltproc` |

## Docker Image for XML Testing

For XML assignments, use a Docker image with XML tools:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libxml2-utils \
    xsltproc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install lxml pytest pytest-json-report

WORKDIR /app

# Copy test files
COPY test_xml.py /app/
COPY schemas/ /app/schemas/
COPY runner.sh /app/

RUN chmod +x /app/runner.sh

CMD ["/bin/sh", "-c", "tail -f /dev/null"]
```

## Sample XML Test File (Python with lxml)

```python
"""
XML Assignment Tests
"""
import pytest
from lxml import etree
import os

SUBMISSION_DIR = '/app/submission'

class TestTask1Catalog:
    @pytest.fixture
    def xml_tree(self):
        xml_file = os.path.join(SUBMISSION_DIR, 'catalog.xml')
        return etree.parse(xml_file)
    
    def test_root_element(self, xml_tree):
        """Root element must be 'catalog'"""
        assert xml_tree.getroot().tag == 'catalog'
    
    def test_minimum_books(self, xml_tree):
        """Must have at least 3 books"""
        books = xml_tree.xpath('/catalog/book')
        assert len(books) >= 3
    
    def test_book_has_id(self, xml_tree):
        """Each book must have an 'id' attribute"""
        books = xml_tree.xpath('/catalog/book')
        for book in books:
            assert 'id' in book.attrib
    
    def test_book_has_title(self, xml_tree):
        """Each book must have a title element"""
        books = xml_tree.xpath('/catalog/book')
        for book in books:
            assert book.find('title') is not None
    
    def test_book_has_author(self, xml_tree):
        """Each book must have an author element"""
        books = xml_tree.xpath('/catalog/book')
        for book in books:
            assert book.find('author') is not None
    
    def test_book_has_price(self, xml_tree):
        """Each book must have a price element"""
        books = xml_tree.xpath('/catalog/book')
        for book in books:
            assert book.find('price') is not None


class TestTask2Schema:
    def test_validates_against_xsd(self):
        """XML must validate against the XSD schema"""
        schema_file = '/app/schemas/books.xsd'
        xml_file = os.path.join(SUBMISSION_DIR, 'books.xml')
        
        schema = etree.XMLSchema(etree.parse(schema_file))
        xml_doc = etree.parse(xml_file)
        
        assert schema.validate(xml_doc), schema.error_log
```

---

## Creating an XML Generator

To create a full XML assignment generator similar to the Python one, you would need to:

1. **Modify the generator** to output XML starter files instead of Python
2. **Create XML-specific test templates** using lxml or xmllint
3. **Update the Dockerfile** to include XML tools
4. **Adjust the runner** to handle XML validation

Would you like me to create a complete XML assignment generator based on this template?

---

## Quick Reference: Existing Python Assignments

| Assignment | Topic | Functions |
|------------|-------|-----------|
| 2 | String Slicing | 10 functions |
| 3 | String Methods | 10 functions |
| 4 | Input & Type Conversion | 10 functions |
| 5 | Operators | 14 functions |
| 6 | Collections | 15 functions |

---

## Tips for Creating Good Assignments

1. **Start simple** - First functions should be easy
2. **Build complexity** - Later functions can combine concepts
3. **3-4 tests per function** - Cover normal, edge, and boundary cases
4. **Clear descriptions** - Students should understand what's expected
5. **Meaningful examples** - Show realistic usage in examples
