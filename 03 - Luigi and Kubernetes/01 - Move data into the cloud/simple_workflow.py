"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
from typing import Generator

import luigi
import pandas as DataFrame
import pandas as pd
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient

from preprocess import drop_nan_columns


class Preprocess(luigi.Task):
    """
    Applies general preprocessing steps to all CSV files loaded.
    """
    gist_input_url: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    container_name: str = luigi.Parameter()

    def run(self):
        # read data from url
        data_in: DataFrame = pd.read_csv(self.gist_input_url, sep=";")
        data_preprocessed = drop_nan_columns(data_in)

        # write contents to azure blob file
        with self.output().open("w") as output_file:
            data_preprocessed.to_csv(output_file)

    def output(self) -> luigi.Target:
        # save the output in the azure blob storage
        # noinspection PyTypeChecker
        return AzureBlobTarget(
            container=self.container_name,
            blob=self.filename,
            client=AzureBlobClient(
                connection_string=self.connection_string)
        )


class PreprocessAllFiles(luigi.WrapperTask):
    """
    Applies defined preprocessing steps to all files in the selected folder.
    """
    # gist where the CSV files are stored
    gist_url = 'https://gist.githubusercontent.com/falknerdominik/425d72f02bd58cb5d42c3ddc328f505f/raw/4ad926e347d01f45496ded5292af9a5a5d67c850/'
    # connection string obtained for the storage unit via azure
    azure_connection_string = '<Insert-Connection-String>'
    container_name = '<Insert-Container-Name>'

    def requires(self) -> Generator[luigi.Task, None, None]:
        for filename in ['test_file1.CSV', 'test_file2.CSV']:
            yield Preprocess(
                gist_input_url=f'{self.gist_url}{filename}',
                filename=filename,
                connection_string=self.azure_connection_string,
                container_name=self.container_name,
            )


if __name__ == "__main__":
    luigi.build([PreprocessAllFiles()], local_scheduler=True)
