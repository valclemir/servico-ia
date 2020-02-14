import json
from utils.connect_db import *


def get_version():
    try:
        path = '/home/projetoia/service-linux/inferencia-service/classificador_fichas/utils/version_ia.json'
        with open(path) as config_file:
            file = json.load(config_file)
        version = file['version']
    except Exception as e:
        ds_msg_error = 'ERRO AO ABRIR O ARQUIVO version_ia.json'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'get_version'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)

    return version
