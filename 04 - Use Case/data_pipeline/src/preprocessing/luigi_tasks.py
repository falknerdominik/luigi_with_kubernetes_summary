"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
import os
from typing import Generator

import luigi
import numpy as np
import pandas as DataFrame
import pandas as pd
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient
from luigi.local_target import LocalFileSystem

from .model import UrbanModels, ModelUtils
from .utils import get_features_and_labels
from sklearn.model_selection import train_test_split

"""
class LoadCSV(luigi.ExternalTask):

    path: str = luigi.Parameter()

    def output(self) -> luigi.Target:
        return luigi.LocalTarget(self.path)
"""


# KubernetesJobTask
class GetFeaturesLabels(luigi.Task):
    """
    Get Features and Labels from CSV files.
    """
    """
    connection_string: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    container_name: str = luigi.Parameter()
    output_path: str = luigi.Parameter()
    """

    gist_input_url: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    container_name: str = luigi.Parameter()
    output_path: str = luigi.Parameter()
   # def requires(self):
   #     return LoadCSV(self.gist_input_url)

    def run(self):
        # list = [self.filename, "test.csv"]
        # for elem in list:
        # directory_in: str = os.path.join(self.gist_input_url, self.filename)
        directory_in: str = os.path.join("clc", "urban_sound_files") #os.path.join(self.gist_input_url)
        data_in: DataFrame = pd.read_csv(os.path.join(directory_in, self.filename), sep=",")

        X, y = get_features_and_labels(data_in, directory_in)

        with self.output()[self.filename+"_x"].open('w') as outfile:
            np.savetxt(outfile, X, delimiter=",")
        with self.output()[self.filename+"_y"].open('w') as outfile:
            np.savetxt(outfile, y, delimiter=",")

    def output(self):
       output_train_x = os.path.join(self.output_path,  "getFeatureLabel", f'train_x_{self.filename}')
       output_train_y = os.path.join(self.output_path, "getFeatureLabel", f'train_y_{self.filename}')
       return {self.filename+"_x": luigi.LocalTarget(output_train_x),
               self.filename+"_y": luigi.LocalTarget(output_train_y)}
    # Output with Azure
    #def output(self):
    #   return {
    #       self.filename+"_x": AzureBlobTarget(container=self.container_name, blob=f'train_x_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
    #        self.filename+"_y": AzureBlobTarget(container=self.container_name, blob=f'train_y_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
    #    }


class ValidationSplit(luigi.Task):

    gist_input_url: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    container_name: str = luigi.Parameter()
    output_path: str = luigi.Parameter()

    def requires(self):
        return GetFeaturesLabels(self.gist_input_url, self.filename, self.connection_string, self.container_name, self.output_path)

    def run(self):
        """
        directory_in_x: str = os.path.join(self.output_path, "train_test", "train_x.csv")
        directory_in_y: str = os.path.join(self.output_path, "train_test", "train_y.csv")
        x_train: DataFrame = pd.read_csv(directory_in_x, sep=",")
        y_train: DataFrame = pd.read_csv(directory_in_y, sep=",")
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=9)
        """
        """
        Try reading AzureBlob with AzureBlobTarget
        tar1 = AzureBlobTarget(container=self.container_name, blob=f'train_x_{self.filename}',
                        client=AzureBlobClient(connection_string=self.connection_string))
        tar2 = AzureBlobTarget(container=self.container_name, blob=f'train_y_{self.filename}',
                        client=AzureBlobClient(connection_string=self.connection_string))

        with tar1.open('r') as infile:
            fr = infile.read()
            x_train: DataFrame = pd.read_csv(fr, sep=",")
        with tar2.open('r') as infile:
            fr = infile.read()
            y_train: DataFrame = pd.read_csv(fr, sep=",")
        """
        directory_in: str = os.path.join(self.output_path, "getFeatureLabel")
        x_train: DataFrame = pd.read_csv(os.path.join(directory_in, f'train_x_{self.filename}'), sep=",")
        y_train: DataFrame = pd.read_csv(os.path.join(directory_in, f'train_x_{self.filename}'), sep=",")
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=9)

        #with self.output()["x_train"].open('w') as outfile:
        #    x_train.to_csv(outfile, line_terminator="")
        #with self.output()["x_val"].open('w') as outfile:
        #    x_val.to_csv(outfile, line_terminator="")
        #with self.output()["y_train"].open('w') as outfile:
        #    y_train.to_csv(outfile, line_terminator="")
        #with self.output()["y_val"].open('w') as outfile:
        #    y_val.to_csv(outfile, line_terminator="")

        with self.output()[self.filename + "_train_x"].open('w') as outfile:
            np.savetxt(outfile, x_train, delimiter=",")
        with self.output()[self.filename + "_train_y"].open('w') as outfile:
            np.savetxt(outfile, y_train, delimiter=",")
        with self.output()[self.filename + "_val_x"].open('w') as outfile:
            np.savetxt(outfile, x_val, delimiter=",")
        with self.output()[self.filename + "_val_y"].open('w') as outfile:
            np.savetxt(outfile, y_val, delimiter=",")

    """
    def output(self):
       return {
           self.filename+"_train_x": AzureBlobTarget(container=self.container_name, blob=f'fin/train_x_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
            self.filename+"_train_y": AzureBlobTarget(container=self.container_name, blob=f'fin/train_y_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
            self.filename+"_val_x": AzureBlobTarget(container=self.container_name, blob=f'fin/val_x_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
           self.filename+"_val_y": AzureBlobTarget(container=self.container_name, blob=f'fin/val_y_{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
        }
    """
    def output(self) -> luigi.Target:
       output_train_x = os.path.join(self.output_path,  "train_val", "x_train_"+self.filename)
       output_train_y = os.path.join(self.output_path, "train_val", "x_val_"+self.filename)
       output_val_x = os.path.join(self.output_path,  "train_val", "y_train_"+self.filename)
       output_val_y = os.path.join(self.output_path, "train_val", "y_val_"+self.filename)
       return {self.filename+"_train_x": luigi.LocalTarget(output_train_x),
               self.filename+"_val_x": luigi.LocalTarget(output_train_y),
               self.filename+"_train_y": luigi.LocalTarget(output_val_x),
               self.filename+"_val_y": luigi.LocalTarget(output_val_y)}


class TrainModel(luigi.Task):
    """
    Train model with given training and validation Data
    Save the trained Model under a given name
    """
    gist_input_url: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    container_name: str = luigi.Parameter()
    output_path: str = luigi.Parameter()
    model_name: str = luigi.Parameter()

    def requires(self):
        return ValidationSplit(self.gist_input_url, self.filename, self.connection_string, self.container_name, self.output_path)

    def run(self):
        x_train = np.genfromtxt(os.path.join(self.output_path,  "train_val", "x_train_"+self.filename), delimiter=',')
        y_train = np.genfromtxt(os.path.join(self.output_path,  "train_val", "y_train_"+self.filename), delimiter=',')
        x_val = np.genfromtxt(os.path.join(self.output_path,  "train_val", "x_val_"+self.filename), delimiter=',')
        y_val = np.genfromtxt(os.path.join(self.output_path,  "train_val", "y_val_"+self.filename), delimiter=',')

        num_labels = y_train.shape[1]
        model = UrbanModels.create_mlp(num_labels)

        # Train model
        model, history = ModelUtils.train_mpl(model, x_train, x_val, y_train, y_val)

        fs = LocalFileSystem()
        fs.mkdir(self.output_path)
        model.save(os.path.join(self.output_path, self.model_name + ".h5"))

        with self.output().open('w') as fout:
            f = open(os.path.join(self.output_path, self.model_name + ".h5"), "rb")
            fr = f.read()
            fout.write(fr)

    def output(self) -> luigi.Target:

        return AzureBlobTarget(
            container=self.container_name,
            blob=os.path.join(self.model_name + ".h5"),
            client=AzureBlobClient(
                connection_string=self.connection_string
            )
            , format=luigi.format.Nop
        )


class RunAllModels(luigi.WrapperTask):
    """

    """
    input_path: str = os.path.join("data_pipeline", "csv")
    output_path: str = os.path.join("clc", "csv")
    model_output_path: str = os.path.join("data_pipeline", "models")
    model_name: str = "CNN"

    def requires(self) -> Generator[luigi.Task, None, None]:
        # gist where the CSV files are stored
        gist_url = 'https://gist.githubusercontent.com/falknerdominik/425d72f02bd58cb5d42c3ddc328f505f/raw/4ad926e347d01f45496ded5292af9a5a5d67c850/'
        # connection string obtained for the storage unit via azure
        azure_connection_string = 'DefaultEndpointsProtocol=https;AccountName=storageaccountclcluigi;AccountKey=NK/tDtLASVTM/lJ0BgsPNSf2r6pXoJYFf9obiipXfWOtPxzz0NAwANmbKNiX9PXol2nyijvZGPJiz0fvzQl06Q==;EndpointSuffix=core.windows.net'
        container_name = 'clcstoragecontainer'

        for filename in ['train_short.csv', 'test.csv']:
            if filename.__contains__("test"):
                yield GetFeaturesLabels(
                    gist_input_url=f'{gist_url}{filename}',
                    filename=filename,
                    connection_string=azure_connection_string,
                    container_name=container_name,
                    output_path=self.output_path
                )
            else:
                yield TrainModel(
                    gist_input_url=f'{gist_url}{filename}',
                    filename=filename,
                    connection_string=azure_connection_string,
                    container_name=container_name,
                    output_path=self.output_path,
                    model_name="trained_mlp_1"
                )


def run_pipeline_wo():
    luigi.build([RunAllModels()], local_scheduler=True)
