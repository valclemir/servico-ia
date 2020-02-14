#!/bin/bash

echo "INICIANDO A CONFIGURACAO DO SERVICO DO CLASSIFICADOR..."

lib="/lib/systemd/system/extrator.service"
etc="/etc/systemd/system/extrator.service"


DIRSERVICE="/usr/bin/extrator-service.sh"


cp -r  /home/projetoia/service-linux/extrator-service/extrator-service.sh $DIRSERVICE #copia o arquivo do servico para o caminho /usr/bin/
chmod +x $DIRSERVICE
echo $DIRSERVICE

#@ ARQUIVO DE CONFIGURACAO DO SERVICO 
echo  "
[Unit]
Description=Rotina de extracao e calculo da ficha
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



#systemctl start extrator
systemctl enable extrator #@ Habilita o servico para iniciar com o SO 

echo "SERVICO CONFIGURADO COM SUCESSO!"
