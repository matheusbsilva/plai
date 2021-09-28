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
        return self() + right

    def __sub__(self, right):
        return self() - right

    def __mul__(self, right):
        return self() * right

    def __truediv__(self, right):
        return self() / right

    def __floordiv__(self, right):
        return self() // right
