"""
Kicks off interactive messaging to page out Support
/page_cs
"""

from flask import jsonify, request, make_response
from jarvis import jarvis_app
from jarvis_run import logger, db
from jarvis.slack_utilities.validate_call import validate_request
from jarvis.models.models import Users
import requests
import re

@jarvis_app.route('/pagecs', methods='POST')
def pagecs():
    """
    Kicks off interactive messaging to page out Cloud Support

    """


@jarvis_app.route('/listener', methods='post')
def listener():
    """
    Listens for events for messaging
    :return:
    """

