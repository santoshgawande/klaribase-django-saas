# Klaribase — project notes

Reference material moved out of the old local `CLAUDE.md` (dated 2026-03-30). Rules live in `CLAUDE.md` and `AGENTS.md`; read this when you need the stack, the roadmap state or the env var names.

---

## Project Overview

**Klaribase** is a multi-tenant SaaS platform built with Django 4.2 + PostgreSQL.
Each tenant (customer) gets an isolated PostgreSQL schema via `django-tenants`.
The product being sold is an LMS (Learning Management System).

---

## Tech Stack

| Layer | Tech |
|---|---|
| Framework | Django 4.2, DRF 3.16 |
| Database | PostgreSQL + django-tenants (schema isolation) |
| Auth | JWT (simplejwt) + Google OAuth (allauth) |
| Task Queue | Celery 5.5 + Redis |
| Payments | Stripe (test mode keys in .env) |
| Email | SMTP (Gmail) → async via Celery |
| SMS | Twilio (to be added) |
| API Docs | drf-spectacular (Swagger) — to be added |
| Testing | pytest-django + Factory Boy — to be added |
| Logging | structlog + Sentry — to be added |

---

## Project Structure

```
klaribase-django-saas/
├── accounts/          # Auth: signup, login, JWT, OAuth, password reset
├── tenants/           # Multi-tenant: Client + Domain models (in dev branch)
├── billing/           # Stripe subscriptions, plans, invoices (to be built)
├── notifications/     # Email/SMS/in-app notifications (to be built)
├── core/              # Shared tenant-scoped utilities (to be built)
├── lms/               # The product — tenant-isolated (to be built)
└── klaribase/         # Django settings, urls, wsgi, asgi
```

---

## Multi-Tenancy Architecture

- **Public schema**: `auth`, `tenants`, `billing`, `notifications`
- **Tenant schemas**: `lms`, `core` — one schema per customer
- Routing: request domain → tenant lookup → schema switch
- Library: `django-tenants` (schema-based, not row-based)

---

## Current State (as of 2026-03-30)

### Done
- [x] Custom user model (email-based auth, roles: owner/admin/member)
- [x] JWT auth: login, logout, refresh, blacklist
- [x] Password management: change, forgot, reset
- [x] Google OAuth2 via allauth
- [x] Basic SMTP email (synchronous)
- [x] Pre-commit hooks (black, isort, flake8)

### In Progress
- [ ] Multi-tenancy (django-tenants in dev branch, not merged)
- [ ] Celery + Redis (installed, not configured)

### Not Started
- [ ] RBAC permission enforcement
- [ ] Stripe billing
- [ ] Notifications system
- [ ] Tenant member management
- [ ] Audit logs
- [ ] API docs (Swagger)
- [ ] Tests
- [ ] LMS app

---

## Known Issues / Bugs

- `accounts/views/reset_password.py:19` — typo: `CustomUser.object.get()` should be `CustomUser.objects.get()` (will 500 at runtime)
- `accounts/views/me.py` — test file is empty
- Logout view has debug `print()` statements (should use `logging`)
- `ALLOWED_HOSTS = []` — will reject all requests in production
- `DEBUG = os.getenv("DEBUG")` — returns string `"False"`, not boolean (truthy bug)

---

## Environment Variables (.env)

```
SECRET_KEY=
DEBUG=True

DATABASE_NAME=klaribase
DATABASE_USER=klaribase
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=5432

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

CLIENT_ID=           # Google OAuth
CLIENT_SECRET=       # Google OAuth

# To be added:
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
REDIS_URL=redis://localhost:6379/0
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
SENTRY_DSN=
```

---

## Coding Conventions

- Use `email` not `username` for auth everywhere
- All views are class-based (APIView)
- Views split into individual files under `app/views/`
- Serializers split into individual files under `app/serializers/`
- Env vars loaded via `python-dotenv` in `settings.py`
- Pre-commit: black (formatter), isort (imports), flake8 (lint)

---

## Development Setup

```bash
git clone <repo>
cd klaribase-django-saas
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in values
python manage.py migrate
python manage.py runserver
```

---

## Useful Commands

```bash
# Run server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate

# Celery worker (once configured)
celery -A klaribase worker -l info

# Celery beat scheduler
celery -A klaribase beat -l info

# Run tests (once set up)
pytest

# Lint + format
pre-commit run --all-files
```

---

## Implementation Roadmap Reference

See `PLAN.md` for the full phased implementation plan.
