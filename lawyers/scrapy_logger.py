import logging
import lawyers.settings as settings
from SlackLogger import SlackHandler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if settings.SLACK_WEBHOOK:
        slack_handler = SlackHandler(settings.SLACK_WEBHOOK)
        logger.addHandler(slack_handler)

    return logger
