# -*- coding: utf-8 -*-

from __future__ import division

 

import requests

import json

import base64

import os

import time

import datetime

from random import randint

 

date_handler = lambda obj: (

    obj.isoformat()

    if isinstance(obj, (datetime.datetime, datetime.date))

    else None

)

 

 

i = 1

headers = {'content-type': 'application/json'}

count = 0

## in os.walk('') please add the path of the shared drive you want to index

 

for (dirname, dirs, files) in os.walk('C:\\KMS\\Core Banking & Payments'):

   for filename in files: 

      

       # this loop exists to stop indexing after a certain number of files are indexed

     

        print filename

        count = count + 1

        category = ""

        ext = ""

        thefile = os.path.join(dirname,filename)

        a = base64.b64encode(open(thefile, "rb").read())

        info = os.stat(thefile)

        modifiedTime = datetime.datetime.fromtimestamp(info.st_mtime)

        createdTime = datetime.datetime.fromtimestamp(info.st_ctime)

        size = info.st_size/(1024*1024)

        filename, file_extension = os.path.splitext(thefile)

        try:

            ext = file_extension.split('.')[1]

        except Exception:

            ext = file_extension.split('.')[0]

        searchedCount = randint(1,1000)

        randomint = randint(1, 7)

        if(randomint%4 == 0):

            category = "technical"

        elif (randomint % 4 == 1):

            category = "business"

        elif (randomint % 4 == 2):

            category = "design"

        else:

            category = "miscellaneous"

        data2 = {

          "filename" : thefile,

          "type":ext,

          "Date Modified":modifiedTime,

          "Date Created":createdTime,

          "size":size,

          "category":category,

          "data":a,

          "searchedCount":searchedCount

         

        }

        r2 = requests.post("http://localhost:9200/customer/_doc/"+str(i)+"?pipeline=attachment", data=json.dumps(data2,default=date_handler),headers=headers)

        print r2.text

        time.sleep(5)

        i = i + 1