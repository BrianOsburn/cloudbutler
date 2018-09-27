"""
Adds user to the DB
Usage:  /adduser @name (user|manager)
"""

from flask import jsonify, request, make_response
from jarvis import jarvis_app
from jarvis_run import logger, db
from jarvis.slack_utilities.validate_call import validate_request
from jarvis.models.models import Users
import requests
import re


@jarvis_app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """
    Adds users to the database:
    /adduser @name (user|manager)
    :return:
    """

    logger.info("Add User function called")

    #  Validate the request from Slack
    validate_request(request)

    #  Check to make sure arguments are passed
    if not request.form['text']:
        message = {'text':  'No arguments specified, please try again'}
        return jsonify(message)

    #  Regex to check to see it matches expected pattern
    # <@userid|username> (manager|user)

    regex = '^<@([^|]+)\|([^>]+)>\s+(manager|user)'

    #  If the search doesn't match that format, something is up
    if re.search(regex, request.form['text'], re.M|re.I) is None:
        logger.info("Invalid Request Received")
        message = {'text':  'Invalid Request - please double check your formatting - /adduser @username (user|manager)'}
        return jsonify(message)

    #  Get the capture group results
    match_object = re.search(regex, request.form['text'], re.M|re.I)

    #  Assign the capture groups
    slack_uid = match_object.group(1)
    slack_uname = match_object.group(2)
    role = match_object.group(3)

    #  Give processing message
    message = {'text':  'Processing request...'}
    response_url = request.form['response_url']
    requests.post(response_url, json=message)

    #  Check to see if requester has access to add users
    req_userid = request.form['user_id']
    user_check = Users.query.filter_by(slack_id=req_userid).first()

    #  If requesting user isn't in the db or is only a user, they cannot update / add users
    if user_check is None:
        logger.info("Requesting user is not in the database:  %s", req_userid)
        message = {'text': 'Unfortunately you do not have the ability to add users.'}
        return jsonify(message)

    if user_check.role != 'manager':
        logger.info("Unable to add user due to missing permissions")
        message = {'text':  'Unfortunately you do not have the ability to add users.'}
        requests.post(response_url, json=message)

    #  Check to see if the user exists, if it does, then run update. Otherwise add
    user_check = Users.query.filter_by(slack_id=slack_uid).first()

    #  If the user to be added doesn't exist, add the user.
    #  Otherwise, update the user
    if user_check is None:
        logger.info("User doesn't exist, so will ADD the user")
        message = {'text': 'User does not exist, so we are going to ADD them.'}
        requests.post(response_url, json=message)

        #  Update the DB Object
        user = Users(slack_id=slack_uid, slack_name=slack_uname, role=role)
        db.session.add(user)
        db.session.commit()

        logger.info("Added new user: user_name=%s, user_id=%s, role=%s", slack_uname, slack_uid, role)

    if user_check is not None:
        logger.info("User exists, running update.")
        message = {'text':  'User exists, so we are going update them.'}
        requests.post(response_url, json=message)

        #  Update the Object data
        user_check.slack_id = slack_uid
        user_check.slack_name = slack_uname
        user_check.role = role

        db.session.commit()
        logger.info("Updated user:  %s", slack_uname)

    #  Send final message
    message = {'text':  ':sun_small_cloud:  Request has been completed at this time'}
    requests.post(response_url, json=message)
    return 200


