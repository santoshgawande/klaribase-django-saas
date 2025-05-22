# klaribase-django-saas  -  Multi-Tenant Platform

## **1. Accounts**

### Create Accounts app
```bash
python manage.py startapp accounts
python manage.py makemigrations accounts
python manage.py migrate
```

### Create Postgres DB
```bash
san@server:~$ sudo -u postgres psql
[sudo] password for san:
psql (16.8 (Ubuntu 16.8-0ubuntu0.24.04.1))
Type "help" for help.

postgres=# \du
                             List of roles
 Role name |                         Attributes
-----------+------------------------------------------------------------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS
 san       |

postgres=# CREATE USER klaribase WITH PASSWORD 'klaripass'
postgres-# ;
CREATE ROLE
postgres=# CREATE DATABASE klaribase;
CREATE DATABASE
postgres=# GRANT ALL PRIVILEGES ON DATABASE klaribase TO klaribase;
GRANT
postgres=# ALTER DATABASE klaribase OWNER TO klaribase;
ALTER DATABASE
postgres=# \l

##  To verify DB connection:
psql -U klaribase -d klaribase -h localhost
Password for user klaribase:
psql (16.9 (Ubuntu 16.9-0ubuntu0.24.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

klaribase=>

## DROP Database
sudo -u postgres psql
[sudo] password for san:
psql (16.9 (Ubuntu 16.9-0ubuntu0.24.04.1))
Type "help" for help.

postgres=# DROP DATABASE IF EXISTS klaribase;
DROP DATABASE
postgres=#

## CREATE Database
postgres=# CREATE DATABASE klaribase OWNER klaribase;
CREATE DATABASE
postgres=#

```

### Unapply all migrations
```bash
python manage.py migrate accounts zero
Operations to perform:
  Unapply all migrations: accounts
Running migrations:
  No migrations to apply.
```

### User signup using Curl
```bash
curl -i -X POST http://127.0.0.1:8000/api/accounts/signup/ -H "Content-Type: application/json" -d "{\"username\":\"san\",\"password\":\"testpass123\",\"email\":\"san@example.com\",\"role\":\"owner\"}"

HTTP/1.1 201 Created
Date: Tue, 20 May 2025 19:43:21 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 68
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
```

### Get api token using Curl
```bash
url -i -X POST http://127.0.0.1:
8000/api/token/ -H "Content-Type: application/json" -d '{"username":"san","password":"testpass123"}'


HTTP/1.1 200 OK
Date: Tue, 20 May 2025 19:45:19 GMT
Server: WSGIServer/0.2 CPython/3.12.3
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 483
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0Nzg1NjcxOSwiaWF0IjoxNzQ3NzcwMzE5LCJqdGkiOiI5OWY3MTAyNGVlZjc0YTU3YTg5ODIxZGZlMTdhYzk1OSIsInVzZXJfaWQiOjJ9.SxmDT5pA4_o-2hkE8gsu_QbduNB5XDtJmurMYVlq_ds","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3NzcwNjE5LCJpYXQiOjE3NDc3NzAzMTksImp0aSI6IjcxMjI1Zjc3OTM5YzQ1ZTA5NWY3YWUxYzkwM2NhNzFkIiwidXNlcl9pZCI6Mn0.YfX98ZZH6pCsg-LckyQfqzaiSD9AqSs3VBPjxviC43U"}
```

### Setup Git Hooks with pre-commit

#### 1. Check if Pre-Commit is Installed
```bash
## Run:
pre-commit --version

## If not installed:
pip install pre-commit

## 2. Check for .pre-commit-config.yaml
## Navigate to your project root (where manage.py is) and check:
ls -a | grep .pre-commit-config.yaml

## If the file does not exist, create one:

touch .pre-commit-config.yaml
```
#### add this code
>vim .pre-commit-config.yaml

```bash
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        name: isort (python import sorting)

```
```bash
## 4. Test Pre-Commit on All Files
pre-commit run --all-files
```

#### 5. Add It to Your pyproject.toml (optional but good practice)

>vim pyproject.toml
```bash
[tool.black]
line-length = 88
target-version = ['py312']

[tool.isort]
profile = "black"

```

#### Next Steps After Commit
1. Install Git Hook

Install the pre-commit Git hook locally (this only needs to be done once per developer/machine):

```bash
pre-commit install

pre-commit installed at .git/hooks/pre-commit
```
This sets up the hook in .git/hooks/pre-commit.
