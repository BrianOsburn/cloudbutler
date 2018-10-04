"""
Kicks off interactive messaging to page out Support
/page_cs
"""

from random import randint
from flask import jsonify, request, make_response
from jarvis import jarvis_app
from jarvis_run import logger, db, sc
from jarvis.slack_utilities.validate_call import validate_request
from jarvis.slack_utilities.lookup_user import lookup_username
from jarvis.messages.pagecs_message import gen_message_one
import requests
import re


@jarvis_app.route('/pagecs', methods=["POST"])
def pagecs():
    """
    Kicks off interactive messaging to page out Cloud Support
    """
    logger.info("pagecs function called")
    validate_request(request)

    #  Generate random callback ID
    callback_number = randint(10000, 99999)
    callback_id = "pagecs-" + str(callback_number)

    logger.info("Page request received from %s", request.form['user_name'])

    logger.info("Calling popup")
    logger.debug("callback_id = %s", callback_id)
    logger.debug("trigger = %s", request.form['trigger_id'])
    gen_message_one(callback_id, request.form['trigger_id'])

    return('', 200)


def parse_casenumber(casenumber):
    """
    Takes the case number, validates it's either a SFDC case format
    or a JIRA.
    sfdc case = 6 / 7 / 8 digits long
    jira = [\w]+\-[\d]
    Can't validate if they're REAL cases though

    :param casenumber:
    :return casetype, caselink:
    """

    sfdc_regex = "^[\d]{6,8}$"
    jira_regex = "^[\w]+\-[\d]+$"

    if re.search(sfdc_regex, casenumber):
        casetype = "SFDC"
        caselink = "https://splunk.my.salesforce.com/_ui/search/ui/UnifiedSearchResults?str=" + casenumber
        logger.info("Case type is identified as SFDC.   CaseLink = %s", caselink)

    elif re.search(jira_regex, casenumber):
        casetype = "JIRA"
        caselink = "https://jira.splunk.com/browse/" + casenumber
        logger.info("Case type is identified as JIRA.  CaseLink = %s", caselink)

    else:
        casetype = "Unknown"
        caselink = "Unknown"
        logger.warning("Case type is set to unknown")

    return casetype, caselink


def process_response(form_response):
    """
    Processes responses from the form for paging cloud support
    inserts it into the DB
    and returns a response
    :param form_response:
    :return:
    """

    submitter_uid = form_response["user"]["id"]
    submitter_name = lookup_username(submitter_uid)
    case_number = form_response["submission"]["case_number"]
    case_priority = form_response["submission"]["priority"]
    case_description = form_response["submission"]["description"]
    channel = form_response["channel"]["id"]

    (case_type, case_link) = parse_casenumber(case_number)

    logger.info("Sending update to requester")




