"""
Simple check to see if the app is functioning
"""

from flask import jsonify, request
from jarvis import jarvis_app
from jarvis_run import logger
from jarvis.slack_utilities.validate_call import validate_request


@jarvis_app.route('/echo', methods=["POST"])
def echo():
    logger.info("Echo function called")
    validate_request(request)
    logger.info(request.form)
    echo_message = {'text':  'Echo Completed'}
    return jsonify(echo_message)

