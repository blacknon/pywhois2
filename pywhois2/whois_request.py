import socket
import socks


def build_whois_query(query: str, whois_host: str) -> bytes:
    normalized_query = query

    # JPRS documents "/e" as the way to suppress Japanese output for
    # command-based lookups. Keep this narrow to the known WHOIS host.
    if whois_host.rstrip(".").lower() == "whois.jprs.jp" and not query.endswith("/e"):
        normalized_query = f"{query}/e"

    return normalized_query.encode("utf-8") + b"\r\n"


def whois_request(query: str, whois_host: str, port: int = 43) -> str:
    response = bytearray()

    with socks.socksocket(socket.AF_INET) as sock:
        sock.connect((whois_host, port))
        sock.sendall(build_whois_query(query, whois_host))

        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response.extend(chunk)

    return response.decode("utf-8", "replace")
