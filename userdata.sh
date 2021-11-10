#!/bin/bash
yum -y update
yum install git -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
git clone https://github.com/QuantumQuackDoctor/data-producers.git
cd data-producers/ && pip3 install -r requirements.txt
