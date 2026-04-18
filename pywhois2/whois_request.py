import socket
import socks


def build_whois_query(query: str, whois_host: str) -> bytes:
    return query.encode("utf-8") + b"\r\n"


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
