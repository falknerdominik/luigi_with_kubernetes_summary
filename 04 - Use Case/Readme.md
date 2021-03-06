A pipeline build with Luigi can be used for different tasks, Machine Learning is one of them. The following Use Case describes the Machine Learning task used in this tutorial about Luigi and Kubernetes. The tutorial does not describe how those Machine Learning Method works or why they have been chosen to solve the Problem at hand. It will focus on how these methods can be implemented by using Luigi and Kubernetes. Moreover, challenges which may arise will be faced.


**Use Case**

Robots navigating through a city to solve certain tasks is imaginable in the future. The most talked about challenge in realizing this is visually recognition of the surrounding. But for us humans auditive perception of our surrounding is very important, as visually we are only able to recognize what is directly before us. One can argue that a robot can be given a 360° camera to see what is around it. But this dose not allow the robot to know what is behind the next street corner. A human can use the auditive perception to notice what is behind the next street corner. So a robot should also be able to perceive auditively the surrounding. Like with pictures identifying the most important objects is critical in order to react fast on unexpected situations. One approach for solving this problem is classifying the sound heard. 

At the 22nd ACM International Conference on Multimedia, Nov. 2014 in Orlando USA, J. Salamon, C. Jacoby and J. P. Bello presented a Dataset and Taxonomy of Urban Sounds [1](#references). This is used to train a Model that recognizes different urban sounds. 

**Dataset**

*"This dataset contains 1302 labeled sound recordings. Each recording is labeled with the start and end times of sound events from 10 classes: air_conditioner, car_horn, children_playing, dog_bark, drilling, enginge_idling, gun_shot, jackhammer, siren, and street_music. Each recording may contain multiple sound events, but for each file only events from a single class are labeled."* [Urban Sound Dataset](https://urbansounddataset.weebly.com/urbansound.html)

###### References:

1. *J. Salamon, C. Jacoby and J. P. Bello, "**A Dataset and Taxonomy for Urban Sound Research**", 22nd ACM International Conference on Multimedia, Orlando USA, Nov. 2014.*

**Execute the Maschine Learing Pipeline**

You will need to exchange the Azure Connection String and Containernme in the luigi_tasks.py and the luigi_tasks_kubernetes.py. 

**Execute Pipeline in Docker**

You need to exchange the ``run_pipeline()`` in the ``__main__.py`` file with ``run_pipeline_wo()``. This calls the pipline without Kubernetes.

Before you can execute the docker build command make sure you have downloaded the urban sound files from the challange and placed them in the directory called urban_sound_files at the same level as the Dockerfile.

Than you need to execute ``docker build -t clc-example:v1 .`` in the data_pipeline directory. This will build a docker container from the DockerImage.

With ``docker run clc-example:v1 python -m clc.preprocessing`` you can run the pipeline in an Docker container. Afterwards you can find the trained Model in your Azure Storage.

**Execute Pipeline with Kubernetes and Docker**


    
