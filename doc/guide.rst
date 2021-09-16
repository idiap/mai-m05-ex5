.. vim: set fileencoding=utf-8 :

.. _logreg_iris_userguide:

============
 User Guide
============

This guide explains how to use this package and obtain results published in our
paper.  Results can be re-generated automatically by executing the following
command:

.. code-block:: sh

   (project) $ python paper.py


For your reference, the paper tables are repeated below, so you can check the
reproducibility of our solution.  You may also limit the output of the program
using command-line options.  You will find more information adding the
``--help`` flag on the command above:

.. code-block:: sh

   (project) $ python paper.py --help



Results for Protocol `proto1`
-----------------------------

Protocol `proto1` is configured to use the first 30 samples for each class in
the dataset for training, and the last 20 samples for each class for testing
our solution.  The samples are **not** randomized.  Results are present in
terms of total Classification Error Rate (CER), in percentage.  The best
results are **bold faced**.

Single Variables
================

CER only using a single variable.

================== ========
   Variable          CER
================== ========
 sepal length        23%
 sepal width         36%
 **petal length**   **3%**
 **petal width**    **3%**
================== ========


Two Variables
=============

CER only using any two variables together.

================== ================== ========
    Variable 1         Variable 2       CER
================== ================== ========
   sepal length       sepal width       16%
 **sepal length**   **petal length**   **1%**
   sepal length       petal width        3%
   sepal width        petal length       3%
   sepal width        petal width        5%
   petal length       petal width        5%
================== ================== ========


Three Variables
===============

CER only using any three variables together.

================== ================== ================== ========
    Variable 1         Variable 2         Variable 3       CER
================== ================== ================== ========
   sepal length       sepal width        petal length       3%
   sepal length       sepal width        petal width        5%
 **sepal length**   **petal length**   **petal width**    **1%**
   sepal width        petal length       petal width        5%
================== ================== ================== ========


All Variables
=============

The CER using all variables available in the dataset is **3%**.


Results for Protocol `proto2`
-----------------------------

Protocol `proto2` is configured to use the last 30 samples for each class in
the dataset for training, and the first 20 samples for each class for testing
our solution.  The samples are **not** randomized.  Results are present in
terms of total Classification Error Rate (CER), in percentage. The best results
are **bold faced**.


Single Variables
================

CER only using a single variable.

================== ========
   Variable          CER
================== ========
 sepal length        33%
 sepal width         46%
 **petal length**   **3%**
 **petal width**    **3%**
================== ========


Two Variables
=============

CER only using any two variables together.

================== ================== ========
    Variable 1         Variable 2       CER
================== ================== ========
   sepal length       sepal width       20%
 **sepal length**   **petal length**   **3%**
   sepal length       petal width        6%
   sepal width        petal length      10%
 **sepal width**    **petal width**    **3%**
 **petal length**   **petal width**    **3%**
================== ================== ========


Three Variables
===============

CER only using any three variables together.

================== ================== ================== ========
    Variable 1         Variable 2         Variable 3       CER
================== ================== ================== ========
   sepal length       sepal width        petal length       6%
 **sepal length**   **sepal width**    **petal width**    **3%**
 **sepal length**   **petal length**   **petal width**    **3%**
 **sepal width**    **petal length**   **petal width**    **3%**
================== ================== ================== ========


All Variables
=============

The CER using all variables available in the dataset is **3%**.


Running the app
---------------

You can use the internal API to run the tests for each combination of variables
individually, like indicated in this section.


Single Variables
================

For all protocols.  The number passed to the function only affects the Table
number as printed on the output.  It does not affect the method.

.. testcode::

   import paper
   paper.test_impact_of_variables_single(1, ['proto1', 'proto2'])

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   Table 1: Single variables for Protocol `proto1`:
   ------------------------------------------------------------
   sepal length    | 23%
   sepal width     | 36%
   petal length    | 3%
   petal width     | 3%

   Table 2: Single variables for Protocol `proto2`:
   ------------------------------------------------------------
   sepal length    | 33%
   sepal width     | 46%
   petal length    | 3%
   petal width     | 3%


Two Variables
=============

For all protocols.  The number passed to the function only affects the Table
number as printed on the output.  It does not affect the method.


.. testcode::

   import paper
   paper.test_impact_of_variables_2by2(1)

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   Table 1: Variable combinations, 2x2 for Protocol `proto1`:
   ------------------------------------------------------------
   sepal length + sepal width     | 16%
   sepal length + petal length    | 1%
   sepal length + petal width     | 3%
   sepal width + petal length     | 3%
   sepal width + petal width      | 5%
   petal length + petal width     | 5%

   Table 2: Variable combinations, 2x2 for Protocol `proto2`:
   ------------------------------------------------------------
   sepal length + sepal width     | 20%
   sepal length + petal length    | 3%
   sepal length + petal width     | 6%
   sepal width + petal length     | 10%
   sepal width + petal width      | 3%
   petal length + petal width     | 3%


Three Variables
===============

For all protocols.  The number passed to the function only affects the Table
number as printed on the output.  It does not affect the method.


.. testcode::

   import paper
   paper.test_impact_of_variables_3by3(1, ['proto1', 'proto2'])

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   Table 1: Variable combinations, 3x3 for Protocol `proto1`:
   ------------------------------------------------------------
   sepal length + sepal width + petal length     | 3%
   sepal length + sepal width + petal width      | 5%
   sepal length + petal length + petal width     | 1%
   sepal width + petal length + petal width      | 5%

   Table 2: Variable combinations, 3x3 for Protocol `proto2`:
   ------------------------------------------------------------
   sepal length + sepal width + petal length     | 6%
   sepal length + sepal width + petal width      | 3%
   sepal length + petal length + petal width     | 3%
   sepal width + petal length + petal width      | 3%


All Variables
=============

For all protocols.  The number passed to the function only affects the Table
number as printed on the output.  It does not affect the method.


.. testcode::

   import paper
   paper.test_impact_of_variables_all(1, ['proto1', 'proto2'])

.. testoutput::
   :options: +NORMALIZE_WHITESPACE

   Table 1: All variables for Protocol `proto1`:
   ------------------------------------------------------------
   sepal length + sepal width + petal length + petal width | 3%

   Table 2: All variables for Protocol `proto2`:
   ------------------------------------------------------------
   sepal length + sepal width + petal length + petal width | 3%
