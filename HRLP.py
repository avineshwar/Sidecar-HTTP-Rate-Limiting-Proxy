#!/usr/bin/python

from sys import argv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys
import traceback
import time
import requests


# magic items
HOST = "0.0.0.0"
PORT = "8080"
#PORT = argv[1] # first argument
BLOCK_AFTER = 5 # maximum number of requests before a reject begins to happen
RESET_AFTER = 36 # block is lifted after these many seconds
rate_maintainer = dict() # dictionary for keeping a count s.t. key=ip, value=attempts
requested_path = "" # initialized as per client's request and forwarded upstream

class Server(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if not self.client_address[0] in rate_maintainer:
            current_time = int(time.time())
            initial_time = current_time # because it is the first request
            rate_maintainer[self.client_address[0]] = [1, initial_time, current_time]
            requested_path_upstream=self.path
            request_headers=self.headers
            upstream_response = upstream(self, requested_path_upstream, request_headers)
            response_header_stuff(self, 200, "text/plain; charset=utf-8")
            self.wfile.write(upstream_response.encode(encoding = "utf-8"))
        else:
            requested_path=self.path
            if (rate_maintainer[self.client_address[0]][2] - rate_maintainer[self.client_address[0]][1] < RESET_AFTER) and rate_maintainer[self.client_address[0]][0] < BLOCK_AFTER:
                rate_maintainer[self.client_address[0]][0] += 1
                rate_maintainer[self.client_address[0]][2] = int(time.time())
                response_header_stuff(self, 200, "text/plain; charset=utf-8")
                self.wfile.write("Hello again...".encode(encoding = "utf-8"))
            elif rate_maintainer[self.client_address[0]][2] - rate_maintainer[self.client_address[0]][1] >= RESET_AFTER:
                current_time = int(time.time())
                initial_time = current_time # because it is the time we reset the counter
                rate_maintainer[self.client_address[0]] = [1, initial_time, current_time]
                response_header_stuff(self, 200, "text/plain; charset=utf-8")
                self.wfile.write("Resetted!".encode(encoding = "utf-8"))
            else:
                response_header_stuff(self, 429, "text/html; charset=utf-8")
                #...
                #self.send_header("X-Retry-After", "3600")
                #...
                #self.end_headers()
                self.wfile.write("<html><head><title>Too Many Requests</title></head><body><h1>Too Many Requests</h1><p>" + str(BLOCK_AFTER) + " requests (in total) per hour only. Try after some time.</p></body></html>")
                current_time = int(time.time())
                rate_maintainer[self.client_address[0]][2] = current_time

def response_header_stuff(self, response_code, content_type):
    self.send_response(response_code)
    self.send_header("Content-type", content_type)
    self.send_header("Content-Encoding", "utf-8")
    self.end_headers()
    return

def upstream(self, requested_path, request_headers, METHOD="get", UPSTREAM="http://google.com"):
    response = requests.request(METHOD, UPSTREAM+requested_path, headers = request_headers)
    return response.text
    
def server_run(server_class=HTTPServer, server_handler=Server, port=int(PORT)):
    try:
        server_address = (HOST, port)
        server_initiate = server_class(server_address, server_handler)
        server_initiate.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard Interrupt! Exiting now...")
    except Exception:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    server_run()
