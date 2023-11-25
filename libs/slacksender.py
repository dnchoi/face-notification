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


def main():
    sender = SlackSender(
        token="xoxb-968063259266-6244532290821-ChGXh7aIMgJ9tmr296s5ypvB",
    )
    response = sender.message_sender(
        channel="C0328RWS0E7",
        message="Hello python",
    )
    print(response)


if __name__ == "__main__":
    main()
