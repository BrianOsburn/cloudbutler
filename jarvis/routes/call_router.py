"""
Routes incoming requests from slack
"""

from flask import jsonify, request, make_response
from jarvis import jarvis_app
from jarvis_run import logger
from jarvis.slack_utilities.validate_call import validate_request
from jarvis.routes.page_cs import process_response
import json


@jarvis_app.route('/event_listener', methods=['Post'])
def message_receiver():
    """
    Message Endpoint from Slack
        Validates the incoming message
        Pulls the callback_id to determine what app to route to
        Hands off to the specific def for that app to handle

    :return:
    """
    validate_request(request)

    logger.info("Valid Received Message from Slack")

    message = json.loads(request.form['payload'])
    request_type = message["callback_id"]

    if request_type.startswith('pagecs'):
        logger.info("Received message for pagecs")

        logger.debug("Received the following:")
        logger.debug(message)

        process_response(message)
        return ('', 200)

    message = {'text': 'Configuration not found for request'}
    logger.warning("Request received for unconfigured request_type:  %s", request_type)
    return jsonify(message)



