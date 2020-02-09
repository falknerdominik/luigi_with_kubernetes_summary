from __future__ import print_function

import keras
from keras import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.engine.saving import load_model
from tensorflow.keras.layers import Activation, GlobalAveragePooling2D, Conv1D, MaxPooling1D, Dense, Dropout
from keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential
import numpy as np


class ModelUtils:
    """
    In this class some important model utils are included.
    """

    def fit_and_evaluate(x_train, x_val, y_train, y_val, EPOCHS=20, BATCH_SIZE=128):
        """
        Function to fit the model.

        :param x_train: Trainings data.
        :param x_val: Validation data.
        :param y_train: Trainings labels.
        :param y_val: Validation labels.
        :param EPOCHS: Amount of Epochs.
        :param BATCH_SIZE: Batch Size.
        :return: Fitted model.
        """

        # early stopping criteria
        patience: int = 5
        early_stopping = EarlyStopping(monitor="val_loss", patience=patience, verbose=1)
        # save model as physical file
        model_checkpoint = ModelCheckpoint("fas_mnist_1.h5", verbose=1, save_best_only=True)

        model = UrbanModels.cnn(x_train, y_train)
        result = model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE,
                            callbacks=[early_stopping, model_checkpoint],
                            verbose=1, validation_split=0.1)

        print("Validation Score: ", model.evaluate(x_val, y_val))

        return result

    def train_mpl(model, x_train, x_test, y_train_val, y_test_val):
        """
        Compile, train and save model.

        :param model: Model.
        :param x_train: Trainings data
        :param x_test: Test data
        :param y_train_val: Trainings label
        :param y_test_val: Test label
        :param model_file: Name of model.
        :return: Scores and loaded model.

        """

        callbacks = [EarlyStopping(monitor="loss", patience=5, verbose=0, mode="auto")]

        # compile the model
        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
        print(model.summary())

        print("training for 200 epochs with batch size 32")
        history = model.fit(x_train, y_train_val, batch_size=15, epochs=200, validation_data=(x_test, y_test_val),
                            callbacks=callbacks)

        # save model to disc
        print("saving model to disk")
        # model.save(model_file)

        return model, history

    def compute(x_test, y_test, model_file):
        """
        Check if model is performing well.

        :param x_test: Test data.
        :param y_test: Test labels.
        :param model_file: Path to our model.
        :return: Returns the score.
        """

        # load model from disc
        loaded_model = load_model(model_file)
        score = loaded_model.evaluate(x_test, y_test)

        return score[0], score[1] * 100, loaded_model


class UrbanModels:
    """
    This class includes different models used to classify different urban sounds. Thereby, the following neuronal
    networks are defined:
    - Multilayer Perception
    - Recurrent Networks (LSTM, GRU, RNNs)
    - CNNs
    """

    @staticmethod
    def lstm(x, y, neurons: int =100):
        """
        This function creates a LSTM.
        :param x:
        :param y:       the shape of the output layer is calculated from this variable
        :param neurons: amount of neurons of the LSTM layer
        :return:        keras sequential model
        """
        num_labels = y.shape[1]
        model = Sequential()

        model.add(LSTM(neurons, dropout=0.2, recurrent_dropout=0.2))

        model.add(Dense(num_labels))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model

    @staticmethod
    def cnn(X, y):
        # todo: add more layer
        """
        Good one -- accuracy ~63%
        :param X:
        :param y:
        :return:
        """
        num_labels = y.shape[1]
        filter_size = 2

        # build model
        model = Sequential()

        model.add(Dense(256, input_shape=(40,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(num_labels))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

        return model

    # !!!!
    @staticmethod
    def get_cnn(x_train, y_train, dropout):
        """
        Define model architecture. Therefore, Keras will be used to create a Convolutional Neuronal Network.

        :param x_train: Trainings data.
        :param y_train: Trainings labels.
        :param dropout: Dropout value.
        :return: Model.
        """

        model = Sequential()
        n_timestamps, n_features, n_outputs = x_train.shape[1], x_train.shape[2], y_train.shape[1]

        model.add(Conv1D(filters=64, kernel_size=3, activation="relu", input_shape=(n_timestamps, n_features)))
        model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
        model.add(Dropout(dropout))
        model.add(MaxPooling1D(pool_size=2))

        # marks the border between feature seach and classification
        model.add(Flatten())

        # classification layer
        model.add(Dense(100, activation='relu'))
        model.add(Dense(n_outputs, activation='softmax'))

        return model

    def create_mlp(num_labels):
        """
        Define model architecture. Therefore, Keras will be used to create a Multi Layer Perceptron network.
        :param num_labels:
        :return: Model.
        """
        model = Sequential()
        model.add(Dense(256, input_shape=(40,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(256, input_shape=(40,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(num_labels))
        model.add(Activation('softmax'))

        return model
