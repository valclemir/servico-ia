# Import Library
import os
import json
import cx_Oracle


def privilegies(privilegie):
    if privilegie == 'default':
        return cx_Oracle.DEFAULT_AUTH
    elif privilegie == 'sysdba':
        return cx_Oracle.SYSDBA
    elif privilegie == 'sysoper':
        return cx_Oracle.SYSOPER
    elif privilegie == 'sysasm':
        return cx_Oracle.SYSASM
    elif privilegie == 'sysbkp':
        return cx_Oracle.SYSBKP
    elif privilegie == 'sysdgd':
        return cx_Oracle.SYSDGD
    elif privilegie == 'syskmt':
        return cx_Oracle.SYSKMT


def connect_db():
    # Add database path
    #os.environ['PATH'] = 'C:\\oracle\\instantclient_11_2\\;'+os.environ['PATH']

    try:
        path = '/home/projetoia/service-linux/config-db.json'
        with open(path) as config_file:
            file = json.load(config_file)
            file = file['config_db']
        ip = file['ip']
        port = file['port']
        service_name = file['service_name']
        user = file['user']
        password = file['password']
        mode = privilegies(file['mode'])
    except Exception as e:
        ds_msg_error = 'ERRO AO ABRIR O ARQUIVO config_db.json'
        ds_error = msg_exception('Error: {}'.format(e))
        ds_method = 'connect_db'
        insert_msg_error('', ds_msg_error, ds_error, ds_method)

    # Tests/Connects database connection
    dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
    conn = cx_Oracle.connect(
        user=user, password=password, dsn=dsn_tns,
        mode=mode, encoding='UTF-8', nencoding='UTF-8')

    return conn


def insert_msg_error(nr_ficha, ds_msg_error, ds_error, ds_method):
    # Database connection
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.callproc('SPIA_FIC_INSERE_LOG_ERRO_IA', [
            nr_ficha, ds_msg_error, ds_method, ds_error])
        conn.commit()
    except Exception as e:
        print('Error occurred: {}'.format(e))
    finally:
        conn.close()


def msg_exception(msg_error):
    # Número máximo de caracteres permitidos
    max = 4000
    if len(msg_error) > max:
        return msg_error[:max]
    else:
        return msg_error
