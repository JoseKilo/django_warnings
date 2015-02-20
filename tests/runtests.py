from flake8.engine import get_style_guide
from flake8.main import DEFAULT_CONFIG, print_report


def flake8():
    flake8_style = get_style_guide(parse_argv=True, config_file=DEFAULT_CONFIG)
    report = flake8_style.check_files()
    if report.total_errors > 0:
        print_report(report, flake8_style)
    return report.total_errors


def nose():
    from django_nose.runner import NoseTestSuiteRunner
    test_runner = NoseTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(['-s', 'tests', '--with-yanc'])
    return failures
