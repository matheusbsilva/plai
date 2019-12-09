class Col:
    def __init__(self, name):
        self.name = name

    def __call__(self, dataframe):
        return dataframe[self.name]
