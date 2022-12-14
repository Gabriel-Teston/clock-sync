from flask import Flask, request
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
                console.log(key, value, xmlhttp.responseText);
            }
        }
        xmlhttp.open("GET", theUrl, false );
        xmlhttp.send();
    }
}

function sendEvent(){
    let theUrl = 'http://' + '""" + ips[HOSTNAME] + """' + '/event';xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=()=>{
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            updateTimes();
        }
    }
    xmlhttp.open("GET", theUrl, false );
    xmlhttp.send();
}

function sendMessage(instance){
    let theUrl = 'http://' + '""" + ips[HOSTNAME] + """' + '/message/' + instance;xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=()=>{
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            updateTimes();
        }
    }
    xmlhttp.open("GET", theUrl, false );
    xmlhttp.send();
}

function sendReset(instance){
    let theUrl = 'http://' + '""" + ips[HOSTNAME] + """' + '/reset';xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=()=>{
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            updateTimes();
        }
    }
    xmlhttp.open("GET", theUrl, false );
    xmlhttp.send();
}
""" +
        f"</script></head><body>{HOSTNAME}<br>" +
        "<input type='button' value='Reset' onclick='sendReset();' />" +
        "<input type='button' value='Event' onclick='sendEvent();' />" +
        "".join([f"<input type='button' value='Message {instance}' onclick='sendMessage(\"{instance}\");' />" for instance,ip in ips.items() if instance != HOSTNAME]) +
        "<input type='button' value='Get Clocks' onclick='updateTimes();' />" +
        "</body></html>"
    )
    
   
@app.route("/time")
def times():
    return f"{local_time(app.counter)}"

@app.route("/event")
def get_event():
    event(HOSTNAME, app.counter)
    return f"{local_time(app.counter)}"

@app.route("/message", methods = ['POST'])
def message():
    if request.method == 'POST':

        timestamp = int(request.form['timestamp'])
            
        new_value = calc_recv_timestamp(timestamp, app.counter)

        app.counter.set(new_value)
        print('Message received at ' + str(HOSTNAME)  + local_time(app.counter))

@app.route("/message/<instance>")
def message_(instance):
    #send_message(f'http://{ips[instance]}', HOSTNAME, app.counter)
    app.counter.increment()
    x = requests.post(f'http://{ips[instance]}/message', data = {'timestamp': app.counter.value()})
    return f"{local_time(app.counter)}"

@app.route("/reset")
def reset():
    app.counter.set(0)