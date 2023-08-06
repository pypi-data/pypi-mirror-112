# Declair :cake:
[![pipeline status](https://gitlab.com/k-cybulski/declair/badges/master/pipeline.svg)](https://gitlab.com/k-cybulski/declair/-/commits/master)
[![coverage report](https://gitlab.com/k-cybulski/declair/badges/master/coverage.svg)](https://gitlab.com/k-cybulski/declair/-/commits/master)

Declair is a framework for declaratively defining hyperparameter optimization experiments. It uses [Sacred](https://github.com/IDSIA/sacred) for storing experiment results and supports [Hyperopt](https://github.com/hyperopt/hyperopt) for optimization.

At its core, Declair provides a YAML/JSON based language for defining parameter spaces for hyperparameter search as well as single experiment runs. These parameter spaces can be easily nested and may include Python objects and outputs of function calls.

Declair is focused on reproducibility and ease of use between machines. By the use of [Sacred observers](https://sacred.readthedocs.io/en/stable/observers.html), it ensures that results of experiments are safely stored, together with the source code of all classes and objects used in them, as well as the Declair experiment configuration itself. To make reproduction of experiments easy between machines, it supports environment configuration files which can be used to store variables, like local dataset paths or secret tokens.

It contains various features to make defining experiments ergonomic. These include variable handling as well as configuration inheritance.

# Usage
For detailed instructions on how to use Declair, see the [documentation](https://k-cybulski.gitlab.io/declair/).

## Installation
You can install Declair via pip.
```
pip install declair
```

## Running the tests
Go into the root of the repository (i.e. where this `README.md` is), install `pip install pytest` and run
```
python -m pytest
```

# Credits
Declair came about from attempts to recreate [DeepSolaris](https://gitlab.com/CBDS/DeepSolaris) results in PyTorch instead of Keras, with a focus on search experiment definition ergonomics and reproducibility. However, it grew to be a more extensive and general framework than originally planned. Its design based on configuration files was heavily inspired by [cbds_common](https://gitlab.com/CBDS/cbds_common).

It is developed with ❤️  at [CBDS](https://www.cbs.nl/en-gb/our-services/unique-collaboration-for-big-data-research).
