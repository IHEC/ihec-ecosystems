from . import validate_ontology

def rule_valid_disease_ontology_curie(attr):
	""" {
        "applies" : ["disease_ontology_curie"],
        "description" : "'disease_ontology_curie' attributes must validate"
	} """
	if not "disease_ontology_curie" in attr: return True
	else:
		return validate_ontology.check_term(attr["disease_ontology_curie"], "disease_ontology_curie")
	

def rule_valid_donor_health_status_ontology_curie(attr):
	""" {
        "applies" : ["donor_health_status_ontology_curie"],
        "description" : "'donor_health_status_ontology_curie' attributes must validate"
	} """
	if not "donor_health_status_ontology_curie" in attr: return True
	else:
		return validate_ontology.check_term(attr["donor_health_status_ontology_curie"], "donor_health_status_ontology_curie")
	

def rule_valid_experiment_ontology_curie(attr):
	""" {
        "applies" : ["experiment_ontology_curie"],
        "description" : "'experiment_ontology_curie' attributes must validate"
	} """
	if not "experiment_ontology_curie" in attr: return True
	else:
		return validate_ontology.check_term(attr["experiment_ontology_curie"], "experiment_ontology_curie")
	

def rule_valid_molecule_ontology_curie(attr):
	""" {
        "applies" : ["molecule_ontology_curie"],
        "description" : "'molecule_ontology_curie' attributes must validate"
	} """
	if not "molecule_ontology_curie" in attr: return True
	else:
		return validate_ontology.check_term(attr["molecule_ontology_curie"], "molecule_ontology_curie")
	

def rule_valid_origin_sample_ontology_curie(attr):
	""" {
        "applies" : ["origin_sample_ontology_curie"],
        "description" : "'origin_sample_ontology_curie' attributes must validate"
	} """
	if not "origin_sample_ontology_curie" in attr: return True
	else:
		return validate_ontology.check_term(attr["origin_sample_ontology_curie"], "origin_sample_ontology_curie")
	

def rule_valid_sample_ontology_curie(attr):
	""" {
        "applies" : ["sample_ontology_curie"],
        "description" : "'sample_ontology_curie' attributes must validate"
	} """
	if not "sample_ontology_curie" in attr: return True
	elif not "biomaterial_type" in attr: return False
	else:
		
		return validate_ontology.check_term(attr["sample_ontology_curie"], "sample_ontology_curie", attr['biomaterial_type'][0])
	
