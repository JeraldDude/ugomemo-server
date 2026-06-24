
# Nintendo Authentication Server ( Nintendo DSi, Flipnote Hatena service )
import random
import string
from datetime import datetime

class NasServer:
    def __init__(self):
        pass

    # Main entry point: handle POST /ac
    def handle_ac_request(self, body: str, client_ip: str) -> str:
        action = self._get_param(body, "action")

        if action != "login":
            return "returncd=600\nretry=0\n"

        challenge = self._random_challenge(8)
        timestamp = self._nas_datetime()

        token_data = "DUMMYTOKEN"
        token = self._build_token(challenge, client_ip, token_data)

        return (
            f"challenge={challenge}\n"
            f"locator=gamespy.com\n"
            f"retry=0\n"
            f"returncd=001\n"
            f"token={token}\n"
            f"datetime={timestamp}\n"
        )

    def _get_param(self, body: str, key: str) -> str:
        for part in body.split("&"):
            if part.startswith(key + "="):
                return part.split("=", 1)[1]
        return ""

    def _random_challenge(self, length: int) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def _nas_datetime(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d%H%M%S")

    def _build_token(self, challenge: str, client_ip: str, token_data: str) -> str:
        return f"NDS/0/{challenge}/no-gsbrcd/{client_ip}|{token_data}/{token_data}"
