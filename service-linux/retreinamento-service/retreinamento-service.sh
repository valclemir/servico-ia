#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='retreinamento-service.log'
DIR='/home/projetoia/service-linux/retreinamento-service/retreinamento_modelo' #@ Diretorio do arquivo .py
DIRECTORYTOEXEC=$DIR

VENV='/home/projetoia/service-linux/venv/bin/python3'

TIMESLEEP=$(cat /home/projetoia/service-linux/retreinamento-service/config-service.json | jq '.config.timesleep')

FLGSILENT=1

FILELOG=$LOGDIRECTORY/$FILELOGNAME

print () {
    if [[ $FLGSILENT -gt 0 ]]; then
        echo $1 >> $FILELOG &
    fi
}

execTo () {
    $VENV $1 1>> $2 2>> $2  #Executa em paralelo
}

if [[ -e $DIRECTORYTOEXEC ]]; then
    print "Run Files"
    while [[ true ]]; do
            sleep $TIMESLEEP;
            systemctl stop inferencia

            FILESPY=$DIR/main_train.py
            print "RNA $FILESPY"
            execTo $FILESPY $FILELOG & #@ Roda em paralelo

            systemctl start inferencia 
            
    done;
else
    print "not exist directory"
fi

