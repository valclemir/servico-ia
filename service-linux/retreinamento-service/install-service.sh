#!/bin/bash

echo "INICIANDO A CONFIGURACAO DO SERVICO..."

lib="/lib/systemd/system/retreinamento.service"
etc="/etc/systemd/system/retreinamento.service"


DIRSERVICE="/usr/bin/retreinamento-service.sh"


cp -r /home/projetoia/service-linux/retreinamento-service/retreinamento-service.sh $DIRSERVICE #copia o arquivo do servico para o caminho /usr/bin/
chmod +x $DIRSERVICE
echo $DIRSERVICE

#@ ARQUIVO DE CONFIGURACAO DO SERVICO 
echo  "
[Unit]
Description=Rotina de retreinamento do modelo
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/bin/bash $DIRSERVICE
StandardInput=tty-force

[Install]
WantedBy=multi-user.target


" > $lib
#echo $lib $etc
cp -r $lib $etc
chmod 644 $etc



#systemctl start retreinamento
systemctl enable retreinamento #@ Habilita o servico para iniciar com o SO 

echo "SERVICO CONFIGURADO COM SUCESSO!"
