from flask import Flask, render_template, send_from_directory
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

env = Environment(loader=FileSystemLoader('templates'))

@app.route('/data/<path:path>')
def serve_static(path):
    return send_from_directory('data', path)


@app.route('/ego/<eid>')
def force_directed(eid):
    egonet_url = "/data/json/e%s.json" % eid
    template = env.get_template('forcedirected.html')
    return template.render(egonet_url=egonet_url)
