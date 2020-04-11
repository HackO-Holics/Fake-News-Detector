import os, json

from flask import Flask, session, redirect, render_template, request, jsonify, flash
import requests
from relatednews import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import pickle
import nltk
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from nltk.tokenize import RegexpTokenizer,WordPunctTokenizer,word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer
app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def search():
    if request.method == "POST" :
        text = request.form.get("message")
        related_news = relatednews(text)
        NBVocab = open('NBVocab.pkl','rb')
        cv = joblib.load(NBVocab)
        model = open('model.pkl','rb')
        clf = joblib.load(model)
        ps = PorterStemmer()
        sw = set(stopwords.words('english'))
        sw.remove('not')
        sw.remove('no')
        sw.add('\n')
        text = text.lower()
        tokenizer = RegexpTokenizer('[A-z]+')
        word_list = tokenizer.tokenize(text)
        clean_list = [w for w in word_list if w not in sw]
        stemmed_list = [ps.stem(w) for w in clean_list]
        clean_text = ' '.join(stemmed_list)
        X_vec = cv.transform([clean_text])
        pred = clf.predict(X_vec)
        pred = pred[0]
        return jsonify({"prediction":pred , "related_news":related_news})
    else :
        return render_template("first.html")
