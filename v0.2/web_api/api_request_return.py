import socket
from wifi_connection import WiFiConnection
from web_api.request_parser import RequestParser


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

    print("Request Received\n")
    request = RequestParser(raw_request)
    print(f"Method: {request.method}\nUrl: {request.url}\nAction: {request.get_action()}")
    data = request.data()
    for k,v in data:
        print(f"{k}: {v}")

    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type: application/json\r\n")
    client.send("\r\n")
    client.send("{ \"sensor\": 12345, \"reading2\": 98765, \"input\": \"hello\" }\r\n")
    client.close()
    print("Request closed\n")
