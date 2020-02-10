# Running the pipeline on kubernetes

Running the pipeline on kubernetes is a multistep process:

- Write your pipeline in a way so it accepts files names as parameters
- Create a runnable docker image from your pipeline
- Create the job specification for kubernetes and deploy it

## Pack it inside a docker container

Kubernetes can not execute python code directly. Therefore we need to create a docker container
that can started on a cluster:

```dockerfile
FROM python

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./src /clc
```

Lets break it down:

- `FROM python`: Specifies our base image as the latest python image it includes all the generic python tools and
  the newest python executable.
- `COPY requirements.txt /requirements.txt`: First we copy our dependencies inside the
  container
- `RUN pip install -r /requirements.txt`: Next install all our dependencies. This ensures our code can be executed
- `COPY ./src /clc`: At last copy the source code into a directory named `/clc`. 

Simply execute the next command in your shell to build the docker container. The nice part is that dependencies are
only downloaded on the first build (thanks to the cache). 

```bash
docker build -t clc-example:v1 .
``` 

The output should look similar to this:

```text
Sending build context to Docker daemon  17.41kB
Step 1/4 : FROM python
 ---> eeadc22d21a9
Step 2/4 : COPY requirements.txt /requirements.txt
 ---> Using cache
 ---> e276df3bf7cf
Step 3/4 : RUN pip install -r /requirements.txt
 ---> Using cache
 ---> 7a7d67b32cd1
Step 4/4 : COPY ./src /clc
 ---> c5c38641b0d3
Successfully built c5c38641b0d3
Successfully tagged clc-example:v1
```

> FYI: Restarting the cluster means the image is no longer in the cache of the minikube, it has to be rebuilt.

... and with that the container is ready and can be started using the following command:

```bash
docker run clc-example:v1 python -m clc.preprocessing
```

After starting the container it executes the `python -m clc.preprocessing` command. This works because our code resides
in `/clc/preprocessing`. If your output does not already exist in the blob storage it will be recreated or luigi will detect 
that the job is already done:

```text
DEBUG: Checking if PreprocessAllFiles() is complete
INFO: Informed scheduler that task   PreprocessAllFiles__99914b932b   has status   DONE
INFO: Done scheduling tasks
INFO: Running Worker with 1 processes
DEBUG: Asking scheduler for work...
DEBUG: Done
DEBUG: There are no more tasks to run at this time
INFO: Worker Worker(salt=344809380, workers=1, host=587ff6c3c04d, username=root, pid=1) was stopped. Shutting down Keep-Alive thread
INFO: 
===== Luigi Execution Summary =====

Scheduled 1 tasks of which:
* 1 complete ones were encountered:
    - 1 PreprocessAllFiles()

Did not run any tasks
This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

## Execute it on the minikube cluster

### Building the container on the cluster

Currently the minikube cluster does not know anything about the `clc-example` image (It was build locally)
Normally you would push your image on a registry that can be accessed by the cluster to avoid further complications
(installing your own registry, ...) we take a shortcut. By executing:

```bash
minikube $(docker-env)
``` 

the environment variables of docker are set to the minikube cluster. 
This makes the image available for deployments in the minikube cluster

### Executing on kubernetes

> If you want to see the job running start the dashboard with `minikube dashboard`

Luigi provides a wrapper to launch kubernetes tasks via the `luigi.contrib.kubernetes` module. It provides
a `KubernetesJobTask`. This makes it possible to specify necessary attributes for kubernetes. In code it looks
like this:

```python
class Preprocess(KubernetesJobTask):
    """
    Applies general preprocessing steps to all CSV files loaded.
    """
    # ...
    # kubernetes methods
    @property
    def name(self):
        """Name of kubernetes job"""
        return 'preprocess-data'

    @property
    def spec_schema(self):
        """Returns the spec schema of the kubernetes job"""
        return {
            "containers": [{
                "name": self.name,  # The name of the container
                "image": 'clc-example:v1',  # The container to use
                "command": self.cmd  # command that is executed on start of the container
            }],
        }

    @property
    def cmd(self):
        """Returns the command that should be executed when the container starts"""
        return ['python', '-m', f'clc.preprocess', self.filename]
```

These are the minimum properties that you have to specify. The `name` property is the job name (althrough in kubernetes
it will show up in combiniation of a UUID). The `spec_schema` specifies what container to launch and what the launch
command should be. In the `cmd` property we specify the command that should be executed on the container. As shown above
we launch a tasks for each file, that is why it needs to be provided in the `cmd` property.

A luigi server can take this tasks and generates all deployment configs for kubernetes. You can start it via:

```bash
luigi &
```

in your virtual environment. It automatically deploys them to the cluster (in minikube specified in `~/.kube/config`). Kubernetes then spawns the pods and executes the pipeline.

The pipeline can be finally launched by first navigating to the script that contains the `KubernetesJobTask` and
executing the luigi pipeline in your virtual environment: 

```bash
PYTHONPATH=. luigi --module simple_workflow_kubernetes PreprocessAllFiles --workers 2
```
