"""
Use a web interface to display HTTP Request message

Credit:
https://github.com/getis/micropython-web-control-panel/blob/main/api_rec_request.py
"""
import socket
from web_api.wifi_connection import WiFiConnection


if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('Network connection failed')


# Open the socket
address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
sock = socket.socket()

sock.bind(address)
sock.listen(1)
print(f"listening on {address}")

while 1:
    client, client_address = sock.accept()
    raw_request = client.recv(1024)
    print("**** Byte String ****\n")
    print(f"{raw_request}\n")

    decoded_request = raw_request.decode('utf-8')
    print("**** Decoded String ****\n")
    print(decoded_request + "\n")

    client.send("HTTP/1.1 200 OK\r\n\r\nRequest Received\r\n")
    client.close()
