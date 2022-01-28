# Plai [![codecov](https://codecov.io/gh/matheusbsilva/plai/branch/development/graph/badge.svg?token=Z56KFD6WPY)](https://codecov.io/gh/matheusbsilva/plai)

Plai is a domain specific programming language(DSL) to create data manipulation pipelines with focus on data treatment, validation and easier syntax. It uses [pandas]() as data manipulation engine so it is meant to work with small data.

## Examples 

Example of pipeline with basic data manipulation using Plai:

```
df = read_file('issues.csv')

pipeline(df) as 'gh_pct_issues_by_language.csv':
    $.groupby(.name, as_index=False).sum()
    (.count/sum(.count)) * 100 as pct
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