# Plai [![codecov](https://codecov.io/gh/matheusbsilva/plai/branch/development/graph/badge.svg?token=Z56KFD6WPY)](https://codecov.io/gh/matheusbsilva/plai)

Plai is a domain specific programming language(DSL) to create data manipulation pipelines with focus on data treatment, validation and easier syntax. It uses [pandas](https://pandas.pydata.org) as data manipulation engine so it is meant to work with small data.

## Examples 

Example of pipeline with basic data manipulation using Plai:

```
df = read_file('issues.csv')

pipeline(df) as 'gh_pct_issues_by_language.csv':
    $.groupby(.name, as_index=False).sum()
    (.count/.count.sum()) * 100 as pct
    {.name, .count, .pct}
```

To create validations for the dataframes being manipulated you can define dictionaries mapping each column to a specific type, and apply
that to a dataframe or pipeline. When applied to the dataframe it will validate its schema accordingly to the defined on the dictionary, that is, it will check data type and column presence. For the pipeline, the result dataframe will be validated. The following snippet is an example of implementation:

```
input_type = {
    'name': 'str',
    'year': 'int',
    'quarter': 'int',
    'count': 'int'
}

output_type = {
    'name': 'str',
    'count': 'int',
    'pct': 'float'
}

input_type::df = read_file('issues.csv')

output_type::pipeline(df) as 'gh_pct_issues_by_language.csv':
    $.groupby(.name, as_index=False).sum()
    (.count/.count.sum()) * 100 as pct
    {.name, .count, .pct}
```

## Development 

1. Install the dependencies by running the command on the root folder of the project:
```
pip install -r requirements-dev.txt
```

2. To run all the tests execute:
```
pytest tests
```

To run a specific test execute:
```
# For a specific test file
pytest tests/test_grammar.py

# For a specific test class
pytest tests/test_grammar.py::TestBasicTokens

# For a specific tests method
pytest tests/test_grammar.py::TestBasicTokens::test_token_number
```

3. To run the interactive terminal execute on the root folder:
```
python -m plai
```

4. To execute the code from a file:
```
python -m plai file.plai
```