.PHONY: test test-20 test-21 test-22 test-23 test-24 test-2-1 test-2-2 test-2-3 test-2-4 test-2-5 test-2-6 test-2-7 test-2-8 test-2-9 test-2-10 test-3-1 test-3-2 test-3-3 test-3-4 test-3-5 test-3-6 test-4-1 test-4-2 test-4-3 test-4-4 test-4-5 test-4-6 test-4-7 test-4-8 test-4-10 test-4-11 test-4-12 test-4-13 test-4-14 test-5-1 test-5-2 test-5-3 test-5-4 test-5-5 test-5-6 test-5-7 test-5-8 test-5-9 test-5-10 test-5-11 test-5-12

test:
	python3 tests/helpers/run_tests.py

test-20:
	python3 tests/helpers/run_tests.py 20

test-21:
	python3 tests/helpers/run_tests.py 21

test-22:
	python3 tests/helpers/run_tests.py 22

test-23:
	python3 tests/helpers/run_tests.py 23

test-24:
	python3 tests/helpers/run_tests.py 24

test-2-1:
	python3 tests/helpers/run_tests.py 2-1

test-2-2:
	python3 tests/helpers/run_tests.py 2-2

test-2-3:
	python3 tests/helpers/run_tests.py 2-3

test-2-4:
	python3 tests/helpers/run_tests.py 2-4

test-2-5:
	python3 tests/helpers/run_tests.py 2-5

test-2-6:
	python3 tests/helpers/run_tests.py 2-6

test-2-7:
	python3 tests/helpers/run_tests.py 2-7

test-2-8:
	python3 tests/helpers/run_tests.py 2-8

test-2-9:
	python3 tests/helpers/run_tests.py 2-9

test-2-10:
	python3 tests/helpers/run_tests.py 2-10

test-3-1:
	python3 tests/helpers/run_tests.py 3-1

test-3-2:
	python3 tests/helpers/run_tests.py 3-2

test-3-3:
	python3 tests/helpers/run_tests.py 3-3

test-3-4:
	python3 tests/helpers/run_tests.py 3-4

test-3-5:
	python3 tests/helpers/run_tests.py 3-5

test-3-6:
	python3 tests/helpers/run_tests.py 3-6

test-4-1:
	python3 tests/helpers/run_tests.py 4-1

test-4-2:
	python3 tests/helpers/run_tests.py 4-2

test-4-3:
	python3 tests/helpers/run_tests.py 4-3

test-4-4:
	python3 tests/helpers/run_tests.py 4-4

test-4-5:
	python3 tests/helpers/run_tests.py 4-5

test-4-6:
	python3 tests/helpers/run_tests.py 4-6

test-4-7:
	python3 tests/helpers/run_tests.py 4-7

test-4-8:
	python3 tests/helpers/run_tests.py 4-8

test-4-10:
	python3 tests/helpers/run_tests.py 4-10

test-4-11:
	python3 tests/helpers/run_tests.py 4-11

test-4-12:
	python3 tests/helpers/run_tests.py 4-12

test-4-13:
	python3 tests/helpers/run_tests.py 4-13

test-4-14:
	python3 tests/helpers/run_tests.py 4-14

test-5-1:
	python3 tests/helpers/run_tests.py 5-1

test-5-2:
	python3 tests/helpers/run_tests.py 5-2

test-5-3:
	python3 tests/helpers/run_tests.py 5-3

test-5-4:
	python3 tests/helpers/run_tests.py 5-4

test-5-5:
	python3 tests/helpers/run_tests.py 5-5

test-5-5-%:
	python3 tests/helpers/run_tests.py 5-5 $*

test-5-6:
	python3 tests/helpers/run_tests.py 5-6

test-5-6-%:
	python3 tests/helpers/run_tests.py 5-6 $*

test-5-7:
	python3 tests/helpers/run_tests.py 5-7

test-5-8:
	python3 tests/helpers/run_tests.py 5-8

test-5-9:
	python3 tests/helpers/run_tests.py 5-9

test-5-10:
	python3 tests/helpers/run_tests.py 5-10

test-5-11:
	python3 tests/helpers/run_tests.py 5-11

test-5-11-%:
	python3 tests/helpers/run_tests.py 5-11 $*

test-5-12:
	python3 tests/helpers/run_tests.py 5-12

test-5-12-%:
	python3 tests/helpers/run_tests.py 5-12 $*
