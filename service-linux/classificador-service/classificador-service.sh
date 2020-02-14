#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='classificador-service.log'
DIR='/home/projetoia/service-linux/classificador-service' #@ Diretorio do arquivo .py
DIRECTORYTOEXEC=$DIR

VENV='/home/projetoia/service-linux/venv/bin/python3'

TIMESLEEP=$(cat /home/projetoia/service-linux/classificador-service/config-service.json | jq '.config.timesleep')

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
            FILESPY=$DIR/classificador_fichas.py
            print "Classificador $FILESPY"
            execTo $FILESPY $FILELOG & #@ Roda em paralelo
            sleep $TIMESLEEP;
    done;
else
    print "not exist directory"
fi


