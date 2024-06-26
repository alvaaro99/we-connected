from flask import Flask
import os
from flask_jwt_extended import JWTManager
from neomodel import install_all_labels

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        JWT_SECRET_KEY = "jwt-secret123",
        FERNET_KEY='tqRu_aP1o9zOvDMD4dBoZhyUb92nTcT4U4nM2ml_p90='
    )
    
    JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config['TESTING'] is not True:
        from . import db
        db.init_app(app)

        from . import auth, person
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(person.person_bp)

        install_all_labels()
    return app
