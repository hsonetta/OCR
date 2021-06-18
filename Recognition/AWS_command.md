#ECR Authentication and token generation 
```
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin 206993404984.dkr.ecr.us-east-1.amazonaws.com/YOUR_REPOSITORY
```

#To push docker image to ECR, list all docker image
```
docker images
```
#tag the project id to the ECR uri
```
docker tag fdf110b5ea47:project 206993404984.dkr.ecr.us-east-1.amazonaws.com/easyocr:latest
```

#push the image to aws
```
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/YOUR_REPOSITORY:latest
```
