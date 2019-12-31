A pipeline with Luigi can be used for different Tasks, Machine Learning is one of them. The following Use Case describes the Machine Learning task used in this Tutorial about Luigi and Kubernetes. The tutorial does not describe how those Machine Learning Method works or why they have been chosen to solve the Problem at hand. It will focus on how to use the Methods in combination with Luigi and Kubernetes and the challenges that arise.

Two different Scenarios are considered. 

1. Batch Processing of the data
2. Stream Processing of the data



**Task 1:**

Having Self-Driving Cars is something car companies try to develop for some years. One of the challenges is the recognition of traffic signs. Machine Learning is a possible method to solve the problem. For training and testing the Method the following Dataset is used: [Traffic Sign Dataset](https://www.kaggle.com/valentynsichkar/traffic-signs-preprocessed#label_names.csv). The goal is to recognize these traffic signs with a method trained with the help of Luigi and Kubernetes. A Convolutional Neural Network (CNN) is used for recognizing the traffic sign in the pictures.



**Task 2:**

San Francisco is a City in the US with a higher than average crime rate. At the end of this tutorial it should be possible to predict if a committed crime can be solved in San Francisco. A combination of Machine Learning, Luigi and Kuberates is used for this. The data for the prediction can be found on keggle ([Crime in San Francisco](https://www.kaggle.com/roshansharma/sanfranciso-crime-dataset)).



**Task 3:**

Imagine going into a clothing store enter your size, select a clothing and a system tells you which size would fit you. This could be the future of shopping. To realize something like this Maschine Learning is used in this Tutorial. The dataset for this is the keggel's [clothing fit dataset](https://www.kaggle.com/rmisra/clothing-fit-dataset-for-size-recommendation).