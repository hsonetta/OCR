FROM public.ecr.aws/lambda/python:3.7

COPY app.py requirements.txt ./
RUN mkdir -p ./model_file
RUN mkdir -p ./user_network
COPY english_g2.pth ./model_file
RUN python3.7 -m pip install -r requirements.txt -t .

COPY app.py   ./
CMD ["app.handler"]  