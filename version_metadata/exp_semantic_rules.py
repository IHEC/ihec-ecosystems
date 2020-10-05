verbose = True

def rule_miRNA_smRNA_strategy(attributes):
	""" {
		"applies" : ["rna-seq", "experiment_type"],
		"description" : "If 'experiment_type' is 'smRNA-Seq', then 'library_strategy' must be set to 'miRNA-Seq'"
		
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

def rule_chip_umi_read_structure(attributes):
	""" {
		"applies" : ["chip-seq", "experiment_type"],
		"description" : "If 'umi_enabled' is 'true', then 'umi_read_structure' must be valid"
	} """
	def read_struct_valid(struct):
		if struct is None: return False
		if not struct.strip(): return False
		else:
			return True
	if verbose:
		print('#__rule:', rule_chip_umi_read_structure.__name__,)
	
	if not attributes['experiment_type'] in ['ChIP-Seq']:
		if verbose: print('#__rule:', rule_chip_umi_read_structure.__name__, '__does_not_apply__') 
		return True
	else:
		print('#__rule:', rule_chip_umi_read_structure.__name__) 

	is_umi = attributes.get('umi_enabled')
	if not is_umi in ['true', 'false']:
		return False
	elif is_umi in  ["true"]:
		return read_struct(attributes.get("umi_read_structure"))
	else:
		return True
