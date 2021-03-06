# pryke
Python library used to interact with [Wrike API](https://developers.wrike.com/documentation/api/overview)

[![Build Status](https://travis-ci.org/wikkiewikkie/pryke.svg?branch=master)](https://travis-ci.org/wikkiewikkie/pryke) [![codecov](https://codecov.io/gh/wikkiewikkie/pryke/branch/master/graph/badge.svg)](https://codecov.io/gh/wikkiewikkie/pryke)

## Running Tests

py.test --cov=pryke/ --cov-report=term-missing

## Test Objectives

* Well-formed and correct parameters are passed to the API.
* Correctly handle data returned by the API.
* Client behaves correctly when API calls produce an error.