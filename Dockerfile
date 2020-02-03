FROM intelpython/intelpython3_full

#FROM ubuntu:18.04
ENV LANG C.UTF-8
WORKDIR /
COPY setup.py setup.py
RUN pip install -e .
COPY nispat/ nispat
WORKDIR /nispat
#COPY test_normative_modeling/ test_normative_modeling
#WORKDIR /
#RUN chmod -R 777 /nispat/*
ENTRYPOINT /bin/bash
#ENTRYPOINT /opt/conda/bin/python -u /nispat/nispat/normative.py -c /mnt/data/test_normative_modeling/covariates_HC.txt -t /mnt/data/test_normative_modeling/covariates_allpatients.txt -r /mnt/data/test_normative_modeling/features_allpatients.txt -a gpr  /mnt//data/test_normative_modeling/features_HC.txt

