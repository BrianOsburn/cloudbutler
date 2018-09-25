"""
Adds user to the DB
Usage:  /adduser @name (user|manager)
"""

from flask import jsonify, request, make_response
from jarvis import jarvis_app
from jarvis_run import logger, db
from jarvis.slack_utilities.validate_call import validate_request
import re


@jarvis_app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """
    Adds users to the database:
    /adduser @name (user|manager)
    :return:
    """

    logger.info("Add User function called")
    validate_request(request)
    logger.debug("Event Received: \n %s", request)

    #  Check to make sure arguments are passed
    if not request.form['text']:
        message = {'text':  'No arguments specified, please try again'}
        return jsonify(message)

    #  Check to make sure it's a valid user in slack


    #  Get the arguments
    regex = '^<@([^|]+)\|([^>]+)>\s(manager|user)'

    #  Check to find there are three matches:
    logger.debug("Found this many options given:  %s", re.compile(regex).groups)
    

    #regex_match = re.match(r'^<@([^|]+)\|([^>]+)>\s(manager|user)', request.form['text'], re.M|re.I)
    #arguments = request.form['text']
    #(user, add_role) = arguments.split(" ")



    #match_objects = re.match(r'^\<\@([^|]+)\|([^>]+)\>\s(manager|user)', user, re.M|re.I)
    #regex_match = re.match(r'^<@([^|]+)\|([^>]+)>', user, re.M|re.I)
    #logger.debug("Match_objects:  %s", match_objects)

    #if regex_match:
    #    add_username = match_objects.group(1)
    #    add_userid = match_objects.group(2)
    #    logger.info("found add_name:  %s", add_username)
    #    logger.info("found add_userid:  %s", add_userid)


    #logger.debug("Received following request:  %s", request.form)

    heartbeat_message = {'text':  'gotit'}
    return jsonify(heartbeat_message)

