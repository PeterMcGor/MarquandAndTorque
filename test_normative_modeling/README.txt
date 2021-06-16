name os the variales in covariates files
python -u /mnt/data_code/nispat/nispat/utils_misc.py generate_batches /mnt/code_data2/test_normative_modeling/ -rtrain /mnt/code_data2/test_normative_modeling/features_HC.txt -rtest /mnt/code_data2/test_normative_modeling/features_allpatients.txt 
python -u /mnt/code_data2/nispat/nispat/utils_misc.py run_per_covariates  /mnt/code_data2/test_normative_modeling/ -ctrain /mnt/code_data2/test_normative_modeling/covariates_HC.txt -ctest /mnt/code_data2/test_normative_modeling/covariates_allpatients.txt -c_names age scode


