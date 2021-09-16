#!/usr/bin/env python
# coding=utf-8

"""User script to conduct the first hypothesis in the course"""


import logging
import itertools

import numpy

numpy.seterr(divide="ignore")

import database
import preprocessor
import algorithm
import analysis


def test_one(protocol, variables):
    """Runs one single test, returns the CER on the test set"""

    # 1. get the data from our preset API for the database
    train = database.get(protocol, "train", database.CLASSES, variables)

    # 2. preprocess the data using our module preprocessor
    norm = preprocessor.estimate_norm(numpy.vstack(train))
    train_normed = preprocessor.normalize(train, norm)

    # 3. trains our logistic regression system
    trainer = algorithm.MultiClassTrainer()
    machine = trainer.train(train_normed)

    # 4. applies the machine to predict on the 'unseen' test data
    test = database.get(protocol, "test", database.CLASSES, variables)
    test_normed = preprocessor.normalize(test, norm)
    test_predictions = machine.predict(numpy.vstack(test_normed))
    test_labels = algorithm.make_labels(test).astype(int)
    return analysis.CER(test_predictions, test_labels)


def test_impact_of_variables_single(tabnum, protocols):
    """Builds the first table of my report"""

    for n, p in enumerate(protocols):

        print(
            "\nTable %d: Single variables for Protocol `%s`:" % (n + tabnum, p)
        )
        print(60 * "-")

        for k in database.VARIABLES:
            result = test_one(p, [k])
            print(("%-15s" % k), "| %d%%" % (100 * result,))

    return len(protocols)


def test_impact_of_variables_2by2(tabnum, protocols):
    """Builds the first table of my report"""

    for n, p in enumerate(protocols):

        print(
            "\nTable %d: Variable combinations, 2x2 for Protocol `%s`:"
            % (n + tabnum, p)
        )
        print(60 * "-")

        for k in itertools.combinations(database.VARIABLES, 2):
            result = test_one(p, k)
            print(("%-30s" % " + ".join(k)), "| %d%%" % (100 * result,))

    return len(protocols)


def test_impact_of_variables_3by3(tabnum, protocols):
    """Builds the first table of my report"""

    for n, p in enumerate(protocols):

        print(
            "\nTable %d: Variable combinations, 3x3 for Protocol `%s`:"
            % (n + tabnum, p)
        )
        print(60 * "-")

        for k in itertools.combinations(database.VARIABLES, 3):
            result = test_one(p, k)
            print(("%-45s" % " + ".join(k)), "| %d%%" % (100 * result,))

    return len(protocols)


def test_impact_of_variables_all(tabnum, protocols):
    """Builds the first table of my report"""

    for k, p in enumerate(protocols):

        print("\nTable %d: All variables for Protocol `%s`:" % (k + tabnum, p))
        print(60 * "-")

        result = test_one(p, database.VARIABLES)
        print(
            ("%-45s" % " + ".join(database.VARIABLES)),
            "| %d%%" % (100 * result,),
        )

    return len(protocols)


def main():
    """Main function to be called from the command-line"""

    import argparse

    example_doc = """\
examples:

    1. Returns all tables in the original report:

       $ python paper.py

    2. Only prints results for protocol "proto2":

       $ python paper.py --protocol=proto2

    3. Only prints results for protocol "proto1" and combinations of
       variables 3 by 3:

       $ python paper.py --protocol=proto1 --case=3
    """

    parser = argparse.ArgumentParser(
        usage="python %(prog)s [options]",
        description="Performs Logistic Regression on Iris Flowers Dataset",
        epilog=example_doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--case",
        choices=[1, 2, 3, 4],
        type=int,
        help="chooses which case to test.  If you choose '1', then "
             "we verify the capacity to discriminate classes using each "
             "variable independently (4 tests).  If you choose '2', "
             "then we test it using all combinations of 2 variables (6 "
             "tests).  The same applies to '3' (4 tests).  If you "
             "choose '4', then we use all 4 variables to build the "
             "classifier (single test).  By default, if no specific "
             "case is select, prints all results.",
             )

    parser.add_argument(
        "-p",
        "--protocol",
        choices=["proto1", "proto2"],
        nargs='*',
        default=["proto1", "proto2"],
        help="decides which protocols to use for reporting results. "
             "Options are %(default)s (default: %(default)s)",
        )

    args = parser.parse_args()

    # keeps a nice sequential table number
    tabnum = 1

    if args.case is not None:

        if args.case == 1:
            test_impact_of_variables_single(tabnum, args.protocol)
        elif args.case == 2:
            test_impact_of_variables_2by2(tabnum, args.protocol)
        elif args.case == 3:
            test_impact_of_variables_3by3(tabnum, args.protocol)
        elif args.case == 4:
            test_impact_of_variables_all(tabnum, args.protocol)

    else:
        tabnum += test_impact_of_variables_single(tabnum, args.protocol)
        tabnum += test_impact_of_variables_2by2(tabnum, args.protocol)
        tabnum += test_impact_of_variables_3by3(tabnum, args.protocol)
        test_impact_of_variables_all(tabnum, args.protocol)


if __name__ == "__main__":
    main()
