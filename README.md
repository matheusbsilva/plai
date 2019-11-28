# plAI

Plai is a programming language to create machine learning pipelines 
with focus on data treatment, validation, and generation of integration tests to ensure more confiability to machine learning systems on production.

# Examples 

```
# This is a commnt

# Import statements
import math
from math import cos 

# To get a specific column of the main dataset on
# a pipeline call:
# .colname or ."colname"

# Function definition
def fn(x: int):
    return 2 * x + 1

# Inline function definition
fn(x: int) = 2 * x + 1

# Specifing columns type of a dataset
#
# Expression can be used to specify a certain type
# to all columns that match the pattern
type T = {
    timestamp: datetime,
    name: str,
    num*: float64,    
}

# Pipeline definition
# 
# Output of each expression became the input of the next
pipeline alt(df: T):
    foo(.name)
    bar(.timestamp)

    # Operation that must be applied term a term on a dataset
    # must use the operator `$` when calling the column
    # if there is no specification of target column 
    # the result will be loaded to the column being used on the operation
    # if there is more than one column being used a target column must be specified
    $.name + 'foo'

    # To specify a column as target of an operation use the operator `as`
    $.name + 'bar' as barname


# Exemple of pipeline
#
pipeline main(df: T, df2): 
    # Drop timestamp column
    drop(.timestamp)         

    bar($.name + '-foo') as name

    # Create new column 
    $.name + '-' + $.country + df2.x as id
    
    # Copy column
    $.id as id2
    
    fn(.name)

    dropna(.foo)

    merge df2 on x

    # Calling another pipeline
    alt

```