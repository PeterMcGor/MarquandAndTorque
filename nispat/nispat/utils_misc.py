import os
import numpy as np
import glob
from nispat.nispat.normative_parallel import split_nm, collect_nm
from nispat.nispat import normative
import argparse
import tempfile

import pandas as pd

def generate_fake_data(output_path, n_features, n_subjects, n_patients=0.1):
    os.makedirs(output_path, exist_ok=True)
    covariates = np.hstack([np.random.randint(12, 80, (n_subjects, 1)), np.random.randint(0, 2, (n_subjects, 1))])
    features = np.random.random((n_subjects, n_features))
    np.savetxt(os.path.join(output_path, "covariates_allpatients.txt"), covariates, fmt='%i')
    np.savetxt(os.path.join(output_path, "features_allpatients.txt"), features, fmt="%f")
    np.savetxt(os.path.join(output_path, "covariates_HC.txt"), covariates[:int(n_subjects * (1 - n_patients))],
               fmt='%i')
    np.savetxt(os.path.join(output_path, "features_HC.txt"), features[:int(n_subjects * (1 - n_patients))], fmt='%f')


def generate_batches(processing_dir, respfile, testresp=None, features_per_batch=50, binary=False):
    def create_path(file):
        return os.path.join(processing_dir, file) if file is not None else None

    def create_paths(file_list):
        return [create_path(file) for file in file_list]

    respfile, testresp = create_paths([respfile, testresp])
    split_nm(processing_dir, respfile, features_per_batch, binary, testresp)


def fit_per_batches(processing_dir, covfile, testcov=None, maskfile=None, from_to=None, batch_pattern='batch_',
                    alg='gpr', cvfolds=None, configparam=None, saveoutput=True, outputsuffix=None, frm_last_exec=False):
    batch_dirs = glob.glob(os.path.join(processing_dir, batch_pattern + '*')) if from_to is None else \
        [os.path.join(processing_dir, batch_pattern + str(batch_number)) for batch_number in
         range(from_to[0], from_to[1])]
    print(batch_dirs)
    init_dir = os.getcwd()
    for batch_dir in batch_dirs:
        if not os.path.exists(os.path.join(batch_dir, "Z"+outputsuffix+".txt")) or not frm_last_exec:
            batch_respfile = glob.glob(os.path.join(batch_dir, "resp_batch_*"))
            batch_respfile = None if len(batch_respfile) != 1 else batch_respfile[0]
            # These two must be always present
            assert batch_respfile is not None
            assert covfile is not None
            batch_testrespfile = glob.glob(os.path.join(batch_dir, "testresp_batch_*"))
            batch_testrespfile = None if len(batch_testrespfile) != 1 else batch_testrespfile[0]
            print(batch_respfile)
            print(batch_testrespfile)
            os.chdir(batch_dir)
            normative.estimate(batch_respfile, covfile, maskfile=maskfile, cvfolds=cvfolds, testcov=testcov,
                               testresp=batch_testrespfile, alg=alg, configparam=configparam, saveoutput=saveoutput,
                               outputsuffix=outputsuffix)
    os.chdir(init_dir)

def run_per_covariates(processing_dir, train_covariates, cov_file, cov_test_file = None, maskfile=None, from_to=None,
                       batch_pattern='batch_',alg='gpr', cvfolds=None, configparam=None, saveoutput=True,
                       frm_last_exec=False):
    def create_covs_filter(covariates_file, output_covariates_file):
        pd.read_csv(covariates_file, sep=" ").filter(items=cov_names).to_csv(output_covariates_file, sep=" ", header=False, index=False)


    tmp_dir = tempfile.gettempdir()
    id_covs = "-".join(train_covariates)
    #id_covs = ""
    print("TRAIN COVARIATES", train_covariates)
    # for cov in train_covariates:
    #     id_covs += cov+"-"
    print("ID_COVS", id_covs)
    tmp_covs_file = os.path.join(tmp_dir, "covs_"+id_covs+".txt")
    # Create a temporal file with the chosen covariates
    print(train_covariates)
    create_covs_filter(cov_file, tmp_covs_file)
    # same for covariates at test data
    tmp_covs_test_file = None
    print(train_covariates)
    if cov_test_file is not None:
        tmp_covs_test_file = os.path.join(tmp_dir, "covs_test_"+id_covs+".txt")
        create_covs_filter(cov_test_file, tmp_covs_test_file)

    fit_per_batches(processing_dir, covfile=tmp_covs_file, testcov=tmp_covs_test_file, maskfile=maskfile,
                    from_to=from_to, batch_pattern=batch_pattern, alg=alg, cvfolds=cvfolds, configparam=configparam,
                    saveoutput=saveoutput, outputsuffix="_"+id_covs, frm_last_exec=frm_last_exec)



class FunctionsID:
    GEN_BATCHES = "generate_batches"
    FIT_BATCHES = "fit_per_batches"
    COLLECT = "collect_results"
    RUN_PER_COVS = "run_per_covariates"


fn_dict = {FunctionsID.GEN_BATCHES: generate_batches, FunctionsID.FIT_BATCHES: fit_per_batches,
           FunctionsID.COLLECT: collect_nm, FunctionsID.RUN_PER_COVS: run_per_covariates}


if __name__ == '__main__':
    print("Utils_misc")
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="function to execute", choices=[f for f in fn_dict.keys()])
    parser.add_argument("processing_dirs", help="a single dir except f you are creating a structure for computation "
                                                "over several dirs")
    parser.add_argument("-rtrain", help="responses (train data)", dest="trainresp", default=None)
    parser.add_argument("-m", help="mask file", dest="maskfile", default=None)
    parser.add_argument("-ctrain", help="covariates file (train data)", dest="covfile", default=None)
    parser.add_argument("-k", help="cross-validation folds", dest="cvfolds", default=None)
    parser.add_argument("-ctest", help="covariates (test data)", dest="testcov", default=None)
    parser.add_argument("-rtest", help="responses (test data)", dest="testresp", default=None)
    parser.add_argument("-a", help="algorithm", dest="alg", default="gpr")
    parser.add_argument("-x", help="algorithm specific config options", dest="configparam", default=None)
    parser.add_argument("-fpb", help="Features per batch", default=50, type=int)
    parser.add_argument("-b", help="binary file", default=False, dest="binary")
    parser.add_argument("-frm", type=int, default=-1)
    parser.add_argument("-to", type=int, default=-1)
    parser.add_argument("-batch_pattern", default='batch_', type=str)
    parser.add_argument("-save_output", default=True)
    parser.add_argument("-outputsuffix", default="")
    parser.add_argument("-frm_last_exec", default=False, help="If True, if a result file is already present the batch "
                                                              "is just skipped")
    parser.add_argument("-c_names", default=["age"], help="Covariates to employ in a list", dest="cov_names", nargs='*')
    parser.add_argument("-collect_suffixes", default=[""], help="Collect the results by the given suffixes",  nargs='*',
                        dest="coll_suf")

    args = parser.parse_args()
    processing_dir = args.processing_dirs
    responses = args.trainresp
    covariates = args.covfile
    test_responses = args.testresp
    test_covariates = args.testcov
    features = args.fpb
    binary = args.binary
    maskfile = args.maskfile
    frm = args.frm
    to = args.to
    batch_pattern = args.batch_pattern
    alg = args.alg
    configparams = args.configparam
    saveoutput = args.save_output
    outputsuffix = args.outputsuffix
    frm_last_exec = args.frm_last_exec
    cov_names = args.cov_names
    coll_suf = args.coll_suf

    from_to = None if frm == -1 or to == -1 else [frm, to]
    print("Function", FunctionsID.RUN_PER_COVS)
    if args.function == FunctionsID.GEN_BATCHES:
        generate_batches(processing_dir, responses, testresp=test_responses,
                         features_per_batch=features, binary=binary)
    elif args.function == FunctionsID.FIT_BATCHES:

        fit_per_batches(processing_dir, covfile=covariates, testcov=test_covariates, maskfile=maskfile, from_to=from_to,
                        batch_pattern=batch_pattern, alg=alg, cvfolds=args, configparam=configparams,
                        saveoutput=saveoutput, outputsuffix=outputsuffix, frm_last_exec=frm_last_exec)
    elif args.function == FunctionsID.COLLECT:
        collect_nm(processing_dir, collect=True, binary=binary, outputsuffixes=coll_suf)
    else:
        run_per_covariates(processing_dir, cov_names, covariates, cov_test_file=test_covariates,  maskfile=maskfile,
                           from_to=from_to, batch_pattern=batch_pattern, alg=alg, cvfolds=args, configparam=configparams,
                           saveoutput=saveoutput, frm_last_exec=frm_last_exec)


    # generate_fake_data('/home/pmacias/Projects/JanJo/MarquandAndTorque/fake_data_3', 50, 700)
    # generate_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", "features_HC.txt",
    #                  testresp="features_allpatients.txt", features_per_batch=5)
    # fit_per_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/",
    #                 "/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_HC.txt",
    #                 testcov="/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_allpatients.txt",
    #                 from_to=[1, 11])
    # collect_nm("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", collect=True)
