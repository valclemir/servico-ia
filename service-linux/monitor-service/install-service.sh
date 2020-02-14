#!/bin/bash

echo "INICIANDO A CONFIGURACAO DO SERVICO..."

lib="/lib/systemd/system/monitor.service"
etc="/etc/systemd/system/monitor.service"


DIRSERVICE="/usr/bin/monitor-service.sh"


cp -r /home/projetoia/service-linux/monitor-service/monitor-service.sh $DIRSERVICE #copia o arquivo do servico para o caminho /usr/bin/
chmod +x $DIRSERVICE
echo $DIRSERVICE

#@ ARQUIVO DE CONFIGURACAO DO SERVICO 
echo  "
[Unit]
Description=Rotina de monitamento do servico
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



#systemctl start monitor
systemctl enable monitor #@ Habilita o servico para iniciar com o SO 

echo "SERVICO CONFIGURADO COM SUCESSO!"
