# -*- coding: utf-8 -*-

# Native libraries
import math
import time
# Essential Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Preprocessing
from sklearn.model_selection import train_test_split
# Algorithms
from tslearn.clustering import TimeSeriesKMeans, KShape, silhouette_score
from sklearn.metrics import accuracy_score,confusion_matrix
#Save trained model
import joblib

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


for producto in [products[0]]:
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

        mySeries.append(df.to_numpy())
        namesOfMySeries.append(station)



        cluster_count = math.ceil(math.sqrt(len(mySeries)))
        # A good rule of thumb is choosing k as the square root of the number of points in the training data set in kNN

        km = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

        labels = km.fit_predict(mySeries)


    # # Realizamos el modelo KMeans
    # start_time = time.time()
    # model_km = TimeSeriesKMeans(n_clusters = 3,
    #                             metric = "euclidean",
    #                             max_iter = 10,
    #                             random_state = seed).fit(X_train)
    #
    # labels_km = model_km.labels_
    #
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # # # Realizamos el modelo KShape
    # # start_time = time.time()
    # # model_ks = KShape(n_clusters=3,
    # #                   verbose=True,
    # #                   n_init=10).fit(X_train)
    #
    # # labels_ks = model_ks.labels_
    #
    # # print("--- %s seconds ---" % (time.time() - start_time))
    #
    #
    # silhouette_score(X_train, labels_km, metric="euclidean")
    # # silhouette_score(X_train, labels_ks, metric="euclidean")
    #
    #
    # # print('Training dataset accuracy for TimeSeriesKMeans clustering with dtw metric: ', accuracy_score(y_train, labels_km))
    #
    # # print('Training dataset accuracy for KShape clustering: ', accuracy_score(y_train, labels_ks))
    #
    # print('Test dataset accuracy for TimeSeriesKMeans clustering with dtw metric: ', accuracy_score(y_test, model_km.predict(X_test)))
    #
    # # print('Test dataset accuracy for KShape clustering: ', accuracy_score(y_test, model_ks.predict(X_test)))
    #
    # confusion_matrix(y_train, labels_km)
    # # confusion_matrix(y_train, labels_ks)
    #
    # confusion_matrix(y_test, model_km.predict(X_test))
    # # confusion_matrix(y_test, model_ks.predict(X_test))
    #
    # joblib.dump(model_km, 'modelo_entrenado_KMeans.pkl') # Guardo el modelo.
    # # joblib.dump(model_ks, 'modelo_entrenado_KShape.pkl') # Guardo el modelo.








# def plot_groups(model):

#     if model == 'kmeans-dtw':
#         model = model_km
#     elif model == 'kshape':
#         model = ks
#     else:
#         sys.exit('Please, provide a valid model string.')
        
#     labels = model.labels_

#     plt.figure(figsize=(10, 10))
#     for yi in range(2):
#         plt.subplot(2, 1, 1 + yi)
#         for xx in X_train[labels == yi]:
#             plt.plot(xx.ravel(), "k-", alpha=.15)
#         plt.plot(model.cluster_centers_[yi].ravel(), "r-")
#         plt.xlim(0, size-1)
        
#         if yi == 0:
#             plt.title("Diesel")
#         else:
#             plt.title("Hidrogen")
#         plt.grid()

#     plt.tight_layout()
#     plt.show()