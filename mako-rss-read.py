import xml.etree.ElementTree as ET
from flask import Flask, send_from_directory, request
from flask import jsonify
import requests
import os

app = Flask(__name__, static_folder='build')


def parse_rss_item(item, source):
    obj_to_return = {'source': source}
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
    return obj_to_return



def parse_results(res, source):
    try:
        news = []
        news_rss_xml_root = ET.fromstring(res.text.encode(encoding=res.encoding, errors='strict'))
        channel = news_rss_xml_root[0]
        for item in channel:
            if item.tag == 'item':
                news.append(parse_rss_item(item, source))
        return jsonify(news)
    except:
        print("error")
        return jsonify([])


def parse_ynet_results(res):
    news = []
    news_rss_xml_root = ET.fromstring(res.content.decode(res.encoding))
    channel = news_rss_xml_root[0]
    for item in channel:
        if item.tag == 'item':
            news.append(parse_rss_item(item, 'ynet'))
    return jsonify(news)

MAKO_NEWS_LINKS = {
    "news": "http://rcs.mako.co.il/rss/31750a2610f26110VgnVCM1000005201000aRCRD.xml",
    "sport": "http://rcs.mako.co.il/rss/87b50a2610f26110VgnVCM1000005201000aRCRD.xml",
    "tarbut": "http://rcs.mako.co.il/rss/c7a987610879a310VgnVCM2000002a0c10acRCRD.xml",
    "fashion": "http://rcs.mako.co.il/rss/women-fashion.xml",
}

YNET_NEWS_LINK = {
    "news":"http://www.ynet.co.il/Integration/StoryRss2.xml",
    "sports": "http://www.ynet.co.il/Integration/StoryRss3.xml"
}

WALLA_NEWS_LINK = {
    "news":"http://rss.walla.co.il/feed/1?type=main",
    "sports": "http://rss.walla.co.il/feed/3?type=main",
    "tech": "http://rss.walla.co.il/feed/6?type=main",
    "tarbut":"http://rss.walla.co.il/feed/4?type=main",
    "celebs": "http://rss.walla.co.il/feed/22?type=main",
}


@app.route("/mako")
def mako():
    cats = request.args.get('cat')
    link = MAKO_NEWS_LINKS[cats]
    try:
        r = requests.get(link)
        if r.status_code == 200:
            return parse_results(r, "mako")
        else:
            print("Error: ", r.status_code, r.text)
            return jsonify([])
    except:
        print("Error")
        return jsonify([])


@app.route("/walla")
def walla():
    cats = request.args.get('cat')
    link = WALLA_NEWS_LINK[cats]
    try:
        r = requests.get(link)
        if r.status_code == 200:
            return parse_results(r, "walla")
        else:
            print("Error: ", r.status_code, r.text)
            return jsonify([])
    except Exception as e:
        print("Error: ", e)
        return jsonify([])


@app.route("/ynet")
def ynet_news():
    cats = request.args.get('cat')
    link = YNET_NEWS_LINK[cats]
    try:
        r = requests.get(link)
        if r.status_code == 200:
            return parse_ynet_results(r)
        else:
            print("Error: ", r.status_code, r.text)
            return jsonify([])
    except Exception as e:
        print("Error: ", e)
        return jsonify([])


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