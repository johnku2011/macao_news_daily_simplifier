#!/usr/bin/env bash

###Sets up python packages in for devcontainer.json

#create a virtualenv
virtualenv ~/.venv
#source virtualenv
source ~/.venv/bin/activate
#append it to bash so every shell launches with it 
echo 'source ~/.venv/bin/activate' >> ~/.bashrc
#install all software 
make install

#for installing torch
pip install --pre torch -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html

#for installing sentence transformer
%wget https://github.com/google/sentencepiece/archive/refs/tags/v0.1.83.tar.gz
%tar zxfv v0.1.83.tar.gz
%cd sentencepiece-0.1.83
%mkdir build
%cd build
%cmake .. -DSPM_ENABLE_SHARED=OFF -DCMAKE_INSTALL_PREFIX=./root
%make -j20 install
%cd ../python
%env PKG_CONFIG_PATH=../build/root/lib/pkgconfig python3 setup.py bdist_wheel
%pip install dist/*.whl