"""Quick Note Application — VirtualWorks Task 2.

Single-page app: write a note, save it, the note is sent to this
Python (Flask) backend, stored in a SQLite database, and displayed
on the same page. Notes can also be edited and deleted.

Run:
    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python app.py
Then open http://127.0.0.1:5000
"""

import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, g, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "notes.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute(
            """CREATE TABLE IF NOT EXISTS notes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   text TEXT NOT NULL,
                   created_at TEXT NOT NULL,
                   updated_at TEXT NOT NULL
               )"""
        )
        db.commit()


def note_to_dict(row):
    return {
        "id": row["id"],
        "text": row["text"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/notes", methods=["GET"])
def list_notes():
    rows = get_db().execute(
        "SELECT * FROM notes ORDER BY id DESC"
    ).fetchall()
    return jsonify([note_to_dict(r) for r in rows])


@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Note text cannot be empty."}), 400
    timestamp = now_iso()
    db = get_db()
    cur = db.execute(
        "INSERT INTO notes (text, created_at, updated_at) VALUES (?, ?, ?)",
        (text, timestamp, timestamp),
    )
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(note_to_dict(row)), 201


@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Note text cannot be empty."}), 400
    db = get_db()
    cur = db.execute(
        "UPDATE notes SET text = ?, updated_at = ? WHERE id = ?",
        (text, now_iso(), note_id),
    )
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Note not found."}), 404
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return jsonify(note_to_dict(row))


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    db = get_db()
    cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Note not found."}), 404
    return jsonify({"deleted": note_id})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
