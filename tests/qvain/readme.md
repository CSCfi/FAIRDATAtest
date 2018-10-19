# Qvain integration tests

This directory contains the integration tests between Qvain and Metax.

## Test order

The Qvain tests should be run in alphabetical order as they are not unit tests and actually test state changes. Arguably the tests could be more self-contained, but this approach will suffice for now.

## Authentication

All Qvain operations require an authenticated user. The easiest way to get a valid user is for an actual human being to log in to the website on the server the tests run on and copy the session cookie. The session id can be stored into the environment variable `QVAIN_SID` or put in the configuration file under `conf_vars['QVAIN']['SID']`. This avoids a whole range of potential problems with stale user and project data as the tests run in the context of the user logged in, just like during real usage.

You can then run Qvain's tests as long as the session is valid:

```
QVAIN_SID="Us0dEnmlYo8kweiQtPWegw" python -m unittest -f tests.qvain.qvain_tests
```

Note the use of the `-f` flag for quick failing tests; this makes sure all tests are skipped if one fails. A likely reason for failure is not being authenticated (anymore), so it is better to quit the whole test.

You can run the full test suite with report creation like this:

```
QVAIN_SID="Us0dEnmlYo8kweiQtPWegw" python run_all.py
```
