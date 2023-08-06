# baselines
a python package used for benchmarking algorithms over various datasets

Data class : 
    show_datasets to show available datasets
    load_dataset to load specific dataset (pass name as argument)

Classification class :
    classification method:
        parameters:
            dataset in csv format or pandas dataframe with classification column at last
        result:
            returns benchmark for dataset with various algorithms and its f1_score
