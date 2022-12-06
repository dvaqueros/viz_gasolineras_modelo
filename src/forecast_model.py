# -*- coding: utf-8 -*-

# https://www.cienciadedatos.net/documentos/py27-forecasting-series-temporales-python-scikitlearn.html

# Tratamiento de datos
# ==============================================================================
import numpy as np
import pandas as pd

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
# plt.rcParams['lines.linewidth'] = 1.5
# %matplotlib inline

# Modelado y Forecasting
# ==============================================================================
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterAutoregCustom import ForecasterAutoregCustom
from skforecast.ForecasterAutoregDirect import ForecasterAutoregDirect
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
from skforecast.utils import save_forecaster
from skforecast.utils import load_forecaster
import pickle

# Configuración warnings
# ==============================================================================
import warnings
# warnings.filterwarnings('ignore')

# Preparación del dato
# ==============================================================================
with open("data/output/dict_df_products_clustering", 'rb') as f:
    dict_df_products_clustering = pickle.load(f)

dict_df_products_forecasting = dict_df_products_clustering

modelos = {}

for product in products:
    modelos[product] = {}
    df = dict_df_products_forecasting[product]
    for cluster in df['Cluster'].unique():

        datos=pd.DataFrame(columns=['date', 'y'])

        temp = df.groupby(['Cluster', 'date'], as_index=False).agg({product+'_adj': 'mean'})[['Cluster', 'date',product+'_adj']]
        datos['date'] = temp[temp['Cluster'] == cluster]['date']
        datos['y'] = temp[temp['Cluster'] == cluster][product+'_adj']
        #datos=datos[datos['date']<datetime(2022,1,1)]
        datos = datos.set_index('date')
        datos = datos.asfreq('D') # Datos diarios
        datos = datos.sort_index()
        datos = datos.ffill()
        datos = datos.bfill()
        datos.head()



        # Verificar que un índice temporal está completo
        # ==============================================================================
        (datos.index == pd.date_range(
                            start = datos.index.min(),
                            end   = datos.index.max(),
                            freq  = datos.index.freq)
        ).all()

        # Separación datos train-test
        # ==============================================================================
        steps = 18
        datos_train = datos[:-steps]
        datos_test  = datos[-steps:]

        # print(f"Fechas train : {datos_train.index.min()} --- {datos_train.index.max()}  (n={len(datos_train)})")
        # print(f"Fechas test  : {datos_test.index.min()} --- {datos_test.index.max()}  (n={len(datos_test)})")

        # fig, ax = plt.subplots(figsize=(9, 4))
        # datos_train['y'].plot(ax=ax, label='train')
        # datos_test['y'].plot(ax=ax, label='test')
        # ax.legend();

        # Crear y entrenar forecaster
        # ==============================================================================
        forecaster = ForecasterAutoreg(
                        regressor = RandomForestRegressor(random_state=123),
                        lags = 6
                     )

        forecaster.fit(y=datos_train['y'])
        forecaster


        # Predicciones
        # ==============================================================================
        steps = 18
        predicciones = forecaster.predict(steps=steps)
        predicciones.head(5)

        # Gráfico
        # ==============================================================================
        # fig, ax = plt.subplots(figsize=(9, 4))
        # datos_train['y'].plot(ax=ax, label='train')
        # datos_test['y'].plot(ax=ax, label='test')
        # predicciones.plot(ax=ax, label='predicciones')
        # ax.legend();

        # Error test
        # ==============================================================================
        error_mse = mean_squared_error(
                        y_true = datos_test['y'],
                        y_pred = predicciones
                    )

        # print(f"Error de test (mse): {error_mse}")

        # Grid search de hiperparámetros
        # ==============================================================================
        steps = 18
        forecaster = ForecasterAutoreg(
                        regressor = RandomForestRegressor(random_state=123),
                        lags      = 12 # Este valor será remplazado en el grid search
                     )

        # Lags utilizados como predictores
        lags_grid = [7, 14, 30, 60, int(len(datos_train)*0.5), int(len(datos_train)*0.75)]

        # Hiperparámetros del regresor
        param_grid = {'n_estimators': [100, 500],
                      'max_depth': [3, 5, 10]}

        resultados_grid = grid_search_forecaster(
                                forecaster         = forecaster,
                                y                  = datos_train['y'],
                                param_grid         = param_grid,
                                lags_grid          = lags_grid,
                                steps              = steps,
                                refit              = True,
                                metric             = 'mean_squared_error',
                                initial_train_size = int(len(datos_train)*0.99),
                                fixed_train_size   = False,
                                return_best        = True,
                                verbose            = False
                          )

        # Resultados Grid Search
        # ==============================================================================
        resultados_grid

        # Crear y entrenar forecaster con mejores hiperparámetros
        # ==============================================================================
        regressor = RandomForestRegressor(max_depth=resultados_grid.reset_index().loc[0,'max_depth'], n_estimators=resultados_grid.reset_index().loc[0,'n_estimators'], random_state=123)
        forecaster = ForecasterAutoreg(
                        regressor = regressor,
                        lags      = resultados_grid.reset_index().loc[0,'lags'][-1].item()
                     )

        forecaster.fit(y=datos_train['y'])



        # Predicciones
        # ==============================================================================
        predicciones = forecaster.predict(steps=steps)

        # Gráfico
        # ==============================================================================
        # fig, ax = plt.subplots(figsize=(9, 4))
        # datos_train['y'].plot(ax=ax, label='train')
        # datos_test['y'].plot(ax=ax, label='test')
        # predicciones.plot(ax=ax, label='predicciones')
        # ax.legend();

        # Error de test
        # ==============================================================================
        error_mse = mean_squared_error(
                        y_true = datos_test['y'],
                        y_pred = predicciones
                    )
        modelos[product][cluster] = {}
        modelos[product][cluster]['model'] = forecaster
        modelos[product][cluster]['error'] = error_mse

        # print(f"Error de test (mse) {error_mse}")

        # # Backtesting
        # # ==============================================================================
        # steps = 36
        # n_backtesting = 36*3 # Se separan para el backtest los últimos 9 años
        #
        # metrica, predicciones_backtest = backtesting_forecaster(
        #                                     forecaster         = forecaster,
        #                                     y                  = datos['y'],
        #                                     initial_train_size = len(datos) - n_backtesting,
        #                                     fixed_train_size   = False,
        #                                     steps              = steps,
        #                                     refit              = True,
        #                                     metric             = 'mean_squared_error',
        #                                     verbose            = True
        #                                  )
        #
        # print(f"Error de backtest: {metrica}")
        #
        # fig, ax = plt.subplots(figsize=(9, 4))
        # datos.loc[predicciones_backtest.index, 'y'].plot(ax=ax, label='test')
        # predicciones_backtest.plot(ax=ax, label='predicciones')
        # ax.legend();
        #
        # # Importancia predictores
        # # ==============================================================================
        # impotancia = forecaster.get_feature_importance()
        # impotancia
        #
        # # Guardar modelo
        # save_forecaster(forecaster, file_name='forecaster.py', verbose=False)

pickle.dump(modelos, open("data/output/modelos", "wb"))
