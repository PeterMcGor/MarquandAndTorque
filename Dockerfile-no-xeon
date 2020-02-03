FROM ubuntu:16.04
#FROM ubuntu:18.04


RUN apt-get update &&\
            apt-get update -y &&\
            apt-get install build-essential -y &&\
            apt-get install git -y &&\
            apt-get install libtool m4 automake pkg-config -y &&\
            apt-get install libssl-dev libxml2-dev zlib1g-dev libboost-dev pbs-drmaa-dev gperf -y

RUN apt-get install environment-modules wget -y

RUN wget --no-check-certificate https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8

WORKDIR /
COPY setup.py setup.py
RUN pip install -e .
COPY nispat/ nispat
WORKDIR /nispat
COPY test_normative_modeling/ test_normative_modeling
WORKDIR /
RUN chmod -R 777 /nispat/*
#ENTRYPOINT /bin/bash
ENTRYPOINT /opt/conda/bin/python -u /nispat/nispat/normative.py -c /mnt/data/test_normative_modeling/covariates_HC.txt -t /mnt/data/test_normative_modeling/covariates_allpatients.txt -r /mnt/data/test_normative_modeling/features_allpatients.txt -a gpr  /mnt//data/test_normative_modeling/features_HC.txt

