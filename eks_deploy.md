
1. Step 1: follow eksctl instruction to create cluster: https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html
* don't delete the cluster
aws ec2 create-key-pair --region us-west-2 --key-name wernerK8sKeyPair

```
eksctl create cluster \
--name yourappname-cluster \
--region us-west-2 \
--with-oidc \
--ssh-access \
--ssh-public-key wernerK8sKeyPair \
--managed
```


2. confirm cluster deployment
```
kubectl get svc
```


3. Jump to Step 4: Create nodes in here:
https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html


4. Install metrics server
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl get deployment metrics-server -n kube-system
```


5. Deploy the Kubernetes Dashboard (web UI)
* primary reference: https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html
* secondary reference: https://aws.amazon.com/premiumsupport/knowledge-center/eks-cluster-kubernetes-dashboard/
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.5/aio/deploy/recommended.yaml

kubectl apply -f eks-admin-service-account.yaml

kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')

kubectl proxy
```
* go to http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login


6. --- deployment ---
* use kube dashboard to deploy and specify proper ports, reference gke_service.yaml
```
    port: 8080
    protocol: TCP
    targetPort: 80
```
* check the default labels of the nodes from kube dashboard
* according to: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
nodes would already have default labels such as `beta.kubernetes.io/instance-type: c5.large`
specify this in nodeselector the yaml file 
```
kubectl get pods -n kube-system
kubectl get nodes --show-labels
kubectl apply -f eks_tess_deployment.yaml
```

* verify pods are running
* check deployment history
```
kubectl get deployments
kubectl get pods -l 'app=yourappname' -o wide | awk {'print $1" " $3 " " $6'} | column -t
kubectl rollout history deployment/your_cluster_name
```

* [optional] delete deployment
```
kubectl delete deployment yourappname
```


7. --- expose deployment ---
[reference] https://aws.amazon.com/premiumsupport/knowledge-center/eks-kubernetes-services-cluster/

```
kubectl apply -f eks_tess_service.yaml
kubectl get services
kubectl get service/yourappname |  awk {'print $1" " $2 " " $4 " " $5'} | column -t
[optional] kubectl delete service yourappname
```
