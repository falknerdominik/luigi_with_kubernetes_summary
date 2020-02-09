"""
This module includes an example preprocessing step.
"""

import pandas as DataFrame


def drop_nan_columns(data: DataFrame) -> DataFrame:
    """
    Drop all columns with more than 80percent missing values.

    :param data: Input DataFrame which should be preprocessed.
    :return: DataFrame where columns with more than 80 percent missing values are deleted.
    """
    data = data.dropna(axis=1, thresh=(len(data)*80)/100)
    return data


def drop_duplicates(data: DataFrame) -> DataFrame:
    """
    Drop duplicated rows and columns.

    :param data: Input DataFrame which should be preprocessed.
    :return: DataFrame where columns with more than 80 percent missing values are deleted.
    """
    data = data.drop_duplicates()
    return data
