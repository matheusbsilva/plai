import operator as op


class Col:
    def __init__(self, name, dataframe):
        self.dataframe = dataframe
        self.name = name

    def __call__(self):
        return self.dataframe[self.name]

    def operation(self, row, operation, *sargs):
        row[self.name] = operation(row[self.name], *sargs)
        return row

    def __add__(self, right):
        return self.dataframe.apply(self.operation, axis=1, args=(op.add, right))
