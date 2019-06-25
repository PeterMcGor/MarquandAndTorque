#!/bin/bash
export OMP_NUM_THREADS=1
cd /nispat/test_normative_modeling/batch_1/
/opt/conda/bin/python /nispat/nispat/normative.py -c /nispat/test_normative_modeling/covariates_HC.txt -t /nispat/test_normative_modeling/covariates_allpatients.txt -r /nispat/test_normative_modeling/batch_1/testresp_batch_1.txt -a gpr /nispat/test_normative_modeling/batch_1/resp_batch_1.txt
