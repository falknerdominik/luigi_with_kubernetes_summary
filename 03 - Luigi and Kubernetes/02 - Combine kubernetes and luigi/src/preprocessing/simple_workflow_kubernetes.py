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
        return ['python', '-m', 'clc.preprocessing', self.filename]


class PreprocessAllFiles(luigi.WrapperTask):
    """
    Applies defined preprocessing steps to all files in the selected folder.
    """
    # connection string obtained for the storage unit via azure
    azure_connection_string = '<Insert-Connection-String>'
    container_name = '<Insert-Container-Name>'

    def requires(self) -> Generator[luigi.Task, None, None]:
        for filename in ['test_file1.CSV', 'test_file2.CSV']:
            yield Preprocess(
                filename=filename,
                connection_string=self.azure_connection_string,
                container_name=self.container_name,
            )


def run_pipeline():
    luigi.build([PreprocessAllFiles()], local_scheduler=True)
