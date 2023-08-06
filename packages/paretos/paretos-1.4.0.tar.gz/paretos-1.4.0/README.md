# Paretos package
This is the paretos package for easy integration of socrates optimization
within customer environments. The package also enables to get the results
of socrates api in an easy and understandable way.

## Installation
The installation of the package is simply done via. pip

```shell
pip install paretos
```

## Usage
In general the complete documentation for usage and classes can be found [here](https://docs.paretos.io/). In this
readme only brief overview of the most important points to get started is given.

## Development

This section is aimed towards developers of the paretos library.

### Getting Started

You will find some executable examples in the `/examples` folder.

See [examples/getting-started.md](examples/getting-started.md) for the necessary steps to run those scripts.

### Linting
- `isort .`
- `black .`
### Unit Testing
- `python -m unittest discover test/unittest`
- `coverage run --source paretos -m unittest discover test/unittest`
- `coverage html`

## Dependencies
- requires connection to Socrates API 1.2.0 or newer
