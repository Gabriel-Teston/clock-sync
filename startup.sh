# Install or update needed software
apt-get update
apt-get install -yq git supervisor python3-pip python3-venv jq

# Fetch source code
mkdir /opt/app
git clone https://github.com/Gabriel-Teston/clock-sync.git /opt/app

# Python environment setup
python3 -m venv /opt/app/env
source /opt/app/env/bin/activate
# sudo curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/requirements" -H "Metadata-Flavor: Google" | sudo tee /opt/app/requirements.txt
pip3 install -r /opt/app/requirements.txt


#sudo curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/flask" -H "Metadata-Flavor: Google" | sudo tee /opt/app/app.py
#sudo curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/lamport" -H "Metadata-Flavor: Google" | sudo tee /opt/app/lamport.py
#sudo curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/helloworld_pb2_grpc" -H "Metadata-Flavor: Google" | sudo tee /opt/app/helloworld_pb2_grpc.py
#sudo curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/helloworld_pb2" -H "Metadata-Flavor: Google" | sudo tee /opt/app/helloworld_pb2.py


#sudo apt-get update && sudo apt -y install apache2 python3-pip python3-venv

#python3 -m venv /opt/venv
#source /opt/venv/bin/activate

#python3 -m pip install flask
#python3 -m flask --app /tmp/app run 


#echo '<!doctype html><html><body><h1>Hello if you see this than you have apache running on '$(hostname)'!</h1></body></html>' | sudo tee /var/www/html/index.html

# Start application
cd /opt/app/
#python3 -m flask run
echo "" > sudo tee /DONE