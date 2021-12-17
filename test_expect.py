import pytest,pytest_check as check

class Test:
    def test_func(self):
        check.is_true(False,'error 1-1')
        check.is_true(False,'error 1-2')

    def test_func2(self):
        check.is_true(False,'error 2-1')
        check.is_true(True,'error 2-2')