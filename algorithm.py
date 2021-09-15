#!/usr/bin/env python
# coding=utf-8

import logging

logger = logging.getLogger()

import numpy
import scipy.optimize


def make_labels(X):
    """Helper function that generates a single 1D array with labels which
    are good targets for stock logistic regression.


    Parameters
    ==========

    X : numpy.ndarray

        The input data matrix. This must be an array with 3 dimensions or an
        iterable containing 2 arrays with 2 dimensions each. Each correspond to
        the data for one of the two classes, every row corresponds to one
        example of the data set, every column, one different feature.


    Returns
    =======

    labels : numpy.ndarray
        With a single dimension, containing suitable labels for all rows and
        for all classes defined in X (depth).

    """

    return numpy.hstack(
        [k * numpy.ones(len(X[k]), dtype=int) for k in range(len(X))]
    )


class Machine:
    """A class to handle all run-time aspects for Logistic Regression

    Parameters
    ==========

    theta : numpy.ndarray
        A set of parameters for the Logistic Regression model. This must be an
        iterable (or numpy array) with all parameters for the model, including
        the bias term, which must be on entry 0 (the first entry at the
        iterable).

    """

    def __init__(self, theta):
        self.theta = numpy.array(theta).copy()

    def __call__(self, X):
        """Spits out the hypothesis given the data.


        Parameters
        ==========

        X : numpy.ndarray

            The input data matrix. This must be an array with 2 dimensions.
            Every row corresponds to one example of the data set, every column,
            one different feature.


        Returns
        =======

        hypothesis : numpy.ndarray
            A 1D array with as many entries as rows in the input 2D array
            ``X``, representing g(x), the sigmoidal hypothesis.

        """

        Xp = numpy.hstack((numpy.ones((len(X), 1)), X))  # add bias term
        return 1.0 / (1.0 + numpy.exp(-numpy.dot(Xp, self.theta)))

    def predict(self, X):
        """Predicts the class of each row of X


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 2 dimensions.
            Every row corresponds to one example of the data set, every column,
            one different feature.


        Returns
        =======

        predictions : numpy.ndarray
            A 1D array with as many entries as rows in the input 2D array
            ``X``, representing g(x), the class predictions for the current
            machine.

        """

        retval = self(X)
        retval[retval < 0.5] = 0.0
        retval[retval >= 0.5] = 1.0
        return retval.astype(int)

    def J(self, X, regularizer=0.0):
        """
        Calculates the logistic regression cost

        Parameters
        ==========

        X : numpy.ndarray

            The input data matrix. This must be an array with 3 dimensions or an
            iterable containing 2 numpy.ndarrays with 2 dimensions each. Each
            correspond to the data for one of the two classes, every row
            corresponds to one example of the data set, every column, one
            different feature.

        regularizer : float
            The regularization parameter


        Returns
        =======

        cost : float
            The averaged (regularized) cost for the whole dataset

        """

        h = numpy.hstack([self(X[k]) for k in (0, 1)])
        y = make_labels(X)

        logh = numpy.nan_to_num(numpy.log(h))
        log1h = numpy.nan_to_num(numpy.log(1 - h))
        regularization_term = regularizer * (self.theta[1:] ** 2).sum()
        main_term = -(y * logh + ((1 - y) * log1h)).mean()
        return main_term + regularization_term

    def dJ(self, X, regularizer=0.0):
        """
        Calculates the logistic regression first derivative of the cost w.r.t.
        each parameter theta


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 3 dimensions or
            an iterable containing 2 arrays with 2 dimensions each. Each
            correspond to the data for one of the two classes, every row
            corresponds to one example of the data set, every column, one
            different feature.

        regularizer : float
            The regularization parameter, if the solution should be regularized.


        Returns
        =======

        grad : numpy.ndarray
            A 1D array with as many entries as columns on the input matrix
            ``X`` plus 1 (the bias term). It denotes the average gradient of
            the cost w.r.t. to each machine parameter theta.

        """

        Xflat = numpy.vstack([k for k in X])
        Xp = numpy.hstack((numpy.ones((len(Xflat), 1)), Xflat))  # add bias term
        y = make_labels(X)

        retval = ((self(Xflat) - y) * Xp.T).T.mean(axis=0)
        retval[1:] += (regularizer * self.theta[1:]) / len(X)
        return retval


class Trainer:
    """A class to handle all training aspects for Logistic Regression


    Parameters
    ==========

    regularizer : float
        The regularization parameter

    """

    def __init__(self, regularizer=0.0):
        self.regularizer = regularizer

    def J(self, theta, machine, X):
        """
        Calculates the vectorized cost *J*.
        """

        machine.theta = theta
        return machine.J(X, self.regularizer)

    def dJ(self, theta, machine, X):
        """
        Calculates the vectorized partial derivative of the cost *J* w.r.t. to
        **all** :math:`\\theta`'s. Use the training dataset.
        """

        machine.theta = theta
        return machine.dJ(X, self.regularizer)

    def train(self, X):
        """
        Optimizes the machine parameters to fit the input data, using
        ``scipy.optimize.fmin_l_bfgs_b``.


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 3 dimensions or
            an iterable containing 2 arrays with 2 dimensions each.  Each
            correspond to the data for one of the two classes, every row
            corresponds to one example of the data set, every column, one
            different feature.


        Returns
        =======

        machine : Machine
            A trained machine.


        Raises
        ======

        RuntimeError
            In case problems exist with the design matrix ``X`` or with
            convergence.

        """

        # check data dimensionality if not organized in a matrix
        if not isinstance(X, numpy.ndarray):
            baseline = X[0].shape[1]
            for k in X:
                if k.shape[1] != baseline:
                    raise RuntimeError(
                        "Mismatch on the dimensionality of input `X`"
                    )

        # prepare the machine
        theta0 = numpy.zeros(X[0].shape[1] + 1)  # include bias terms
        machine = Machine(theta0)

        logger.debug("Settings:")
        logger.debug("  * initial guess = %s", [k for k in theta0])
        logger.debug("  * cost (J) = %g", machine.J(X, self.regularizer))
        logger.debug("Training using scipy.optimize.fmin_l_bfgs_b()...")

        # Fill in the right parameters so that the minimization can take place
        theta, cost, d = scipy.optimize.fmin_l_bfgs_b(
            self.J,
            theta0,
            self.dJ,
            (machine, X),
        )

        if d["warnflag"] == 0:

            logger.info("** LBFGS converged successfuly **")
            machine.theta = theta
            logger.debug("Final settings:")
            logger.debug("  * theta = %s", [k for k in theta])
            logger.debug("  * cost (J) = %g", cost)
            return machine

        else:
            message = "LBFGS did **not** converged:"
            if d["warnflag"] == 1:
                message += " Too many function evaluations"
            elif d["warnflag"] == 2:
                message += "  %s" % d["task"]
            raise RuntimeError(message)


class MultiClassMachine:
    """A class to handle all run-time aspects for Multiclass Log. Regression


    Parameters
    ==========

    machines : :py:class:`list` or :py:class:`tuple`
        An iterable over any number of machines that will be stored.

    """

    def __init__(self, machines):
        self.machines = machines

    def __call__(self, X):
        """Spits out the hypothesis for each machine given the data


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 2 dimensions.
            Every row corresponds to one example of the data set, every column,
            one different feature.


        Returns
        =======

        hypothesis : numpy.ndarray
            A 2D array with as many entries as rows in the input 2D
            array ``X``, representing g(x), the sigmoidal hypothesis. Each
            column on the output array represents the output of one of the
            logistic regression machines in this

        """

        return numpy.vstack([m(X) for m in self.machines]).T

    def predict(self, X):
        """Predicts the class of each row of X


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 3 dimensions or
            an iterable containing 2 arrays with 2 dimensions each.  Each
            correspond to the data for one of the two classes, every row
            corresponds to one example of the data set, every column, one
            different feature.


        Returns
        =======

        predictions : numpy.ndarray
            A 1D array with as many entries as rows in the input 2D array
            ``X``, representing g(x), the class predictions for the current
            machine.

        """

        return self(X).argmax(axis=1)


class MultiClassTrainer:
    """A class to handle all training aspects for Multiclass Log. Regression


    Parameters
    ==========

    regularizer : float
        The regularization parameter

    """

    def __init__(self, regularizer=0.0):
        self.regularizer = regularizer

    def train(self, X):
        """
        Trains multiple logistic regression classifiers to handle the multiclass
        problem posed by ``X``.


        Parameters
        ==========

        X : numpy.ndarray
            The input data matrix. This must be an array with 3 dimensions or
            an iterable containing 2 arrays with 2 dimensions each.  Each
            correspond to the data for one of the input classes, every row
            corresponds to one example of the data set, every column, one
            different feature.


        Returns
        =======

        machine : Machine
            A trained multiclass machine.

        """
        _trainer = Trainer(self.regularizer)

        if (
            len(X) == 2
        ):  # trains and returns a single logistic regression classifer

            return _trainer.train(X)

        else:  # trains and returns a multi-class logistic regression classifier

            # use one-versus-all strategy
            machines = []
            for k in range(len(X)):
                NC_range = list(range(0, k)) + list(range(k + 1, len(X)))
                Xp = [numpy.vstack(X[NC_range]), X[k]]
                machines.append(_trainer.train(Xp))

            return MultiClassMachine(machines)
