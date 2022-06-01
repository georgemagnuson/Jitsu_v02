#!/usr/bin/env python3
"""tests for hello.py"""

import os
from subprocess import getstatusoutput, getoutput

prg = "./gmail_to_postgresql.py"


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
# def test_runnable():
#     """Runs using python3"""
#
#     out = getoutput(f"python3 {prg}")
#     assert out.strip() == "Hello, World!"
#
#
# # --------------------------------------------------
# def test_executable():
#     """Says 'Hello, World!' by default"""
#
#     out = getoutput(prg)
#     assert out.strip() == "Hello, World!"
#
#
# # --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python {prg} {flag}")
        assert rv == 0
        assert out.lower().startswith("usage")


# # --------------------------------------------------
# def test_input():
#     """test for input"""
#
#     for val in ["Universe", "Multiverse"]:
#         for option in ["-n", "--name"]:
#             rv, out = getstatusoutput(f"{prg} {option} {val}")
#             assert rv == 0
#             assert out.strip() == f"Hello, {val}!"

# --------------------------------------------------
def test_input():
    """test for input"""

    for option in ["-t", "--test"]:
        rv, out = getstatusoutput(f"python {prg} {option}")
        print(f"rv  = {rv}")
        print(f"out = {out}")
        output_lines = out.splitlines()
        assert "INFO     test mode - non-destructive on" in output_lines[2]
        # the third line says "INFO test mode -non-destructive on"
        # the last line says "INFO done."
