import pandas.api.types as ptypes

VALIDATORS = {
    str: ptypes.is_object_dtype,
    int: ptypes.is_integer_dtype,
    float: ptypes.is_float_dtype,
    'datetime64': ptypes.is_datetime64_dtype
}


def validate_schema(dataframe, schema):
    validations = [VALIDATORS[dtype](dataframe[col]) for col, dtype in schema.items()]
    return all(validations)
