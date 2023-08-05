# Classification Reportzr

Automate machine learning classification task report for Pak Zuherman

## Install

```bash
pip install -U classification-reportzr
```

## Test

```bash
pytest -v
```

## Usage

### Setting-up the experiment

```python
from sklearn import datasets
from sklearn.svm import SVC

from reporterzr import Reporterzr

iris = datasets.load_iris()
samples, labels = iris.data[:-1], iris.target[:-1]

param_grid = {
    'C': [10,50,100],
    'gamma': [0.005,0.05,0.5],
    'kernel': ['poly', 'rbf', 'linear']
}
svc_reporter = Reporterzr(SVC, param_grid)
```

### Run The Experiment

```python
# `test_sizes` defaults to [0.1, ..., 0.9]
# `repetition` defaults to 10
report = svc_reporter.run_experiment(samples, labels, test_sizes=[0.1, 0.2], repetition=5)
print(report)
```

prints

```
   Test Size   C  gamma  kernel                     Train Accuracies  \
0        0.1  10  0.005    poly  [0.881, 0.888, 0.873, 0.888, 0.881]
1        0.1  10  0.005     rbf   [0.978, 0.955, 0.955, 0.955, 0.97]
2        0.1  10  0.005  linear    [0.978, 0.97, 0.985, 0.978, 0.97]
3        0.1  10  0.050    poly  [0.985, 0.978, 0.978, 0.978, 0.985]
4        0.1  10  0.050     rbf  [0.985, 0.993, 0.993, 0.993, 0.993]

   Max Train Acc  Mean Train Acc  Stdev Train Acc  \
0          0.888           0.882            0.006
1          0.978           0.963            0.010
2          0.985           0.976            0.006
3          0.985           0.981            0.003
4          0.993           0.991            0.003

                       Test Accuracies  Max Test Acc  Mean Test Acc  \
0      [0.867, 0.867, 1.0, 0.8, 0.933]         1.000          0.893
1  [0.933, 0.933, 0.933, 0.867, 0.933]         0.933          0.920
2            [1.0, 1.0, 1.0, 1.0, 1.0]         1.000          1.000
3          [1.0, 1.0, 1.0, 1.0, 0.933]         1.000          0.987
4        [0.933, 1.0, 1.0, 0.867, 1.0]         1.000          0.960

   Stdev Test Acc                         Experiment Times (sec)
0           0.068  [0.00095, 0.00077, 0.00072, 0.00077, 0.00074]
1           0.026   [0.00079, 0.0008, 0.00082, 0.00082, 0.00081]
2           0.000   [0.0005, 0.00052, 0.00045, 0.00049, 0.00049]
3           0.027  [0.00052, 0.00055, 0.00052, 0.00054, 0.00053]
4           0.053  [0.00062, 0.00062, 0.00064, 0.00061, 0.00065]
```
