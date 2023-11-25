from libs.slacksender import SlackSender
from libs.logger import Logger
import os
from libs import utils as ut
logger = None

def main(slack_cfg:dict,):
    global logger

    sender = SlackSender(
        token=slack_cfg["token"],
    )
    response = sender.message_sender(
        channel=slack_cfg["channel"],
        message="Hello python",
    )
    logger.info(response)


if __name__ == "__main__":
    cfg = ut.read_config("config.json")
    slack_cfg = cfg["slack"]
    log_cfg = cfg["log"]

    logger = Logger(
        class_name=os.path.basename(__file__).split(".")[0],
        level=log_cfg["level"],
        file_path=log_cfg["dst"],
        save=log_cfg["save"],
    ).logger

    main(slack_cfg=slack_cfg)
