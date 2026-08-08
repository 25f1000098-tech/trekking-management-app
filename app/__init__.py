from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # redirects here if login required but not logged in

    with app.app_context():
        from app import models
        db.create_all()

        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.staff import staff_bp
    app.register_blueprint(staff_bp)

    from app.routes.user import user_bp
    app.register_blueprint(user_bp)
    
    return app