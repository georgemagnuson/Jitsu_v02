# test gmail access here


# check that gmail account is reachable and valid

# check that messages can be downloaded/read

# check that messages labels can be changed

# check that messages can be marked as READ

#!/usr/bin/env python3
"""tests for hello.py"""

import os
from subprocess import getstatusoutput, getoutput

prg = './gmail_access.py'
parameters = './database.ini'

# --------------------------------------------------
def test_gmail_access_exists():
    """exists"""

    assert os.path.isfile(prg)

# check that database.ini exists
# --------------------------------------------------
def test_parameters_exists():
    """database.ini exists"""

    assert os.path.isfile(parameters)

# --------------------------------------------------
# def test_runnable():
    # """Runs using python3"""

    # out = getoutput(f'python3 {prg}')
    # assert out.strip() == 'Hello, World!'


# --------------------------------------------------
# def test_executable():
    # """Says 'Hello, World!' by default"""

    # out = getoutput(prg)
    # assert out.strip() == 'Hello, World!'


# --------------------------------------------------
# def test_usage():
    # """usage"""

    # for flag in ['-h', '--help']:
        # rv, out = getstatusoutput(f'{prg} {flag}')
        # assert rv == 0
        # assert out.lower().startswith('usage')


# --------------------------------------------------
# def test_input():
    # """test for input"""

    # for val in ['Universe', 'Multiverse']:
        # for option in ['-n', '--name']:
            # rv, out = getstatusoutput(f'{prg} {option} {val}')
            # assert rv == 0
            # assert out.strip() == f'Hello, {val}!'

# --------------------------------------------------
# def test_person_has_fullname():
    # given
    # person = Person("Jack", "Smith")

    # when
    # fullname = person.fullname

    # then
    # assert fullname == "Jack Smith"
