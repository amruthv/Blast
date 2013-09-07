#!/usr/bin/python
__author__="yajitj"

import server
import sys
import content


def load_config_data():
    try:
        with open("Blast.conf",'r') as f:
            config = {}
            for line in f.readlines():
                print line
                if not line.startswith("#"):
                    param,value=(''.join(line.strip())).split('=')
                    config[param]=value
    except IOError:
        print "Blast.conf not found! Using default port 8000 and ./Content"
        config = {'port':8000,'basedir':'./'}
    print config
    return config




if __name__ == "__main__":
    config=load_config_data();
    content_handler = content.ContentHandler(config['basedir'])
    inventory_server = server.BlastManagerServer(int(config['port']),content_handler,handler_class=server.BlastHTTPRequestHandler)





