# configmerger

merge multi level configurations.

## Usage

``` py
from configmerger import Merger

# your configurations, read from app.json, machine.yaml, user.toml, or more
confs = [
    read_from_app(),
    read_from_machine(),
    read_from_user(),
]

# merge all configurations into one.
runtime_conf = Merger().merge(confs)
```

## Merge Rules

Here is the default merge rules:

``` py
merger = Merger()

# for dict, a little like Chainmap
merger.merge([
    {'a': 1},
    {'a': 2, 'b': 3},
    {        'b': 4}
])
#   {'a': 2, 'b': 4}

# for list, default behavior is connect each
# change `merger.connect_list` to `False` can change this behavior
merger.merge([ [1, 2, 3], [4, 5] ]) # [4, 5, 1, 2, 3]

# for str, int and others, latest have highest priority
merger.merge([ 'first', 'last' ]) # 'last'

# basic, `None` is ignored
merger.merge([ 1, None ]) # 1

# but if all values is `None`, return `None`
merger.merge([ None, None ]) # None

# if type changed, merge will stop,
merger.merge([
    {'a': 1},   # <--- ignored
    1,          # <--- type changed, ignore all before this
    {'b': 2},
    None,       # <--- None is ignored
    {'c': 3},
])# {'b': 2, 'c': 3}
```

Override any methods to modify the default behavior.
