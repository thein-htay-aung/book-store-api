from flask import Flask
from db import init_db, close_db
from routes.authors import authors_bp
from routes.books import books_bp

def create_app():
    app = Flask(__name__)

    app.teardown_appcontext(close_db)
    init_db(app)

    app.register_blueprint(authors_bp, url_prefix="/authors")
    app.register_blueprint(books_bp, url_prefix="/books")

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)