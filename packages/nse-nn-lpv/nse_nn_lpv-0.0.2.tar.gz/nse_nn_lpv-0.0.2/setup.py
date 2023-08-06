from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='nse_nn_lpv',
      version='0.0.2',
      description='Helper functions for NSE as LPV with Neural Networks',
      # license="GPLv3",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jan Heiland',
      author_email='jnhlnd@gmail.com',
      # url="https://github.com/highlando/dolfin_navier_scipy",
      # packages=['dolfin_navier_scipy'],  # same as name
      install_requires=['numpy', 'scipy',
                        'dolfin_navier_scipy>=1.1.2',
                        'multidim_galerkin_pod>=1.0.3'],
      # 'sadptprj_riclyap_adi'],  # ext packages dependencies
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          ]
      )
