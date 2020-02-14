import os, json, cx_Oracle

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


def switch_case(case):
         options = {0:'Ativo', 768:'Inativo'}
         return options[case]
         
         

def status_service():
    status_service_extrator = os.system('systemctl is-active --quiet extrator') #Obtem o status do servico de extracao
    status_service_inferencia = os.system('systemctl is-active --quiet inferencia') #Obtem o status do servico da inferencia
    statu_service_classificador = os.system('systemctl is-active --quiet classificador') #Obtem o status do servico de classificacao da fila da ficha

    lista = ['Servico classificador da ficha ,'+switch_case(statu_service_classificador), 
             'Servico extrator da ficha ,'+switch_case(status_service_extrator), 
             'Servico de inferencia da ficha ,'+switch_case(status_service_inferencia)]
    return lista


      

def save_status_service(lista):
        try: 
            con = conn()
            cur = con.cursor()

            for i in lista:
                i = i.split(',')             
                sql = (f""" INSERT INTO TBIA_FIC_STATUS_SERVICO 
                            VALUES (SEQ_STATUS_SERVICO.nextval, '{i[1].rstrip()}', '{i[0].rstrip()}', CURRENT_TIMESTAMP)
                """) 
                cur.execute(sql)
        except Exception as Error: 
            DS_ERRO = 'Erro ao inserir na tabela de status do servico'
            DS_METODO = 'TBIA_FIC_STATUS_SERVICO'
            sql_error = (f"""
                            BEGIN
                                SPIA_FIC_INSERE_LOG_ERRO_IA(NULL, '{DS_ERRO}', '{DS_METODO}', '{Error}' );
                            END;
                          """)
            cur.execute(sql_error)
            print(Error)
        finally: 
            con.commit()
            con.close()
        
save_status_service(status_service()) 
