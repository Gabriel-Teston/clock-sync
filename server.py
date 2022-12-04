from flask import Flask
from lamport import *
import requests

base_metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/"

ips = {
    "instance-from-template-a": requests.get(f"{base_metadata_url}instance_a_address").text,
    "instance-from-template-b": requests.get(f"{base_metadata_url}instance_b_address").text,
    "instance-from-template-c": requests.get(f"{base_metadata_url}instance_c_address").text"
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
        "<br>".join([f"{instance} {f'http://{ip}/time'}"
            for instance, ip in ips.items() if instance != HOSTNAME]) + 
        "</body></html>"
    )
   
@app.route("/time")
def times():
    return f"{local_time(app.counter)}"