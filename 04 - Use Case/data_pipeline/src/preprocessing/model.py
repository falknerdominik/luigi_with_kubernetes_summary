from __future__ import print_function

from keras import Sequential
from keras.engine.saving import load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential


class ModelUtils:
    """
    In this class some important model utils are included.
    """

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
    This class includes Multilayer Perception to classify different urban sounds.
    """
    @staticmethod
    def create_mlp(num_labels):
        """
        Define model architecture. Therefore, Keras will be used to create a MultiLayer Perceptron network.
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
