## Docker Torque

#### Introduction

This image runs the Torque scheduler and a single worker on a Ubuntu host. One user is provided for submission of jobs. --> This is from https://github.com/neilav/docker-torque

I have included Andre Marquand work for nispat --> https://github.com/amarquand/nispat

#### Build

`docker build -t torque .`

#### Run the docker with a link to you machine where the data is placed (-v argument). The "data" folder must contain files: covariates_allpatients.txt, covariates_HC.txt, features_allpatients.txt, features_HC.txt

`docker run -v /path/to/the/data/dir:/mnt/data -h master --privileged -it torque bash`

#### Once within the docker
###### change to user "batchuser"
`su batchuser`
###### Run the script "run_normative_parallel_test.py" pointing to your data (mounted) with "processing_dir" argument specifiying testrespfile_path and testcovfile_path (without CV)
`/opt/conda/bin/python nispat/test_normative_modeling/run_normative_parallel_test.py --processing_dir /mnt/data/`

###### Run the script "run_normative_parallel_test.py" pointing to your data (mounted) with "processing_dir" argument and CV specifying the number of folds
`/opt/conda/bin/python nispat/test_normative_modeling/run_normative_parallel_test.py --processing_dir /mnt/data/ --cv_folds #folds`


