import os
import numpy as np
import glob
import yaml
from nispat.nispat.normative_parallel import split_nm


def generate_fake_data(output_path, n_features, n_subjects, n_patients=0.1):
    os.makedirs(output_path, exist_ok=True)
    covariates = np.hstack([np.random.randint(12, 80, (n_subjects, 1)), np.random.randint(0, 2, (n_subjects, 1))])
    features = np.random.random((n_subjects, n_features))
    np.savetxt(os.path.join(output_path, "covariates_allpatients.txt"), covariates, fmt='%i')
    np.savetxt(os.path.join(output_path, "features_allpatients.txt"), features, fmt="%f")
    np.savetxt(os.path.join(output_path, "covariates_HC.txt"), covariates[:int(n_subjects*(1 - n_patients))], fmt='%i')
    np.savetxt(os.path.join(output_path, "features_HC.txt"), features[:int(n_subjects * (1 - n_patients))], fmt='%f')


def modify_yml_file(yml_file, dict_params_to_modify, outfile=None):
    with open(yml_file, 'r') as stream:
        params = yaml.load(stream)
    params = {**params, **dict_params_to_modify}
    outfile = yml_file if outfile is None else outfile
    with open(outfile, 'w') as writer:
        yaml.dump(params, writer, default_flow_style=False)

def generate_k8s_kubernetes(processing_dir, respfile, covfile, yml_template, maskfile=None, cvfolds=None, testcov=None, testresp=None,
                            alg='gpr', configparam=None, saveoutput=True, outputsuffix=None, features_per_batch=50,
                            binary=False):
    def create_path(file):
        return os.path.join(processing_dir, file) if file is not None else None

    def create_paths(file_list):
        return [create_path(file) for file in file_list]

    respfile, covfile, maskfile,testcov, testresp = create_paths([respfile, covfile, maskfile, testcov, testresp])
    split_nm(processing_dir, respfile, features_per_batch, binary, testresp)
    batch_dirs = glob.glob(os.path.join(processing_dir, 'batch_*'))
    for batch_dir in batch_dirs:
        batch_respfile = glob.glob(os.path.join(batch_dir, "resp_batch_*"))
        batch_respfile = None if len(batch_respfile) != 1 else batch_respfile[0]
        batch_testrespfile = glob.glob(os.path.join(batch_dir, "testresp_batch_*"))
        batch_testrespfile = None if len(batch_testrespfile) != 1 else batch_testrespfile[0]
        print(batch_respfile)
        print(batch_testrespfile)






if __name__ == '__main__':
    print("Utils_misc")
    #generate_fake_data('/home/pmacias/Projects/JanJo/MarquandAndTorque/fake_data_3', 50, 700)
    generate_k8s_kubernetes("/home/pmacias/Projects/JanJo/MarquandAndTorque/FakeData/fake_data/", "features_HC.txt",
                            "covariates_HC.txt", testcov="covariates_allpatients.txt",
                            testresp="features_allpatients.txt")