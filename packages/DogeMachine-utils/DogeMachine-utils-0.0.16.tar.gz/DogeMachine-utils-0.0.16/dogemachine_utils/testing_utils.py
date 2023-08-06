import warnings


def ignore_warnings(test_func):
    """
    Use a decorator to skip warnings in your unit tests.

    See the solution here for more details: https://stackoverflow.com/questions/26563711/disabling-python-3-2-resourcewarning#answer-26620811
    :param test_func:
    :return:
    """
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warning_type = kwargs.get("warning_type", ResourceWarning)
            warnings.simplefilter("ignore", warning_type)
            test_func(self, *args, **kwargs)
    return do_test
