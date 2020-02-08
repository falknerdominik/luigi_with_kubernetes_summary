"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
import h5py
import os
from typing import Generator

import luigi
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient
import numpy as np
from luigi.local_target import LocalFileSystem

from src.trainModel.model import UrbanModels, ModelUtils
from azure.storage.blob import BlockBlobService

"""


    # Create Model
    num_labels = y_train.shape[1]
    model = UrbanModels.create_mlp(num_labels)

    # Train model
    model, history = ModelUtils.train_mpl(model, x_train, x_test, y_train, y_test, model_file)
"""


class NonAtomicKerasTarget(luigi.Target):
    fs = LocalFileSystem()

    def __init__(self, path: str):
        self.path = path

    def save(self, model: any) -> None:
        # @TODO: add self.makedirs() if keras doesn't automatically create the necessary directories
        model.save(self.path)

    def exists(self) -> bool:
        return self.fs.exists(self.path)


class NonAtomicKerasAzureTarget(luigi.Target):
    fs = LocalFileSystem()

    def __init__(self, path: str, account_name: str, account_key: str, container_name: str):
        self.path = path
        # self.account_name = account_name
        # self.account_key = account_key
        self.container_name = str(container_name)
        self.block_blob_service = BlockBlobService(account_name=str(account_name), account_key=str(account_key))

    def save(self, model: any) -> None:
        # @TODO: add self.makedirs() if keras doesn't automatically create the necessary directories
        # os.makedirs(self.path)
        model.save(self.path)
        local_path = os.path.abspath(os.path.curdir)
        full_path_to_file = os.path.join(local_path, self.path)
        # Upload the created file, use local_file_name for the blob name
        self.block_blob_service.create_blob_from_path(self.container_name, str('testLuigi.h5'), str(full_path_to_file))

    # def load(self) -> any:
    #    # @TODO: call the correct keras function for model loading here
    #    return load_model(self.path)

    def exists(self) -> bool:
        return self.fs.exists(self.path)


class HdfAttributeTarget(luigi.Target):

    def __init__(self, filename, dataset, attribute):
        self.filename = filename
        self.dataset = dataset
        self.attribute = attribute

    def exists(self):
        if not os.path.isfile(self.filename):
            return False
        try:
            with h5py.File(self.filename, 'r') as f:
                return self.dataset in f and self.attribute in f[self.dataset].attrs
        except:
            return False


class ModelTarget(luigi.Target):
    fs = LocalFileSystem()

    def __init__(self, path=None):
        self.path = path

    def exists(self):
        return self.fs.exists(self.path)

    def read(self, **kwargs):
        """
        Opens bcolz ctable/carray in read-only mode.
        """
        if self.exists():
            data = h5py.open(self.path, mode='r', **kwargs)

            return data

    def write(self, model, **kwargs):
        """
        Write a dataframe or bcolz ctable/carray to the specified
        filepath.
        """
        self.makedirs()

        return h5py.File(self.path, 'w')

    def makedirs(self):
        """
        Create all parent folders if they do not exist.
        """
        normpath = os.path.normpath(self.path)
        parentfolder = os.path.dirname(normpath)
        if parentfolder:
            try:
                os.makedirs(parentfolder)
            except OSError:
                pass


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

    # connection_string: str = luigi.Parameter()
    # container_name: str = luigi.Parameter()

    # def requires(self):
    #    pass

    def run(self):
        x_train = np.genfromtxt(os.path.join(self.input_path, "x_train.csv"), delimiter=',')
        y_train = np.genfromtxt(os.path.join(self.input_path, "y_train.csv"), delimiter=',')
        x_val = np.genfromtxt(os.path.join(self.input_path, "x_val.csv"), delimiter=',')
        y_val = np.genfromtxt(os.path.join(self.input_path, "y_val.csv"), delimiter=',')
        x_test = np.genfromtxt(os.path.join(self.input_path, "x_test.csv"), delimiter=',')
        y_test = np.genfromtxt(os.path.join(self.input_path, "y_test.csv"), delimiter=',')
        model_file = "Ressource/models/trained_mlp.h5"
        model_name = "trained_mlp"

        num_labels = y_train.shape[1]
        model = UrbanModels.create_mlp(num_labels)

        # Train model
        model, history = ModelUtils.train_mpl(model, x_train, x_test, y_train, y_test, model_file)

        model.save(os.path.join(self.output_path, "trained_mlp.h5"))

        # Speichern das Modes lokal mit einem Eigenen Target NonAtomicKerasTarget
        # self.output()['output1'].save(model)
        with self.output().open('wb') as fout:
            f = open(os.path.join(self.output_path, "trained_mlp.h5"), "rb")
            fr = f.read()
            fout.write(fr)

    def output(self) -> luigi.Target:
        output_dir1 = os.path.join(self.output_path, "trained_mlp.h5")
        output_dir2 = os.path.join(self.output_path, "train_short22.csv")
        luigi.LocalTarget(output_dir1)

        account_name = 'storageaccountclcluigi',
        account_key = 'NK/tDtLASVTM/lJ0BgsPNSf2r6pXoJYFf9obiipXfWOtPxzz0NAwANmbKNiX9PXol2nyijvZGPJiz0fvzQl06Q=='
        container_name = 'clcstoragecontainer'
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=storageaccountclcluigi;AccountKey=NK/tDtLASVTM/lJ0BgsPNSf2r6pXoJYFf9obiipXfWOtPxzz0NAwANmbKNiX9PXol2nyijvZGPJiz0fvzQl06Q==;EndpointSuffix=core.windows.net'

        # Versuch das Modul im Azure Blob Storage zu speichern mit dem Azure Blob Target --> Connection funkioniert
        # nicht
        return AzureBlobTarget(
            container='clcstoragecontainer',
            blob="trained_mlp.h5",
            client=AzureBlobClient(
                connection_string='DefaultEndpointsProtocol=https;AccountName=storageaccountclc;AccountKey=soGFPvXy+lmdLUvj3v0qK7q0rtHe5kdNBL4w2cQd6qqhQ7py5CJQDUEvyqq6AyWnn+AWV/kiIStjDQgXlri7ng==;EndpointSuffix=core.windows.net'
            )
        )
        # Speichern das Modul im Azure Blob Storage mit einem eigenen Target
        #               --> funktioniert irgendwie nicht (ohne Luigi funktioniert der selbe Code aber ...
        # return {'output1': NonAtomicKerasAzureTarget(output_dir1, account_name, account_key, container_name)}
        # Speicher das Modul lokal mit einem eigenem Target
        # return {'output1': NonAtomicKerasTarget(output_dir1)}

    """
    Dominik
    azure_connection_string = 'DefaultEndpointsProtocol=https;AccountName=storageaccountclc;AccountKey=soGFPvXy+lmdLUvj3v0qK7q0rtHe5kdNBL4w2cQd6qqhQ7py5CJQDUEvyqq6AyWnn+AWV/kiIStjDQgXlri7ng==;EndpointSuffix=core.windows.net'
    # container_name = '<Insert-Container-Name>'
    container_name = 'clcstoragecontainer'

    """


class PreprocessAllFiles(luigi.WrapperTask):
    """
    Applies defined preprocessing steps to all files in the selected folder.
    """

    input_path: str = os.path.join("test")
    output_path: str = os.path.join("test1")

    # connection string obtained for the storage unit via azure
    # azure_connection_string = '<Insert-Connection-String>'
    # container_name = '<Insert-Container-Name>'

    def requires(self) -> Generator[luigi.Task, None, None]:
        yield TrainModel(input_path=self.input_path, output_path=self.output_path  # ,
                         # connection_string=self.azure_connection_string,
                         # container_name=self.container_name
                         )
        """
        for filename in os.listdir(self.input_path):
            csv_input_path: str = os.path.join(self.input_path, filename)
            csv_output_path: str = os.path.join(self.output_path, filename)

            yield TrainModel(input_path=csv_input_path, output_path=csv_output_path)
        """


if __name__ == "__main__":
    # luigi.build([PreprocessAllFiles()], local_scheduler=True)
    luigi.build([TrainModel(os.path.join("test"), os.path.join("test1"))], local_scheduler=True)
