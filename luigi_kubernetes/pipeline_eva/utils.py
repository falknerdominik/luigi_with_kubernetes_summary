"""

"""
import os

import librosa
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder


def get_feature_label(row, directory):
    file_name = os.path.join("data_pipeline", "urban_sound_files", str(row.ID) + '.wav')
    # handle exception to check if there isn't a file which is corrupted
    try:
        # here kaiser_fast is a technique used for faster extraction
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        # extract mfcc feature from data
        mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
        mfccs_scaled: np = np.mean(mfccs.T, axis=0)

    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None, None

    feature: np = mfccs_scaled
    label = row.Class

    return feature, label


def get_data_labels(featues_df: DataFrame) -> DataFrame:
    """
    Convert features and corresponding classification labels into numpy arrays so that they can be feeded into
    neuronal network.

    :param temp:
    :return: X and y parameter y is our target variable
    """
    X: np = np.array(featues_df.feature.tolist())
    y: np = np.array(featues_df.label.tolist())

    # encode label classification
    le = LabelEncoder()
    # one hot encoded labels
    # yy = to_categorical(le.fit_transform(y))

    return X, X# yy


def get_features_and_labels(data_in, directory):
    """
    """
    # function to load files and extract features
    train_temp: DataFrame = pd.DataFrame(columns=['feature', 'label'])
    for idx, row in data_in.iterrows():
            feature, label = get_feature_label(row, directory)
            train_temp = train_temp.append({'feature': feature, 'label': label}, ignore_index=True)
    train_temp.columns = ['feature', 'label']
    x_train, y_train = get_data_labels(train_temp)

    return x_train, y_train

