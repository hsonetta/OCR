FROM python:3.8-slim

RUN mkdir -p /home/inference/api
WORKDIR /home/inference/api
COPY . /home/inference/api
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get update && pip install -r /home/inference/api/requirements.txt

# nvidia-docker run -p 5000:8080 wernerchao/craftapi:craftapi-v0-0-0-1
# 5000:8080 -> docker_port:flask_port
# http://0.0.0.0:5000/
EXPOSE 5000
RUN chmod +x /home/inference/api/app.py
ENTRYPOINT [ "python3" ]
CMD [ "/home/inference/api/app.py" ]