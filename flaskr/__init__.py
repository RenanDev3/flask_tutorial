# imports
import os
from flask import Flask

# creation and configuration of the app factory


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except Exception as e:
        raise e

    @app.route('/hello')
    def hello():
        return '<h1>Hello, World!</h1>'

    return app
