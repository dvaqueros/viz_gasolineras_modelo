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



df = pd.get_dummies(df, columns = ["name",
                                   "address",
                                   "town",
                                   "zip_code",
                                   "road_side",
                                   "restriction",
                                   "sender",
                                   "schedule",
                                   "region_name",
                                   "province_name",
                                   "municipality_name"])


X_train, X_test, y_train, y_test = train_test_split(df[[x for x in df.columns if x != product]],
                                                    df[product],
                                                    test_size = 0.33,
                                                    random_state = seed)


print(f'Tipo X_train: {type(X_train)} Tipo y_train: {type(y_train)}')

# Realizamos el modelo KMeans
start_time = time.time()
model_km = TimeSeriesKMeans(n_clusters = 3, 
                            metric = "euclidean",
                            max_iter = 10, 
                            random_state = seed).fit(X_train)

labels_km = model_km.labels_

print("--- %s seconds ---" % (time.time() - start_time))

# # Realizamos el modelo KShape
# start_time = time.time()
# model_ks = KShape(n_clusters=3, 
#                   verbose=True,
#                   n_init=10).fit(X_train)

# labels_ks = model_ks.labels_

# print("--- %s seconds ---" % (time.time() - start_time))


# silhouette_score(X_train, labels_km, metric="euclidean") 
# silhouette_score(X_train, labels_ks, metric="euclidean") 


print('Training dataset accuracy for TimeSeriesKMeans clustering with dtw metric: ', accuracy_score(y_train, labels_km))

# print('Training dataset accuracy for KShape clustering: ', accuracy_score(y_train, labels_ks))

print('Test dataset accuracy for TimeSeriesKMeans clustering with dtw metric: ', accuracy_score(y_test, model_km.predict(X_test)))

# print('Test dataset accuracy for KShape clustering: ', accuracy_score(y_test, model_ks.predict(X_test)))

confusion_matrix(y_train, labels_km)
# confusion_matrix(y_train, labels_ks)

confusion_matrix(y_test, model_km.predict(X_test))
# confusion_matrix(y_test, model_ks.predict(X_test))

joblib.dump(model_km, 'modelo_entrenado_KMeans.pkl') # Guardo el modelo.
# joblib.dump(model_ks, 'modelo_entrenado_KShape.pkl') # Guardo el modelo.








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