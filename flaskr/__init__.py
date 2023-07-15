# imports
import os
from flask import Flask

# creation and configuration of the app factory


def create_app(test_config=None):
    # __name__ is the name of the current Python module.
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_mapping() sets some default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # you can use a config.py file or create a dict to instantiate create_app
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except Exception as e:
        pass

    @app.route('/hello')
    def hello():
        return '<h1>Hello, World!</h1>'

    return app
