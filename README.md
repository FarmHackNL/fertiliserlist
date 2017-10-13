# List of sold/available fertilizers

A lot of different fertilizers are sold. For regulations, growth-optimization and 
comparisson calculations a user of fertilizer needs to keep track of the used products with their
compound specifications. This data-package aims to provide a list of available fertilizers in a
country with their relevant attributes.

This list provides a common/trade name, a code, unit of application, nutrients-contents, and more.

We aim to make this a reasonably complete list.

## Contributing

You can extend and improve this list by 

- submiting a pull request
- editing the underlying [Google Sheets](https://docs.google.com/spreadsheets/d/1oplc6Zr62abCfWWfN68MPQUT8uVkaa6Mr8sDHl2LKNQ/edit#gid=0) document.

## Compose data package

Run `./scripts/reader.py` to load our shared google docs sheet into the 'data/fertilisers.csv' datapackage.

## How to use

We use the Frictionless Datapackages approach for distributing this data. See http://frictionlessdata.io/data-packages/ for more info.
