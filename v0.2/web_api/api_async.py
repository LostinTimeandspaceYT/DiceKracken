"""
Async web server on the Raspberry Pi Pico-W based on Bob Grant's work.

Original Source:
https://github.com/getis/micropython-web-control-panel/tree/main

Video Reference:
https://www.youtube.com/watch?v=h18LMskRNMA


Module names have been updated to match the naming conventions
found in Micropython builds >= 1.20.

File and module have been modified to match the snake_casing convention present
in this project. 

"""

import asyncio
from machine import Pin
from web_api.request_parser import RequestParser
from web_api.response_builder import ResponseBuilder
from web_api.wifi_connection import WiFiConnection

# Import Characters as needed
from character_sheet import PulpCharacter

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')

file_path = 'pulp_cthulhu_sheet.json'
Randolph = PulpCharacter(file_path)

async def handle_request(reader, writer):
    #TODO: Flesh method out as needed. 
    try:
        raw_request = await reader.read(2048)

        request = RequestParser(raw_request)

        responder = ResponseBuilder()

        if request.url_match("/api"):
            action = request.get_action()

            if action == 'load_character':  # User wants to load a character to the browser
                print(request.data())  # for debugging
                
                # ajax request for data
                responder.set_body_from_dict(Randolph())
                
            elif action == 'download_character':  # User wants to download character to device
                status = 'OK'
                response = {
                    'status': status,
                    'state': True,
                }
                responder.set_body_from_dict(response)

            elif action == 'download_game':  # User wants to download game to device
                status = 'OK'
                response = {
                    'status': status,
                    'state': True,
                }
                responder.set_body_from_dict(response)

            else:  # Unkown action
                responder.set_status(404)

        else:
            responder.serve_static_file(request.url, "/api_index.html")

        responder.build_response()

        writer.write(responder.response)
        await writer.drain()
        await writer.wait_closed()
                

    except OSError as e:
        print(f"Connection error {e.errno}: {e}")


async def blink_led():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        await asyncio.sleep(.5)



async def main():
    print("Setting up web server...\n")

    server = asyncio.start_server(handle_request, "0.0.0.0", 80)
    asyncio.create_task(server)

    asyncio.create_task(blink_led())

    #TODO: Put other web based api code here


    while True:
        await asyncio.sleep(0)


try:
    asyncio.run(main())

finally:
    asyncio.new_event_loop()    
