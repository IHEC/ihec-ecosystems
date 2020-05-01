#!/bin/bash






examples() {
	cd ..
	m="version_metadata"
    python -m $m -sample -out:$m/examples/samples.versioned.xml $m/examples/sample_1.0_1.1.xml -overwrite-outfile;
	python -m $m -sample -out:$m/examples/samples.versioned.xml $m/examples/samples.xml -overwrite-outfile; 
	python -m $m -sample -out:$m/examples/samples.with_one_invalid.versioned.xml $m/examples/samples.with_one_invalid.xml -overwrite-outfile ;
	python -m $m -sample -out:$m/examples/samples.with_multiple_valid_invalid.versioned.xml $m/examples/samples.with_multiple_valid_invalid.xml -overwrite-outfile ;
	python -m $m -experiment $m/examples/experiment.xml -out:$m/examples/experiment.validated.xml -overwrite-outfile ;
	python -m $m  -experiment $m/examples/experiment.some_invalid.xml -out:$m/examples/experiment.some_invalid.validated.xml -overwrite-outfile ; 
	cd -
}

examples 2>&1 
