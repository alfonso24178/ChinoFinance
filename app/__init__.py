from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # <-- Importante

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chinofinance-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinofinance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # <-- Importante

    from app.routes import main
    app.register_blueprint(main)

    return app
