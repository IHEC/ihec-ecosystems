from . import exp_semantic_rules
from .utils import json2

def experiment_rules():
	return [e for e in dir(exp_semantic_rules) if e.startswith('rule_')]
	
def experiment_rule_desc(r):
	f = getattr(exp_semantic_rules, r)
	return json2.loads(f.__doc__)

def sample_rules():
	return []

def sample_rule_desc(r):
	return None

def rules(sid):
	assert sid in ['experiment', 'sample']
	if sid in ['experiment']:
		return experiment_rules()
	else:
		return sample_rules()
