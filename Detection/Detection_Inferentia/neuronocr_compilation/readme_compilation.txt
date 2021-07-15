"Neuron Model Compilation"

This module is used to compile the EasyOCR pytorch model to inferentia compatible Neuron model.

Steps:
1. Launch Inf1 instance on AWS - Creating an EC2 instance using Deep Learning AMI (Ubuntu 18.04) Version 44.0, select inferentia instance (https://docs.aws.amazon.com/dlami/latest/devguide/launch-config.html)
2. Once the connection is established, in the WSL update all the packages (https://docs.aws.amazon.com/dlami/latest/devguide/tutorial-inferentia-launching.html)
3. Set up the jupyter notebook server (https://docs.aws.amazon.com/dlami/latest/devguide/setup-jupyter.html)
4. If you want to switch jupyter note book environment to different framework (https://docs.aws.amazon.com/dlami/latest/devguide/tutorial-jupyter.html#tutorial-jupyter-switching)
5. Make sure Neuron-RTD is running: 
	sudo systemctl status neuron-rtd
6. Before starting the jupyter notebook activate pytorch neuron environment 'source activate aws_neuron_pytorch_p36'
7. open save_neuron_model.ipynb file and run all the cells to save the neuron model which is further used in Flask app to generate inference.


Handy Commands:
- SSH in the EC2 instance:
	ssh -i ~/inf1-west2-hs.pem ubuntu@ec2-34-209-89-115.us-west-2.compute.amazonaws.com
	
- To activate neuron:
	source activate aws_neuron_pytorch_p36
	source deactivate
	
- To connect Jupyter Notebook
	jupyter notebook --certfile=~/ssl/mycert.pem --keyfile ~/ssl/mykey.key
- In another terminal create a proxy tunnel between host and EC2 instance to access jupyter notebook locally- 
	ssh -i ~/inf1-west2-hs.pem -N -f -L 8888:localhost:8888 ubuntu@ec2-34-209-89-115.us-west-2.compute.amazonaws.com
	
- To reset Neuron-CLI, when insufficient NCs:
neuron-cli reset


	
	
	