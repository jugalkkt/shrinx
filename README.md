# shrinx

A URL shortener. Sign up, paste a long URL, and get a 7-character short link (e.g. `/aZ3kP9q`) that redirects to it. Each user sees a dashboard listing the links they've created.

**Live:** https://shrinx-coral.vercel.app

## Features

- Email/password sign up and login (passwords hashed with bcrypt)
- Sessions via a JWT stored in an HTTP-only cookie (valid for 7 days)
- Random base62 short codes, with retries on collision and a blocklist of reserved paths (`links`, `login`, `signup`, `logout`, `static`)
- Per-user dashboard of created links
- `GET /{code}` redirects to the destination URL (302), or returns 404

## Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), served with Uvicorn
- **Database:** MongoDB (Atlas) via [Beanie](https://beanie-odm.dev/) ODM and PyMongo's async client
- **Auth:** bcrypt + PyJWT
- **Templates:** Jinja2 (server-rendered HTML)
- **Config:** pydantic-settings, loaded from `.env`
- **Tests:** pytest
- **Deployment:** Vercel (`api/index.py` exposes the app; `vercel.json` routes every request to it)

## Project layout

```
app/
  main.py         # FastAPI app, MongoDB/Beanie setup on startup
  models.py       # User and Link documents, request models
  routes/
    auth.py       # /signup, /login, /logout
    links.py      # /, /links/new, /{code}
  core/           # config, JWT, password hashing, short code generation, auth dependencies
templates/        # Jinja2 pages
tests/            # pytest tests
api/index.py      # Vercel entrypoint
```

## Running locally

Requires Python 3.11+ and a MongoDB instance (a free MongoDB Atlas cluster works, or a local `mongod`).

1. Clone the repo and install dependencies:

   ```bash
   git clone https://github.com/jugalkkt/shrinx.git
   cd shrinx
   uv sync
   ```

   Or with pip:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:

   ```env
   MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
   atlas_username=<user>
   atlas_password=<password>
   JWT_SECRET=<a long random string>
   ```

   | Key              | Description                                                        |
   | ---------------- | ------------------------------------------------------------------ |
   | `MONGODB_URI`    | MongoDB connection string. Data is stored in the `shrinx_db` database. |
   | `atlas_username` | MongoDB Atlas username. Required by the settings loader.           |
   | `atlas_password` | MongoDB Atlas password. Required by the settings loader.           |
   | `JWT_SECRET`     | Secret used to sign session tokens (HS256).                        |

   All four keys must be set or the app will fail to start. One way to generate a secret:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. Start the server:

   ```bash
   uvicorn app.main:app --reload
   ```

   (With uv: `uv run uvicorn app.main:app --reload`.)

4. Open http://127.0.0.1:8000. You'll be redirected to `/signup`; create an account, log in, and start shortening links. FastAPI's interactive API docs are at http://127.0.0.1:8000/docs.

## Running tests

```bash
pytest
```

(With uv: `uv run pytest`.) The tests cover short code generation and the base62 encode/decode helpers and don't need a database.
