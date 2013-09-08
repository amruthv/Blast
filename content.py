#!/usr/bin/python

import json
import urllib
from geopy import geocoders,distance
import urllib2
import os
import sqlite3 as lite
import datetime
import simplejson
from pygeocoder import Geocoder

class ContentHandler:    
    def __init__(self):
        
        self.build_database()

    def connect_to_database(self):
        con = None
        try:
            con = lite.connect('content.db')

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
        return con

    def add_to_database(self,input):
        con = self.connect_to_database()
        cur = con.cursor() 
        USERID = input[0]
        CONTENT = input[1]
        GPS = input[2]+','+input[3]
        LOCATION = str(Geocoder.reverse_geocode(float(input[2]),float(input[3]))[0])
        TIME = str(datetime.datetime.utcnow())
        with con:
            cur.execute("INSERT INTO BLASTS(USERID,CONTENT,GPS,LOCATION,TIME) VALUES(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');" % (USERID, CONTENT, GPS, LOCATION, TIME))
        con.close()    
    
    def build_database(self):
        con = self.connect_to_database()
        cur = con.cursor()    
        cur.execute("CREATE TABLE IF NOT EXISTS BLASTS(BLASTID INTEGER PRIMARY KEY, USERID VARCHAR(20), CONTENT VARCHAR(50), GPS VARCHAR(100), LOCATION VARCHAR(100), TIME VARCHAR(20));")
        con.close()

    def get_blastIDs(self,location):
        con = self.connect_to_database()
        cur = con.cursor()
        cur.execute("SELECT BLASTID FROM BLASTS")
        IDs = [num_pair[0] for num_pair in cur.fetchall()]
        ID_distance_list = []
        for ID in IDs:
            cur.execute("select GPS from BLASTS where BLASTID='%s'" % (str(ID)))
            coords = cur.fetchone()[0].split(',',2)
            if distance.distance(location,coords).mi < 1.0:
                ID_distance_list.append([str(ID),distance.distance(location,coords).mi])
        print ID_distance_list   
        sorted(ID_distance_list, key=lambda ID: ID[1])
        print ID_distance_list
        return [num_pair[0] for num_pair in ID_distance_list][:min([len(ID_distance_list), 20])]

    def build_json_file(self,ID_list): 
        con=self.connect_to_database()
        cur = con.cursor()
        json_data=""
        blasts=[]
        for ID in ID_list:
            cur.execute("select USERID from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict={'USERID':cur.fetchone()[0]}
            cur.execute("select CONTENT from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['CONTENT']=cur.fetchone()[0].replace('%20',' ').replace('%',' ')
            cur.execute("select GPS from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['GPS']=cur.fetchone()[0]
            cur.execute("select LOCATION from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['LOCATION']=cur.fetchone()[0]
            cur.execute("select TIME from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['TIME']=cur.fetchone()[0]
            blasts.append(blast_as_dict)
        
        return simplejson.dumps(blasts)