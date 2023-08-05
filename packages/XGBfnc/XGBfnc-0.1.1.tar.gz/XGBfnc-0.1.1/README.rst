* Written by Miguel Romero
* Last update: 01/07/21

Classification of nodes with structural properties
--------------------------------------------------

This algorithm aims to evaluate whether the structural (topological)
properties of a network are useful for predicting node attributes of
nodes (i.e., node classification). It uses a combination of multiple
machine learning techniques, such as, XGBoost and the SMOTE sampling
technique.

Example
-------

The example illustrates how the algorithm can be used to check whether
the structural properties of the gene co-expression network improve the
performance of the prediction of gene functions for rice
(*Oryza sativa Japonica*). In this example, a gene co-expression network
gathered from ATTED II is used.

How to run the example?
