Alveo Galaxy Tools
==================

Galaxy tools written to process speech and language data for the Alveo project.

Testing
-------

Each tool includes tests that can be run with the planemo command line tool.  Since
the tools require access to the Alveo API you need to supply a valid API key
for an account that has access to the AusNC collections on Alveo.  Enter this
in the file test-data/api-key.dat.  You should then be able to run the tests
with planemo (e.g. for the apitools):

    % planemo test --conda_dependency_resolution apitools/*.xml

run from this directory.  This generates a file tool_test_output.html with the
summary test results.  

Tools
-----

Tools are grouped into sub-directories based on their main function and their
common dependencies (requirements).  

 * apitools - tools that use the pyalveo library to work against the Alveo API
 * textgrid - tools that use the tgt python library to work with TextGrid files
 * wrassp - tools that do signal processing with the R wrassp package
 * vowel-plot - plot vowel formants with the R phonR package
 * parse_eval - R based syllable parsing analysis
 * nltk - text processing tools based on the python NLTK module

Since the tools work together, there is shared test data in the test-data directory.
