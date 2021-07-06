1. authenticate
make sure have latest acccess key setup, check ~/.aws/
```
aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 206993404984.dkr.ecr.us-east-1.amazonaws.com
```
<br />  

2. build docker
```
sudo docker build -t your_lambda_fn_name:latest -f Dockerfile .
```
<br />

3. run docker locally (optional)
```
sudo docker run -p 8080:8080 your_lambda_fn_name

# restrict number of CPU core to use for the function, this simulates how it would be on deployed Lambda
sudo docker run -p 8080:8080 --cpus="2" your_lambda_fn_name

# -d means detach mode, doesn't occupy the terminal
docker run -d -p 8080:8080 your_lambda_fn_name  

# ssh into the docker
sudo docker ps
sudo docker exec -it <mycontainerID> bash
i.e.
sudo docker exec -it 36ea64a4f9e4 bash

curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"image": "trigger"}'
OR use the sample Python testing code to test

# stop all containers
docker stop $(docker ps -a -q)

# optionally remove the image
docker rm $(docker ps -a -q)

# optionally remove the image
docker rmi imageid
```
<br />

4. tag and push image
```
sudo docker tag your_lambda_fn_name:latest 206993404984.dkr.ecr.us-east-1.amazonaws.com/your_lambda_fn_name:latest

sudo docker push 206993404984.dkr.ecr.us-east-1.amazonaws.com/your_lambda_fn_name:latest
```
<br />
