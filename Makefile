# `make verify` is the green-before-merge check.
# It runs black and isort formatters in check mode, performs Django system check,
# and executes the test suite in Docker without relying on host python or external db.

CODE = accounts klaribase manage.py

.PHONY: verify test format

verify:
	docker build -q -t klaribase-verify - < verify.Dockerfile
	docker run --rm -e SECRET_KEY=verify-secret-key -e DATABASE_ENGINE=django.db.backends.sqlite3 -e DATABASE_NAME=:memory: \
	  -v "$(CURDIR)":/src:ro -w /src klaribase-verify \
	  sh -c "black --check $(CODE) && isort --check-only --profile=black $(CODE) && python manage.py check && python manage.py test accounts"

format:
	black $(CODE)
	isort --profile=black $(CODE)
