# Import Library
import pickle
import numpy as np
import pandas as pd
from utils.model import *
from utils.load_data import *
from utils.connect_db import *

import tensorflow
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Data
try:
    df = load_data_train()
    if df.empty:
        ds_msg_error = 'NENHUM DADO PARA PROCESSAR'
        ds_error = 'Error: DataFrame is empty'
        ds_method = 'load_data_train'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
        exit()
    df = df_repeated(df)
    nr_ficha = df['NR_FICHA']
    Y = df['AUDITORIA']
    df = df.drop(columns=['NR_FICHA', 'ESP_DA_FICHA', 'ESP_DA_FUNC', 'AUDITORIA'])
    _, n_features = df.shape
except Exception as e:
    ds_msg_error = 'ERRO AO PROCESSAR O load_data_train'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_train'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Feature and label scaling
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(df)
le = LabelEncoder()
Y = le.fit_transform(Y)

# Saves the model parameters
try:
    with open('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/scaler.pickle', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)
    with open('/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/label.pickle', 'wb') as label_file:
        pickle.dump(le, label_file)
except Exception as e:
    ds_msg_error = 'ERRO AO SALVAR OS PARÂMETROS DO MODELO'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_train'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)

# KFold cross validation
seed = 7
np.random.seed(seed)
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
num_members = 5
for i in range(num_members):
    aux_fold = 1
    accuracy = []
    print('\n*** Rede Neural Especialista: {}'.format(i+1))
    for train, test in skf.split(X, Y):
        # Divide the kfold in train and test
        X_train = X[train]
        X_test = X[test]
        Y = Y.reshape(-1, 1)
        Y_train = to_categorical(Y[train])
        Y_test = to_categorical(Y[test])

        # Train the model
        model = fit_model(X_train, Y_train, n_features=n_features)

        # Evaluate the model
        _, score_train = model.evaluate(X_train, Y_train, verbose=0)
        _, score_test = model.evaluate(X_test, Y_test, verbose=0)
        print('*** KFold: {}'.format(aux_fold))
        print('*** Acurácia do Treinamento: {:.2f}'.format(score_train*100))
        print('*** Acurácia do Teste: {:.2f}'.format(score_test*100))

        # Scores
        accuracy.append(score_test*100)
        aux_fold += 1

    # Show the scores
    print('*** Acc do Especialista {} no Teste: {:.2f}'.format(i+1, np.mean(accuracy)))
    print('*** Std do Especialista {} no Teste: {:.2f}'.format(i+1, np.std(accuracy)))

    Y_aux = Y.reshape(-1, 1)
    Y_aux = to_categorical(Y_aux)
    model = fit_model(X, Y_aux, n_features=n_features)
    _, score = model.evaluate(X, Y_aux, verbose=0)
    print('*** Acc do Especialista {}: {:.2f}'.format(i+1, score*100))

    try:
        # Save the model
        filename = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/modelo_rede_especialista_{}.h5'.format(i+1)
        model.save(filename)
        # Save the model and weights
        model_json = model.to_json()
        filename_model = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/modelo_rede_especialista_{}.json'.format(i+1)
        with open(filename_model, 'w') as json_file:
            json_file.write(model_json)
    except Exception as e:
        ds_msg_error = 'ERRO AO SALVAR O MODELO ESPECIALISTA'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'main_train'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)

# Load all models
i = 1
Y_test_member = to_categorical(Y)
all_members = load_all_models_members(num_members, n_features=n_features)
for model_member in all_members:
    _, acc = model_member.evaluate(X, Y_test_member, verbose=0)
    print('Acurácia da Rede Neural Especialista {}: {:.2f}'.format(i, acc*100))
    i += 1

# Define combined model
modelo_decisor = define_decisor_model(all_members)
# Fit decision model for the test dataset
modelo_decisor = fit_decisor_model(modelo_decisor, X, Y)
# Predict and evaluate
Y_pred = predict_decisor_model(modelo_decisor, X)
Y_pred = np.argmax(Y_pred, axis=1)
acc = accuracy_score(Y, Y_pred)
print('Acurácia da Rede Neural Decisora: {:.2f}'.format(acc*100))

try:
    # Save the model decisor
    filename = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/pesos_rede_decisora.h5'
    modelo_decisor.save_weights(filename)
    # Save the model as .json
    filename_model = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/model/modelo_rede_decisora.json'
    model_json = modelo_decisor.to_json()
    with open(filename_model, 'w') as json_file:
        json_file.write(model_json)
except Exception as e:
    ds_msg_error = 'ERRO AO SALVAR O MODELO REDE DECISORA'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_train'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)
