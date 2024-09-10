import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    
    db.init_app(app)

    import main.resources as resources
    api.add_resource(resources.MatchesResource, "/matches")
    api.add_resource(resources.MatchResource, "/match/<id>")
    
    api.init_app(app)

    # Registration of authentication routes
    from main.auth import routes
    app.register_blueprint(routes.auth)

    return app