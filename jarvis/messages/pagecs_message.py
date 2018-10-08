# -*- coding: utf-8 -*-

"""
Starts dialog with requester for pagecs
"""

from jarvis_run import logger, sc, app_config
from datetime import datetime
from functools import singledispatch
from pytz import timezone

#  Define functions
@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)


@to_serializable.register(datetime)
def ts_datetime(val):
    """Used if *val* is an instance of datetime."""
    return val.isoformat() + "Z"


def generate_timestamp():
    """
    Generates timestamp for insertion into the DB in epoch format
    Timezone is set to pacific time for standardization
    :return timestamp, current_time:
    """

    pacific_time = timezone('America/Los_Angeles')
    current_time = datetime.now(pacific_time)
    timestamp = current_time.timestamp()

    return timestamp, current_time


def gen_message_one(callback, trigger):
    """
    Generates popup for the requester
    :param callback:
    :param trigger:
    :return:
    """

    logger.debug("Passed values - callback:  %s", callback)
    logger.debug("Passed values - trigger:  %s", trigger)

    sc.api_call("dialog.open", timeout=None, trigger_id=trigger,
                dialog={
                            "callback_id":  callback,
                            "title":  "Notify Cloud Support",
                            "submit_label":  "Submit",
                            "elements":  [
                                {
                                    "type":  "text",
                                    "label":  "Case Number",
                                    "name":  "case_number"
                                },
                                {
                                    "type":  "select",
                                    "label":  "Priority",
                                    "name":  "priority",
                                    "options":  [
                                        {
                                            "label":  "P1",
                                            "value":  "P1"
                                        },
                                        {
                                            "label":  "P2",
                                            "value":  "P2"
                                        },
                                        {
                                            "label":  "P3",
                                            "value":  "P3"
                                        },
                                        {
                                            "label":  "P4",
                                            "value":  "P4"
                                        }
                                    ]
                                },
                                {
                                    "type":  "textarea",
                                    "label":  "Description of issue",
                                    "name":  "description",
                                    "hint":  "Be as descriptive as possible"
                                },
                            ]
                        }
                       )


def gen_support_notification(case_number, case_link, case_description, case_priority, submitter):
    """
    Sends notification to specified room(s)
    :param case_number:
    :param case_link:
    :param case_description:
    :param case_priority:
    :param submitter:
    :return:
    """

    for channel in app_config['pagecs']['posttorooms']:
        logger.info("Found the following channels:  %s", channel)

        #  Get the Slack Room Names
        logger.info("Channel Name:  %s", channel)

        fallback_text = "Case notification for " + case_number

        (timestamp, current_time) = generate_timestamp()

        sc.api_call("chat.postMessage", timeout=None, channel=channel,
                    attachments=[{
                                        "fallback": fallback_text,
                                        "color": "#0000FF",
                                        "pretext": "Case Notification Received",
                                        "title": case_number,
                                        "title_link": case_link,
                                        "text": case_description,
                                        "fields": [
                                            {
                                                "title": "Priority",
                                                "value": case_priority,
                                                "short": True
                                            },
                                            {
                                                "title": "Submitted",
                                                "value": submitter,
                                                "short": True
                                            },
                                            {
                                                "title": "Time Submitted",
                                                "value": to_serializable(
                                                    current_time.strftime('%m/%d/%y - %H:%M:%S - %Z')
                                                                         ),

                                                "short": False
                                            }
                                        ],
                                        "footer": "Jarvis",
                                        "ts": to_serializable(timestamp)
                                    }
                                    ]
                                   )
