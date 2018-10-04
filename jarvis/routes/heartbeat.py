"""
Simple check to see if the app is functioning
"""

from flask import jsonify, request
from jarvis import jarvis_app
from jarvis_run import logger
from jarvis.slack_utilities.validate_call import validate_request


@jarvis_app.route('/heartbeat', methods=["POST"])
def heartbeat():
    logger.info("Heartbeat function called")
    validate_request(request)
    heartbeat_message = {'text':  'I\'m Alive'}

    return jsonify(heartbeat_message)

