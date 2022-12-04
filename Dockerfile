FROM hashicorp/terraform:latest

RUN apk --no-cache add curl bash which python3
RUN curl -sSL https://sdk.cloud.google.com > /tmp/gcl && bash /tmp/gcl --install-dir=~/gcloud --disable-prompts

#RUN apk add py-pip
#RUN curl -sSL https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py && python3 /tmp/get-pip.py
COPY . .
RUN python3 -m pip install -r requirements.txt

ENV PATH $PATH:~/gcloud/google-cloud-sdk/bin