import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
from mlxtend.evaluate import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix

OUTPUT = "Ressource/plots/"


class Plots:
    """
    This class includes plots to visualize the results of the model.
    """

    def accuracy(hist, model_name) -> None:
        """
        Plot models to see their progress.

        :param hist: Calculated history of the model.
        :param model_name: Name of the model.
        """

        plt.figure()
        plt.ioff()
        plt.plot(hist.history["acc"])
        plt.plot(hist.history["val_acc"])
        plt.title('Model Accuracy')
        plt.ylabel("Accuracy")
        plt.xlabel("Epoch")
        plt.legend(["train", "validation"], loc="upper left")
        #plt.savefig(OUTPUT + "_accuracy_" + model_name)
        plt.legend()
        plt.show()

    def loss(hist, model_name) -> None:
        """
        Plot loss of the history of the model to see their progress.

        :param hist: Calculated history of the model.
        :param model_name: Name of the model.
        :return: None.
        """

        plt.figure()
        plt.ioff()
        plt.plot(hist.history["loss"])
        plt.plot(hist.history["val_loss"])
        plt.title('Model Loss')
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend(["train", "validation"], loc="upper left")
        #plt.savefig(OUTPUT + "_loss_" + model_name)
        #plt.savefig(OUTPUT + "_loss_" + MODEL_NAME)
        plt.legend()
        plt.show()

    def confusion_matrix(y_pred, y_test, model_name) -> None:
        """
        Confusion matrix based on the predicted and the test labels.

        :param y_pred: Predicted labels.
        :param y_test: Test labels.
        :param model_name: Name of the model.
        :return:
        """

        y_target = np.argmax(y_test, axis=1)
        y_pred = np.argmax(y_pred, axis=1)

        cm = confusion_matrix(y_target=y_target,
                              y_predicted=y_pred,
                              binary=False)

        print(cm)
        fig, ax = plot_confusion_matrix(conf_mat=cm)
        plt.title('Confusion Matrix')
        plt.savefig(OUTPUT + "_confusionmatrix_" + model_name)
        plt.show()


def confusionsMatrix2(yhat, yTest):
    ######################################################################################
    # Helpful Links
    # https://rasbt.github.io/mlxtend/user_guide/evaluate/confusion_matrix/
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.argmax.html

    y_target = np.argmax(yTest, axis=1)
    y_predicted = np.argmax(yhat, axis=1)

    cm = confusion_matrix(y_target=y_target,
                          y_predicted=y_predicted,
                          binary=False)

    print(cm)

    fig, ax = plot_confusion_matrix(conf_mat=cm)
    plt.show()