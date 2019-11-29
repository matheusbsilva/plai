class Symbol:

    data: str
    CACHE = {}

    def __new__(cls, data):
        try:
            return cls.CACHE[data]
        except KeyError:
            cls.CACHE[data] = new = super().__new__(cls)
            new._data = data
            return new
