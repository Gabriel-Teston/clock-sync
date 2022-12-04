from flask import Flask
from flask_cors import CORS, cross_origin
from lamport import *
import requests
import os

#base_metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/"

ips = {
    "instance-from-template-a": os.getenv('INSTANCE_A_ADRESS'),
    "instance-from-template-b": os.getenv('INSTANCE_B_ADRESS'),
    "instance-from-template-c": os.getenv('INSTANCE_C_ADRESS')
}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.counter = Counter()

@app.route("/")
def index():
    return f"<!doctype html><html><body><h1>Hello if you see this than you have apache running on {HOSTNAME}!</h1></body></html>"

@app.route("/dashboard")
@cross_origin()
def dashboard():
    return (
        "<!doctype html><html><head><script src='https://cdn.jsdelivr.net/npm/p5@1.5.0/lib/p5.js'></script>" + 
        f"<script>let ips = {ips};" +
        """
function updateTimes(){
    for (const [key, value] of Object.entries(ips)) {
        let theUrl = 'http://' + value + '/time';xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=()=>{
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
                console.log(key, value);
            }
        }
        xmlhttp.open("GET", theUrl, false );
        xmlhttp.send();
    }
}""" +
        "</script>" +
        "</head><body>" +
        "</body></html>"
    )
    
   
@app.route("/time")
def times():
    return f"{local_time(app.counter)}"