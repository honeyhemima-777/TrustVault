from app import app, get_db

with app.test_client() as client:
    with get_db() as db:
        user = db.execute(
            "SELECT id FROM users WHERE username = ?",
            ("viewer",)
        ).fetchone()

    with client.session_transaction() as session:
        session["user_id"] = user["id"]

    for page in ["/dashboard", "/shared-documents"]:
        response = client.get(page)
        print("\nPAGE:", page)
        print("STATUS:", response.status_code)
        print("CONTENT:")
        print(response.data.decode("utf-8", errors="replace")[:500])