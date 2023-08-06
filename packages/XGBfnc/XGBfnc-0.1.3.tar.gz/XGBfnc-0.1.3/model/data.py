#!/usr/bin/env python3
# coding: utf-8

# Node classification (attribute prediction) - flat approach
# Data preprocessing
# Miguel Romero, 2021 jul 1

"""
Module for computing the structural properties of a network.
"""

import numpy as np
import igraph as ig
import pandas as pd
import networkx as nx
import multiprocessing

# Node embedding
from node2vec import Node2Vec
from sklearn.manifold import TSNE
from sklearn.cluster import AffinityPropagation

# Cross-validation and scaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings(action='ignore',category=DeprecationWarning)
warnings.filterwarnings(action='ignore',category=FutureWarning)


# Scale data
def scale_data(data):
  """
  Scale the data of a dataset without modifying the distribution of data.

  :param data: Dataset
  :type data: DataFrame

  :return: Dataset with scaled features
  :rtype: Dataframe
  """
  # MinMaxScaler does not modify the distribution of data
  minmax_scaler = MinMaxScaler() # Must be first option
  rob_scaler = RobustScaler() # RobustScaler is less prone to outliers

  new_data = pd.DataFrame()
  for fn in data.columns:
    scaled_feature = minmax_scaler.fit_transform(data[fn].values.reshape(-1,1))
    new_data[fn] = scaled_feature[:,0].tolist()

  return new_data


# compute structural properties and feature embedding
def compute_strc_prop(adj_mad, nodes=None, dimensions=16, p=1, q=0.5,
                      path=None, log=False, seed=None):
  """
  Compute multiple structural properties of the input network. Two types of
  properties are computed: hand-crafted and node embeddings.

  :param adj_mad: Adjacency matrix representation of the network, square and
    symmetric matrix.
  :type adj_mad: np.matrix[int]
  :param nodes: List of identifiers of nodes, must match the number of rows of
    the adjacency matrix.
  :type nodes: List[string], optional
  :param dimensions: Dimension of the node embedding, defaults to 16
  :type dimensions: int
  :param p: Return parameter of node2vec, defaults to 1
  :type p: float
  :param q: In-out parameter of node2vec, defaults to 0.5
  :type q: floar
  :param path: Relative path where the dataset will be saved, defaults to
    current path
  :type path: string
  :param log: Flag for logging of the results of the test, default to False
  :type log: bool
  :param seed: Random number seed, defaults to None
  :type seed: float

  :return: Dataset with scaled features representing the structural properties
    of the network and list of labels (names) of the features.
  :rtype: Tuple(Dataframe, List[string])
  """
  # create graph for adjacency matrix
  g = nx.Graph()
  edgelist = np.transpose(np.nonzero(adj_mad)).tolist()
  g.add_nodes_from(np.arange(len(adj_mad)))
  g.add_edges_from(edgelist)
  if log: print(nx.info(g))

  # node embedding for prediction
  workers = multiprocessing.cpu_count() // 2
  node2vec = Node2Vec(g, dimensions=dimensions, walk_length=5, num_walks=300, workers=workers, p=p, q=q)
  model = node2vec.fit(window=5, min_count=1, batch_words=5, workers=workers)
  embeddings = np.array([model.wv.get_vector(str(x)) for x in list(g.nodes)])

  # dimensionality reduction for clustering
  tsne = TSNE(n_components=2, random_state=seed, perplexity=15)
  embeddings_2d = tsne.fit_transform(embeddings)

  clustering_model = AffinityPropagation(damping=0.9)
  clustering_model.fit(embeddings_2d)
  yhat = clustering_model.predict(embeddings_2d)

  # igraph
  g = ig.Graph.Adjacency((sm_ppi > 0).tolist())
  g = g.as_undirected()
  if log: prin(ig.summary(g))

  # get node properties form graph
  clust = np.array(g.transitivity_local_undirected(mode="zero"))
  deg = np.array(g.degree())
  neigh_deg = np.array(g.knn()[0])
  centr_betw = np.array(g.betweenness(directed=False))
  centr_clos = np.array(g.closeness())
  eccec = np.array(g.eccentricity())
  pager = np.array(g.personalized_pagerank(directed=False))
  const = np.array(g.constraint())
  hubs = np.array(g.hub_score())
  auths = np.array(g.authority_score())
  coren = np.array(g.coreness())
  diver = np.array(g.diversity())

  # add node properties to df
  # cretae dataset
  strc_df = pd.DataFrame()

  strc_df['clust'] = pd.Series(clust) # clustering
  strc_df['deg'] = pd.Series(deg) # degree
  strc_df['neigh_deg'] = pd.Series(neigh_deg) # average_neighbor_degree
  strc_df['betw'] = pd.Series(centr_betw) # betweenness_centrality
  strc_df['clos'] = pd.Series(centr_clos) # closeness_centrality
  strc_df['eccec'] = pd.Series(eccec) # eccentricity
  strc_df['pager'] = pd.Series(pager) # page rank
  strc_df['const'] = pd.Series(const) # constraint
  strc_df['hubs'] = pd.Series(hubs) # hub score
  strc_df['auths'] = pd.Series(auths) # authority score
  strc_df['coren'] = pd.Series(coren) # coreness
  strc_df['diver'] = pd.Series(diver) # diversity

  for i in range(dimensions):
    strc_df['emb_{0}'.format(i)] = pd.Series(embeddings[:,i])
  strc_df['emb_clust'] = pd.Series(yhat)

  columns = list(strc_df.columns)
  strc_df = scale_data(strc_df)
  if nodes != None:
    strc_df['node'] = pd.Series(nodes)
  if path != None:
    strc_df.to_csv('{0}/data.csv'.format(path), index=False)
  else:
    strc_df.to_csv('data.csv', index=False)

  return df, columns
