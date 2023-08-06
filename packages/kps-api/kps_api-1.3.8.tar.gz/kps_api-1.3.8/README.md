# For customer use of xi iot client sdk is documented at 
* https://docs.google.com/document/d/1Rlt6EqIm8FgHVLXyFQm_nRaKGnM-2d2QvW_J2Nwb_OE/edit?usp=sharing

# For internal Use: 
## For setting up generated code for python2
<pre>
./setup.sh -2
</pre>

## For setting up generated code for python3
<pre>
./setup.sh -3
</pre>

# To run a sample api test
## for running unittests in python2
<pre>
cd tests

python -m unittest test_application_api.TestApplicationApi

python -m unittest test_project_api.TestProjectApi

python -m unittest test_edge_api.TestEdgeApi
</pre>

## for running unittests in python3
<pre>
cd tests

python3 -m unittest test_application_api.TestApplicationApi

python3 -m unittest test_project_api.TestProjectApi

python3 -m unittest test_edge_api.TestEdgeApi
</pre>

# Release tests
<pre>
./sdk_tools.sh download_release_sdk 1219
</pre>
<pre>
./sdk_tools.sh download_setup_test_release_sdk 1219
</pre>