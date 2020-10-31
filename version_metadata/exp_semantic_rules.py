import re

verbose = True


class UMIValidator:
	def __init__(self):
		self.umi_regex= re.compile('((\d+)(T|B|M|S))+')
	def __call__(self, term):
		# http://fulcrumgenomics.github.io/fgbio/tools/latest/ExtractUmisFromBam.html
		term = term.strip()
		if len(term) == 0: return False
		
		if not term[-1] in 'TBMS': return False
		
		term2 = term.split('+')[0]
		if not len(term2) in [len(term)-2, len(term)]: return False
		
		matched = self.umi_regex.match(term2)
		if not matched: return False
		(start, end) = matched.span()
		return end == len(term2) and start == 0
	def tests():
		umi = UMIValidator()
		good = '3M2S75T'
		good2 =  '3M2S+T'
		assert umi(good)
		assert umi(good2)
		assert not umi("")
		assert not umi("A"+ good)
		assert not umi(good + "A")
		assert not umi("3M2S++T")
		return True

umi_validator = UMIValidator()

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
			return umi_validator(struct)
	
	if not attributes['experiment_type'] in ['ChIP-Seq']:
		if verbose: print('#__rule:', rule_chip_umi_read_structure.__name__, '__does_not_apply__') 
		return True
	elif verbose:
		print('#__rule:', rule_chip_umi_read_structure.__name__) 

	is_umi = attributes.get('umi_enabled')
	if not is_umi in ['true', 'false']:
		return False
	elif is_umi in  ["true"]:
		return read_struct(attributes.get("umi_read_structure"))
	else:
		return True


if __name__ == "__main__":
	print("__umi_tests_ok__", UMIValidator.tests())
