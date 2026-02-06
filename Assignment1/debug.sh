#!/bin/bash
# Debugging script to diagnose web platform integration issues

echo "=== SYSTEM INFO ===" >&2
echo "User: $(whoami)" >&2
echo "PWD: $PWD" >&2
echo "Shell: $SHELL" >&2
echo >&2

echo "=== ENVIRONMENT ===" >&2
env | sort >&2
echo >&2

echo "=== FILE STRUCTURE ===" >&2
echo "Docker version:" >&2
docker version 2>&1 | head -5 >&2
echo >&2

echo "=== DOCKER-COMPOSE CONFIG ===" >&2
echo "docker-compose file:" >&2
cat /Users/enfec/Desktop/Assignment_Android/Assignment1/docker-compose.yml >&2
echo >&2

echo "=== DOCKERFILE ===" >&2
head -20 /Users/enfec/Desktop/Assignment_Android/Assignment1/Dockerfile >&2
echo >&2

echo "=== IMAGE CHECK ===" >&2
docker images | grep assignment1-x86 >&2
echo >&2

echo "=== RUNNING CONTAINER ===" >&2
echo "Command: docker run --rm -v ./src:/app/submission:ro assignment1-x86:latest /bin/sh -c \"export PYTHONPATH=/app/submission:/app:\$PYTHONPATH && /app/runner.sh\"" >&2
echo >&2
echo "Output:" >&2
