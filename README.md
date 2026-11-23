# Quick Note Application — VirtualWorks Task 2

A single-page application where you write a note, save it, the note is
sent to a Python (Flask) backend, stored in a SQLite database, and
displayed on the same page. Notes can be edited and deleted, and each
note shows the time it was saved.

## How it works

- Frontend: one page (`templates/index.html`) with a "New Note" box and
  a "Your Saved Notes" list. It talks to the backend with `fetch()`.
- Backend: Flask (`app.py`) with a REST API:
  - `GET /api/notes` — list all notes (newest first)
  - `POST /api/notes` — save a new note (`{"text": "..."}`)
  - `PUT /api/notes/<id>` — edit a note
  - `DELETE /api/notes/<id>` — delete a note
- Database: SQLite (`notes.db`, created automatically), table `notes`
  with `id`, `text`, `created_at`, `updated_at`.

## Run it

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Then open http://127.0.0.1:5000 in a browser.

## Files

- `app.py` — Flask backend + SQLite database
- `templates/index.html` — the single page
- `static/style.css` — styling
- `requirements.txt` — Flask dependency
- `notes.db` — created on first run (not in the repo)

## Submitting to VirtualWorks

Push this folder to a GitHub repo and submit that repo link in the
VirtualWorks workspace under Task 2, "Quick Note Application".
(A video walkthrough link is also accepted instead.)
