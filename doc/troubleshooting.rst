.. vim: set fileencoding=utf-8 :

.. _logreg_iris_troubleshooting:

Troubleshooting
---------------

You can run unit tests I have prepared like this (install pytest_ first):


.. code-block:: shell

  # use your package manager to install the package "pytest"
  # here, I examplify with "miniconda":
  (project) $ conda install pytest
  (project) $ pytest -sv ./test.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /.../conda/envs/project/bin/python
  cachedir: .pytest_cache
  rootdir: /.../ex5
  plugins: cov-2.12.1
  collected 4 items

  test.py::test_CER_0 PASSED
  test.py::test_CER_50_50 PASSED
  test.py::test_CER_20_80 PASSED
  test.py::test_CER_1 PASSED

  ============================== 4 passed in 0.46s ===============================

In case of problems, please get in touch with me `by e-mail
<mailto:john.doe@example.com>`_.

.. include:: links.rst
