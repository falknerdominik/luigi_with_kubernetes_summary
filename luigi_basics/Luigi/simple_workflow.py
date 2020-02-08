"""Preprocessing example to show how luigi works (only one preprocessing step will be executed!)."""
import os
from typing import Generator

import luigi
import pandas as DataFrame
import pandas as pd
from luigi.format import TextWrapper

from luigi_basics.Luigi.preprocessing import drop_nan_columns, drop_duplicates


class LoadCSV(luigi.ExternalTask):
    """
    Gives access to the CSV dump files which should be preprocessed.
    """

    path: str = luigi.Parameter()

    def output(self) -> luigi.Target:
        return luigi.LocalTarget(self.path)


class Preprocess(luigi.Task):
    """
    Applies general preprocessing steps to all CSV files loaded.
    """
    input_path: str = luigi.Parameter()
    output_path: str = luigi.Parameter()

    def requires(self):
        return LoadCSV(self.input_path)

    def run(self):
        data_in: DataFrame = pd.read_csv(self.input_path, sep=";")

        data_preprocessed = drop_nan_columns(data_in)
        # data_preprocessed = drop_duplicates(data_in)

        output_file: TextWrapper

        with self.output().open("w") as output_file:
            data_preprocessed.to_csv(output_file)

    def output(self) -> luigi.Target:
        return luigi.LocalTarget(self.output_path)


class PreprocessAllFiles(luigi.WrapperTask):
    """
    Applies defined preprocessing steps to all files in the selected folder.
    """

    input_path: str = os.path.join("data", "raw")
    output_path: str = os.path.join("data", "processed")

    def requires(self) -> Generator[luigi.Task, None, None]:
        for filename in os.listdir(self.input_path):
            csv_input_path: str = os.path.join(self.input_path, filename)
            csv_output_path: str = os.path.join(self.output_path, filename)

            yield Preprocess(input_path=csv_input_path, output_path=csv_output_path)


if __name__ == "__main__":
    luigi.build([PreprocessAllFiles()], local_scheduler=True)
