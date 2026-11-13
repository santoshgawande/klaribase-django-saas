# klaribase-django-saas — Claude rules

Mirrors `AGENTS.md`; the two must agree.

- **Purpose:** multi-tenant LMS SaaS on Django 4.2 + DRF + PostgreSQL. Each tenant gets its own schema via `django-tenants` (public: auth/tenants/billing; tenant: lms/core). Multi-tenancy is not merged yet.
- **Verify:** `make verify` runs black and isort in check mode (the versions pinned in `.pre-commit-config.yaml`) over `accounts`, `klaribase` and `manage.py`, in Docker with no network. It proves formatting and that every file parses, not behaviour: no tests exist (`accounts/tests.py` is a stub; pytest-django is planned).
- **Auth:** email, not username, everywhere. Custom user model with roles owner/admin/member; JWT (simplejwt) plus Google OAuth (allauth).
- **Conventions:** class-based `APIView`s, one file per view under `app/views/` and one per serializer under `app/serializers/`. Env vars load via `python-dotenv` in `klaribase/settings.py`.
- **Known bugs (as of 2026-03-30):** `accounts/views/reset_password.py` calls `CustomUser.object.get()` (should be `objects`); `DEBUG = os.getenv("DEBUG")` yields a string, so `"False"` is truthy; `ALLOWED_HOSTS = []`.
- **Secrets:** config comes from a gitignored `.env`; never read it or put real values in files. Stripe keys are test-mode only.
- **Flow:** `feat/*` -> `dev` -> `main` per the old plan, but the global branch/PR rules win.
- **Read when needed:** `PROJECT-NOTES.md` (stack, roadmap state, env var names, known issues), `README.md` (setup notes), `klaribase/settings.py` and `klaribase/urls.py` (config, routing), `accounts/` (the only built app).
