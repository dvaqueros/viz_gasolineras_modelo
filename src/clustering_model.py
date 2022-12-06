# Native libraries
import os
import math
# Essential Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Preprocessing
from sklearn.preprocessing import MinMaxScaler
# Algorithms
from minisom import MiniSom
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans

from sklearn.decomposition import PCA

columnas_clust_drop = [
    'name',
    'address',
    'zip_code',
    'road_side',
    'restriction',
    'sender',
    'schedule',
    'vivienda_agua_electricidad_combustibles',
    'min_distance',
    'district',
    'neighbourhood',
    'schedule_parsed',
    'name_parsed',
    'num_combustibles'
]

dict_df_products_clustering = dict_df_products.copy()
for producto in products:
    dict_df_products_clustering[producto]=dict_df_products_clustering[producto].drop(columns=columnas_clust_drop)


for producto in products:
    #print(producto)
    mySeries = []
    namesOfMySeries = []
    for station in dict_df_products_clustering[producto]['station_id'].unique():
        #print(station)
        df = dict_df_products_clustering[producto][dict_df_products_clustering[producto]['station_id']==station]
        df = df.loc[:, [producto]]
        # While we are at it I just filtered the columns that we will be working on
        #df.set_index("date", inplace=True)
        # ,set the date columns as index
        #df.sort_index(inplace=True)

        mySeries.append(df.to_numpy().transpose()[0])
        namesOfMySeries.append(station)

    som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(mySeries))))
    # I didn't see its significance but to make the map square,
    # I calculated square root of map size which is
    # the square root of the number of series
    # for the row and column counts of som

    som = MiniSom(som_x, som_y, len(mySeries[0]), sigma=0.3, learning_rate=0.1)

    som.random_weights_init(mySeries)
    som.train(mySeries, 50000)


    # Little handy function to plot series
    # def plot_som_series_averaged_center(som_x, som_y, win_map):
    #     fig, axs = plt.subplots(som_x, som_y, figsize=(5, 5))
    #     fig.suptitle('Clusters')
    #     for x in range(som_x):
    #         for y in range(som_y):
    #             cluster = (x, y)
    #             if cluster in win_map.keys():
    #                 for series in win_map[cluster]:
    #                     axs[cluster].plot(series, c="gray", alpha=0.5)
    #                 axs[cluster].plot(np.average(np.vstack(win_map[cluster]), axis=0), c="red")
    #             cluster_number = x * som_y + y + 1
    #             axs[cluster].set_title(f"Cluster {cluster_number}")
    #
    #     plt.show()



    win_map = som.win_map(mySeries)
    # Returns the mapping of the winner nodes and inputs

    # plot_som_series_averaged_center(som_x, som_y, win_map)


    # def plot_som_series_dba_center(som_x, som_y, win_map):
    #     fig, axs = plt.subplots(som_x, som_y, figsize=(5, 5))
    #     fig.suptitle('Clusters')
    #     for x in range(som_x):
    #         for y in range(som_y):
    #             cluster = (x, y)
    #             if cluster in win_map.keys():
    #                 for series in win_map[cluster]:
    #                     axs[cluster].plot(series, c="gray", alpha=0.5)
    #                 axs[cluster].plot(dtw_barycenter_averaging(np.vstack(win_map[cluster])),
    #                                   c="red")  # I changed this part
    #             cluster_number = x * som_y + y + 1
    #             axs[cluster].set_title(f"Cluster {cluster_number}")
    #
    #     plt.show()


    win_map = som.win_map(mySeries)

    # plot_som_series_dba_center(som_x, som_y, win_map)

    # Let's check first 5
    for series in mySeries[:5]:
        print(som.winner(series))

    cluster_map = []
    for idx in range(len(mySeries)):
        winner_node = som.winner(mySeries[idx])
        cluster_map.append((namesOfMySeries[idx], f"Cluster {winner_node[0] * som_y + winner_node[1] + 1}"))

    df_som = pd.DataFrame(cluster_map, columns=["Series", "Cluster"]).sort_values(by="Cluster").set_index("Series").reset_index()








    cluster_count = math.ceil(math.sqrt(len(mySeries)))
    # A good rule of thumb is choosing k as the square root of the number of points in the training data set in kNN

    km = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    labels = km.fit_predict(mySeries)

    plot_count = math.ceil(math.sqrt(cluster_count))



    # fig, axs = plt.subplots(plot_count, plot_count, figsize=(5, 5))
    # fig.suptitle('Clusters')
    # row_i = 0
    # column_j = 0
    # # For each label there is,
    # # plots every series with that label
    # for label in set(labels):
    #     cluster = []
    #     for i in range(len(labels)):
    #         if (labels[i] == label):
    #             axs[row_i, column_j].plot(mySeries[i], c="gray", alpha=0.4)
    #             cluster.append(mySeries[i])
    #     if len(cluster) > 0:
    #         axs[row_i, column_j].plot(np.average(np.vstack(cluster), axis=0), c="red")
    #     axs[row_i, column_j].set_title("Cluster " + str(row_i * som_y + column_j))
    #     column_j += 1
    #     if column_j % plot_count == 0:
    #         row_i += 1
    #         column_j = 0
    #
    # plt.show()

    plot_count = math.ceil(math.sqrt(cluster_count))

    # fig, axs = plt.subplots(plot_count, plot_count, figsize=(5, 5))
    # fig.suptitle('Clusters')
    # row_i = 0
    # column_j = 0
    # for label in set(labels):
    #     cluster = []
    #     for i in range(len(labels)):
    #         if (labels[i] == label):
    #             axs[row_i, column_j].plot(mySeries[i], c="gray", alpha=0.4)
    #             cluster.append(mySeries[i])
    #     if len(cluster) > 0:
    #         axs[row_i, column_j].plot(dtw_barycenter_averaging(np.vstack(cluster)), c="red")
    #     axs[row_i, column_j].set_title("Cluster " + str(row_i * som_y + column_j))
    #     column_j += 1
    #     if column_j % plot_count == 0:
    #         row_i += 1
    #         column_j = 0
    #
    # plt.show()

    fancy_names_for_labels = [f"Cluster {label}" for label in labels]
    df_kmeans = pd.DataFrame(zip(namesOfMySeries, fancy_names_for_labels), columns=["Series", "Cluster"]).sort_values(
        by="Cluster").set_index("Series").reset_index()

    # pca = PCA(n_components=2)
    #
    # mySeries_transformed = pca.fit_transform(mySeries)
    #
    # kmeans = KMeans(n_clusters=cluster_count, max_iter=5000)
    #
    # labels = kmeans.fit_predict(mySeries_transformed)
    #
    # plot_count = math.ceil(math.sqrt(cluster_count))
    #
    # fig, axs = plt.subplots(plot_count, plot_count, figsize=(5, 5))
    # fig.suptitle('Clusters')
    # row_i = 0
    # column_j = 0
    # for label in set(labels):
    #     cluster = []
    #     for i in range(len(labels)):
    #         if (labels[i] == label):
    #             axs[row_i, column_j].plot(mySeries[i], c="gray", alpha=0.4)
    #             cluster.append(mySeries[i])
    #     if len(cluster) > 0:
    #         axs[row_i, column_j].plot(np.average(np.vstack(cluster), axis=0), c="red")
    #     axs[row_i, column_j].set_title("Cluster " + str(row_i * som_y + column_j))
    #     column_j += 1
    #     if column_j % plot_count == 0:
    #         row_i += 1
    #         column_j = 0
    #
    # plt.show()
    #
    # fancy_names_for_labels = [f"Cluster {label}" for label in labels]
    # pd.DataFrame(zip(namesOfMySeries, fancy_names_for_labels), columns=["Series", "Cluster"]).sort_values(
    #     by="Cluster").set_index("Series")
    df_original=dict_df_products_clustering[producto]
    dict_df_products_clustering[producto] = df_original.merge(df_som, left_on='station_id', right_on='Series', how='left').drop(columns='Series')
    dict_df_products_clustering[producto] = df_original.merge(df_kmeans, left_on='station_id', right_on='Series', how='left', suffixes=('_som', '_kmeans')).drop(columns='Series')

pickle.dump(dict_df_products_clustering, open("data/output/dict_df_products_clustering", "wb"))