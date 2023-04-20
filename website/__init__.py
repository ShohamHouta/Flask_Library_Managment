from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "Library.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Secret Key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    from .models import Book, User

    with app.app_context():
        if not path.exists("website/"+DB_NAME):
            db.create_all()
            print("Created Database!")

    login_manager = LoginManager()
    login_manager.login_view = "auth.Login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
