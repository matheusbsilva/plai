from plai.validation import validate_schema


class TestSchemaValidation:
    def test_valid_dataframe_dtypes(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'datetime64'
        }
        assert validate_schema(dataframe, schema) == {}

    def test_invalid_dataframe_dtypes(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'float',
            'floats': 'int',
            'dates': 'datetime64'
        }
        expected_errors = {
            'errors': [
                {'number': 'expected type `float` got `int64`'},
                {'floats': 'expected type `int` got `float64`'}
            ]
        }
        assert validate_schema(dataframe, schema) == expected_errors
