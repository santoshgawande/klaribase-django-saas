# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Staff administrative idle-timeout logout via `django-session-security==2.6.8` with server-side session termination and client warning modal (`KLARI-1`).
- Admin template overrides (`templates/admin/base_site.html`) with jQuery namespacing and conditional session security bootstrap for authenticated staff users.
- Automated test suite in `accounts/tests.py` verifying all 6 acceptance criteria (idle logout, active refresh, multi-tab ping, JWT isolation, HTML inclusion, and clean system checks).
- Architecture and security deep dive documentation with explain-back questions in `docs/learning/django-session-security.md`.
- Repository verification suite and Docker test container (`Makefile`, `verify.Dockerfile`).
- Agent guidelines and conventions (`AGENTS.md`).

### Fixed
- Dependency drift across `requirements.txt` and `pyproject.toml` adding missing runtime dependencies (`django-allauth`, `dj-rest-auth`, `cryptography`, `requests`).
