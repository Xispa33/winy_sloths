import os
try:
    import coverage
    os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'
    coverage.process_startup()
except ImportError:
    pass