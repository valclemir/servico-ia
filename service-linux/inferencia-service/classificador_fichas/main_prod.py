# Import Library
import pickle
import numpy as np
import pandas as pd
from utils.model import *
from utils.load_data import *
from utils.connect_db import *
from utils.confusion_matrix import *

import tensorflow
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Model features
model_columns = [
    'ESP_DIVERGENTE', 'TOTALEVENTOSDAFICHA', 'VALORTOTALEVENTOSDAFICHA',
    'QTDEVENTOSREST', 'VALOREVENTOSREST', 'QTDEVENTOS3FACES',
    'VALOREVENTOS3FACES', 'QTDEVENTOS1FACE', 'VALOREVENTOS1FACES',
    'QTDEVENTOSRXOBRG', 'VALOREVENTOSRXOBRG', 'VALOROUTLIERFICHA',
    'QTDEVENTOALTRISCO', 'FICHAPOSSUIIMAGEM', 'QTDEVENTOSPORFICHADODENT',
    'VALOREVENTOSPORFICHADODENT', 'QTDEVENPORDIAREALDODENTPBENE',
    'MDEVENTOSRXPORBENEDENT', 'MDEVENTOSRXPORBENEESP',
    'QTDEVENTOSPORFICHADAESP', 'VALOREVENTOSPORFICHADAESP',
    'COMPLEXIDADEDOEVENTO', 'PESO']

# Data
try:
    df = load_data_prod()
    if df.empty:
        ds_msg_error = 'NENHUM DADO PARA PROCESSAR'
        ds_error = 'Error: DataFrame is empty'
        ds_method = 'load_data_prod'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
        exit()
    nr_ficha = df['NR_FICHA']
    esp_da_ficha = df['ESP_DA_FICHA']
    esp_da_func = df['ESP_DA_FUNC']
    df = df.drop(columns=['NR_FICHA', 'ESP_DA_FICHA', 'ESP_DA_FUNC'])
    # Checks that all columns are in the same order of training
    if (not np.array_equal(df.columns.values, model_columns)):
        ds_msg_error = 'AS VARIÁVEIS DO MODELO NÃO ESTÃO NA ORGEM CORRETA'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'main_prod'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
        exit()
except Exception as e:
    ds_msg_error = 'ERRO AO PROCESSAR O load_data_prod'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_prod'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Loads the model parameters
try:
    with open('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/scaler.pickle', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    with open('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/label.pickle', 'rb') as label_file:
        le = pickle.load(label_file)
    # Feature scaling
    X = scaler.transform(df)
except Exception as e:
    ds_msg_error = 'ERRO AO CARREGAR OS PARÂMETROS DO MODELO'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_prod'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Load the model decisor
try:
    filename_model = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/modelo_rede_decisora.json'
    with open(filename_model, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json)
    # Load the weights
    model.load_weights('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/pesos_rede_decisora.h5')
except Exception as e:
    ds_msg_error = 'ERRO AO CARREGAR O MODELO'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_prod'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Shows model features
# model.summary()

# Predict
try:
    y_pred = predict_decisor_model(model, X)
    y_pred = np.argmax(y_pred, axis=1)
except Exception as e:
    ds_msg_error = 'ERRO NO PREDICT DOS DADOS'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'predict_decisor_model'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Transform label [Baixo -> 1, Moderado -> 2, Alto -> 3]
y_pred_inv = le.inverse_transform(y_pred)
# plot_cm(Y, y_pred_inv)
y_pred_inv = np.where(y_pred_inv == 'Baixo', 1, y_pred_inv)
y_pred_inv = np.where(y_pred_inv == 'Moderado', 2, y_pred_inv)
y_pred_inv = np.where(y_pred_inv == 'Alto', 3, y_pred_inv)

# Insert result into database
df['NR_FICHA'] = nr_ficha
df['ESP_DA_FICHA'] = esp_da_ficha
df['ESP_DA_FUNC'] = esp_da_func
df['ID_CLASSIFICACAO'] = y_pred_inv
insert_data_prod(df)
