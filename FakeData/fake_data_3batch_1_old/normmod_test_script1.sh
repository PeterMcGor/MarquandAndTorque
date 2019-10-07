#!/bin/bash
export OMP_NUM_THREADS=1
cd /mnt/data/FakeData/fake_data_3batch_1/
/opt/conda/bin/python /nispat/nispat/normative.py -c /mnt/data/FakeData/fake_data_3/covariates_HC.txt -t /mnt/data/FakeData/fake_data_3/covariates_allpatients.txt -r /mnt/data/FakeData/fake_data_3batch_1/testresp_batch_1.txt -a gpr /mnt/data/FakeData/fake_data_3batch_1/resp_batch_1.txt
