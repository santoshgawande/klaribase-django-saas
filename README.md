# klaribase-django-saas  -  Multi-Tenant Platform

## 1. Accounts

### Create Accounts app
```bash
python manage.py startapp accounts
python manage.py makemigrations accounts
python manage.py migrate
```

### Create Postgres DB
```psql
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

```



#### User signup using Curl
```bash
curl -i -X POST http://127.0.0.1:8000/api/accounts/signup/ -H "Content-Type: application/json" -d "{\"username\":\"john\",\"password\":\"testpass123\",\"email\":\"john@example.com\",\"role\":\"owner\"}"

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
8000/api/token/ -H "Content-Type: application/json" -d '{"username":"john","password":"testpass123"}'


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

