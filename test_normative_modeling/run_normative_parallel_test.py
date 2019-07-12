# -----------------------------------------------------------------------------
# Run parallel normantive modelling.
# All processing takes place in the processing directory (processing_dir)
# All inputs should be text files or binaries and space seperated
#
# It is possible to run these functions using...
#
# * k-fold cross-validation
# * estimating a training dataset then applying to a second test dataset
#
# First,the data is split for parallel processing.
# Second, the splits are submitted to the cluster.
# Third, the output is collected and combined.
#
# witten by (primarily) T Wolfers, (adaptated) SM Kia, H Huijsdens, L Parks,
# AF Marquand
# Newer modifications by P.M. Gordaliza
# -----------------------------------------------------------------------------

"""
    This function is a motherfunction that executes all parallel normative
    modelling routines. Different specifications are possible using the sub-
    functions.
    ** Input:
        * processing_dir     -> Full path to the processing directory. 
                                This will be the directory which you have   
                                cloned from Rindkind/test_normative_modeling.
        * python_path        -> Full path to the python distribution
        * normative_path     -> Full path to the normative.py
        * job_name           -> Name for the bash script that is the output of
                                this function
        * covfile_path       -> Full path to a .txt file that contains all
                                covariats (subjects x covariates) for the
                                responsefile
        * respfile_path      -> Full path to a .txt that contains all features
                                (subjects x features)
        * batch_size         -> Number of features in each batch
        * memory             -> Memory requirements written as string
                                for example 4gb or 500mb
        * duation            -> The approximate duration of the job, a string
                                with HH:MM:SS for example 01:01:01
        * cv_folds           -> Number of cross validations
        * testcovfile_path   -> Full path to a .txt file that contains all
                                covariats (subjects x covariates) for the
                                testresponse file
        * testrespfile_path  -> Full path to a .txt file that contains all
                                test features
        * log_path           -> Pathfor saving log files
        * binary             -> If True uses binary format for response file
                                otherwise it is text
"""


# run normative parallel - set up the scripts to call the test files-
# setup
import argparse

import os
import multiprocessing

import nispat.nispat as nispat


def main():
    processing_dir = args.processing_dir
    python_path = '/opt/conda/bin/python'
    normative_path = os.path.join(os.sep,"nispat", "nispat", "normative.py")
    job_name = 'normmod_test_script'
    covfile_path = os.path.join(processing_dir, 'covariates_HC.txt')
    respfile_path = os.path.join(processing_dir, 'features_HC.txt')
    testcovfile_path = os.path.join(processing_dir, 'covariates_allpatients.txt')
    testrespfile_path = os.path.join(processing_dir, 'features_allpatients.txt')
    batch_size = args.batch_size
    memory = args.memory
    duration = args.duration
    cv_folds = args.cv_folds
    log_path = os.path.join(processing_dir, job_name+".log")
    testrespfile_path = testrespfile_path if cv_folds is None else None
    testcovfile_path = testcovfile_path if cv_folds is None else None
    cpu_cores = args.cpu_cores


    nispat.normative_parallel.execute_nm(processing_dir,
                                         python_path,
                                         normative_path,
                                         job_name,
                                         covfile_path,
                                         respfile_path,
                                         batch_size,
                                         memory,
                                         duration,
                                         cpu_cores=cpu_cores,
                                         cv_folds=cv_folds,
                                         testcovfile_path=testcovfile_path,
                                         testrespfile_path=testrespfile_path,
                                         log_path=log_path
                                         )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--processing_dir',
        help='Full path to the processing directory.',
        type=str,
        default=None
    )
    parser.add_argument(
        '--cv_folds',
        help='Folds for CV.',
        type=int,
        default=None
    )

    parser.add_argument(
        '--cpu_cores',
        help='CPU cores to use.',
        type=int,
        default=multiprocessing.cpu_count() - 2
    )

    parser.add_argument(
        '--batch_size',
        help='Number of features in each batch.',
        type=int,
        default=50
    )

    parser.add_argument(
        '--memory',
        help='Memory requirements written as string for example 4gb or 500mb. By default 8gb',
        type=str,
        default='8gb'
    )

    parser.add_argument(
        '--duration',
        help='The approximate duration of the job, a string with HH:MM:SS for example 01:01:01. By default 3 hours',
        type=str,
        default='03:00:00'
    )

    args = parser.parse_args()
    arguments = args.__dict__

    main()







