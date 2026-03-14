from flask import Flask, render_template
from sqlalchemy import select
from myapp.extensions import db,login_manager
from myapp.models import User
from myapp.errors import register_errors
from myapp.commands import register_commands
from myapp.settings import config
from myapp.blueprints.main_bp import main_bp

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(main_bp)

    db.init_app(app)
    login_manager.init_app(app)

    register_errors(app)
    register_commands(app)

    @app.route('/')
    def index():
        return render_template("basic_page.html")

    return app