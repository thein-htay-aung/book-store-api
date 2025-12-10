from flask import Blueprint, request, jsonify
from db import get_db
from config import SECRET_API_KEY

books_bp = Blueprint('books', __name__)

def require_api_key(req):
    key = req.headers.get('X-API-KEY')
    return key == SECRET_API_KEY

@books_bp.get('/')
def get_books():
    if not require_api_key(request):
        return jsonify({"error": "Unauthorized."}), 401
    
    db = get_db()
    books = db.execute(
        "SELECT b.*, a.name AS author_name"
        " FROM books b LEFT JOIN authors AS a ON b.author_id=a.id"
    ).fetchall()
    
    return jsonify([dict(b) for b in books])

@books_bp.post('/create')
def add_book():
    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    author_id = data.get("author_id")
    release_date = data.get("release_date")
    isbn = data.get("isbn")

    if not name or not author_id:
        return jsonify({"error": "Missing required fields: name or author_id"}), 400
    
    db = get_db()
    
    # ------------------    Check author
    author = db.execute(
        "SELECT name FROM authors WHERE id=?", (author_id,)
    ).fetchone()
    
    if not author:
        return jsonify({"error": "Author doesn't exists."}), 400
    
    # ------------------

    cur = db.execute(
        "INSERT INTOR books (name, description, author_id, release_date, isbn)"
        " VALUES(?, ?, ?, ?, ?)",
        (name, description, author_id, release_date, isbn)
    )
    
    db.commit()
    
    new_id = cur.lastrowid
    book = db.execute(
        "SELECT * FROM books WHERE id=?", (new_id,)
    ).fetchone()
    
    return jsonify(dict(book)), 201