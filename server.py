from flask import Flask
from lamport import *
import requests


ips = {
    "instance-from-template-a": "35.202.254.81",
    "instance-from-template-b": "34.122.120.150",
    "instance-from-template-c": "34.132.83.52"
}

app = Flask(__name__)
app.counter = Counter()

@app.route("/")
def index():
    return f"<!doctype html><html><body><h1>Hello if you see this than you have apache running on {HOSTNAME}!</h1></body></html>"

@app.route("/dashboard")
def dashboard():
    return (
        "<!doctype html><html><body>" +
        "<br>".join([f"{instance} {requests.get(f'http://{ip}/time').text}"
            for instance, ip in ips.items() if instance != HOSTNAME]) + 
        "</body></html>"
    )
   
@app.route("/time")
def times():
    return f"{local_time(app.counter)}"