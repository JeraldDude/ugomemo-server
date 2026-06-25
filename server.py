# ---------------------------------------------------------
# Startup Banner
# ---------------------------------------------------------

print("███ █   █ ███ █   █  █  ███ ███     █ █ ███ ███ ███ █  █ ███     ███ ███ ███ █ █ ███ ███")
print("█   █   █ █ █ ██  █ █ █  █  █       █ █ █ █  █  █   ██ █ █ █     █   █   █ █ █ █ █   █ █")
print("███ █   █ ███ █ █ █ █ █  █  ███     ███ ███  █  ███ █ ██ ███     ███ ███ ███ █ █ ███ ███")
print("█   █   █ █   █  ██ █ █  █  █       █ █ █ █  █  █   █  █ █ █       █ █   ██  █ █ █   ██")
print("█   ███ █ █   █   █  █   █  ███     █ █ █ █  █  ███ █  █ █ █     ███ ███ █ █  █  ███ █ █")

# ---------------------------------------------------------
# Flipnote Frog Mascot
# ---------------------------------------------------------

print("   ██  ██")
print("  █ ████ █")
print("  █ ████ █")
print("  ████████")
print(" ██████████")
print(" ██      ██")
print("███      ███")
print("████    ████")
print(" ████  ████")
print("████████████")

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import time
import socket
import importlib
from flask import Flask, request, make_response


# ---------------------------------------------------------
# Helper: Detect LAN IP
# ---------------------------------------------------------

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()


# ---------------------------------------------------------
# Helper: Boot Step Printer
# ---------------------------------------------------------

def boot_step(name, module_path):
    print(f"Importing {name}...", end="", flush=True)
    time.sleep(0.3)
    importlib.import_module(module_path)
    print(" Done!")


IP = get_local_ip()
PORT = 80

print("\nStarting Flipnote Hatena server...\n")
time.sleep(0.4)

# ---------------------------------------------------------
# Real Module Imports (your actual folder structure)
# ---------------------------------------------------------

boot_step("Nintendo Authentication Server", "src.modules.nintendoAuth.nintendoAuth")
boot_step("Nintendo Connection Test Server", "src.modules.connectionTest.NintendoConnectionTest")
boot_step("UGO Menu Compiler", "src.modules.tools.UGO")

# Add more modules here if needed:
# boot_step("User Database", "src.modules.user.user")
# boot_step("Flipnote Delivery", "src.modules.delivery.delivery")


# ---------------------------------------------------------
# Flask App
# ---------------------------------------------------------

app = Flask(__name__)


# ---------------------------------------------------------
# Browser Blocker — 403 Forbidden / 405 Method Not Allowed
# ---------------------------------------------------------

@app.before_request
def block_non_dsi_clients():
    ua = request.headers.get("User-Agent", "")

    # Allow Flipnote Studio (DSi)
    if "Flipnote Studio" in ua:
        return

    # Allow internal tools (curl, Python scripts)
    if "curl" in ua or "Python" in ua:
        return

    # Block POST/PUT/DELETE from browsers
    if request.method not in ("GET", "HEAD"):
        resp = make_response(
            "405 - Method Not Allowed\nFlipnote Hatena Server is for Nintendo DSi consoles only",
            405
        )
        resp.headers["Content-Type"] = "text/plain"
        return resp

    # Block normal browser GET requests
    resp = make_response(
        "403 - Forbidden\nFlipnote Hatena Server is for Nintendo DSi consoles only",
        403
    )
    resp.headers["Content-Type"] = "text/plain"
    return resp


# ---------------------------------------------------------
# Root Route (DSi will never hit this, browsers will)
# ---------------------------------------------------------

@app.route("/")
def root():
    return "403 - Forbidden\nFlipnote Hatena Server is for Nintendo DSi consoles only", 403


# ---------------------------------------------------------
# Final Startup Message
# ---------------------------------------------------------

print("")
print(f"Flipnote Hatena server running at {IP} on Port {PORT}")
print("")
print("Enter this in your Nintendo DSi Proxy Settings:")
print(f"Proxy Server: {IP}")
print(f"Port: {PORT}")
print("")
print("==============================================")
print("        Press CTRL+C to stop the server       ")
print("==============================================")

# ---------------------------------------------------------
# Start Flask Server
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
