from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import importlib
import os
import shutil

dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

for file in os.listdir(dir_path):
    # Check if the file is a Python module and not this __init__.py file
    if file.endswith(".py") and not file.startswith("__"):
        # Remove the extension from the file name to get the module name
        module_name = file[:-3]
        # Import the module dynamically
        importlib.import_module(f"app.models.{module_name}")


def ensure_db(instance_path):
    """Return the path to the working db, creating it from the placeholder if missing.

    instance/app.db holds your own stories and is gitignored. instance/placeholder.db
    is the empty starter db (schema, questions, principles, no stories) that's checked in.
    """
    db_path = os.path.join(instance_path, "app.db")
    if not os.path.exists(db_path):
        os.makedirs(instance_path, exist_ok=True)
        shutil.copyfile(os.path.join(instance_path, "placeholder.db"), db_path)
    return db_path


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + ensure_db(app.instance_path)
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
