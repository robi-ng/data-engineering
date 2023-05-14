# Machine Learning on Car Data

## Overview

This section shows using machine learning model to predict the car buying price based on data from https://archive.ics.uci.edu/ml/datasets/Car+Evaluation.

## How to run

### 1. Ensure that pip is updated

Ensure that python environment with pip is available. Installing `scikit-learn` may fail on older pip. Ensure that pip is updated by running `pip install --upgrade pip`.

### 2. Install requirements

Run `pip install -r requirements.txt` to install the dependencies.

### 3. Run the python script

Run `python predict_car_buying_price.py` to run the machine learning model and predict.

### 4. Output is generated

Sample parameters:

```
{
    "maintenance": ["high"],
    "doors": ["4"],
    "lug_boot": ["big"],
    "safety": ["high"],
    "class_value": ["good"],
}
```

Sample output:

```
Predicted buying price: vhigh
```
