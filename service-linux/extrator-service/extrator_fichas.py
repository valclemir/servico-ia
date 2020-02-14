import pandas as pd
import cx_Oracle
import json
 
DIR_CONFIG_DB = '/home/projetoia/service-linux/config-db.json'
DIR_CONFIG_SERVICE = '/home/projetoia/service-linux/extrator-service/config-service.json'

def read_config_db():
    with open(DIR_CONFIG_DB, 'r') as read:
        read_json = json.load(read)
    return read_json

def read_config_service():
    with open(DIR_CONFIG_SERVICE, 'r')  as read:
         read_json = json.load(read)
    return read_json

def conn():
    config_db = read_config_db()['config_db']
    ip = config_db['ip']
    port = config_db['port']
    service_name = config_db['service_name']
    user = config_db['user']
    password = config_db['password']
    mode = config_db['mode']
 
    dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service_name)
    con = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    return con


def SPIA_FIC_COLETA_FICHAS():
    try:
        con = conn()
        cur = con.cursor()
        #EXTRAI FICHAS DA FILA E CALCULA
        sql = (f"""
                BEGIN
                    SPIA_FIC_COLETA_FICHAS({read_config_service()['config']['quantidadeFichasProcessamento']});
                END;
                """)
        cur.execute(sql)
        
    except Exception as Error:
        MSG_ERRO = 'Erro ao processar a coleta da ficha.'
        METOD = 'SPIA_FIC_COLETA_FICHAS'
       
        print(Error)
        sql1= (f"""
                BEGIN
                    SPIA_FIC_INSERE_LOG_ERRO_IA(NULL, '{MSG_ERRO}', '{METOD}', '{Error}' );
                END;
            """)
        cur.execute(sql1)
        
    finally:
        con.commit()
        con.close()
    


def SPIA_FIC_GER_INPUT_MODELO():
    try:
        con = conn()
        cur = con.cursor()
        #GERA INPUT PARA O MODELO 
        sql = (f"""
                BEGIN
                    SPIA_FIC_GER_INPUT_MODELO;
                END;
            """)
        cur.execute(sql)
 
    except Exception as Error:
        MSG_ERRO = 'Erro ao processar o calculo da ficha.'
        METOD = 'SPIA_FIC_GER_INPUT_MODELO'
       
        print(Error)
        sql1= (f"""
                BEGIN
                    SPIA_FIC_INSERE_LOG_ERRO_IA(NULL, '{MSG_ERRO}', '{METOD}', '{Error}' );
                END;
            """)
        cur.execute(sql1)
        
    
    finally:
        con.commit()
        con.close()
 
SPIA_FIC_COLETA_FICHAS() #Coleta e calcula fichas 
SPIA_FIC_GER_INPUT_MODELO() #Gera input para o modelo 
