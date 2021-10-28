from plai.validation import validate_schema


class TestSchemaValidation:
    def test_valid_dataframe_schema(self, dataframe):
        schema = {'name': str, 'number': int, 'floats': float, 'dates': 'datetime64'}
        assert validate_schema(dataframe, schema) is True

    def test_invalid_dataframe_schema(self, dataframe):
        schema = {'name': str, 'number': float, 'floats': int, 'dates': 'datetime64'}
        assert validate_schema(dataframe, schema) is False
