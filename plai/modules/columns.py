class Col:
    def __init__(self, name, dataframe):
        self.dataframe = dataframe
        self.name = name

    def __getattr__(self, attr):
        return getattr(self(), attr)

    def __call__(self):
        return self.dataframe[self.name]

    def __add__(self, right):
        if(isinstance(right, Col)):
            right = right()
        return self().__add__(right)

    def __sub__(self, right):
        if(isinstance(right, Col)):
            right = right()
        return self().__sub__(right)

    def __mul__(self, right):
        if(isinstance(right, Col)):
            right = right()
        return self().__mul__(right)

    def __truediv__(self, right):
        if(isinstance(right, Col)):
            right = right()
        return self().__truediv__(right)

    def __floordiv__(self, right):
        if(isinstance(right, Col)):
            right = right()
        return self().__floordiv__(right)

    def __gt__(self, right):
        return self()[self() > right]

    def __ge__(self, right):
        return self()[self() >= right]

    def __lt__(self, right):
        return self()[self() < right]

    def __le__(self, right):
        return self()[self() <= right]

    def __eq__(self, right):
        return self()[self() == right]

    def __ne__(self, right):
        return self()[self() != right]

    def contains(self, name):
        return self()[self().str.contains(name)]
