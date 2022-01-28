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

    def __repr__(self):
        return self._data

    def __str__(self):
        return self._data


Symbol.PIPELINE = Symbol('pipeline')
Symbol.BEGIN = Symbol('begin')
Symbol.ATTR = Symbol('.')
Symbol.COLUMN = Symbol('.column')
Symbol.ASSIGNMENT = Symbol('=')
Symbol.ALIAS = Symbol('as')
Symbol.LIST = Symbol('list')
Symbol.SLICE_DF = Symbol('{}')
Symbol.OUTPUT = Symbol('->')
Symbol.DICT = Symbol('dict')
Symbol.TYPE = Symbol('type')
Symbol.TYPED = Symbol('typed')
Symbol.FUNCTION = Symbol('function')
Symbol.DF_ATTR_CALL = Symbol('$')
