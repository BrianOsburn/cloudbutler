"""
Kicks off interactive messaging to page out Support
/page_cs
"""

from random import randint
from flask import request
from jarvis import jarvis_app
from jarvis_run import logger, db, sc
from jarvis.slack_utilities.validate_call import validate_request
from jarvis.slack_utilities.lookup_user import lookup_username
from jarvis.messages.pagecs_message import gen_message_one, gen_support_notification
from jarvis.models.models import TicketQueue, TicketDetails
import json
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


def check_ticket(ticket_number):
    """
    Checks for the existence of the ticket in the DB.  If it does, redirect the user to use /escalate
    :param ticket_number:
    :return:
    """

    ticket_check = TicketQueue.query.filter_by(case_number=ticket_number).first()
    logger.info("Checking for existence of ticket:  %s", ticket_number)

    if ticket_check is not None:
        logger.info("Ticket exists, redirecting to use the escalate command")
        exists = True

    if ticket_check is None:
        logger.info("Ticket does not exist, okay to insert")
        exists = False

    return exists


def update_user(update_message, response_url):
    """
    Updates the customer and does error checking
    :param update_message:
    :param response_url:
    :return:
    """

    response = requests.post(
        response_url, data=json.dumps(update_message),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        logger.critical("Unable to post to slack - error:  %s", response.status_code)
        logger.critical("Response text:  %s", response.text)


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

    (case_type, case_link) = parse_casenumber(case_number)

    logger.info("Sending update to requester")
    response_url = form_response['response_url']
    update_user1 = {'text': ':mostly_sunny: Working on request now'}

    update_user(update_user1, response_url)

    ticket_exists = check_ticket(case_number)

    if ticket_exists is True:
        update_user2 = {'text': ':mostly_sunny:  Ticket exists in DB.  Please use /escalate command'}
        update_user(update_user2, response_url)
        return('', 200)

    else:
        update_user2 = {'text': ':mostly_sunny:  Ticket does not exist in DB, adding and notifying'}
        update_user(update_user2, response_url)
        status = "New"

    logger.debug("Submitting the following to the DB:")
    logger.debug("case_number:  %s", case_number)
    logger.debug("req_uid:  %s", submitter_uid)
    logger.debug("req_name:  %s", submitter_name)
    logger.debug("status:  %s", status)
    logger.debug("priority:  %s", case_priority)
    logger.debug("description:  %s", case_description)
    logger.debug("casetype:  %s", case_type)
    logger.debug("case_link:  %s", case_link)

    #  Update the main ticket table
    ticketqueue = TicketQueue(case_number=case_number,
                              req_uid=submitter_uid,
                              req_uname=submitter_name,
                              status=status,
                              priority=case_priority,
                              description=case_description,
                              casetype=case_type,
                              case_link=case_link)

    db.session.add(ticketqueue)

    #  Update the ticket details table
    ticketdetails = TicketDetails(case_number=case_number,
                                  event="Initial Page",
                                  update_uid=submitter_uid,
                                  update_uname=submitter_name)

    db.session.add(ticketdetails)

    #  Commit to DB
    db.session.commit()

    logger.info("Ticket added to the database")


    #  Notify Cloud Support Chat
    gen_support_notification(case_number, case_link, case_description, case_priority, submitter_name)

    #  Send successful message

    update_user3 = {'text': ':sunny:  Ticket submitted'}
    update_user(update_user3, response_url)

    return('', 200)








