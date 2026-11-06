import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, abort, send_file
from pathlib import Path
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set a stable secret in your terminal before running Flask.
secret = os.environ.get("TRUSTVAULT_SECRET_KEY")
if not secret:
    raise RuntimeError("Set TRUSTVAULT_SECRET_KEY before starting the app.")
app.secret_key = secret

DATABASE =str(Path(__file__).resolve().parent / "trustvault.db")
UPLOAD_FOLDER = Path(__file__).resolve().parent / "private_uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg"}
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
def log_activity(user_id, username, action, document_id=None, details=None, db=None):
    query = """
        INSERT INTO audit_logs
        (user_id, username, action, document_id, details)
        VALUES (?, ?, ?, ?, ?)
    """

    values = (user_id, username, action, document_id, details)

    if db is not None:
        db.execute(query, values)
    else:
        with get_db() as connection:
            connection.execute(query, values)

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK(role IN ('admin', 'owner', 'viewer'))
            )
        """)

        # Create documents table
        db.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                original_name TEXT NOT NULL,
                stored_name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)
        # Document sharing permissions
        db.execute("""
            CREATE TABLE IF NOT EXISTS document_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                permission TEXT NOT NULL
                    CHECK(permission IN ('read', 'edit')),
                granted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(document_id, user_id),
                FOREIGN KEY (document_id) REFERENCES documents(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        # Create activity audit logs table
        db.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                document_id INTEGER,
                details TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (document_id) REFERENCES documents(id)
            )
        """)
        demo_users = [
            ("admin", "admin"),
            ("owner", "owner"),
            ("viewer", "viewer")
        ]

        for username, role in demo_users:
            existing = db.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if not existing:
                db.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (
                        username,
                        generate_password_hash("Honey12345"),
                        role
                    )
                )

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            log_activity(
                user["id"],
                user["username"],
                "USER_LOGIN",
                details="Successful login"
            )
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))
        log_activity(
            None,
            username or "Unknown",
            "LOGIN_FAILED",
            details="Invalid username or password"
        )

        return render_template(
            "login.html",
            error="Invalid username or password"
        ), 401

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    with get_db() as db:
        user = db.execute(
            "SELECT username, role FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=user["username"]
)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    with get_db() as db:
        admin = db.execute(
            "SELECT username, role FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        if admin is None or admin["role"] != "admin":
            abort(403)

        total_users = db.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        total_documents = db.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0]

        total_shares = db.execute(
            "SELECT COUNT(*) FROM document_permissions"
        ).fetchone()[0]

        users = db.execute("""
            SELECT id, username, role
            FROM users
            ORDER BY id
        """).fetchall()

        documents = db.execute("""
            SELECT d.id, d.original_name, d.category,
                d.uploaded_at, u.username AS owner_name
            FROM documents d
            JOIN users u ON d.owner_id = u.id
            ORDER BY d.uploaded_at DESC
        """).fetchall()

        shares = db.execute("""
            SELECT d.original_name,
                owner.username AS owner_name,
                viewer.username AS shared_with,
                p.permission, p.granted_at
            FROM document_permissions p
            JOIN documents d ON p.document_id = d.id
            JOIN users owner ON d.owner_id = owner.id
            JOIN users viewer ON p.user_id = viewer.id
            ORDER BY p.granted_at DESC
        """).fetchall()

    return render_template(
        "admin_dashboard.html",
        username=admin["username"],
        total_users=total_users,
        total_documents=total_documents,
        total_shares=total_shares,
        users=users,
        documents=documents,
        shares=shares
    )
@app.route("/audit-logs")
def audit_logs():
    if "user_id" not in session:
        return redirect(url_for("login"))

    with get_db() as db:
        admin = db.execute(
            "SELECT username, role FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        if admin is None or admin["role"] != "admin":
            abort(403)

        logs = db.execute("""
            SELECT id, username, action, document_id, details, created_at
            FROM audit_logs
            ORDER BY created_at DESC, id DESC
        """).fetchall()

    return render_template(
        "audit_logs.html",
        username=admin["username"],
        logs=logs
    )
@app.route("/upload", methods=["GET", "POST"])
def upload():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    with get_db() as db:
        user = db.execute(
            "SELECT id, role FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    if not user:
        session.clear()
        abort(401)

    if user["role"] != "owner":
        abort(403)

    if request.method == "GET":
        return render_template("upload.html")

    file = request.files.get("document")
    category = request.form.get("category", "")

    if not file or not file.filename:
        return "Please select a document.", 400

    if category not in {"Academic", "Personal", "Official", "Other"}:
        return "Invalid category.", 400

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return "File type not allowed.", 400

    # Read and validate the actual content, not just the extension.
    content = file.read()

    if not content:
        return "Empty files are not allowed.", 400

    if extension == ".pdf" and not content.startswith(b"%PDF-"):
        return "Invalid PDF file.", 400

    if extension == ".png" and not content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "Invalid PNG file.", 400

    if extension in {".jpg", ".jpeg"} and not (
        content.startswith(b"\xff\xd8\xff") and content.endswith(b"\xff\xd9")
    ):
        return "Invalid JPEG file.", 400

    if extension == ".txt":
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            return "Invalid text file.", 400

    stored_name = uuid4().hex + extension
    destination = UPLOAD_FOLDER / stored_name

    try:
        with open(destination, "xb") as saved_file:
            saved_file.write(content)

        with get_db() as db:
            db.execute("""
                INSERT INTO documents
                (owner_id, original_name, stored_name, category)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                file.filename,
                stored_name,
                category
            ))

    except Exception:
        destination.unlink(missing_ok=True)
        app.logger.exception("Document upload failed")
        return "Unable to save document.", 500
    return "Document uploaded and saved in database successfully!"


@app.route("/replace/<int:document_id>", methods=["POST"])
def replace_document(document_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    new_file = request.files.get("document")

    if not new_file or not new_file.filename:
        return "Please select a replacement document.", 400

    original_name = secure_filename(new_file.filename)

    if not original_name:
        return "Invalid filename.", 400

    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return "File type not allowed.", 400

    content = new_file.read()

    if not content:
        return "Empty files are not allowed.", 400

    if extension == ".pdf" and not content.startswith(b"%PDF-"):
        return "Invalid PDF file.", 400

    if extension == ".png" and not content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "Invalid PNG file.", 400

    if extension in {".jpg", ".jpeg"} and not (
        content.startswith(b"\xff\xd8\xff") and content.endswith(b"\xff\xd9")
    ):
        return "Invalid JPEG file.", 400

    if extension == ".txt":
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            return "Invalid text file.", 400

    with get_db() as db:
        document = db.execute("""
            SELECT d.id, d.owner_id, d.stored_name, p.permission
            FROM documents d
            LEFT JOIN document_permissions p
                ON d.id = p.document_id AND p.user_id = ?
            WHERE d.id = ?
        """, (user_id, document_id)).fetchone()

        if document is None:
            abort(404)

        is_owner = document["owner_id"] == user_id
        can_edit = document["permission"] == "edit"

        if not is_owner and not can_edit:
            abort(403)

        old_stored_name = document["stored_name"]

        new_stored_name = uuid4().hex + extension
        new_path = UPLOAD_FOLDER / new_stored_name

        try:
            with open(new_path, "xb") as saved_file:
                saved_file.write(content)

            db.execute("""
            UPDATE documents
            SET original_name = ?,
                stored_name = ?,
                uploaded_at = datetime('now', 'localtime')
            WHERE id = ?
            """, (original_name, new_stored_name, document_id))

        except Exception:
            new_path.unlink(missing_ok=True)
            app.logger.exception("Document replacement failed")
            return "Unable to replace document.", 500
    with get_db() as db:
        user = db.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if user:
            log_activity(
                user_id,
                user["username"],
                "DOCUMENT_REPLACED",
                document_id,
                f"Replaced document with {original_name}"
            )
    old_path = UPLOAD_FOLDER / old_stored_name

    try:
        old_path.unlink(missing_ok=True)
    except OSError:
        app.logger.exception("Unable to remove previous document file")

    if is_owner:
        return redirect(url_for("my_documents"))

    return redirect(url_for("shared_documents"))

@app.route("/my-documents")
def my_documents():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    with get_db() as db:
        documents = db.execute("""
            SELECT id, original_name, category, uploaded_at
            FROM documents
            WHERE owner_id = ?
            ORDER BY uploaded_at DESC
        """, (user_id,)).fetchall()

        shares = db.execute("""
            SELECT
                p.document_id,
                u.id AS shared_user_id,
                u.username AS shared_with,
                p.permission,
                p.granted_at
            FROM document_permissions p
            JOIN documents d ON p.document_id = d.id
            JOIN users u ON p.user_id = u.id
            WHERE d.owner_id = ?
            ORDER BY p.granted_at DESC
        """, (user_id,)).fetchall()

    return render_template(
        "my_documents.html",
        documents=documents,
        shares=shares
    )

@app.route("/shared-documents")
def shared_documents():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    with get_db() as db:
        documents = db.execute("""
            SELECT
                d.id,
                d.original_name,
                d.category,
                u.username AS owner_name,
                p.permission,
                p.granted_at
            FROM document_permissions p
            JOIN documents d ON p.document_id = d.id
            JOIN users u ON d.owner_id = u.id
            WHERE p.user_id = ?
            ORDER BY p.granted_at DESC
        """, (user_id,)).fetchall()
        print("TRUSTVAULT DEBUG ROUTE REACHED", flush=True)
    print("DEBUG - Shared documents:", [dict(doc) for doc in documents])

    return render_template(
        "shared_documents.html",
        documents=documents
    )

@app.route("/download/<int:document_id>")
def download_document(document_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    with get_db() as db:
        document = db.execute("""
            SELECT
                d.id,
                d.owner_id,
                d.original_name,
                d.stored_name,
                p.permission
            FROM documents d
            LEFT JOIN document_permissions p
                ON d.id = p.document_id AND p.user_id = ?
            WHERE d.id = ?
        """, (user_id, document_id)).fetchone()

    if document is None:
        abort(404)

    is_owner = document["owner_id"] == user_id
    has_read_permission = document["permission"] in ("read", "edit")

    if not is_owner and not has_read_permission:
        abort(403)

    file_path = UPLOAD_FOLDER / document["stored_name"]

    if not file_path.is_file():
        abort(404)
    with get_db() as db:
        user = db.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    if user:
        log_activity(
            user_id,
            user["username"],
            "DOCUMENT_DOWNLOADED",
            document_id,
            f"Downloaded {document['original_name']}"
        )

    return send_file(
        str(file_path),
        as_attachment=True,
        download_name=document["original_name"]
    )


@app.route("/share/<int:document_id>", methods=["POST"])
def share_document(document_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    owner_id = session["user_id"]
    print("DEBUG - Logged-in user ID:", owner_id)
    print("DEBUG - Document ID:", document_id)

    # Only document owners can share their documents
    with get_db() as db:

        document = db.execute("""
            SELECT id FROM documents
            WHERE id = ? AND owner_id = ?
        """, (document_id, owner_id)).fetchone()

        if document is None:
            abort(403)

        username = request.form.get("username", "").strip()
        permission = request.form.get("permission", "").strip().lower()

        if not username:
            return "Please enter a username.", 400

        if permission not in ("read", "edit"):
            return "Invalid permission.", 400

        target_user = db.execute("""
            SELECT id FROM users
            WHERE username = ?
        """, (username,)).fetchone()

        if target_user is None:
            return "User not found.", 404

        if target_user["id"] == owner_id:
            return "You cannot share a document with yourself.", 400

        db.execute("""
            INSERT INTO document_permissions
                (document_id, user_id, permission)
            VALUES (?, ?, ?)
            ON CONFLICT(document_id, user_id)
            DO UPDATE SET permission = excluded.permission
        """, (document_id, target_user["id"], permission))
        owner = db.execute(
            "SELECT username FROM users WHERE id = ?",
            (owner_id,)
        ).fetchone()

        log_activity(
            owner_id,
            owner["username"],
            "DOCUMENT_SHARED",
            document_id,
            f"Shared with {username} using {permission.upper()} permission",
            db=db
        )
    return redirect(url_for("my_documents"))
@app.route("/revoke-share/<int:document_id>/<int:user_id>", methods=["POST"])
def revoke_share(document_id, user_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    owner_id = session["user_id"]

    with get_db() as db:

        document = db.execute("""
            SELECT id, original_name
            FROM documents
            WHERE id = ? AND owner_id = ?
        """, (document_id, owner_id)).fetchone()

        if document is None:
            abort(403)

        result = db.execute("""
            DELETE FROM document_permissions
            WHERE document_id = ? AND user_id = ?
        """, (document_id, user_id))

        if result.rowcount == 0:
            return "Share permission not found.", 404
        revoked_user = db.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        owner = db.execute(
            "SELECT username FROM users WHERE id = ?",
            (owner_id,)
        ).fetchone()

        log_activity(
            owner_id,
            owner["username"],
            "DOCUMENT_ACCESS_REVOKED",
            document_id,
            f"Revoked access for {revoked_user['username']} to {document['original_name']}",
            db=db
        )

    return redirect(url_for("my_documents"))
if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5002, debug=False)