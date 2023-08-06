# baselines
a python package used for benchmarking algorithms over various datasets<br>

# Installation
```bash
pip install base2lines
```

# Introduction
## Data class : 
### show_datasets: 
show available datasets
### load_dataset : 
load specific dataset (pass name as argument)

## Classification class :
### classification method:
##### parameters:
###### dataset in csv format or pandas dataframe with classification column at last
##### result:
####### returns benchmark for dataset with various algorithms and its f1_score

## Regression Class:
### regressor method:
##### parameters:
###### dataset (pandas dataframe)
###### resultantColumn (name of column which has the value to be predicted)

## Pipeline Class:
### __init__ method:
##### parameters:
###### dataset (pandas dataframe)
### show_graph method:
##### parameters:
###### pipeline_show (sklearn Pipeline object which will be inturn turned to graph)

# How to use
## Data Class
```python
from baseline.Data import Data
data = Data()
dataset_names = data.show_dataset()
#name should be only from dataset_names 
dataset = data.load_dataset('name') 
```

## Classification Class
```python
from baseline.classification import Classification
classifier = Classification()
# dataset's last column should be the column to be classified
results = classifier.classification(dataset)
print(results)
```
## Regression Class
```python
from baseline.regression import Regression
regressors = Regression()
# also pass the resultant column
results = regressors.regressor(dataset , resultantColumn)
print(results)

```
## Pipeline Class
```python
from baseline.pipeline import Pipeline
graph = Pipeline(dataset)
#pipeline should only have sklearn components
graph.show_graph(pipelineToBeShown)
```
