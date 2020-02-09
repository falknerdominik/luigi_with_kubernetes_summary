"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
from typing import Generator

import luigi
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient
from luigi.contrib.kubernetes import KubernetesJobTask


class Preprocess(KubernetesJobTask):
    """
    Applies general preprocessing steps to all CSV files loaded.
    """
    # gist_input_url: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    container_name: str = luigi.Parameter()

    def output(self) -> luigi.Target:
        # save the output in the azure blob storage
        # noinspection PyTypeChecker
        return AzureBlobTarget(
            container=self.container_name,
            blob=self.filename,
            client=AzureBlobClient(
                connection_string=self.connection_string)
        )

    # kubernetes methods
    @property
    def name(self):
        """Name of kubernetes job"""
        return 'train-model'

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
        return ['python', '-m', f'clc.preprocessing', self.filename]


class PreprocessAllFiles(luigi.WrapperTask):
    """
    Applies defined preprocessing steps to all files in the selected folder.
    """
    # connection string obtained for the storage unit via azure
    # azure_connection_string = '<Insert-Connection-String>'
    azure_connection_string = 'DefaultEndpointsProtocol=https;AccountName=storageaccountclc;AccountKey=soGFPvXy+lmdLUvj3v0qK7q0rtHe5kdNBL4w2cQd6qqhQ7py5CJQDUEvyqq6AyWnn+AWV/kiIStjDQgXlri7ng==;EndpointSuffix=core.windows.net'
    # container_name = '<Insert-Container-Name>'
    container_name = 'clcstoragecontainer'

    def requires(self) -> Generator[luigi.Task, None, None]:
        for filename in ['train_short.csv', 'test.csv']:
            yield Preprocess(
                filename=filename,
                connection_string=self.azure_connection_string,
                container_name=self.container_name,
            )


def run_pipeline():
    luigi.build([PreprocessAllFiles()], local_scheduler=True)
