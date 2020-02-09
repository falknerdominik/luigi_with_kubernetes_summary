import os
from typing import Generator
import luigi
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient
import numpy as np
from luigi.local_target import LocalFileSystem
from .model import UrbanModels, ModelUtils


class DummyPreprocessClass():
    path: str = luigi.Parameter()

    def output(self) -> luigi.Target:
        return luigi.LocalTarget(self.path)


class TrainModel(luigi.Task):
    """
    Train model with given training and validation Data
    Save the trained Model under a given name

    """

    input_path: str = luigi.Parameter()
    output_path: str = luigi.Parameter()
    model_name: str = luigi.Parameter()

    # def requires(self):
    #    pass

    def run(self):
        x_train = np.genfromtxt(os.path.join(self.input_path, "x_train.csv"), delimiter=',')
        y_train = np.genfromtxt(os.path.join(self.input_path, "y_train.csv"), delimiter=',')
        x_val = np.genfromtxt(os.path.join(self.input_path, "x_val.csv"), delimiter=',')
        y_val = np.genfromtxt(os.path.join(self.input_path, "y_val.csv"), delimiter=',')
        model_name = "trained_mlp"

        num_labels = y_train.shape[1]
        model = UrbanModels.create_mlp(num_labels)

        # Train model
        model, history = ModelUtils.train_mpl(model, x_train, x_val, y_train, y_val)

        fs = LocalFileSystem()
        fs.mkdir(self.output_path)
        model.save(os.path.join(self.output_path, model_name))

        with self.output().open('w') as fout:
            f = open(os.path.join(self.output_path, model_name + ".h5"), "rb")
            fr = f.read()
            fout.write(fr)

    def output(self) -> luigi.Target:

        return AzureBlobTarget(
            container=self.container_name,
            blob="trained_mlp.h5",
            client=AzureBlobClient(
                connection_string=self.connection_string
            )
            , format=luigi.format.Nop
        )


class RunTrainModel(luigi.WrapperTask):
    """
    Trains a model with data from input_path
    """

    input_path: str = os.path.join(os.path.abspath(os.path.curdir), "clc", "test")
    output_path: str = os.path.join(os.path.abspath(os.path.curdir), "clc", "test1")

    # connection string obtained for the storage unit via azure
    azure_connection_string = 'DefaultEndpointsProtocol=https;AccountName=storageaccountclcluigi;AccountKey=NK/tDtLASVTM/lJ0BgsPNSf2r6pXoJYFf9obiipXfWOtPxzz0NAwANmbKNiX9PXol2nyijvZGPJiz0fvzQl06Q==;EndpointSuffix=core.windows.net'
    container_name = 'clcstoragecontainer'

    def requires(self) -> Generator[luigi.Task, None, None]:
        yield TrainModel(input_path=self.input_path, output_path=self.output_path,
                         connection_string=self.azure_connection_string,
                         container_name=self.container_name
                         )


def run_pipeline_wo():
    """
    Run pipeline with docker only
    """
    luigi.build([RunTrainModel()], local_scheduler=True)
