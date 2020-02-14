#!/bin/bash


#PREPARANDO O AMBIENTE
# Verifica se o diretorio /projetoia exists 
DIR='/home/projetoia/'
if [[ ! -d $DIR ]]; then 
	mkdir $DIR;
fi;

FIND_SERVICE=$(find / -name "service-linux") 
sudo mv $FIND_SERVICE $DIR


#####################################
	#PASSO 1: INSTALACAO DE PACOTES #
#####################################
sudo echo 'PASSO 1: INSTALANDO PACOTES E DEPENDENCIAS...' 
#sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm #Add repositorio python3 --centos 7
sudo yum install python3 -y #Instala o python3   
sudo yum install jq -y #@ para ler arquivos em formato json
sudo yum install python3-pip -y #@ Responsavel por baixar pacotes python

####################################
	#INSTALA ORACLE INSTANT CLIENT #
####################################
# Instala dependencias basicas
sudo yum -y install libaio bc flex
sudo dnf install libnsl

sudo rpm -ivh upload/oracle-instantclient11.2-basic-*
sudo rpm -ivh upload/oracle-instantclient11.2-devel-*

#######################################
	# CONFIGURA VARIAVEIS DE AMBIENTE #
#######################################
sudo echo '#Configuracao cliente oracle' >> $HOME/.bashrc
sudo echo 'export ORACLE_VERSION="11.2"' >> $HOME/.bashrc
sudo echo 'export ORACLE_HOME="/usr/lib/oracle/$ORACLE_VERSION/client64/"' >> $HOME/.bashrc
sudo echo 'export PATH=$PATH:"$ORACLE_HOME/bin"' >> $HOME/.bashrc
sudo echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$ORACLE_HOME/lib"' >> $HOME/.bashrc
. $HOME/.bashrc

sudo sh -c "echo /usr/lib/oracle/11.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

###################################################
	#PASSO 2: CRIA AMBIENTE VIRTUAL PARA O PYTHON #
###################################################
sudo echo 'PASSO 2: CRIA AMBIENTE VIRTUAL PARA O PYTHON...'
sudo pip3 install virtualenv #install virtualenv
virtualenv -p python3 /home/projetoia/service-linux/venv #cria ambiente virtual


#################################################
	#PASSO 5: INSTALL PACKAGES FROM REQUIREMENTS#
#################################################

sudo echo 'INSTALL PACKAGES FROM REQUIREMENTS...'
sudo /home/projetoia/service-linux/venv/bin/pip install -r requirements.txt



########################################
	#PASSO 3: SET PERMISSIONS FILES.SH #
########################################

sudo echo 'PASSO 2: SET PERMISSAO NOS ARQUIVOS .sh ...'
#Extrator 
sudo chmod +x /home/projetoia/service-linux/extrator-service/install-service.sh
sudo chmod +x /home/projetoia/service-linux/extrator-service/extrator-service.sh


#Classificador 
sudo chmod +x /home/projetoia/service-linux/classificador-service/install-service.sh 
sudo chmod +x /home/projetoia/service-linux/classificador-service/classificador-service.sh


#Inferencia 
sudo chmod +x /home/projetoia/service-linux/inferencia-service/install-service.sh
sudo chmod +x /home/projetoia/service-linux/inferencia-service/inferencia-service.sh

#Monitor 
sudo chmod +x /home/projetoia/service-linux/monitor-service/install-service.sh
sudo chmod +x /home/projetoia/service-linux/monitor-service/monitor-service.sh


#Retreinamento 
sudo chmod +x /home/projetoia/service-linux/retreinamento-service/install-service.sh
sudo chmod +x /home/projetoia/service-linux/retreinamento-service/retreinamento-service.sh




########################################
	#PASSO 4: Instala os servicos #
########################################

sudo echo 'PASSO 2: Instalando servicos ...'
#Extrator 
sudo /home/projetoia/service-linux/extrator-service/install-service.sh

#Classificador 
sudo /home/projetoia/service-linux/classificador-service/install-service.sh 

#Inferencia 
sudo /home/projetoia/service-linux/inferencia-service/install-service.sh

#Monitor 
sudo /home/projetoia/service-linux/monitor-service/install-service.sh

#Retreinamento
sudo /home/projetoia/service-linux/retreinamento-service/install-service.sh



echo "CONFIGURACAO CONCLUIDA!"


