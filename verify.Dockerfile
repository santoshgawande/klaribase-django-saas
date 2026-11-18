# Tools for `make verify`, pinned to the versions in .pre-commit-config.yaml and requirements.
FROM python:3.12-slim
WORKDIR /src
RUN pip install --no-cache-dir --disable-pip-version-check --root-user-action=ignore \
    black==23.3.0 isort==5.13.2 pytest==8.1.1 pytest-django==4.8.0 \
    django==4.2 djangorestframework==3.16.0 djangorestframework-simplejwt==5.5.0 \
    django-allauth==0.57.2 dj-rest-auth==5.0.2 django-session-security==2.6.8 \
    python-dotenv==1.1.0 psycopg2-binary==2.9.10
