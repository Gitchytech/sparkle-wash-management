from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-change-this"

    if test_config is not None:
        app.config.update(test_config)

    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
