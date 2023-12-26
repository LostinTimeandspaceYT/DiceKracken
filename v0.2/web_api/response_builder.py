"""
Credit:
https://github.com/getis/micropython-web-control-panel/blob/main/ResponseBuilder.py
"""

import json
import os


class ResponseBuilder:
    protocol = "HTTP/1.1"
    server = "Pico-W Dice Kracken"
    status_messages = {
        200 : "OK",
        400 : "Bad Request",
        403 : "Forbidden",
        404 : "Not Found", 
    }

    def __init__(self):
        self.status: int = 200
        self.content_type: str = "text/html"
        self.body = ""
        self.response = ""

    def set_content_type(self, content_type):
        self.content_type = content_type
    
    def set_status(self, status: int):
        self.status = status

    def set_body(self, body):
        self.body = body

    def set_body_from_dict(self, d: dict):
        self.body = json.dumps(d)
        self.set_content_type("application/json")

    def get_status_message(self):
        if self.status in self.__class__.status_messages:
            return self.__class__.status_messages[self.status]
        else:
            return "Invalid Status"

    def serve_static_file(self, req_file, default_file="/web_api/api_index.html"):

        if req_file.find("/") == -1:
            req_file = "/" + req_file
        
        if req_file.find("?") != -1:
            req_file, qs = req_file.split("?", 1)
        
        if req_file.find("#") != -1:
            req_file, qs = req_file.split("#", 1)

        if req_file == "/":
            req_file = default_file

        path, file_name = req_file.rsplit("/", 1)
        print(f"path: {path}")
        print(f"file_name: {file_name}")

        if len(path) == 0:
            path = "/"

        os.chdir("/")

        dir_contents = os.listdir(path)

        if file_name in dir_contents:
            name, file_type = file_name.rsplit(".", 1)
            
            if file_type == "js":
                self.content_type = "text/javascript"

            elif file_type == "css":
                self.content_type = "text/css"

            else: # it is actually html, or the browser will figure it out
                self.content_type = "text/html"

            # load content
            file = open(path + "/" + file_name)
            self.set_body(file.read())
            self.set_status(200)

        else:
            self.set_status(404)

    def build_response(self):
        self.response = ""
        self.response += (self.__class__.protocol 
                     + " " 
                     + str(self.status) 
                     + " " 
                     + self.get_status_message() 
                     + "\r\n"
        )

        self.response += f"Server: {self.server}\r\n"
        self.response += f"Content-Type: {self.content_type}\r\n"
        self.response += f"Content-Length: {str(len(self.body))}\r\n"
        self.response += "Connection: Closed\r\n"
        self.response += "\r\n"

        if len(self.body) > 0:
            self.response += self.body
                   
