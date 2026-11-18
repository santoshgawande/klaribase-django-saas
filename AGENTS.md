# klaribase-django-saas — Agent Guidelines

- **Board Key:** `KLARI`
- **Verify:** `make verify` runs `black` and `isort` in check mode, runs `python manage.py check`, and executes the unit test suite inside Docker.
- **Branch Pattern:** `<type>/KLARI-<slug>`, e.g. `feat/KLARI-1-admin-idle-timeout`.
- **Purpose:** Multi-tenant LMS SaaS starter built on Django 4.2, DRF 3.16, PostgreSQL, and Celery.
- **Auth:** Email-based authentication using `CustomUser` (owner/admin/member roles). JWT via `djangorestframework-simplejwt` and Google OAuth via `allauth`.
- **Admin Session Security:** Staff sessions in `/admin/` are protected by `django-session-security` with server-side inactivity expiration and browser warning dialogs.
- **Code Style:** Black formatting, isort imports (`--profile=black`), class-based APIViews, one view per file under `app/views/`.
- **Secrets:** Environment variables are loaded via `python-dotenv` in `klaribase/settings.py`. Never commit secrets or `.env` files.
- **Workflow:** Green PR before merge. Santosh merges with `--squash`. Agents never merge.
