import sys
import os
from pathlib import Path

# Usage:
# python3 generic_assignment_generator.py "starter.xml" "solution.xml" "assignment_name" "assignment_id" "description"
# The script will read the two XML files and generate all assignment files, build the Docker image, and create the x86 tar file in a new folder.

from zipfile import ZipFile
import subprocess

TEMPLATE_FILES = [
    ("Dockerfile", '''FROM python:3.11-slim\n\nUSER root\n\nWORKDIR /app\n\nRUN pip install pytest pytest-json-report lxml\n\nCOPY conftest.py /app/conftest.py\nCOPY pytest.ini /app/pytest.ini\nCOPY test_assignment.py /app/test_assignment.py\nCOPY runner.sh /app/runner.sh\nCOPY enhance_json.py /app/enhance_json.py\n\nRUN chmod +x /app/runner.sh /app/enhance_json.py\n\nCMD [\"/bin/sh\", \"-c\", \"export PYTHONPATH=/app/submission:/app:$PYTHONPATH && /app/runner.sh\"]\n'''),
    ("runner.sh", '''#!/bin/bash\nset +e\n\nexport PYTHONPATH=/app/submission:/app:$PYTHONPATH\n\npytest /app/test_assignment.py --json-report --json-report-file=/tmp/report.json -v > /dev/null 2>&1\n\npython3 /app/enhance_json.py /tmp/report.json\n\nexit 0\n'''),
    ("enhance_json.py", '''#!/usr/bin/env python3\n\nimport json\nimport sys\nimport os\n\nos.environ['PYTHONUNBUFFERED'] = '1'\n\ndef enhance_report(report_file):\n    try:\n        if not os.path.exists(report_file):\n            raise FileNotFoundError(f\"Report file {report_file} not found\")\n        with open(report_file, 'r') as f:\n            content = f.read()\n        data = json.loads(content)\n        summary = data.get('summary', {})\n        passed = summary.get('passed', 0)\n        failed = summary.get('failed', 0)\n        total = summary.get('total', 0)\n        if total > 0:\n            marks = passed / total\n        else:\n            marks = 0\n        data['stats'] = {\n            'total_tests': total,\n            'passed': passed,\n            'failed': failed,\n            'marks': round(marks, 2),\n            'percentage': round(marks * 100, 2)\n        }\n        output = json.dumps(data, indent=2)\n        sys.stdout.write(output)\n        sys.stdout.write('\\n')\n        sys.stdout.flush()\n    except Exception as e:\n        error_data = {\n            'error': str(e),\n            'stats': {\n                'total_tests': 0,\n                'passed': 0,\n                'failed': 1,\n                'marks': 0.0,\n                'percentage': 0.0\n            }\n        }\n        output = json.dumps(error_data, indent=2)\n        sys.stdout.write(output)\n        sys.stdout.write('\\n')\n        sys.stdout.flush()\n    return 0\n\nif __name__ == '__main__':\n    if len(sys.argv) < 2:\n        error_output = json.dumps({'error': 'Missing report file argument', 'stats': {'total_tests': 0, 'passed': 0, 'failed': 1, 'marks': 0.0, 'percentage': 0.0}})\n        sys.stdout.write(error_output)\n        sys.stdout.write('\\n')\n        sys.stdout.flush()\n        sys.exit(0)\n    enhance_report(sys.argv[1])\n    sys.exit(0)\n'''),
    ("conftest.py", '''import sys\nfrom pathlib import Path\nsubmission_path = Path("/app/submission").resolve()\nif submission_path not in [Path(p).resolve() for p in sys.path]:\n    sys.path.insert(0, str(submission_path))\n'''),
    ("pytest.ini", '''[pytest]\npython_files = test_*.py\npython_classes = Test*\npython_functions = test_*\nmarkers =\n    layout: Layout related tests\n    textview: TextView related tests\n    smoke: Smoke tests\n'''),
    ("docker-compose.yml", '''version: '3.8'\nservices:\n  judge:\n    image: {image_name}:latest\n    platform: linux/amd64\n    working_dir: /app\n    volumes:\n      - ./src:/app/submission:ro\n    networks:\n      - judge-network\n    security_opt:\n      - no-new-privileges:true\n    cap_drop:\n      - ALL\n    deploy:\n      resources:\n        limits:\n          cpus: '1'\n          memory: 512M\n        reservations:\n          cpus: '0.5'\n          memory: 256M\n    tmpfs:\n      - /tmp:rw,noexec,nosuid,size=50m\n    stdin_open: true\n    tty: true\n    command: /bin/sh -c \"export PYTHONPATH=/app/submission:/app:$PYTHONPATH && /app/runner.sh\"\nnetworks:\n  judge-network:\n    driver: bridge\n'''),
    ("test_assignment.py", '''import pytest\nfrom lxml import etree\nimport os\n\nSUBMISSION_DIR = '/app/submission'\n\n@pytest.fixture\ndef xml_tree():\n    xml_file = os.path.join(SUBMISSION_DIR, 'activity_main.xml')\n    if not os.path.exists(xml_file):\n        pytest.skip(f\"XML file not found at {xml_file}\")\n    try:\n        tree = etree.parse(xml_file)\n        return tree\n    except Exception as e:\n        pytest.fail(f\"XML parsing failed: {e}\")\n\n@pytest.fixture\ndef root_element(xml_tree):\n    return xml_tree.getroot()\n\nclass TestLayout:\n    def test_xml_is_wellformed(self, xml_tree):\n        assert xml_tree is not None, \"XML file could not be parsed\"\n\n    def test_root_is_linear_layout(self, root_element):\n        assert root_element.tag.endswith('LinearLayout'), f\"Root element should be LinearLayout, got {root_element.tag}\"\n\n    def test_layout_dimensions(self, root_element):\n        width = root_element.get('{http://schemas.android.com/apk/res/android}layout_width')\n        height = root_element.get('{http://schemas.android.com/apk/res/android}layout_height')\n        assert width == 'match_parent', f\"Layout width should be match_parent, got {width}\"\n        assert height == 'match_parent', f\"Layout height should be match_parent, got {height}\"\n\n    def test_layout_gravity_center(self, root_element):\n        gravity = root_element.get('{http://schemas.android.com/apk/res/android}gravity')\n        assert gravity is not None and 'center' in gravity.lower(), f\"Layout gravity should be center, got {gravity}\"\n\nclass TestTextView:\n    def test_textview_exists(self, root_element):\n        textviews = root_element.findall('.//TextView')\n        assert len(textviews) > 0, \"No TextView found in the layout\"\n\n    def test_textview_text(self, root_element):\n        textviews = root_element.findall('.//TextView')\n        found = any(tv.get('{http://schemas.android.com/apk/res/android}text') == 'Hi Android' or tv.get('android:text') == 'Hi Android' for tv in textviews)\n        assert found, \"TextView with text 'Hi Android' not found\"\n\n    def test_textview_dimensions(self, root_element):\n        textviews = root_element.findall('.//TextView')\n        assert any(tv.get('{http://schemas.android.com/apk/res/android}layout_width') in ['wrap_content', '400dp'] for tv in textviews), \"TextView width should be wrap_content or 400dp\"\n        assert any(tv.get('{http://schemas.android.com/apk/res/android}layout_height') in ['wrap_content', '70dp'] for tv in textviews), \"TextView height should be wrap_content or 70dp\"\n\n    def test_textview_textsize(self, root_element):\n        textviews = root_element.findall('.//TextView')\n        found = False\n        for tv in textviews:\n            size = tv.get('{http://schemas.android.com/apk/res/android}textSize')\n            if size:\n                try:\n                    value = int(''.join(filter(str.isdigit, size)))\n                    if value >= 24:\n                        found = True\n                        break\n                except Exception:\n                    continue\n        assert found, \"TextView textSize should be at least 24sp\"\n\n    def test_textview_textstyle_bold(self, root_element):\n        textviews = root_element.findall('.//TextView')\n        found = any('bold' in (tv.get('{http://schemas.android.com/apk/res/android}textStyle') or '') for tv in textviews)\n        assert found, \"TextView should have textStyle bold\"\n'''),
    ("ARCHITECTURE.md", "# This assignment was generated automatically.\n"),
    ("README.md", "# This assignment was generated automatically.\n")
]

def main():
    if len(sys.argv) < 6:
        print("Usage: python3 generic_assignment_generator.py <starter.xml> <solution.xml> <assignment_name> <assignment_id> <description>")
        sys.exit(1)
    starter_path, solution_path, assignment_name, assignment_id, description = sys.argv[1:6]
    with open(starter_path) as f:
        starter_xml = f.read()
    with open(solution_path) as f:
        solution_xml = f.read()
    # Always create the assignment folder in the root directory
    root_dir = Path(__file__).parent.resolve()
    base_dir = root_dir / assignment_name.replace(' ', '_').lower()
    base_dir.mkdir(exist_ok=True)
    (base_dir / "src").mkdir(exist_ok=True)
    # Write template files
    for fname, content in TEMPLATE_FILES:
        if fname == "docker-compose.yml":
            content = content.format(image_name=assignment_name.replace(' ', '_').lower() + "-x86")
        (base_dir / fname).write_text(content)
    # Write zips
    with ZipFile(base_dir / "startercode.zip", 'w') as zf:
        zf.writestr("activity_main.xml", starter_xml)
    with ZipFile(base_dir / "solution.zip", 'w') as zf:
        zf.writestr("activity_main.xml", solution_xml)
    # Build docker image and save tar
    image_name = assignment_name.replace(' ', '_').lower() + "-x86"
    os.system(f"cd {base_dir} && docker buildx build --platform linux/amd64 -t {image_name}:latest .")
    os.system(f"cd {base_dir} && docker save -o x86.tar {image_name}:latest")
    print(f"✅ All files generated in {base_dir}/, Docker image built, and x86.tar created!")

if __name__ == "__main__":
    main()
