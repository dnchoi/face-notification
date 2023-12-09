from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackSender:
    def __init__(
        self,
        token,
    ) -> None:
        self.client = WebClient(token=token)

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
            print(f"error message - {e_msg.response['error']}")
