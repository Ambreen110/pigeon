from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    with app.app_context():
        from .routes import main_bp
        from .admin_routes import admin_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        db.create_all()

    return app
