import xml.etree.ElementTree as ET
from flask import Flask, send_from_directory
from flask import jsonify
import requests
import os

app = Flask(__name__, static_folder='build')


def parse_results(res):
    news = []
    news_rss_xml_root = ET.fromstring(res.text.encode(encoding=res.encoding, errors='strict'))
    channel = news_rss_xml_root[0]
    for item in channel:
        if item.tag == 'item':
            obj_to_return = {'source': 'mako'}
            for child in item:
                if child.tag == 'title':
                    obj_to_return['title'] = child.text
                if child.tag == 'link':
                    obj_to_return['link'] = child.text
                if child.tag == 'pubDate':
                    obj_to_return['publication_date'] = child.text
                if child.tag == 'shortDescription':
                    obj_to_return['desc'] = child.text
            news.append(obj_to_return)
    return jsonify(news)


def parse_ynet_results(res):
    news = []
    news_rss_xml_root = ET.fromstring(res.content.decode(res.encoding))
    channel = news_rss_xml_root[0]
    for item in channel:
        if item.tag == 'item':
            obj_to_return = {'source': 'ynet'}
            for child in item:
                if child.tag == 'title':
                    obj_to_return['title'] = child.text
                if child.tag == 'link':
                    obj_to_return['link'] = child.text
                if child.tag == 'pubDate':
                    obj_to_return['publication_date'] = child.text
                if child.tag == 'description':
                    obj_to_return['desc'] = child.text
                if child.tag == 'guid':
                    obj_to_return['id'] = child.text
            news.append(obj_to_return)
    return jsonify(news)

@app.route("/mako_news")
def mako_news():
    NEWS_LINK = "http://rcs.mako.co.il/rss/31750a2610f26110VgnVCM1000005201000aRCRD.xml"
    try:
        r = requests.get(NEWS_LINK)
        if r.status_code == 200:
            return parse_results(r)
    except:
        print("Error")

@app.route("/ynet_news")
def ynet_news():
    ynet_news_link = "http://www.ynet.co.il/Integration/StoryRss2.xml"
    try:
        r = requests.get(ynet_news_link)
        if r.status_code == 200:
            return parse_ynet_results(r)
    except:
        print("Error")

@app.route("/mako_sport")
def mako_sport():
    NEWS_LINK = "http://rcs.mako.co.il/rss/87b50a2610f26110VgnVCM1000005201000aRCRD.xml"
    try:
        r = requests.get(NEWS_LINK)
        if r.status_code == 200:
            return parse_results(r)
    except:
        print("Error")


@app.route("/mako_tarbut")
def mako_tarbut():
    NEWS_LINK = "http://rcs.mako.co.il/rss/c7a987610879a310VgnVCM2000002a0c10acRCRD.xml"
    try:
        r = requests.get(NEWS_LINK)
        if r.status_code == 200:
            return parse_results(r)
    except:
        print("Error")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == "":
        return send_from_directory(app.static_folder, 'index.html')
    if os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return "Not Found", 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3344)