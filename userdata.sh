#!/bin/bash
yum -y update
yum -y install git 
python -m ensurepip --upgrade
cd /home/ec2-user
su ec2-user -c "git clone https://github.com/QuantumQuackDoctor/data-producers.git"
cd data-producers/ && pip3 install -r requirements.txt
