# workspacesaver

A utility to replicate matlab's workspace saving function.

This module uses `shelve` to pickle global variables and add them to a persistent database, and retrieve them again.

It was written for python 3 but may work in python 2.

## Installation

```bash
git clone git@github.com:clbarnes/workspacesaver.git
cd workspacesaver
python setup.py install
```

`sudo` may be required.

## Usage

### Using the class:

```python
from workspacesaver import WorkspaceSaver
ws = WorkspaceSaver('workspace.db', globals())
# generate some variables
ws.save()
```

Variables initialised before the `WorkspaceSaver` are ignored.

### Using the context manager:

```python
from workspacesaver import WorkspaceSaver
with WorkspaceSaver('workspace.db', globals()):
    # generate some variables
```

### Retrieving the workspace:
```python
from workspacesaver import retrieve_workspace
load_workspace('workspace.db', globals())
```

By default, callables (types and functions) are not added to the database and will not be retrieved from any database
. To enable them, use `allow_callables=True` when calling `WorkspaceSaver.save()` and using `load_workspace()`.
