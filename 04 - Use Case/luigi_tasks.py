"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
import os
from typing import Generator

import luigi
import numpy as np
import pandas as DataFrame
import pandas as pd
from luigi.contrib.azureblob import AzureBlobTarget, AzureBlobClient
from utils import get_features_and_labels


class LoadCSV(luigi.ExternalTask):
    """
    Gives access to the CSV dump files which should be preprocessed.
    """

    path: str = luigi.Parameter()

    def output(self) -> luigi.Target:
        return luigi.LocalTarget(self.path)


class GetFeaturesLabels(luigi.Task):
    """
    Get Features and Labels from CSV files.
    """
    connection_string: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    container_name: str = luigi.Parameter()

    output_path: str = luigi.Parameter()

    def requires(self):
        return LoadCSV(self.gist_input_url)

    def run(self):
        # list = [self.filename, "test.csv"]
        # for elem in list:
        # directory_in: str = os.path.join(self.gist_input_url, self.filename)
        directory_in: str = os.path.join(self.gist_input_url)
        data_in: DataFrame = pd.read_csv(directory_in, sep=",")

        X, y = get_features_and_labels(data_in, directory_in)

        with self.output()[self.filename+"_x"].open('w') as outfile:
            np.savetxt(outfile, X, delimiter=",")
        with self.output()[self.filename+"_y"].open('w') as outfile:
            np.savetxt(outfile, y, delimiter=",")

    def output(self):
       return {
           'train_x_short.csv': AzureBlobTarget(container=self.container_name, blob=f'train_x{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
            'train_y_short.csv': AzureBlobTarget(container=self.container_name, blob=f'train_y{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
            'test_x.csv': AzureBlobTarget(container=self.container_name, blob=f'test_x{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
            'test_y.csv': AzureBlobTarget(container=self.container_name, blob=f'test_y{self.filename}', client=AzureBlobClient(connection_string=self.connection_string)),
        }


"""
class ValidationSplit(luigi.Task):

    gist_input_url: str = luigi.Parameter()
    connection_string: str = luigi.Parameter()
    filename: str = luigi.Parameter()
    container_name: str = luigi.Parameter()

    output_path: str = luigi.Parameter()

    def requires(self):
        return GetFeaturesLabels(self.gist_input_url, self.output_path)

    def run(self):
        directory_in_x: str = os.path.join(self.output_path, "train_test", "train_x.csv")
        directory_in_y: str = os.path.join(self.output_path, "train_test", "train_y.csv")
        x_train: DataFrame = pd.read_csv(directory_in_x, sep=",")
        y_train: DataFrame = pd.read_csv(directory_in_y, sep=",")
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=9)

        with self.output()["x_train"].open('w') as outfile:
            x_train.to_csv(outfile, line_terminator="")
        with self.output()["x_val"].open('w') as outfile:
            x_val.to_csv(outfile, line_terminator="")
        with self.output()["y_train"].open('w') as outfile:
            y_train.to_csv(outfile, line_terminator="")
        with self.output()["y_val"].open('w') as outfile:
            y_val.to_csv(outfile, line_terminator="")

    def output(self) -> luigi.Target:
       output_train_x = os.path.join(self.output_path,  "train_val", "x_train.csv")
       output_train_y = os.path.join(self.output_path, "train_val", "x_val.csv")
       output_val_x = os.path.join(self.output_path,  "train_val", "y_train.csv")
       output_val_y = os.path.join(self.output_path, "train_val", "y_val.csv")
       return {'x_train': luigi.LocalTarget(output_train_x),
               'x_val': luigi.LocalTarget(output_train_y),
               'y_train': luigi.LocalTarget(output_val_x),
               'y_val': luigi.LocalTarget(output_val_y)}
"""


class RunAllModels(luigi.WrapperTask):
    """

    """
    input_path: str = os.path.join("data_pipeline", "csv")
    output_path: str = os.path.join("data_pipeline", "csv")
    model_output_path: str = os.path.join("data_pipeline", "models")
    model_name: str = "CNN"

    def requires(self) -> Generator[luigi.Task, None, None]:
        # gist where the CSV files are stored
        gist_url = 'https://gist.githubusercontent.com/falknerdominik/425d72f02bd58cb5d42c3ddc328f505f/raw/4ad926e347d01f45496ded5292af9a5a5d67c850/'
        # connection string obtained for the storage unit via azure
        azure_connection_string = '<Insert-Connection-String>'
        container_name = '<Insert-Container-Name>'

        for filename in ['train_short.csv', 'train_long.csv']:
            # yield ValidationSplit(input_path=self.input_path, output_path=self.output_path)
            yield GetFeaturesLabels(
                gist_input_url=f'{self.gist_url}{filename}',
                filename=filename,
                connection_string=self.azure_connection_string,
                container_name=self.container_name,
            )


if __name__ == "__main__":
    luigi.build([RunAllModels()], local_scheduler=True)
