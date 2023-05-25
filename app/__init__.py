import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s in %(module)s] '%(message)s' in func: %(func)s",
                "datefmt": "%d.%m.%y %H:%M:%S",
            },
            "minimum": {
                "format": f"%(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "minimum",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "app.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
        "loggers": {
            "extra": {
                "level": "DEBUG",
                "handlers": ["file"],
                "propagate": False,
            }
        },
    }
)

logger = logging.getLogger('extra')

def create_app(test_config=None):
    """The Application factory"""
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db = SQLAlchemy()
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')
    return app

