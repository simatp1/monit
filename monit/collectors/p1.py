"""Get reports on the status of the hardware at P1 from webserver, e.g.

example input file is in examples/resources.txt

The same file sits on the webserver https://squid.cern.sh/resources.txt

Returns:
    list of hostnames of the resources that should be available to do work, e.g.
    ['vm-sp1-cn-00001', 'vm-sp1-cn-00002', ..., 'vm-sp1-cn-94042']
"""


def list_resources():
    # 1. grab list from file or webserver
    # 2. drop everything that is no "prod simp1"
    # 3. take the remaining hostnames and turn them into a list of strings
    return ['stuff', 'more stuff']
