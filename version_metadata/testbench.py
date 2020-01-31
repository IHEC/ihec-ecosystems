import os


def testbench():
	tests = [
    'python  __main__.py -sample -out:./examples/samples.versioned.xml ./examples/samples.xml -overwrite-outfile',
    'python __main__.py -sample -out:./examples/samples.with_one_invalid.versioned.xml ./examples/samples.with_one_invalid.xml -overwrite-outfile',
    'python __main__.py -sample -out:./examples/samples.with_multiple_valid_invalid.versioned.xml ./examples/samples.with_multiple_valid_invalid.xml -overwrite-outfile',
    'python  __main__.py -experiment ./examples/experiment.xml -out:examples/experiment.validated.xml -overwrite-outfile',
    'python __main__.py -experiment ./examples/experiment.some_invalid.xml -out:examples/experiment.some_invalid.validated.xml -overwrite-outfile']
	for t in tests:
		os.system(t)



if __name__ == '__main__':
	testbench()



