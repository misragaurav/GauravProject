# -*- coding: utf-8 -*-
"""
Function for parallel downloading npi entries from the CMS database. 200 concurrent connections are enough to download a few hundred MBs of
data in a matter of minutes
"""

from threading import Thread
import sys
from queue import Queue
import requests

concurrent = 200
q = Queue(concurrent * 2)
url = "https://npiregistry.cms.hhs.gov/api?"
npi_dict={}
def parallel_download(npi_array,npi_col_num):
    def doWork():
        while True:
            (url,params)=q.get()
            # sending get request and saving the response as response object
            r = requests.get(url = url, params = params )
            data = r.json()
            npi_dict[str(params['number'])]=data
            q.task_done()
    
    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()
    
    try:
        for npi in npi_array[:,npi_col_num]: # Getting data for all unique providers
            #print(npi.astype(int))
            # defining a params dict for the parameters to be sent to the API
            params = {'number':npi.astype(int), 'limit':200} 
            q.put((url,params))
    
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)

    return npi_dict
