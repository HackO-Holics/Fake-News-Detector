import os, json

from flask import Flask, session, redirect, render_template, request, jsonify, flash
import requests
from relatednews import *

app = Flask(__name__)

@app.route("/")
    def home():
        return

@app.route("/search")
    def search():
        news = request.form.get()
        related_news = relatednews(news)
        predection =
        return jsonify()
