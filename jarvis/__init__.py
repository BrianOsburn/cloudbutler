# -*- coding:  utf-8 -*-

"""
Jarvis - Cloud Support Butler and Notification
"""

#  imports below:
import os
import sys
import yaml
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#  Set the app name
jarvis_app = Flask(__name__, template_folder='../templates')


#  Initialize Config File
def init_config():
    """
    Reads jarvis.yaml file, returns config handle
    :return:
    app_config config dict
    """

    app_config_file = os.path.join(os.getcwd(), "config/jarvis.yaml")

    if not os.path.isfile(app_config_file):
        print("Couldn't find config file at %s", app_config_file)
        sys.exit(1)

    with open(app_config_file, 'r') as configfile:
        app_config = yaml.load(configfile)

    return app_config


def init_logging():
    """
    Sets up logging using logging.yaml
    :return:
    """

    log_config_file = os.path.join(os.getcwd(), "config/logging.yaml")

    if not os.path.isfile(log_config_file):
        print("Could not find logging config at %s", log_config_file)
        sys.exit(1)

    with open(log_config_file, 'rt') as log_cf:
        log_config = yaml.safe_load(log_cf.read())
        logging.config.dictConfig(log_config)

    logging.info("Logging initialized")

    return logging


def init_db(flask_app, app_config):
    """
    Initializes SQLITE instance
    :param flask_app:
    :param app_config:
    :return db:
    """

    db_filename = app_config['sqlite']['db_name']
    db_location = app_config['sqlite']['directory']
    db_fullpath = os.path.join(os.getcwd(), db_location, db_filename)
    db_name = "sqlite:///" + db_fullpath

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_name
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not os.path.isdir(db_location):
        try:
            os.mkdir(db_location)
        except OSError as e:
            logging.critical("Couldn't create DB Directory")
            logging.critical(e)
            sys.exit(1)

    db = SQLAlchemy(flask_app)

    return db

