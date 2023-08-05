[![pipeline status](https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/fdsnextender/badges/master/pipeline.svg)](https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/fdsnextender/commits/master)

[![coverage report](https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/fdsnextender/badges/master/coverage.svg)](https://gricad-gitlab.univ-grenoble-alpes.fr/OSUG/RESIF/fdsnextender/commits/master)

# RESIF Tool to extend fdsn network code

## Prerequisite

SELECT privileges in the `networks` and `station` tables from `resifInv` database

## Installation

``` shell
pip install fdsnextender
```

## Usage

``` python

from fdsnextender import fdsnextender

myextender = fdsnextender.FdsnExtender(dburi="postgresql://...")
myextender.extend(network_code='ZO', year=2013)
```
Returns a string `ZO2008` for instance.

## Specification

1. Have an internal structure allowing to compute the extended network code from a given FDSN network code and a year
2. Expose a function to make the computation

The internal structure can be initialized with a request to the station webservice. Baseurl should be configurable

The overall programm is a class.
