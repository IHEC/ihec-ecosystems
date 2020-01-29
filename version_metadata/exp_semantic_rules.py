verbose = True

def rule_miRNA_smRNA_strategy(attributes):
	""" {
		"rule" : "miRNA",
		"desc" : "If 'experiment_type' is 'smRNA-Seq', then 'library_strategy' must be set to 'miRNA-Seq'"
		
	}  """

	if verbose:
		print('#__rule:', rule_miRNA_smRNA_strategy.__name__,)

	try:
		miRNA_experiment_type =  attributes['experiment_type'] in ['smRNA-Seq']	
		miRNA_strategy = attributes['library_strategy'] in ['miRNA-Seq']
		validation_status = miRNA_strategy  if miRNA_experiment_type else not miRNA_strategy
		return validation_status
	except Exception as e:
		return False
