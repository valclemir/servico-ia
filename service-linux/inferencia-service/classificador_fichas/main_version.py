import json
from utils.connect_db import *

try:
    path = 'utils/version_ia.json'
    with open(path) as config_file:
        file = json.load(config_file)
    version = file['version']
    description = file['description']
except Exception as e:
    ds_msg_error = 'ERRO AO ABRIR O ARQUIVO version_ia.json'
    ds_error = msg_exception('Error: {}'.format(e))
    ds_method = 'main_version'
    insert_msg_error('', ds_msg_error, ds_error, ds_method)
    exit()

# Database connection
conn = connect_db()
try:
    cur = conn.cursor()
    cur.callproc('SPIA_FIC_INSERE_VERSAO_IA', [
        version, description])
    conn.commit()
except Exception as e:
    print('Error occurred: {}'.format(e))
finally:
    conn.close()
