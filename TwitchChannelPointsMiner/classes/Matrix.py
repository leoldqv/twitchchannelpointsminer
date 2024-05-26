from textwrap import dedent
import sys
import logging
import requests
from urllib.parse import quote

sys.path.append("/home/leoscoding/PointsMiner/TwitchChannelPointsMiner/classes/")
from Settings import Events


class Matrix(object):
    __slots__ = ["access_token", "homeserver", "room_id", "events"]

    def __init__(self, username: str, password: str, homeserver: str, room_id: str, events: list):
        self.homeserver = homeserver
        self.room_id = quote(room_id)
        self.events = [str(e) for e in events]

        body = requests.post(
            url=f"https://{self.homeserver}/_matrix/client/r0/login",
            json={
                "user": username,
                "password": password,
                "type": "m.login.password"
            }
        ).json()

        self.access_token = body.get("access_token")

        if not self.access_token:
            logging.getLogger(__name__).info("Invalid Matrix password provided. Notifications will not be sent.")

    def send(self, message: str, event: Events) -> None:
        if str(event) in self.events:
            requests.post(
                url=f"https://{self.homeserver}/_matrix/client/r0/rooms/{self.room_id}/send/m.room.message?access_token={self.access_token}",
                json={
                    "body": dedent(message),
                    "msgtype": "m.text"
                }
            )
