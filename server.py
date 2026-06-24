# ---------------------------------------------------------
# Startup Banner
# ---------------------------------------------------------

print ("███ █   █ ███ █   █  █  ███ ███     █ █ ███ ███ ███ █  █ ███     ███ ███ ███ █ █ ███ ███")
print ("█   █   █ █ █ ██  █ █ █  █  █       █ █ █ █  █  █   ██ █ █ █     █   █   █ █ █ █ █   █ █")
print ("███ █   █ ███ █ █ █ █ █  █  ███     ███ ███  █  ███ █ ██ ███     ███ ███ ███ █ █ ███ ███")
print ("█   █   █ █   █  ██ █ █  █  █       █ █ █ █  █  █   █  █ █ █       █ █   ██  █ █ █   ██")
print ("█   ███ █ █   █   █  █   █  ███     █ █ █ █  █  ███ █  █ █ █     ███ ███ █ █  █  ███ █ █")

# ---------------------------------------------------------
# Flipnote Frog Mascot
# ---------------------------------------------------------

print ("   ██  ██")
print ("  █ ████ █")
print ("  █ ████ █")
print ("  ████████")
print (" ██████████")
print (" ██      ██")
print ("███      ███")
print ("████    ████")
print (" ████  ████")
print ("████████████")

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os
import socket
import threading

from src.modules.connectionTest import NintendoConnectionTest
from src.modules.nintendoAuth import NintendoAuth

# ---------------------------------------------------------
# Initialize Modules
# ---------------------------------------------------------

conntest = NintendoConnectionTest()
nas = NintendoAuth()

# Path to static assets
ASSET_ROOT = os.path.join("src", "assets")

# ---------------------------------------------------------
# Static Asset Handler
# ---------------------------------------------------------

def try_serve_asset(path):
    if path == "/":
        path = "/index.html"

    file_path = os.path.join(ASSET_ROOT, path.lstrip("/"))

    if not os.path.isfile(file_path):
        return None

    ext = file_path.split(".")[-1].lower()
    content_types = {
        "html": "text/html",
        "htm": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "xml": "text/xml",
        "txt": "text/plain",
    }
    content_type = content_types.get(ext, "application/octet-stream")

    with open(file_path, "rb") as f:
        return 200, content_type, f.read()

# ---------------------------------------------------------
# Request Router
# ---------------------------------------------------------

def handle_request(method, path, headers, body, client_ip):
    # 1. Serve static assets first
    asset = try_serve_asset(path)
    if asset:
        return asset

    # 2. Connection Test
    if method == "GET" and path == "/":
        return 200, "text/html", conntest.handle_root().encode()

    # 3. NAS Authentication
    if method == "POST" and path == "/ac":
        response = nas.handle_ac(body, client_ip)
        return 200, "text/plain", response.encode()

    # 4. Default 404
    return 404, "text/plain", b"Not Found"

# ---------------------------------------------------------
# HTTP Server
# ---------------------------------------------------------

def client_thread(conn, addr):
    client_ip = addr[0]

    try:
        data = conn.recv(8192).decode("utf-8", errors="ignore")
        if not data:
            conn.close()
            return

        lines = data.split("\r\n")
        request_line = lines[0]
        method, path, _ = request_line.split(" ")

        headers = {}
        i = 1
        while i < len(lines) and lines[i] != "":
            if ":" in lines[i]:
                k, v = lines[i].split(":", 1)
                headers[k.strip()] = v.strip()
            i += 1

        body = lines[-1] if "\r\n\r\n" in data else ""

        status, content_type, response_body = handle_request(
            method, path, headers, body, client_ip
        )

        http_response = (
            f"HTTP/1.1 {status} OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode() + response_body

        conn.sendall(http_response)

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()

# ---------------------------------------------------------
# Start Server
# ---------------------------------------------------------

def start_server(host="0.0.0.0", port=80):
    print(f"\nServer running on {host}:{port}\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(50)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_thread, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
