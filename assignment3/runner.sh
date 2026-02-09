#!/bin/bash
set +e

export PYTHONPATH=/app/submission:/app:$PYTHONPATH

pytest /app/test_assignment.py --json-report --json-report-file=/tmp/report.json -v > /dev/null 2>&1

python3 /app/enhance_json.py /tmp/report.json

exit 0
