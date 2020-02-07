"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
import os
from typing import Generator

import luigi
import numpy as np
import pandas as DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split

from luigi_kubernetes.pipeline_eva.utils import get_features_and_labels


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
    input_path: str = luigi.Parameter()
    output_path: str = luigi.Parameter()

    def requires(self):
        return LoadCSV(self.input_path)

    def run(self):
        list = ["train_short.csv", "test.csv"]
        for elem in list:
            directory_in: str = os.path.join(self.input_path, elem)
            data_in: DataFrame = pd.read_csv(directory_in, sep=",")

            X, y = get_features_and_labels(data_in, directory_in)

            with self.output()[elem+"_x"].open('w') as outfile:
                np.savetxt(outfile, X, delimiter=",")
            with self.output()[elem+"_y"].open('w') as outfile:
                np.savetxt(outfile, y, delimiter=",")

    def output(self) -> luigi.Target:
       output_train_x = os.path.join(self.output_path, "train_test", "train_x.csv")
       output_train_y = os.path.join(self.output_path, "train_test", "train_y.csv")
       output_test_x = os.path.join(self.output_path, "train_test", "test_x.csv")
       output_test_y = os.path.join(self.output_path, "train_test", "test_y.csv")
       return {'train_short.csv_x': luigi.LocalTarget(output_train_x),
            'train_short.csv_y': luigi.LocalTarget(output_train_y),
            'test.csv_x': luigi.LocalTarget(output_test_x),
            'test.csv_y': luigi.LocalTarget(output_test_y)}


class ValidationSplit(luigi.Task):
    """
    """

    input_path: str = luigi.Parameter()
    output_path: str = luigi.Parameter()

    def requires(self):
        return GetFeaturesLabels(self.input_path, self.output_path)

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


#class CreateModel(luigi.Task):


class RunAllModels(luigi.WrapperTask):
    """

    """
    input_path: str = os.path.join("data_pipeline", "csv")
    output_path: str = os.path.join("data_pipeline", "csv")
    model_output_path: str = os.path.join("data_pipeline", "models")
    model_name: str = "CNN"

    def requires(self) -> Generator[luigi.Task, None, None]:
        yield ValidationSplit(input_path=self.input_path, output_path=self.output_path)


if __name__ == "__main__":
    luigi.build([RunAllModels()], local_scheduler=True)
