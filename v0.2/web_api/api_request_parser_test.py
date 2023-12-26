# use web interface to control an LED

import socket
from web_api.request_parser import RequestParser
from web_api.wifi_connection import WiFiConnection

# connect to WiFi
if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# main loop
while True:
    client, client_addr = s.accept()
    raw_request = client.recv(1024)

    print("Request received")
    request = RequestParser(raw_request)
    print(request.method, request.url, request.get_action())
    for key in request.data():
        print(key, request.data()[key])

    client.send("HTTP/1.1 200 OK\r\n\r\nRequest Received\r\n")
    client.close()
    print("Request closed")
    print()
