![Build](https://github.com/radon-h2020/radon-defect-predictor/workflows/Build/badge.svg)
![Documentation](https://github.com/radon-h2020/radon-defect-predictor/workflows/Documentation/badge.svg)
![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/radon-h2020/radon-defect-predictor)
![pypi-version](https://img.shields.io/pypi/v/radon-defect-predictor)
![pypi-status](https://img.shields.io/pypi/status/radon-defect-predictor)
![release-date](https://img.shields.io/github/release-date/radon-h2020/radon-defect-prediction-cli)
![python-version](https://img.shields.io/pypi/pyversions/radon-defect-predictor)

# radon-defect-prediction
The RADON command-line client for Infrastructure-as-Code Defect Prediction.


## How to Install

From [PyPI](https://pypi.org/project/radon-defect-predictor/):

`pip install radon-defect-predictor`

From source code:

```text
git clone https://github.com/radon-h2020/radon-defect-prediction.git
cd radon-defect-predictor
pip install -r requirements.txt
pip install .
```

## Quick Start

```text
usage: radon-defect-predictor [-h] [-v] {train,predict,model} ...

A Python library to train machine learning models for defect prediction of infrastructure code

positional arguments:
  {train,predict,model}
    train               train a brand new model from scratch
    model               get a pre-trained model to test unseen instances
    predict             predict unseen instances

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```


# How to build Docker container

`docker build --tag radon-dp:latest .`


# How to run Docker container

First, create a host volume to share data and results between the host machine and the Docker container:

`mkdir /tmp/radon-dp-volume/` 
 
## Train

Create a training dataset `metrics.csv` and copy/move it to `/tmp/radon-dp-volume/`.
See how to generate the training data for defect prediction [here](https://radon-h2020.github.io/radon-repository-miner/cli/metrics/). 

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor train metrics.csv ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/train/) for more details about this command. 

The built model can be accessed at `/tmp/radon-dp-volume/radondp_model.joblib`.



## Model

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor download-model ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/model/) for more details about this command. 

The downloaded model can be accessed at `/tmp/radon-dp-volume/radondp_model.joblib`.



## Predict

Move the model and the files to predict in the shared volume.
For example, if you want to run the prediction on a .csar, then

`cp patah/to/file.csar /tmp/radon-dp-volume`.

Alternatively, you can create a volume from the folder containing the .csar (in that case, make sure to move the model within it).

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor predict ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/predict/) for more details about this command. 

The predictions can be accessed at `/tmp/radon-dp-volume/radondp_predictions.json`.

