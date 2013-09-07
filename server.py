#!/usr/bin/python

import BaseHTTPServer
import os
import gzip
import StringIO
import urllib2
import sys
import threading


class BlastHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

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

    def serve_music(self,path):
        location = self.content_handler.get_song_location_from_id(path)
        #if this returns a path then do the following. if it returns a get request execute get request
        if location[0]=='path':
            print location
            type = self.get_type(location[1])
            size = os.path.getsize(location[1])
            try:
                with open(location[1],'r') as stream:
                    self.send_response(200)
                    self.send_header('Accept-Ranges', 'bytes')
                    self.send_header('Content-Type',type)
                    self.send_header('Content-Length',size)
                    self.send_header('Cache-Control','max-age=86400')
                    self.end_headers()
                    self.wfile.write(stream.read()); self.wfile.close()
            except IOError:
                print 'Music File not found! Maybe you need to refresh database files.'
                self.send_error(404, 'File not found: %s' % (path,))
        else:
            print 'Forwarding request'

            try:
                self.send_response(301)
                self.send_header('Location',location[1])
                self.end_headers()
            except IOError:
                print 'Music File not found for proper redirect! Maybe you need to refresh database files.'
                self.send_error(404, 'File not found: %s' % (path,))    
                
      
            


    def serve_data(self,data,type,size,encode=True):
        self.send_response(200)
        self.send_header('Content-Type',type);
        if 'Accept-Encoding' in self.headers and encode:
            zbuf = StringIO.StringIO()
            zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf, compresslevel = 6)
            zfile.write(data)
            zfile.close()
            data = zbuf.getvalue()
            size = len(data)
            self.send_header('Vary','Accept-Encoding')
            self.send_header('Content-Encoding','gzip')
        self.send_header('Content-Length',str(size))
        self.end_headers()
        self.wfile.write(data)
        self.wfile.close()



    def do_GET(self):
        webdir = "www"
        try:
            #Return root html file
            if self.path == '/':
                res_path = os.path.join(webdir,'index.html')
                with open(res_path,'r') as f:
                    data = f.read()
                    type = self.get_type(res_path)
                    size = len(data)
                    self.serve_data(data,type,size)
            #Header for music files
            elif self.path.startswith('/content/music'):
                res_path = os.path.basename(self.path)
                self.serve_music(res_path)
            #Header for albumart
            elif self.path.startswith('/content/albumart/'):
                res_path = os.path.basename(self.path)
                image = self.content_handler.get_album_art_from_id(res_path)
                #if this returns a path then do the following. if it returns a get request execute get request
                type = 'image/png'
                size = len(image)
                self.serve_data(image,type,size,encode=False)
            #Header to get the json file
            elif self.path.startswith('/content/database'):
                database_name=self.path[18:]
                database = self.content_handler.get_music_database(database_name)
                type = self.get_type(".json")
                size = len(database)
                self.serve_data(database,type,size,encode=False)
            elif self.path.startswith('/content/meta/artist/image'):
                artistMetaData = self.content_handler.getArtistImage(self.path[27:])
                type = self.get_type(".jpg")
                size = len(artistMetaData)
                self.serve_data(artistMetaData,type,size)
            elif self.path.startswith('/content/meta/artist/similarArtists'):
                artistMetaData = self.content_handler.getSimilarArtists(self.path[36:])
                type = self.get_type(".json")
                size = len(artistMetaData)
                self.serve_data(artistMetaData,type,size)
            elif self.path.startswith('/content/meta/artist/bio'):
                artistMetaData = self.content_handler.getArtistBio(self.path[25:])
                type = self.get_type(".html")
                size = len(artistMetaData)
                self.serve_data(artistMetaData,type,size)
            elif self.path.startswith('/content/refresh_open_directories'):
                
                scanner=threading.Thread(target=self.content_handler.scanOpenDirectories())
                scanner.start()
                print 'dabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnlndabafibafabfafboajvlnln'

                type = self.get_type(".html")
                size = len('scanning')
                self.serve_data('scanning',type,size)
                
            elif self.path.startswith('/content/check_database'):
                user=self.path[24:]
                if user=='client':
                    database_flag = self.content_handler.newDatabase
                else:
                    database_flag = str(self.content_handler.databaseTime)
                type = self.get_type(".html")
                size = len(database_flag)
                self.serve_data(database_flag,type,size)
                
            elif self.path.startswith('/content/server_list'):  # sends a json object that is a list of the servers
                server_list=self.content_handler.serverFiles_JSON_Creator()
                type = self.get_type(".json")
                size = len(server_list)
                self.serve_data(server_list,type,size)
            #Everything else
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

class InventoryManagerServer:
    def __init__(self,port,content_handler,server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
        server_address = ('', port)
        try:
            handler_class.content_handler=content_handler
            httpd = server_class(server_address, handler_class)
            httpd.serve_forever()
        except RuntimeError:
            print 'Could not start server. Perhaps the content_handler wasn\'t registered?'
#run(handler_class=My_Handler)