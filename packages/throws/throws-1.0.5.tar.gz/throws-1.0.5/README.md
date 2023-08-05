# Python: throws

Small but simple library providing a function decorator similar to Kotlins *@throws(...)*
decorator with the small difference that multiple exceptions or errors can be combined in just one
single annotation. Should maily used for documentation and debugging purposes.

## Installation

Installation is possible using the Python *pip* command line tool. For you the command to install
this library may look like this:

```bash
pip3 install throws
```

## Usage

To use the *@throw* decorator simply place it before the function declaration providing every
possible exception raised by the function. For a quick example see below:

```python
from throws import throws

@throws(IOError, ValueError)
def check_version(version_file: str) -> bool:
    with open(version_file, "r", encoding = "utf-8") as vf:
        if (float(vf.read() > 1.0):
            return true
        return false
```

The library provides two Exceptions by itself, the *EmptyListException* and the
*InvalidRaisedException*. The first one is raised when there are no parameters provided to
*@throw* and the function decorated is run. The second one occours when the function raises an
exception which is not provided to the decorator, providing the developer with feedback that he
might have forgotten about handling this specific exception!

## Links

Library at the Python Package Index (PyPI): https://pypi.org/project/throws/
