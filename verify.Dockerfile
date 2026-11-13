# Tools for `make verify`, pinned to the versions in .pre-commit-config.yaml.
FROM python:3.12-slim
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore \
    --default-timeout 120 --retries 5 black==23.3.0 isort==5.13.2
