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
        if col not in dataframe:
            errors.append("DataFrame has no column '{}'".format(col))
            continue

        valid = VALIDATORS[dtype](dataframe[col])
        if not valid:
            col_dtype = dataframe[col].dtype
            errors.append("Expected '{}' to be '{}' got '{}'".format(col, dtype, col_dtype))

    if errors:
        return {'errors': errors}

    return {}
