class Data():
    """
    Class to check available datasets 
    """
    def __init__(self) -> None:
        pass
    def add_dataset(self,dataset):
        print(dataset)
    def show_dataset(self):
        """
        Returns the list of datasets already availabe
        """
        import seaborn
        return seaborn.get_dataset_names()
    def load_dataset(self,name):
        """
        Returns the dataset whose name is passed
        """
        import seaborn
        dataset = seaborn.load_dataset(name)
        return dataset