"Neuron Detection"

This module uses the compiled neuron model generated from Neuron compilation module. The EasyOCR module loads the neuron model and is wrapped around in Flask app. The Flask app is further containerized to be deployed on Kubernetes pods.

Steps:

1. Generate Flask App (app.py)
2. Generate Dockerfile to dockerize the flask app (Dockerfile)
3. To build a docker image and to run the dockerized neuron application follow the steps:
	1. Follow instructions in here: Step 1, 2, 3, 4 (Only till verfying the docker hello-world)
	https://awsdocs-neuron.readthedocs-hosted.com/en/1.12.2/neuron-deploy/tutorial-docker-runtime1.0.html
	2. Now setup a docker image that will map the inferentia device to docker. Follow Step 1
	https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-deploy/docker-example/index.html (essential to stop neuron-rtd on the host)
	3. Create a docker image consisting of your application and run it. Follow step 2
	https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-deploy/docker-example/index.html
	 
	*Imp Note: When you run the neuron-rtd image you should stop the neuron-rtd on host to allow the mapping of inf chip to the docker environment. Read Step 3.1 for more details.
4. Once the docker image is built and currently running, pass the test image using flask_test_inferentia.ipynb inside test folder.


Handy Commands:
- Docker Build and Run commands:
	sudo docker build -t ocr_detect:latest -f neuronocr_deployment/Dockerfile .
	docker run --device=/dev/neuron0 --cap-add IPC_LOCK -v /tmp/neuron_rtd_sock/:/sock -it neuron-rtd
	sudo docker run --env NEURON_RTD_ADDRESS=unix:/sock/neuron.sock -v /tmp/neuron_rtd_sock/:/sock -p 8080:5000 ocr_detect
	
- Neuron-RTD commands:
	neuron-ls
	sudo systemctl status neuron-rtd
	sudo systemctl restart neuron-rtd
	sudo service neuron-rtd stop	
	
- Commands to push docker image to ECR:
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 206993404984.dkr.ecr.us-west-2.amazonaws.com/detectocr
	docker tag 80aba6029b68 206993404984.dkr.ecr.us-west-2.amazonaws.com/detectocr
	docker push 206993404984.dkr.ecr.us-west-2.amazonaws.com/detectocr
	
Errors:
1. ModuleNotFoundError: neuronocr_compilation not found:
	https://stackoverflow.com/questions/40304117/import-statement-works-on-pycharm-but-not-from-terminal
- Go to the root directory of your project and set:
	export PYTHONPATH=$PATHONPATH:`pwd`

2. Neuron Runtime Error:
	Either Neuron-RTD image is not run which opens the socket of inferentia chip to Docker
Or
	The Neuron-rtd id not stopped on the host before running the neuron-rtd image.	
	
	



	
	
	
	