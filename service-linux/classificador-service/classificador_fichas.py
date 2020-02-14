import pandas as pd
import cx_Oracle
import json
 
DIR_CONFIG_DB = '/home/projetoia/service-linux/config-db.json'

def read_config_db():
    with open(DIR_CONFIG_DB, 'r') as read:
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
 
def execProcedures():
    con = conn()
    try:
        cur = con.cursor()
        #ATUALIZA TABELAS TBOD_FICHA E TBOD_FICHA_DTCORTE
        sql1 = (f"""
		BEGIN 
                   SPIA_FIC_GRAVA_RISCO_FICHA;
                END;
	""")
        cur.execute(sql1)
 
    except Exception as Error:
        MSG_ERRO = 'Erro ao processar o calculo da ficha.'
        METOD = 'SPIA_FIC_GRAVA_RISCO_FICHA'
        
 
        sql2= (f"""
		   BEGIN 
                   	_FIC_INSERE_LOG_ERRO_IA(NULL, '{MSG_ERRO}', '{METOD}', '{Error}' );
                   END;
                
            """)
        cur.execute(sql2)     
    
    finally:
        con.commit()
        con.close()
    return 0
 
execProcedures()
