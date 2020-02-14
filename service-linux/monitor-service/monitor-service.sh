#!/bin/bash

LOGDIRECTORY='/var/log'
FILELOGNAME='monitor-service.log'
DIR='/home/projetoia/service-linux/monitor-service' #@ Diretorio do arquivo .py
DIRECTORYTOEXEC=$DIR

VENV='/home/projetoia/service-linux/venv/bin/python3'

TIMESLEEP=$(cat /home/projetoia/service-linux/monitor-service/config-service.json | jq '.config.timesleep')

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
	    FILESPY=$DIR/monitor.py
            print "Monitor $FILESPY"
	    execTo $FILESPY $FILELOG & #@ Roda em paralelo
            sleep $TIMESLEEP;
    done;
else
    print "not exist directory"
fi


