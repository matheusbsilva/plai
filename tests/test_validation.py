from plai.validation import validate_schema


class TestSchemaValidation:
    def test_valid_dataframe_dtypes(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str'
        }
        assert validate_schema(dataframe, schema) == {}

    def test_invalid_dataframe_dtypes(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'float',
            'floats': 'int',
            'dates': 'str'
        }
        expected_errors = {
            'errors': [
                "Expected 'number' to be 'float' got 'int64'",
                "Expected 'floats' to be 'int' got 'float64'",
            ]
        }
        assert validate_schema(dataframe, schema) == expected_errors

    def test_column_not_present_on_dataframe(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'int',
            'floats': 'float',
            'dates': 'str',
            'foo': 'str'
        }
        expected_errors = {
            'errors': [
                "DataFrame has no column 'foo'",
            ]
        }
        assert validate_schema(dataframe, schema) == expected_errors

    def test_colmun_not_present_and_invalid_dtypes(self, dataframe):
        schema = {
            'name': 'str',
            'number': 'float',
            'floats': 'int',
            'dates': 'str',
            'foo': 'str'
        }
        expected_errors = {
            'errors': [
                "Expected 'number' to be 'float' got 'int64'",
                "Expected 'floats' to be 'int' got 'float64'",
                "DataFrame has no column 'foo'"
            ]
        }

        assert validate_schema(dataframe, schema) == expected_errors
