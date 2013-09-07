#!/usr/bin/python



import json
import urllib
from geopy import geocoders,distance
import urllib2
import httplib
from BeautifulSoup import BeautifulSoup
import os
from collections import defaultdict
try:
    import cPickle as pickle
except ImportError:
    import pickle # fall back on Python version
import sqlite3 as lite
import datetime
import opml
import simplejson




class ContentHandler:    
    def __init__(self,basedir):
        self.basedir = os.path.abspath(basedir)
        self.build_database(basedir)


    def connect_to_database(self):
        con = None
        try:
            con = lite.connect('content.db')

        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
        
        return con

    
    def build_database(self,basedir):
        con = self.connect_to_database()
        cur = con.cursor()    
        cur.execute('DROP TABLE BLASTS')
        cur.execute("CREATE TABLE IF NOT EXISTS BLASTS(BLASTID VARCHAR(5),USERID VARCHAR(5),CONTENT VARCHAR(50), GPS VARCHAR(30), TIME VARCHAR(20));")
        
        # f=open(basedir+'/inventory.xml','r')
        # outline=opml.parse(f)
        # for category_index in range(len(outline[0])):
        #     for subcategory_index in range(len(outline[0][category_index])):
        #         print "subcategory_index="+str(subcategory_index)
        #         for ID_index in range(len(outline[0][category_index][subcategory_index])):
        #             for subsubcategory_index in range(len(outline[0][category_index][subcategory_index][ID_index])):
        #                 for description_index in range(len(outline[0][category_index][subcategory_index][ID_index][subsubcategory_index])):
        #                     for image_index in range(len(outline[0][category_index][subcategory_index][ID_index][subsubcategory_index][description_index])):
        #                         with con:
        #                             #print "INSERT INTO Inventory(ID,SUBID,CATEGORY,SUBCATEGORY,IMAGE FILE, DESCRIPTION) VALUES(outline[0][category_index][subcategory_index][ID_index].text,outline[0][category_index][subcategory_index][ID_index][description_index][image_index].text.split('.',1)[0],outline[0][category_index].text,outline[0][category_index][subcategory_index].text,outline[0][category_index][subcategory_index][ID_index][description_index][image_index].text),outline[0][category_index][subcategory_index][ID_index][description_index].text)"
        #                             ID=outline[0][category_index][subcategory_index][ID_index].text
        #                             SUBID=outline[0][category_index][subcategory_index][ID_index][subsubcategory_index][description_index][image_index].text.split('.',1)[0]
        #                             CATEGORY=outline[0][category_index].text
        #                             SUBCATEGORY=outline[0][category_index][subcategory_index].text
        #                             SUBSUBCATEGORY=outline[0][category_index][subcategory_index][ID_index][subsubcategory_index].text
        #                             IMAGE=outline[0][category_index][subcategory_index][ID_index][subsubcategory_index][description_index][image_index].text
        #                             DESCRIPTION=outline[0][category_index][subcategory_index][ID_index][subsubcategory_index][description_index].text
        #                             print '============='
        #                             print ID
        #                             print SUBID
        #                             print CATEGORY
        #                             print SUBCATEGORY
        #                             print category_index
        #                             print subcategory_index
        #                             print '============='
        #                             #print 'INSERT INTO Inventory(ID,SUBID,CATEGORY,SUBCATEGORY,IMAGE_FILE,DESCRIPTION) VALUES('+"'"+ID+"'"+','+"'"+SUBID+"'"+','+CATEGORY+','+SUBCATEGORY+','+IMAGE+','+DESCRIPTION+');'
        BLASTID='0001'
        USERID='YAJIT'
        CONTENT='EMERGENCY CAR ACCIDENT'
        g=geocoders.GoogleV3()
        _, ne = g.geocode('500 Memorial Drive, Cambridge, MA')
        GPS=str(ne[0])+','+str(ne[1])
        TIME=str(datetime.datetime.utcnow())
        print 'INSERT INTO BLASTS(BLASTID,USERID,CONTENT,GPS,TIME) VALUES('+"'"+BLASTID+"'"+','+"'"+USERID+"'"+','+"'"+CONTENT+"'"+','+"'"+GPS+"'"+','+"'"+TIME+"'"+');'
        with con:
            cur.execute('INSERT INTO BLASTS(BLASTID,USERID,CONTENT,GPS,TIME) VALUES('+"'"+BLASTID+"'"+','+"'"+USERID+"'"+','+"'"+CONTENT+"'"+','+"'"+GPS+"'"+','+"'"+TIME+"'"+');')

        con.close()    

            

            

    def get_music_database(self,database_file):
        #take database file and return its contents as string
        if database_file=='local':
            f=open('inventory_database.json','r')
        else:
            f=open(database_file,'r')
        json_file=f.read()
        return json_file


    def get_blastIDs(location):
        con=self.connect_to_database()
        cur = con.cursor()
        


        distance=distance.distance(ne,ge).mi
        return ID_list


    

    def build_json_file(self,ID_list): 
        con=self.connect_to_database()
        cur = con.cursor()
        json_data=""
        blasts=[]
        for ID in ID_list:
            cur.execute("select USERID from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict={'USERID':cur.fetchone()}
            cur.execute("select CONTENT from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['CONTENT']=cur.fetchone()
            cur.execute("select GPS from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['GPS']=cur.fetchone()
            cur.execute("select TIME from BLASTS where BLASTID='"+ID+"'")
            blast_as_dict['TIME']=cur.fetchone()
            blasts.append(blast_as_dict)
        
        return simplejson.dumps(blasts)

            
        
        # for ID in IDs:
            
        #     albums_data=""
        #     albums=con.execute('SELECT DISTINCT album FROM Music WHERE type='+'"'+home+'"'+'AND artist='+'"'+artist[0]+'"'+' ORDER BY album'+';')
        #     albumIndex=0
        #     for album in albums:
                
        #         songs_data=""
                
        #         titles=con.execute('SELECT DISTINCT title FROM Music WHERE type='+'"'+home+'"'+'AND artist='+'"'+artist[0]+'"'+' AND '+'album='+'"'+album[0]+'"'+' ORDER BY title'+';')
        #         songIndex=0
        #         for title in titles:
        #             cur.execute('SELECT DISTINCT ID FROM Music WHERE type='+'"'+home+'"'+'AND artist='+'"'+artist[0]+'"'+' AND '+'album='+'"'+album[0]+'"'+' AND '+'title='+'"'+title[0]+'"'+';')
        #             ID=cur.fetchone()
                    
        #             songs_data+=",{"+'"'"title"+'":"'+title[0]+'"'+","+'"'"ID"+'":"'+''+ID[0]+'.'+str(artistIndex)+'.'+str(albumIndex)+'.'+str(songIndex)+'"'+"}"
        #             songIndex=songIndex+1
        #         songs_data=songs_data[1:]
        #         albums_data+=",{"+'"'+"album"+'":"'+album[0]+'"'+","+'"songs"'+':'+"["+songs_data+"]"+"}"
        #         albumIndex=albumIndex+1
        #     albums_data=albums_data[1:]
        #     artists_data+=",{"+'"'+"artist"+'":"'+artist[0]+'"'+","+'"albums"'+':'+"["+albums_data+"]"+"}"
        #     artistIndex=artistIndex+1
        # artists_data=artists_data[1:]
        # json_data="{"+'"'+"artists"+'"'+":["+artists_data+"]}"
        
        # if home=='local':
        #     objects_file = 'music_database.json'
        # else:
        #     objects_file = home+'.json'
        # f = open(objects_file,'w')
        
        # f.write(json_data)
        # f.close()
        # return json_data


            
contenthandler = ContentHandler('./Content')
contenthandler.build_json_file(['0001'])



