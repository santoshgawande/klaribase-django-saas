# `make verify` is the green-before-merge check. It runs the formatters from
# .pre-commit-config.yaml in check mode, at the same versions, over the code.
# black also fails on a file that does not parse. The tools live in a small image
# (verify.Dockerfile) so the check itself runs with no network and changes no files.
# There is no test suite yet: accounts/tests.py is a stub.

CODE = accounts klaribase manage.py

.PHONY: verify

verify:
	docker build -q -t klaribase-verify - < verify.Dockerfile
	docker run --rm --network none -v "$(CURDIR)":/src:ro -w /src klaribase-verify \
	  sh -c "black --check $(CODE) && isort --check-only --profile=black $(CODE)"
