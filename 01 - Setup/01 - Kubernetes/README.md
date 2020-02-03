# Setup Kubernetes

Kubernetes will be used as a cluster for this tutorial. 
It acts as a managing layer for the deployments. To follow this tutorial ensure that you 
have a kubernetes up and running.

Depending on your situation you can use a local (running on a single node) cluster or a cloud cluster.

## Local Setup

A local cluster can be done via the `minicube` application. It is a cheap and easy option for testing deployments.

>Be aware that your operating system and hardware need to support virtualization. 

To install `minicube` follow the up-to-date instructions (available for linux / macOS / windows) provided [here](https://kubernetes.io/docs/tasks/tools/install-minikube/). Specific instructions for Archlinux can be obtained [here](http://blog.programmableproduction.com/2018/03/08/Archlinux-Setup-Minikube-using-KVM/).
Installing minikube will automatically configure your local kubectl for it. The final output should look similar to this:

```text
😄  minikube v1.6.2 on Arch 18.1.5
✨  Selecting 'kvm2' driver from user configuration (alternates: [none])
🔥  Creating kvm2 VM (CPUs=2, Memory=2000MB, Disk=20000MB) ...
🐳  Preparing Kubernetes v1.17.0 on Docker '19.03.5' ...
💾  Downloading kubeadm v1.17.0
💾  Downloading kubelet v1.17.0
🚜  Pulling images ...
🚀  Launching Kubernetes ... 
⌛  Waiting for cluster to come online ...
🏄  Done! kubectl is now configured to use "minikube"
```

### Dashboard
To verify that the application started start the dashboard like this:
 
```bash 
$ minikube dashboard
``` 

If the browser window does not open, you can access the URL via `minikube dashboard --url`. 

### Config file

If you need to refer to any configuration files of your minikube instance, you will find it in the `~/.kube/config` directory.

## Cloud Setup

Instructions for the cloud setup can be found [here](https://github.com/clc3-CloudComputing/clc3-ws19/tree/master/3%20Kubernetes/exercise%203.1).
TODO: Write down what parameters (url port) we need from this and where we get them (screenshot)

