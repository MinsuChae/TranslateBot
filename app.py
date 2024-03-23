from dotenv import load_dotenv
import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event
from function.command import command
import sys

if os.path.exists(".env"):
    env_path = ".env"
    load_dotenv(env_path)

if "SLACK_APP_TOKEN" not in os.environ or "SLACK_BOT_TOKEN" not in os.environ:
    print("Please set SLACK_APP_TOKEN and SLACK_BOT_TOKEN environment.\n",file=sys.stderr)
    exit(1)

client = SocketModeClient(
    app_token=os.environ["SLACK_APP_TOKEN"],
    web_client=WebClient(token=os.environ["SLACK_BOT_TOKEN"])
)

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        channel = req.payload["event"]["channel"]
        event_type = req.payload["event"]["type"]
        thread_ts = req.payload["event"]["event_ts"] # Reply

        if event_type == "message":
            message = req.payload["event"]["text"]
            is_bot = "bot_id" in req.payload["event"] # Ignore bot message

            if not is_bot:
                parsing = message.split(maxsplit=1)
                parsing = [text.strip() for text in parsing]

                result = command(cmd=parsing[0], )
                if result is not None:
                    client.web_client.chat_postMessage(channel=channel, text=result, thread_ts=thread_ts)

client.socket_mode_request_listeners.append(process)
client.connect()
Event().wait()
