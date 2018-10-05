from jarvis_run import sc, logger


def lookup_username(user_id):
    """
    Takes the userid and returns the full user name.
    It accomplishes this by connecting to the slack api using users.info
    and getting the real_name_normalized from the results
    This is per Slacks Warning that name will be going away
    sc = slackclient connection
    user_id = user id to look up
    :param sc, user_id:
    :return user_full_name:
    """

    logger.info("Looking up user name from Slack API")
    profile = sc.api_call("users.info", timeout=None, user=user_id)
    logger.debug("Profile returned:  ")
    logger.debug(profile)
    user_full_name = profile['user']['profile']['real_name_normalized']

    return user_full_name
