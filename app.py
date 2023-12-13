import os

import flask
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from database import db
from routes.user import user_bp
from routes.animal import animals_bp
from routes.vaccine import vaccine_bp
from routes.ima import ima_bp


def create_app():
    """App factory"""
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(vaccine_bp)
    app.register_blueprint(ima_bp)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mycowsdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/health-check')
    def health_check():
        return flask.render_template("healthcheck.html")

    return app


if __name__ == "__main__":
    current_app = create_app()
    current_app.run(debug=True)
