from setuptools import setup, find_packages

REQUIRED_PACKAGES = ["pandas", "scipy", "nibabel", "sklearn", "torch"]

setup(name='nispat',
      version='0.2',
      install_requires=REQUIRED_PACKAGES,
      description='Spatial methods for neuroimaging data Pedro M. Gordaliza docker',
      url='http://github.com/amarquand/nispat',
      author='Pedro M. Gordaliza modified from Andre Marquand',
      author_email='pmacias@ing.uc3m.es',
      license='GNU GPLv3',
      packages=find_packages(),
      zip_safe=False)
