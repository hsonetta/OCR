FROM public.ecr.aws/lambda/python:3.7
	
COPY . ./

RUN python3.7 -m pip install -r requirements.txt -t .

CMD ["app.py"]  