from flask import Blueprint, request, jsonify
from db import get_db
from config import SECRET_API_KEY

authors_bp = Blueprint('authors', __name__)

def require_api_key(req):
    key = req.headers.get('X-API-KEY')
    return key == SECRET_API_KEY

@authors_bp.get("/")
def get_authors():
    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    db = get_db()
    authors = db.execute(
        "SELECT * FROM authors ORDER BY id DESC"
    ).fetchall()
    
    return jsonify([dict(a) for a in authors])

@authors_bp.post("/create")
def add_author():
    if not require_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    name = data.get("name")
    country = data.get("country")
    birth_year = data.get("birth_year")

    if not name:
        return jsonify({"error": "Missing required field: name."}), 400
    
    db = get_db()
    cur = db.execute(
        "INSERT INTO authors (name, country, birth_year)"
        " VALUES(?, ?, ?)",
        (name, country, birth_year)
    )
    db.commit()
    
    new_id = cur.lastrowid
    author = db.execute(
        "SELECT * FROM authors WHERE id=?", (new_id, )
    ).fetchone()
    return jsonify(dict(author)), 201


