import pytest
import json
import os

#@pytest.mark.hookwrapper
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    x = yield
    x._result.max_score = getattr(item._obj, 'max_score', 0)
    x._result.visibility = getattr(item._obj, 'visibility', 'visible')

def pytest_terminal_summary(terminalreporter, exitstatus):
    json_results = {'tests': []}

    all_tests = []
    if ('passed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['passed']
    if ('failed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['failed']

    simulator = os.getenv('SIM').lower()
    for s in all_tests:
        output = ''
        score = s.max_score
        if (s.outcome == 'failed'):
            score = 0
            output = str(s.longrepr.chain[0][0].reprentries[0])
            output += str(s.caplog)
        if(s.max_score != 0):
            json_results["tests"].append(
                {
                    'score': score,
                    'max_score': s.max_score,
                    'name': s.location[0] + ":" + s.location[2] + " (" + simulator + ")",
                    'output': output,
                    'visibility': s.visibility
                }
            )

    with open('results.json', 'w') as results:
        results.write(json.dumps(json_results, indent=4))
