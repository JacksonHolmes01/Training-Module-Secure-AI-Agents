ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
WORKDIR /app
COPY runner.py .
# Runs as a non-root user; the container is further locked down in compose
USER 10001:10001
CMD ["python", "-I", "runner.py"]
