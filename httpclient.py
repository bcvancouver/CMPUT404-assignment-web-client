#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Michael Xi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys, socket, re, urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"


class URL(object):
    def __init__(self, urlstr):
        # https://docs.python.org/2/library/urlparse.html#urlparse.urlparse
        self.parse = urlparse(urlstr)
        self.root = self.get_root()
        # By default assign port 80
        self.port = int(self.parse.port)
        self.path = self.get_path()
        self.scheme = self.get_scheme()


    def get_scheme(self):
        return self.parse.scheme

    def get_root(self):
        temp = self.parse.netloc.split(":")
        if len(temp[0]) != 0:
            return temp[0]
        else:
            return 80

    def get_path(self):
        if len(self.parse.path) != 0:
            return self.parse.path
        else:
            return "/"


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Copied and modified from lab 2
        # socket.AF_INET indicates that we want an IPv4 socket
        # socket.SOCK_STREAM indicates that we want a TCP socket
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        code = int(data.split(" ")[1])
        return code

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        body = ""
        localurl = URL(url)
        clientSocket = self.connect(localurl.root, localurl.port)
        request = "GET " + localurl.path + " HTTP/1.1\r\nHost: " + localurl.root + "\r\n\r\n"
        clientSocket.sendall(request)
        response = self.recvall(clientSocket)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 404
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
