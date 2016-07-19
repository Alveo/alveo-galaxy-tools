Alveo Galaxy Tools
==================

Tools that make use of the Alveo API to import data into the Galaxy workflow
engine. These tools rely on the pyalveo Python module. 

Testing
-------

Each tool includes tests that can be run with the planemo command line tool.  Since
the tools require access to the Alveo API you need to supply a valid API key
for an account that has access to the AusNC collections on Alveo.  Enter this
in the file test-data/api-key.dat.  You should then be able to run the tests
with:

    % planemo test

run from this directory.  This generates a file tool_test_output.html with the
summary test results.  

Tools
-----

Store Alveo API Key - prompts for an API key from Alveo, verifies that it works
and stores it for use by later tools.

Get Alveo Item Lists - retrieves metadata for the item lists defined by the
user and any world-readable item lists that are available.  This allows the later
selection of an item list for downloading etc.

Get Text from Alveo - get text documents for each item in an item list. Store the
results as a dataset collection.

Get Files from Alveo - get files of different kinds for each item in an item list,
the tool can use a filename pattern (eg. \*.wav) to match files to download. Store
the results as a dataset collection.
