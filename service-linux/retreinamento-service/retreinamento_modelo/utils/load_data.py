# Import Library
import pandas as pd
from utils.version_ia import *
from utils.connect_db import *


DIR_CONFIG_SERVICE = '/home/projetoia/service-linux/inferencia-service/config-service.json'

def read_config_service():
    with open(DIR_CONFIG_SERVICE, 'r')  as read:
         read_json = json.load(read)
    return read_json



def load_data_train():
    """Connect to DB and return data.

    Returns
    -------
    df : dataframe
        A dataframe according to database.
    """
    # Database connection
    conn = connect_db()

    sql_string = """select * from TBIA_FIC_REPO_TRAIN_COMITE"""

    # Load table to a DataFrame
    df = pd.DataFrame()
    try:
        df = pd.read_sql(sql_string, conn)
    except Exception as e:
        ds_msg_error = 'ERRO AO PROCESSAR O load_data_train'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'load_data_train'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)
    finally:
        conn.close()

    return df


def df_repeated(df):
    X_new = pd.DataFrame()

    s_baixo = df.loc[df['AUDITORIA'] == 'Baixo']
    s_baixo = pd.concat([s_baixo]*1, ignore_index=True)
    X_new = pd.concat([X_new, s_baixo])

    s_mode = df.loc[df['AUDITORIA'] == 'Moderado']
    s_mode = pd.concat([s_mode]*2, ignore_index=True)
    X_new = pd.concat([X_new, s_mode])

    s_alto = df.loc[df['AUDITORIA'] == 'Alto']
    s_alto = pd.concat([s_alto]*9, ignore_index=True)
    X_new = pd.concat([X_new, s_alto])

    return X_new
