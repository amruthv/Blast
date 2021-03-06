#!/usr/bin/python

import BaseHTTPServer
import os
import gzip
import StringIO
import urllib2
import sys
import threading
from urlparse import urlparse
import pdb

class BlastHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    # def do_GET(self):
    #     pdb.set_trace()
    #     arg_dict = urlparse.parse_qs(self.path)
    #     pdb.set_trace()

    def get_type(self,path):
        ext = os.path.splitext(path)[1]

        if ext=='.html' or ext==".htm":
            return 'text/html'
        elif ext=='.jpg':
            return 'image/jpeg'
        elif ext=='.js':
            return 'text/javascript'
        elif ext=='.json':
            return 'application/json'
        elif ext=='.mp3':
            return 'audio/mpeg'
        elif ext=='.ogg':
            return 'audio/off'
        elif ext==".png":
            return 'image/png'
        elif ext==".css":
            return 'text/css'
        else:
            return 'application/octet-stream'

    def serve_data(self,data,ctype,size,encode=False):
        self.send_response(200)
        self.send_header('Content-Type',ctype);
        if 'Accept-Encoding' in self.headers and encode:
            zbuf = StringIO.StringIO()
            zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=6)
            zfile.write(data)
            zfile.close()
            data = zbuf.getvalue()
            self.send_header('Vary','Accept-Encoding')
            self.send_header('Content-Encoding','gzip')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()

        self.wfile.write(data)
        self.wfile.close()

    def do_GET(self):
        webdir = "www"
        try:

            if self.path == '/':
                res_path = os.path.join(webdir,'index.html')
                with open(res_path,'r') as f:
                    data = f.read()
                    type = self.get_type(res_path)
                    size = len(data)
                    self.serve_data(data,type,size)

            elif self.path.startswith('/getcontent'):
                data = self.path[12:]
                location = data.split('&',2)
                location[0]=location[0].replace('lat=','')
                location[1]=location[1].replace('lon=','')
                json = self.content_handler.build_json_file(self.content_handler.get_blastIDs(location))
                type = self.get_type(".json") 
                size = len(json)  
                self.serve_data(json,type,size,encode=False)

            elif self.path.startswith('/postcontent'):
                data=self.path[13:]
                input=data.split('&',4)
                input[0]=input[0].replace('userid=','')
                input[1]=input[1].replace('content=','')
                input[2]=input[2].replace('lat=','')
                input[3]=input[3].replace('lon=','')
                self.content_handler.add_to_database(input)
                self.send_response(200)



            else:
                res_path = os.path.join(webdir,self.path[1:])
                with open(res_path,'r') as f:
                    data=f.read()
                    type = self.get_type(res_path)
                    size = len(data)
                    self.serve_data(data,type,size)
        except IOError as e:
            print e
            self.send_error(404, 'Content not found here: %s' % (self.path,))

class BlastManagerServer:
    def __init__(self,port,content_handler,server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
        server_address = ('', port)
        try:
            handler_class.content_handler=content_handler
            httpd = server_class(server_address, handler_class)
            httpd.serve_forever()
        except RuntimeError:
            print 'Could not start server. Perhaps the content_handler wasn\'t registered?'