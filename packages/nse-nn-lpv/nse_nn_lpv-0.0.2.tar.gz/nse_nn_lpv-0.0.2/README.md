Neural Networks for NSE as low-dimensional LPV
---

# Active workflow

## Installation

```sh
# package for sparse cholesky factorizations 
# not needed but speed up with FEM norms and POD
apt install libsuitesparse-dev
pip install scikit-sparse==0.4.5

# fenics -- for the FEM part
apt install fenics  # see https://fenicsproject.org/download/

# install this module and helper modules
pip install .
```

## Generate the data

```sh
cd ../simulations-training-data
mkdir simu-data
mkdir train-data
source start-generic-tdp-sim.sh
# python3 time_dep_nse_generic.py
cd -
```

## Check the NN

```sh
python3 data_fem_checks.py
python3 CNN_AE.py
```

## Python Machine-Learning Resources

 * an [overview](https://analyticsindiamag.com/top-7-python-neural-network-libraries-for-developers/)
   1. Tensorflow -- see below
   2. Pytorch -- see below
   3. NeuroLab
   4. ffnet
   5. Scikit-Neural Network
   6. Lasagne
   7. pyrenn

### Tensorflow

 * [website](https://www.tensorflow.org/)
 * [Article for understanding NN using TensorFlow](https://towardsdatascience.com/building-your-first-neural-network-in-tensorflow-2-tensorflow-for-hackers-part-i-e1e2f1dfe7a0)
 * Previous experience with building NN
* Visualization feature [TensorBoard](https://www.tensorflow.org/tensorboard)
* Based on keras 

### PyTorch

 * [website](https://pytorch.org/)
 * [Tutorial for simple NN](https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html)
 * Recommended by colleagues (Lessig, Richter)

### Scikit-Learn

 * [website](https://scikit-learn.org/stable/index.html)
 * looks well maintained
 * many routines for data processing
 * a few on neural network 

## Install

```sh
# not needed anymore
# pip install -e .  # Python3 needed here! install the module (and one dependency)
```

`pip install -e` installs the module `nse_nn_lpv` to be used in the `tests/...`
but keeps track of all changes made in `nse_nn_lpv`.
