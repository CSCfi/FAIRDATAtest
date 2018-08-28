# FAIRDATA Integration Tests

A repository for integration testing between the various Fairdata services.

The purpose of these tests is to find out whether some recent change in features or configuration of a service has resulted in a regression in a depending service, by sending various UI-imitating http requests (or other kind of useful requests) to related services, which then communicate with other live services.

The current integration test environment consists of "<service>-stable" servers, but any other server can be used by configuring the tests to use them, and making sure firewalls etc permit it.

### When and why would I want to run integration tests?

**When:** Before deploying anything to production. Before testing, you should ensure that the versions of the services you are testing with, are either the same versions as their production instances, OR, the same newer versions that you will be deploying to production with. **Why:** Because you hate manually testing if your service still works when someone else decided to update a service you depend on.

### Dependencies

    python >=3.4

## Repository layout

    config/ # contains configuration files and templates
    reports/ # is a generated directory. will contain generated html reports of test runs
    test_data/ # any static test data or templates for testing
    tests/ # source code containing the actual tests
    utils.py # some general shared utils

`tests/` will contain a directory per service, such as `tests/ida/`, which would contain all tests related to tests that originate from Ida to other services. The actual tests are in `tests/ida/ida_tests.py`, while service-related helper methods are in `tests/ida/ida.py`.

While files can be named in different ways or located in different places in the repository according to what feels useful, executing the main test file `run_all.py` will only find tests cases from source code files that end in `*_tests.py`.

The intent is that service developers should consider e.g. `tests/ida/` their personal domain, where they will do whatever they consider as necessary and useful to ensure their service will play nicely with whatever services it depends on.

## Installation

    git clone https://github.com/CSCfi/FAIRDATAtest
    cd FAIRDATAtest
    python3 -m venv venv
    source venv/bin/activate
    venv/bin/pip install -r requirements.txt
    cp config/config_template.py config/config.py

After copying the config template to config.py, fill in service info for the services being tested. Test suites for services which are not found in the config.py or do not have a host set, will be automatically skipped.

## Configuration

A template configuraion file can be found in `config/config_template.py`. By following the steps above, you should have ended up with another config file, `config/config.py`, which will be the real config file used by test suites. In `config/config.py`, fill in information for any services that you are going to test. Mostly the information required is just service hostnames, and user/password information for http requests. Services are free to add any additional configurations there as needed.

## Running the tests

Note: All example commands described here should be executed from the root of the repository, unless stated otherwise.

### Run all tests

Run all tests for all services which have configurations in place in `config/config.py`:

    python run_all.py

The above command searches the repository for unittest TestSuites in all files whose filename ends in `*_tests.py`, and executes them (unless there is some reason to automatically skip them). Uses HTMLTestRunner which autogenerates a test report to `reports/`.

Unfortunately HTMLTestRunner seems to be hiding output from any `print()` clauses, so while writing your tests or debugging, any extra printing etc will not be very helpful. In order to see any prints, use the option `--runner=default` to use unittest's default TextTestRunner instead:

    python run_all.py --runner=default

Note: While using the defaul test runner, you might see some (at first glance) crazy looking output, such as seemingly arbitrary appearances of lines of dots, s, F, or E characters... Those mean s=skipped, F=failed, E=error, and .=success (without presence of any custom print lines, it would be just a nice line of ..........F..E..sss etc).

### Run tests of a specific service or component

For example, to run only Ida's tests, execute command:

    python -m unittest tests.ida.ida_tests

This uses unittest's default TextTestRunner, which does not generate a report, and may print extra warnings and whatever extra printing the tests contain. In order to suppress warnings, use `-W ignore` option:

    python -W ignore -m unittest tests.etsin.etsin_tests

Be careful though, you may accidentally hide useful information.

## Writing new tests

### Where to place my tests

* If your service does not exist in the directory `tests/` already, create a new directory for it, similar to what other services have.
* If your service already exists within the repo, extend some existing test suite of your service, or create new ones as sensible. It's also fine to create other files in your service's directory, as long as the files containing actual tests end with `*_tests.py`.

### What kind of tests to write

* The integration tests should not be used to execute your service's internal unit tests. If your service's unit tests are failing, then that version of your service should not be deployed in the integration test network in the first place.
* Write tests that causes your service to communicate with other services, preferably ones that imitate real UI requests to your backend, or execute some scheduled thing that talks with another service, etc...

### How to write my tests

* Try to write descriptive `test suite` names (python class name of the unittest) and `test case` names (the methods whose names start with test_* inside your test suite class), since those will be visible on the html reports. Terrible test names will make your PO stand in awkward silence if you ask them if they understand what's going on in the html report.
* Individual test cases should not depend on results produced by other test cases.
* Avoid using `sleep()` to wait for some background process to complete. Instead, figure out some way poll the related service (or maybe it's reasonable to poll it from another related service?) when some task is complete, so that the tests don't take forever to complete, or the tests don't suddenly start failing since sometimes the hardcoded sleep time is not good enough, etc...
* Ensure each new test case or suite finally resets the related services to their initial state, so that later tests will not get disturbed by unexpected conditions. Even if your test does not outright fail because of this, it may be that it is only succeeding because of conditions left by a previous test (i.e. some resource is found, because it was not cleaned up by a previous test).

### Also...

* If you find that *YOUR* service is unable to perform the previous step, kindly consider doing something about it, unless you want to be manually resetting your test server everytime someone else is doing something with it and is getting mystical results.
* A good location for this kind of cleanup code for other services to call (i.e. a simple api call) would probably be among your service's helper methods, such as in `tests/ida/ida.py`

### How to get my tests/changes/whatever included in the repo

Make a pull request.

## Reporting

When running tests by executing `python run_all.py`, html reports are generated to sub-directory `reports/`.

The test suites utilize a fork of HTMLTestRunner https://github.com/JamesMTSloan/HtmlTestRunner This fork has a useful feature which combines different reports into a single report (the upstream version will be used once that feature PR is merged to it).

In the report, tests are grouped by test suite, and ordering is alphabetical. If the report does not seem to be containing enough information, it is possible to customize the template.
