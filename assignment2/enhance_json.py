#!/usr/bin/env python3

import json
import sys
import os

os.environ['PYTHONUNBUFFERED'] = '1'

def enhance_report(report_file):
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
        sys.stdout.write('\n')
        sys.stdout.flush()
    except Exception as e:
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
        sys.stdout.write('\n')
        sys.stdout.flush()
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        error_output = json.dumps({'error': 'Missing report file argument', 'stats': {'total_tests': 0, 'passed': 0, 'failed': 1, 'marks': 0.0, 'percentage': 0.0}})
        sys.stdout.write(error_output)
        sys.stdout.write('\n')
        sys.stdout.flush()
        sys.exit(0)
    enhance_report(sys.argv[1])
    sys.exit(0)
