import os
import numpy as np
import glob
from nispat.nispat.normative_parallel import split_nm, collect_nm
from nispat.nispat import normative


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



if __name__ == '__main__':
    print("Utils_misc")
    # generate_fake_data('/home/pmacias/Projects/JanJo/MarquandAndTorque/fake_data_3', 50, 700)
    # generate_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", "features_HC.txt",
    #                  testresp="features_allpatients.txt", features_per_batch=5)
    # fit_per_batches("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/",
    #                 "/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_HC.txt",
    #                 testcov="/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/covariates_allpatients.txt",
    #                 from_to=[1, 11])
    # collect_nm("/home/pmacias/Projects/JanJo/MarquandAndTorque/test_normative_modeling/", collect=True)
