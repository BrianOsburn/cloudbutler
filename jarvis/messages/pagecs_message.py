# -*- coding: utf-8 -*-

"""
Starts dialog with requester for pagecs
"""

from jarvis_run import logger, db, sc
from jarvis.slack_utilities.validate_call import validate_request


def gen_message_one(callback, trigger):
    """
    Generates popup for the requester
    :param callback:
    :param trigger:
    :return:
    """

    logger.debug("Passed values - callback:  %s", callback)
    logger.debug("Passed values - trigger:  %s", trigger)

    test = sc.api_call("dialog.open", timeout=None, trigger_id=trigger,
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

    logger.debug(test)

    #return('', 200)
