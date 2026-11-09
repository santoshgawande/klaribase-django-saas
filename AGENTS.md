# klaribase-django-saas — agent rules

- **Purpose:** multi-tenant LMS SaaS on Django 4.2 + DRF + PostgreSQL. Each tenant gets its own schema via `django-tenants` (public: auth/tenants/billing; tenant: lms/core). Multi-tenancy is not merged yet.
- **Verify:** none yet (WS-104 follow-up). No tests exist (`accounts/tests.py` is a stub); pytest-django is planned. Today the only check is `pre-commit run --all-files` (black, isort, flake8, whitespace).
- **Auth:** email, not username, everywhere. Custom user model with roles owner/admin/member; JWT (simplejwt) plus Google OAuth (allauth).
- **Conventions:** class-based `APIView`s, one file per view under `app/views/` and one per serializer under `app/serializers/`. Env vars load via `python-dotenv` in `klaribase/settings.py`.
- **Known bugs (as of 2026-03-30):** `accounts/views/reset_password.py` calls `CustomUser.object.get()` (should be `objects`); `DEBUG = os.getenv("DEBUG")` yields a string, so `"False"` is truthy; `ALLOWED_HOSTS = []`.
- **Secrets:** config comes from a gitignored `.env`; never read it or put real values in files. Stripe keys are test-mode only.
- **Flow:** `feat/*` -> `dev` -> `main` per the old plan, but the global branch/PR rules win.
- **Read when needed:** `README.md` (setup notes), `klaribase/settings.py` and `klaribase/urls.py` (config, routing), `accounts/` (the only built app), `system_designs/` (design notes).
