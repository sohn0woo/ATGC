from flask import Flask, request, jsonify, send_file
import requests
import feedparser
import os

app = Flask(__name__)

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY", "YOUR_TWELVE_DATA_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")

@app.route('/')
def home():
    return "📊 Stock + News API Server is running"

@app.route('/quote')
def get_quote():
    symbol = request.args.get('symbol')
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route('/news')
def get_news():
    query = request.args.get('query')
    feed_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(feed_url)
    articles = [{
        "title": entry.title,
        "link": entry.link,
        "published": entry.published
    } for entry in feed.entries[:5]]
    return jsonify({"articles": articles})

@app.route('/openapi.json')
def serve_openapi():
    return send_file('openapi.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
