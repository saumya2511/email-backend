from flask import Flask, request, jsonify
import pickle as c
import os
from sklearn import *
from collections import Counter
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def load(clf_file):
    clf = c.load(open(clf_file, 'rb'))
    return clf
def make_dict():
    direc = "data/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    words = []

    for email in emails:
        f = open(email, errors='ignore')
        blob = f.read()
        words += blob.split(" ")

    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(5000)

@app.route('/')
def test():
    return "hello"

@app.route('/classify', methods=['POST'])
def flasktest():
    clf = load("classifymodel.mdl")
    d = make_dict()
    features = []
    request_data = request.get_json()
    #inp = (sys.argv[1]).split(" ")
    #inp = input()
    for word in d:
        features.append(request_data['msg'].count(word[0]))
    res = clf.predict([features])
    print(res[0])
    return jsonify({"result": str(res[0])})

