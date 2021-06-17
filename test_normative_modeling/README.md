## The very first time clone the repository
`git clone https://github.com/PeterMcGor/MarquandAndTorque.git`

## Be sure about...
Covariates files must contain a header with covariates names. Check `~/MarquandAndTorque/test_normative_modeling/covariates_HC.txt` and `~/MarquandAndTorque/test_normative_modeling/covariates_allpatients.txt` as an example

## Run the docker image with a link to the cloned repository
`docker run -v /path/to/local_repository/MarquandAndTorque:/mnt/data_code -it petermcgor/xeon-normative`

## Generate batches
-fpb (features per batch) number of features to fit per batch (paralelization purposes). By Default 50
`python -u /mnt/data_code/nispat/nispat/utils_misc.py generate_batches /mnt/data_code/test_normative_modeling/ -rtrain /mnt/data_code/test_normative_modeling/features_HC.txt -rtest /mnt/data_code/test_normative_modeling/features_allpatients.txt -fpb 10`

## Fit the models 
`python -u /mnt/data_code/nispat/nispat/utils_misc.py run_per_covariates  /mnt/data_code/test_normative_modeling/ -ctrain /mnt/data_code/test_normative_modeling/covariates_HC.txt -ctest /mnt/data_code/test_normative_modeling/covariates_allpatients.txt -c_names age scode`

### With CV
`python -u /mnt/data_code/nispat/nispat/utils_misc.py run_per_covariates  /mnt/data_code/test_normative_modeling/ -ctrain /mnt/data_code/test_normative_modeling/covariates_HC.txt -c_names age scode -k 3`

