FROM amazonlinux:2

RUN echo $'[neuron] \n\
name=Neuron YUM Repository \n\
baseurl=https://yum.repos.neuron.amazonaws.com \n\
enabled=1' > /etc/yum.repos.d/neuron.repo

RUN rpm --import https://yum.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB

RUN yum install -y aws-neuron-tools
RUN yum install -y aws-neuron-runtime
RUN yum install -y tar gzip
RUN yum -y install python3 python3-pip
Run yum install -y opencv opencv-devel opencv-python

ENV PATH="/opt/aws/neuron/bin:${PATH}"

RUN mkdir -p /home/inference/api
WORKDIR /home/inference/api
COPY . /home/inference/api
ARG DEBIAN_FRONTEND=noninteractive

Run python3 -m pip install pip install -r /home/inference/api/requirements.txt
RUN python3 -m pip install torch_neuron-1.8.1.1.4.1.0-py3-none-linux_x86_64.whl

EXPOSE 5000
RUN chmod +x /home/inference/api/app.py
ENTRYPOINT [ "python3" ]

CMD [ "/home/inference/api/app.py" ]