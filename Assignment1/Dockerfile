FROM python:3.11-slim

USER root

WORKDIR /app

RUN pip install pytest pytest-json-report lxml

COPY conftest.py /app/conftest.py
COPY pytest.ini /app/pytest.ini
COPY test_assignment.py /app/test_assignment.py
COPY runner.sh /app/runner.sh
COPY enhance_json.py /app/enhance_json.py

RUN chmod +x /app/runner.sh /app/enhance_json.py

CMD ["/bin/sh", "-c", "export PYTHONPATH=/app/submission:/app:$PYTHONPATH && /app/runner.sh"]
