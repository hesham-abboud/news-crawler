# -*- coding: utf-8 -*-
import json

from flask import Flask
from flask import Response
from scrapper.models.news_repo import NewsRepo

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/json/news/<keyword>')
def search_news_by_word(keyword):
    repo = NewsRepo()
    articles = repo.search_news_by_keyword(keyword)
    repo.close_conn
    resp = Response(response=json.dumps(articles),
                    status=200,
                    mimetype="application/json")
    return resp


@app.route('/api/json/tags/<keyword>')
def search_news_by_tag(keyword):
    repo = NewsRepo()
    articles = repo.search_news_by_tag(keyword)
    repo.close_conn
    resp = Response(response=json.dumps(articles),
                    status=200,
                    mimetype="application/json")
    return resp
