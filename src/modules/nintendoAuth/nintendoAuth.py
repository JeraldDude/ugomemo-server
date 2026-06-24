import random
import string
from datetime import datetime


class NintendoAuth:
    """
    Realistic Nintendo DS/DSi NAS Authentication Module.
    This matches the structure of the real Gamespy NAS server.
    """

    def handle_ac(self, body: str, client_ip: str) -> str:
        params = self._parse_params(body)
        action = params.get("action", "")

        if action != "login":
            return "returncd=600\nretry=0\n"

        # Extract real NAS fields
        userid     = params.get("userid", "")
        password   = params.get("password", "")
        gsbrcd     = params.get("gsbrcd", "")
        macaddr    = params.get("macaddr", "")
        gamecd     = params.get("gamecd", "")
        ingamesn   = params.get("ingamesn", "")
        devname    = params.get("devname", "")
        birthdate  = params.get("birthdate", "")
        region     = params.get("region", "")
        lang       = params.get("lang", "")
        sdkver     = params.get("sdkver", "")
        firmver    = params.get("firmver", "")
        serialnum  = params.get("serialnum", "")

        # Generate challenge
        challenge = self._random_challenge(8)

        # Generate 128‑byte encrypted token (placeholder)
        encrypted_token = self._fake_128_byte_token()

        # Build Gamespy token string
        token = self._build_token(
            challenge=challenge,
            client_ip=client_ip,
            encrypted_token=encrypted_token
        )

        # Timestamp
        timestamp = self._nas_datetime()

        # Build response
        return (
            f"challenge={challenge}\n"
            f"locator=gamespy.com\n"
            f"retry=0\n"
            f"returncd=001\n"
            f"token={token}\n"
            f"datetime={timestamp}\n"
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _parse_params(self, body: str) -> dict:
        params = {}
        for part in body.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v
        return params

    def _random_challenge(self, length: int) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def _nas_datetime(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d%H%M%S")

    def _fake_128_byte_token(self) -> str:
        """
        Placeholder for the real encrypted 128‑byte NAS token.
        Replace this with your real cash later.
        """
        return "".join(random.choice("0123456789ABCDEF") for _ in range(256))

    def _build_token(self, challenge: str, client_ip: str, encrypted_token: str) -> str:
        """
        Real Gamespy token format:
        NDS/0/<challenge>/<gsbrcd>/<ip>|<128byte>/<128byte>
        """
        return f"NDS/0/{challenge}/no-gsbrcd/{client_ip}|{encrypted_token}/{encrypted_token}"
