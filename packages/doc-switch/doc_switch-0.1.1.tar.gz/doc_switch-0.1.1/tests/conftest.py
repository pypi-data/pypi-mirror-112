import sys
import os

sys.path.insert(0, os.path.abspath("../doc_switch"))


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 5:
        session.exitstatus = 0
