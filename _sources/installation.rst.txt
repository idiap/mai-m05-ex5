.. vim: set fileencoding=utf-8 :

.. _logreg_iris_installation:


Installation
------------

This package depends on numpy_ and scipy_ to run properly. Please install a
modern version of these packages before trying to run the code examples.  I
recommend the miniconda_ package manager for this work, but your mileage may
vary.  A file called `environment.yml` is included with all the packages I
typically use when running this package code.

To download a copy of this package, clone it from its repository in GitHub:

.. code:: sh

   $ git clone git@github.com:idiap/mai-m05-ex5 project
   $ cd project
   $ conda env create -f environment.yml -n project
   $ conda activate project
   (project) $ #you are ready to run baselines!

.. include:: links.rst
