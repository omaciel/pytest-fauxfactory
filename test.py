import os
import subprocess


os.environ['COVERAGE_PROCESS_START'] = ".coveragerc"


def test_via_subproc():
    proc = subprocess.Popen(["pytest", "-v", "-n", "auto"])
    proc.wait()
