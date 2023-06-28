import os

from flask import Flask

from database import db
from routes.user import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
