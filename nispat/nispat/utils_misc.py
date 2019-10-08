import os
import numpy as np
import glob
from nispat.nispat.normative_parallel import split_nm, collect_nm
from nispat.nispat import normative
import argparse


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
                    alg='gpr', cvfolds=None, configparam=None, saveoutput=True, outputsuffix=None):
    batch_dirs = glob.glob(os.path.join(processing_dir, batch_pattern + '*')) if from_to is None else \
        [os.path.join(processing_dir, batch_pattern + str(batch_number)) for batch_number in
         range(from_to[0], from_to[1])]
    print(batch_dirs)
    init_dir = os.getcwd()
    for batch_dir in batch_dirs:
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


class FunctionsID:
    GEN_BATCHES = "generate_batches"
    FIT_BATCHES = "fit_per_batches"
    COLLECT = "collect_results"


fn_dict = {FunctionsID.GEN_BATCHES: generate_batches, FunctionsID.FIT_BATCHES: fit_per_batches,
           FunctionsID.COLLECT: collect_nm}


if __name__ == '__main__':
    print("Utils_misc")
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="function to execute", choices=[f for f in fn_dict.keys()])
    parser.add_argument("processing_dir")
    parser.add_argument("responses")
    parser.add_argument("-m", help="mask file", dest="maskfile", default=None)
    parser.add_argument("-c", help="covariates file", dest="covfile",
                        default=None)
    parser.add_argument("-k", help="cross-validation folds", dest="cvfolds",
                        default=None)
    parser.add_argument("-t", help="covariates (test data)", dest="testcov",
                        default=None)
    parser.add_argument("-r", help="responses (test data)", dest="testresp",
                        default=None)
    parser.add_argument("-a", help="algorithm", dest="alg", default="gpr")
    parser.add_argument("-x", help="algorithm specific config options",
                        dest="configparam", default=None)
    parser.add_argument("-fpb", help="Features per batch", default=50, type=int)
    parser.add_argument("-b", help="binary file", default=False, dest="binary")
    parser.add_argument("-frm", type=int)
    parser.add_argument("-to", type=int)
    parser.add_argument("-batch_pattern", default='batch_', type=str)
    parser.add_argument("-save_output", default=True)
    parser.add_argument("-outputsuffix", default=None)

    args = parser.parse_args()
    processing_dir = args.processing_dir
    responses = args.responses
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

    if args.function == FunctionsID.GEN_BATCHES:
        generate_batches(processing_dir, args.responses, testresp=test_responses,
                         features_per_batch=features, binary=binary)
    elif args.function == FunctionsID.FIT_BATCHES:
        fit_per_batches(processing_dir, covfile=covariates, testcov=test_covariates, maskfile=maskfile, from_to=[frm, to],
                        batch_pattern=batch_pattern, alg=alg, cvfolds=args, configparam=configparams,
                        saveoutput=saveoutput, outputsuffix=outputsuffix)
    else:
        collect_nm(processing_dir, collect=True)


    # generate_fake_data('/home/pmacias/Projects/JanJo/MarquandAndTorque/fake_data_3', 50, 700)
    # generate_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", "features_HC.txt",
    #                  testresp="features_allpatients.txt", features_per_batch=5)
    # fit_per_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/",
    #                 "/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_HC.txt",
    #                 testcov="/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_allpatients.txt",
    #                 from_to=[1, 11])
    # collect_nm("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", collect=True)
