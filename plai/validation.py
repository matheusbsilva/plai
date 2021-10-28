import pandas.api.types as ptypes

VALIDATORS = {
    'str': ptypes.is_object_dtype,
    'int': ptypes.is_integer_dtype,
    'float': ptypes.is_float_dtype,
    'datetime64': ptypes.is_datetime64_dtype
}


def validate_schema(dataframe, schema):
    errors = []

    for col, dtype in schema.items():
        valid = VALIDATORS[dtype](dataframe[col])
        if not valid:
            col_dtype = dataframe[col].dtype
            errors.append({col: 'expected type `{}` got `{}`'.format(dtype, col_dtype)})

    if errors:
        return {'errors': errors}

    return {}
