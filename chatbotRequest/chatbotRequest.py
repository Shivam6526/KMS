import requests

 

from flask import Flask, render_template , jsonify,request

import webbrowser

 

app = Flask(__name__)

 

@app.route('/')

def index():

    return render_template('searchPage.html')

 

@app.route('/search/<searchTopic>')

def clicked(searchTopic):

    endpoint = "http://localhost:9200/customer/_search?pretty"

#    listbox.delete(0,last = END)

#    searchParameter = raw_input("What would you like to search for?\n")

    print endpoint

    data = {

    "query": {

        "match" : {

            "attachment.content" : searchTopic

        }

    },

    "highlight" : {

        "fields" : {

            "attachment.content" : {}

        }

    }

}

 

    r = requests.get(url = endpoint,json=data)

    print r

 

    results = []

    highlight = []

    response = r.json()[u'hits'][u'hits']

    highlighteddText = ""

    fileScores = {}

    x = len(response)

    for i in range(0,x):

        highlighteddText = ""

        z = response[i][u'_source']

        highlight = response[i][u'highlight'][u'attachment.content']

        for text in highlight:

            highlighteddText += text + '.....'

        score = 0

        if(searchTopic in z):

            score = z[searchTopic]

        new_score = response[i][u'_score'] * (1+0.1*score)

        response[i]['newScore'] = new_score

        response[i]["summary"]=highlighteddText

 

    for val in sorted(response, key = lambda a:a['newScore'],reverse=True):

#        listbox.insert(END,val[u'_source'][u'file'][u'url'])

        results.append({"name":val[u'_source'][u'filename'],"id":val[u'_id'],"summary":val["summary"],"snapshot":val[u'_source']})

#        entries[val[u'_source'][u'file'][u'url']] = val[u'_id']

    response2 = ""

 

    #for i in range(0,x):

    #    response2 += response[i][u'_source'][u'file'][u'url'] + "\n"

    #    listbox.insert(END,response[i][u'_source'][u'file'][u'url'])

    #    entries[response[i][u'_source'][u'file'][u'url']] = response[i][u'_id']

 

    if(x==0):

        response2= "Sorry, your search returned no results"

    print results

    return jsonify(results)

    #lbl.configure(text = response2)

import json

@app.route('/openFile', methods=['POST'])

def openFile():

    da = request.data

    da = json.loads(da)

    filename = da[u'name']

    id = da[u'id']

    data2 = {

            "script": "ctx.searchedCount += 1"

        }

    endpoint2 = "http://localhost:9200/customer/_doc/" + id + "/_update"

    r2 = requests.post(url=endpoint2, json=data2)

    #filename = listbox.get(ACTIVE)

    webbrowser.open(filename)

    return jsonify(filename)

 

@app.route('/positiveFeedback',methods=['POST'])

def positive():

    #filename = listbox.get(ACTIVE)

#    id = entries[filename]

    id = request.data

    id = json.loads(id)

    id = id[u'id']

    searchTopic = request.data

    searchTopic = json.loads(searchTopic)

    searchTopic = searchTopic[u'searchTopic']

    endpoint1 = "http://localhost:9200/customer/_doc/" + id

    r3 = requests.get(endpoint1)

    h = r3.json()[u'_source']

    if(searchTopic in h):

        data2 = {

            "script": "ctx._source." + searchTopic + " += 1"

        }

    else:

        data2 = {

            "script": "ctx._source." + searchTopic + " = 1"

        }

 

    endpoint2 = "http://localhost:9200/customer/_doc/" + id + "/_update"

    r2 = requests.post(url=endpoint2, json=data2)

    print r2

    return jsonify(id)

 

@app.route('/negativeFeedback',methods=['POST'])

def negative():

    #filename = listbox.get(ACTIVE)

#    id = entries[filename]

    id = request.data

    id = json.loads(id)

    id = id[u'id']

    searchTopic = request.data

    searchTopic = json.loads(searchTopic)

    searchTopic = searchTopic[u'searchTopic']

    endpoint1 = "http://localhost:9200/customer/_doc/" + id

    r3 = requests.get(endpoint1)

    h = r3.json()[u'_source']

    if (searchTopic in h):

        data2 = {

            "script": "ctx._source." + searchTopic + " -= 1"

        }

    else:

        data2 = {

            "script": "ctx._source." + searchTopic + " = -1"

        }

 

    endpoint2 = "http://localhost:9200/customer/_doc/" + id + "/_update"

    r2 = requests.post(url=endpoint2, json=data2)

    print r2

    return jsonify(id)

 

if __name__ == '__main__':

    app.run(debug=True,host= '0.0.0.0')