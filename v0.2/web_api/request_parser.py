"""
Credit: 
https://github.com/getis/micropython-web-control-panel/blob/main/RequestParser.py
"""

import re
import json

class RequestParser:

    def __init__(self, raw_request):
        if isinstance(raw_request, bytes):
            raw_request = raw_request.decode("utf-8")
        self.method = ""
        self.full_url = ""
        self.url = ""
        self.query_string = ""
        self.protocol = ""
        self.headers = {}
        self.query_params = {}
        self.post_data = {}
        self.boundary = False
        self.content = []

        self.parse_request(raw_request)

    def parse_request(self, raw_request):
        if len(raw_request) <= 0:
            return
        else:
            el_char = '\r\n' # default as per HTTP protocol
            if raw_request.find(el_char) == -1:
                el_char = '\n'

            request_lines = raw_request.split(el_char)
            self.parse_first_line(request_lines[0])
            
            num_req_lines = len(request_lines)
            if num_req_lines <= 1:
                pass
            else:
                line_num = 1;
                while line_num < num_req_lines and len(request_lines[line_num]) != 0:
                    header, value = self.parse_header_line(request_lines[line_num])
                    if header:
                        self.headers[header] = value
                    line_num += 1
                
                line_num += 1
                if line_num > num_req_lines - 1: 
                    return
                
                self.content = request_lines[line_num:]
                
                content_type = self.get_header_value('Content-Type')
                if content_type:
                    
                    if content_type.find('multipart/form-data') != -1:
                        content_type_parts = content_type.split('boundary=')
                        if len(content_type_parts) == 2:
                            self.boundary = content_type_parts[1]
                        else:
                            self.boundary = False
                            return
                        self.parse_content_form_data()

                    elif content_type.find('application/x-www-form-urlencoded') != -1:
                        self.parse_content_form_url_encoded()

                    elif content_type.find('application/json') != -1 \
                        or content_type.find('application/javascript') != -1:
                        self.parse_json_body()
                
                    else:  # Treat as text
                        pass
                else:
                    pass
            

    def get_header_value(self, header_name):
        if header_name in self.headers:
            return self.headers[header_name] 
    
    def parse_first_line(self, first_line):
        line_parts = first_line.split()

        if len(line_parts) == 3:
            self.method = line_parts[0]
            self.full_url = line_parts[1]
            url_parts = line_parts[1].split('?', 1)
            self.url = url_parts[0]
            if len(url_parts) > 1:
                self.query_string = url_parts[1]
            self.protocol = line_parts[2]

            if len(self.query_string) > 0:
                self.query_params = self.decode_query_string(self.query_string)
            else:
                self.method = "ERROR"
            
    def parse_header_line(self, header_line):
        line_parts = header_line.split(':')
        if len(line_parts) != 2:
            return (False, False)
        else:
            return(line_parts[0].strip(), line_parts[1].strip())
        
    def decode_query_string(self, query_string):
        param_strings = query_string.split('&')
        params = {}
        for param_string in param_strings:
            try:
                key, val = param_string.split('=')
                val = self.unquote(val)
            except:
                key = param_string
                val = False

            params[key] = val

        return params
    
    def parse_content_form_data(self):
        if not self.boundary:
            return 
        line_num = 0
        content_len = len(self.content)
        while line_num < content_len:
            while line_num < content_len and self.content[line_num].find(self.boundary) == -1:  # do we need to be constantly checking the line num
                line_num +=1
            
            if line_num >= content_len - 1:
                return  # if we are performing this check?
            
            line_num += 1

            while self.content[line_num].find("Content-Disposition:") == -1 and len(self.content[line_num]) != 0:
                line_num += 1
            
            if line_num >= content_len - 1:
                return

            matches = re.search(r'name=\"([^\"]+)', self.content[line_num])
            line_num += 1

            try:
                var_name = matches.group(1)
            except:
                continue

            while line_num < content_len and len(self.content[line_num]) != 0:
                line_num += 1
            line_num += 1  # skip blaink line

            if line_num > content_len - 1:
                return
            
            var_value = ""
            while self.content[line_num].find(self.boundary) == -1:
                if len(var_value) > 0:
                    var_value += "\n"
                var_value += self.content[line_num]
                line_num += 1
            
            self.post_data[var_name] = var_value


    def parse_content_form_url_encoded(self):
        self.post_data = self.decode_query_string(self.content[0])

    def parse_json_body(self):
        line_num = 0
        json_str = ""
        content_len = len(self.content)
        while line_num < content_len:
            if len(json_str) > 0:
                json_str += "\n"
            json_str += self.content[line_num]
            line_num += 1
        
        self.post_data = json.loads(json_str)

    def url_match(self, test_url: str):
        test_url = '/' + test_url.strip().strip('/')
        if test_url == '/':
            return True if self.url == '/' else False
        
        return True if self.url == test_url else False
    
    def unquote(self, url_str: str):
        url_str = re.sub(r'%20', '', url_str)
        url_str = re.sub(r'%0A', '\n', url_str)
        return url_str
    
    def data(self):
        if self.method == 'POST':
            return self.post_data
        elif self.method == 'GET':
            return self.query_params
        else:
            return False
        
    def get_action(self):
        if self.method == 'POST':
            if 'action' in self.post_data:
                return self.post_data['action']
            else:
                return False
        elif self.method == 'GET':
            if 'action' in self.query_params:
                return self.query_params['action']
            else:
                return False
        else:
            return False



