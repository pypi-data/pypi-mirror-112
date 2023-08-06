# python-seravo
Shared Python features for Seravo's internal use

## Usage

```python3
from seravo.helpers.http import get

my_timezone = get(url='https://seravo.com/wp-json').get('timezone_string',
                                                        None)
print(my_timezone)
```


## Development
You may eg. just insert `src/` to your Python path, eg. with.

    PYTHONPATH="$(pwd)/src" python3

to launch xxx.
