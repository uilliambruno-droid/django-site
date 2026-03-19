# django-site

A full-stack Django web application featuring a polls system, a contacts module, and user authentication — all structured with environment-based settings, a comprehensive test suite, and production-ready deployment configuration for [Render](https://render.com).

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Apps](#apps)
  - [Polls](#polls)
  - [Contacts](#contacts)
  - [Accounts](#accounts)
- [Settings Architecture](#settings-architecture)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
- [Running the Development Server](#running-the-development-server)
- [Admin Panel](#admin-panel)
- [Testing](#testing)
- [URL Reference](#url-reference)
- [Deploy to Render](#deploy-to-render)
- [Tech Stack](#tech-stack)

---

## Overview

**django-site** is a multi-app Django project built as a learning and reference platform. It demonstrates:

- Django function-based views with forms, model relationships, and permission control
- Environment-based settings split (`development` / `production`) with `.env` file support
- A full pytest test suite covering models, views, and forms (30+ tests)
- Static file serving with WhiteNoise (including Brotli compression)
- Production-ready WSGI server via Gunicorn
- One-click deploy to Render via `render.yaml`

---

## Project Structure

```
django-site/                  ← repository root
├── render.yaml               ← Render deploy config
├── .gitignore
├── README.md
└── mysite/                   ← Django project root (Poetry workspace)
    ├── manage.py
    ├── pyproject.toml
    ├── build.sh              ← Render build script
    ├── .env.example          ← environment variable template
    ├── db.sqlite3            ← local SQLite database (gitignored)
    ├── polls/                ← Polls app
    ├── contacts/             ← Contacts app
    ├── accounts/             ← Accounts (auth) app
    └── mysite/               ← Django project package
        ├── settings.py       ← environment selector
        ├── settings_base.py  ← shared settings
        ├── settings_development.py
        ├── settings_production.py
        ├── urls.py
        ├── wsgi.py
        ├── asgi.py
        └── tests/            ← all test files
            ├── polls/
            ├── contacts/
            └── accounts/
```

---

## Apps

### Polls

A classic Django tutorial-style polling system extended with an `active` flag.

**Models:**

| Model | Fields |
|---|---|
| `Question` | `question_text`, `pub_date`, `active` |
| `Choice` | `question` (FK), `choice_text`, `votes` |

`Question.was_published_recently()` returns `True` if the question was published within the last 24 hours.

**Views:**

| View | URL | Description |
|---|---|---|
| `index` | `/polls/` | Lists the 5 most recent questions |
| `detail` | `/polls/<id>/` | Shows a question and its choices |
| `results` | `/polls/<id>/results/` | Shows vote results |
| `vote` | `/polls/<id>/vote/` | Handles POST vote submission |

---

### Contacts

A contact form module with permission-gated submission and a simple name form.

**Models:**

| Model | Fields |
|---|---|
| `Contact` | `subject`, `email`, `message`, `cc_myself` |

**Forms:**

| Form | Description |
|---|---|
| `NameForm` | Simple form with a single `your_name` CharField |
| `ContactForm` | Full ModelForm for `Contact` with email validation |

**Views:**

| View | URL | Auth required | Description |
|---|---|---|---|
| `get_name` | `/contacts/` | No | Renders and processes `NameForm` |
| `create` | `/contacts/create/` | Yes (`contacts.add_contact`) | Renders and saves `ContactForm` |
| `thanks` | `/contacts/thanks/<name>/` | No | Confirmation page |

> The `create` view requires the `contacts.add_contact` permission. Anonymous users are redirected to the login page.

---

### Accounts

Custom authentication views using Django's built-in `authenticate` / `login` / `logout` functions.

**Views:**

| View | URL | Description |
|---|---|---|
| `authenticate_user` | `/accounts/login/` | Renders login form; authenticates and logs in on POST |
| `logout_user` | `/accounts/logout/` | Logs out and redirects to login |

---

## Settings Architecture

The project uses a three-file settings pattern controlled by the `DJANGO_ENV` environment variable:

```
mysite/settings.py          ← reads DJANGO_ENV, imports the right module
    ├── settings_development.py   ← DEBUG=True, insecure cookies
    └── settings_production.py   ← DEBUG=False, HTTPS, HSTS, security headers
            ↑ both inherit from
        settings_base.py          ← shared: apps, middleware, DB, static, etc.
```

`settings_base.py` provides two helper functions:

```python
env_bool("VAR_NAME", default=False)   # reads a bool from an env var
env_list("VAR_NAME", default="")      # reads a comma-separated list
```

`python-dotenv` is used to load `.env` automatically, with a graceful fallback if the package is not installed.

---

## Environment Variables

Copy `.env.example` to `.env` inside the `mysite/` directory and fill in the values:

```zsh
cp mysite/.env.example mysite/.env
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `DJANGO_ENV` | No | `development` | `development` or `production` |
| `DJANGO_DEBUG` | No | `true` (dev) / `false` (prod) | Enable debug mode |
| `DJANGO_SECRET_KEY` | **Yes in prod** | insecure dev key | Django secret key |
| `DJANGO_ALLOWED_HOSTS` | **Yes in prod** | `127.0.0.1,localhost` | Comma-separated allowed hosts |
| `DJANGO_SECURE_SSL_REDIRECT` | No | `true` (prod) | Redirect HTTP → HTTPS |
| `DJANGO_SECURE_HSTS_SECONDS` | No | `31536000` | HSTS max-age in seconds |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | No | `true` | Enable HSTS for subdomains |
| `DJANGO_SECURE_HSTS_PRELOAD` | No | `true` | Enable HSTS preload |

`.env.example`:

```dotenv
DJANGO_ENV=development
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=django-insecure-change-me
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Production-only security options (used when DJANGO_ENV=production)
DJANGO_SECURE_SSL_REDIRECT=true
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true
DJANGO_SECURE_HSTS_PRELOAD=true
```

---

## Getting Started

**Prerequisites:** Python ≥ 3.12, [Poetry](https://python-poetry.org/docs/#installation)

```zsh
# 1. Clone the repository
git clone https://github.com/uilliambruno-droid/django-site.git
cd django-site

# 2. Install dependencies
cd mysite
poetry install

# 3. Set up environment variables
cp .env.example .env
# Edit .env and set at least DJANGO_SECRET_KEY

# 4. Apply migrations
poetry run ./manage.py migrate

# 5. Create a superuser (optional, needed to access /admin/)
poetry run ./manage.py createsuperuser
```

---

## Running the Development Server

```zsh
cd mysite
poetry run ./manage.py runserver
```

The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

**Available routes:**

| Prefix | App |
|---|---|
| `/polls/` | Polls |
| `/contacts/` | Contacts |
| `/accounts/` | Authentication |
| `/admin/` | Custom Django admin |

---

## Admin Panel

The project uses a custom `AdminSite` instance. Access it at `/admin/` after creating a superuser.

To give a user access to the `contacts.add_contact` permission (required to access `/contacts/create/`), go to **Admin → Users → [user] → Permissions** and assign it.

---

## Testing

The project uses **pytest** with **pytest-django**. All tests use an in-memory SQLite database (no external dependencies needed).

```zsh
cd mysite

# Run all tests
poetry run pytest -q

# Run with verbose output
poetry run pytest -v

# Run only a specific app
poetry run pytest mysite/tests/polls/ -v
```

**Test coverage by module:**

| Module | File | Tests |
|---|---|---|
| `polls` models | `tests/polls/test_models.py` | 4 |
| `polls` views | `tests/polls/test_views.py` | 6 |
| `contacts` models | `tests/contacts/test_models.py` | 1 |
| `contacts` views | `tests/contacts/test_views.py` | 8 |
| `contacts` forms | `tests/contacts/test_forms.py` | 7 |
| `accounts` views | `tests/accounts/test_views.py` | 4 |
| **Total** | | **30** |

All tests follow the **Given / When / Then** pattern:

```python
@pytest.mark.django_db
def test_was_published_recently_with_recent_question():
    # Given: a question published 12 hours ago
    question = Question(pub_date=timezone.now() - datetime.timedelta(hours=12))
    # When: was_published_recently is called
    result = question.was_published_recently()
    # Then: it should return True
    assert result is True
```

---

## URL Reference

| Method | URL | View | Auth |
|---|---|---|---|
| GET | `/polls/` | `polls.index` | — |
| GET | `/polls/<id>/` | `polls.detail` | — |
| GET | `/polls/<id>/results/` | `polls.results` | — |
| POST | `/polls/<id>/vote/` | `polls.vote` | — |
| GET/POST | `/contacts/` | `contacts.get_name` | — |
| GET/POST | `/contacts/create/` | `contacts.create` | `contacts.add_contact` |
| GET | `/contacts/thanks/<name>/` | `contacts.thanks` | — |
| GET/POST | `/accounts/login/` | `accounts.authenticate_user` | — |
| GET | `/accounts/logout/` | `accounts.logout_user` | — |
| — | `/admin/` | Django Admin | Superuser |

---

## Deploy to Render

This repository includes a `render.yaml` file at the root for one-click deployment.

If your service was created as a regular **Web Service** (not Blueprint), Render may ignore `render.yaml` and use the default Python build command (`pip install -r requirements.txt`).

To support this flow, the repository now includes:

- `requirements.txt` (repo root)
- `mysite/requirements.txt`

### Steps

1. Push this repository to GitHub.
2. Go to [Render](https://render.com) → **New** → **Blueprint** and connect your repository.
3. Render will detect `render.yaml` and configure the service automatically.
4. After the first deploy, update `DJANGO_ALLOWED_HOSTS` in the Render dashboard to include your app's domain (e.g. `your-app.onrender.com`).

### If you created a regular Web Service (manual setup)

Use these settings in Render (free plan friendly):

| Field | Value |
|---|---|
| Build Command | `./build.sh` |
| Start Command | `./start.sh` |

`build.sh` and `start.sh` are now available at the repository root and internally switch to `mysite/`, so this works even when `Root Directory` is empty.

If you prefer to keep Render's default build command, it will also work because `requirements.txt` is present at the repository root.

### Build & Start Commands

| Step | Command |
|---|---|
| Build | `./build.sh` |
| Start | `poetry run gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT` |

`build.sh` runs the following on every deploy:

```bash
pip install --upgrade poetry
poetry install --no-root --only main
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate
```

### Environment Variables on Render

| Variable | Value |
|---|---|
| `DJANGO_ENV` | `production` |
| `DJANGO_DEBUG` | `false` |
| `DJANGO_SECRET_KEY` | *(auto-generated by Render)* |
| `DJANGO_ALLOWED_HOSTS` | `your-app.onrender.com` |

> `DJANGO_SECRET_KEY` is set with `generateValue: true` in `render.yaml`, so Render creates a secure random key automatically on first deploy.

### Verifying locally with production settings

```zsh
cd mysite
export DJANGO_ENV=production
export DJANGO_SECRET_KEY='a-long-random-secret-key'
export DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
poetry run ./manage.py check --deploy
```

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| [Django](https://www.djangoproject.com/) | ≥ 6.0.3 | Web framework |
| [Python](https://www.python.org/) | ≥ 3.12, < 3.15 | Language |
| [Poetry](https://python-poetry.org/) | latest | Dependency management |
| [pytest](https://pytest.org/) | ≥ 8.4 | Test runner |
| [pytest-django](https://pytest-django.readthedocs.io/) | ≥ 4.12 | Django integration for pytest |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | ≥ 1.1 | `.env` file loading |
| [WhiteNoise](http://whitenoise.evans.io/) | latest | Static file serving (+ Brotli) |
| [Gunicorn](https://gunicorn.org/) | ≥ 25.1 | Production WSGI server |
| [isort](https://pycli.readthedocs.io/en/latest/isort.html) | ≥ 8.0 | Import sorting |
