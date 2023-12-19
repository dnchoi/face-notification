from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from libs.logger import Logger
import os


class SlackSender:
    def __init__(
        self,
        token,
    ) -> None:
        self.client = WebClient(token=token)
        self.logger = Logger(
            class_name=os.path.basename(__file__).split(".")[0],
            lvl="INFO",
            file_path="logs",
        ).logger

    def message_sender(
        self,
        channel,
        message,
    ):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message,
            )
            return response
        except SlackApiError as e_msg:
            self.logger.info(f"error message - {e_msg.response['error']}")

    def file_sender(
        self,
        channel,
        filepath,
        message,
    ):
        try:
            response = self.client.files_upload(
                channels=channel,
                file=filepath,
                initial_comment=message,
            )
            return response
        except SlackApiError as e_msg:
            self.logger.info(f"error message - {e_msg.response['error']}")
