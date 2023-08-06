* Written by Miguel Romero
* Last update: 07/07/21

Classification of nodes with structural properties
--------------------------------------------------

This package aims to evaluate whether the structural (topological)
properties of a network are useful for predicting node attributes of
nodes (i.e., node classification). It uses a combination of multiple
machine learning techniques, such as, XGBoost and the SMOTE sampling
technique.

Installation
------------

The xgbfnc package can be install using pip, the requirements will be
automatically installed::

  python3 -m pip install xgbfnc

The source code and examples can be found in the
`GitHub repository <https://github.com/migueleci/XGBfnc>`_.

Documentation
-------------

Documentation of the package can be found `here <https://xgbfnc.readthedocs.io/en/latest/>`_.

Example
-------

The example illustrates how the algorithm can be used to check whether
the structural properties of the gene co-expression network improve the
performance of the prediction of gene functions for rice
(*Oryza sativa Japonica*). In this example, a gene co-expression network
gathered from ATTED II is used.

How to run the example?
^^^^^^^^^^^^^^^^^^^^^^^

The example can be found in the
`GitHub repository <https://github.com/migueleci/XGBfnc>`_. After creating
adjacency matrix ``adj`` for the network, the structural properties are computed
using the module `data` of the package::

  df, strc_cols = data.compute_strc_prop(adj)

This method returns a DataFrame with the structural properties of the network
and a list of the names of these properties (i.e., column names). After adding
the additional features of the network to the DataFrame, the XGBfnc module is
used to instantiate the XGBfnc class::

  test = XGBfnc()
  test.load_data(df, strc_cols, y, term, output_path='output')
  ans, pred, params = test.structural_test()

The data of the network is loaded using the ``load_data`` method. And the
structural test is execute using the ``structural_test`` method. The test
returns a boolean value which indicates whether the structural properties
help to improve the prediction performance, the prediction for the model
including the structural properties and its best parameters.

To run the example execute the following commands::

  cd test/
  python3 test_small.py
