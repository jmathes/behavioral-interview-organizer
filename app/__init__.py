from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import importlib
import os

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

for file in os.listdir(dir_path):
    # Check if the file is a Python module and not this __init__.py file
    if file.endswith(".py") and not file.startswith("__"):
        # Remove the extension from the file name to get the module name
        module_name = file[:-3]
        # Import the module dynamically
        importlib.import_module(f"app.models.{module_name}")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import and register blueprints/routes here
    from app.routes import bio_bp

    app.register_blueprint(bio_bp)

    return app, migrate


app, migrate = create_app()

if __name__ == "__main__":
    app.run(debug=True)
