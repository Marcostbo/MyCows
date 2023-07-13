import os

from flask import Flask
from flask_migrate import Migrate
from database import db
from routes.user import user_bp
from routes.cow import cows_bp


def create_app():
    """App factory"""
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(cows_bp)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)
    migrate = Migrate(app, db)

    return app


if __name__ == "__main__":
    current_app = create_app()
    current_app.run(debug=True)
