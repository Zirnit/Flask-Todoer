import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="mikey",
        DATABASE_HOST=os.getenv("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.getenv("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.getenv("FLASK_DATABASE_USER"),
        DATABASE=os.getenv("FLASK_DATABASE"),
    )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import todo
    app.register_blueprint(todo.bp)
    

    @app.route("/hola")
    def hola():
        return "Chanchito feliz"
    return app
