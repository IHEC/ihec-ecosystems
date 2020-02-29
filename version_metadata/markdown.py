


def std_exp(e):
	names =	{
	  "chromatin_accessibility": "Chromatin Accessibility",
	  "bisulfite-seq": "Bisulfite Seq",
	  "medip-seq": "MeDIP-Seq",
	  "mre-seq": "MRE-Seq",
	  "chip-seq": "ChIP-Seq",
	  "rna-seq": "RNA-Seq",
	  "wgs": "WGS",
	  "other": "Other"
	}
	return names[e]


def markdown(classification, schema, constraints, sid):
	def mk_strong(x):
		return '<strong>{0}</strong>'.format(x)

	def entry(k, record, constraints):
		required = k in constraints.required
		rules =  constraints.rules.get(k, []) 
			
		m = "{0}:{1}".format( mk_strong(k.upper()), record["description"])
		if not m[-1] == '.': m = m  + '.'
		
		desc = [m, ' This attribute is <strong>required</strong>.'] if required else [m]
		
		if record["enum"]: 
			desc.append( "Allowed values are: {0}.".format(", ".join( ['"{0}"'.format(e) for e in sorted(record["enum"])]  )))
		
		try:
			num = "At most {0} instance(s) are allowed.".format(record["maxItems"] - record["minItems"] + 1)
			desc.append(num)
		except Exception as err:
			pass

		if rules:
			desc.append("\n\n * " + "\n * ".join(rules))
		
		return ' '.join(desc)

	dependencies = constraints.dependencies
	

	if sid in ['experiment']:
		md = ['\n\n## {0} \n\nThe metadata specification for {0} experiments is as defined below.'.format(std_exp(classification))]
	elif sid in ['sample']:
		md = ['\n\n## {0} \n\nThe metadata specification for {0} samples is as defined below.'.format(classification)]
	else:
		raise Exception(sid)

	if dependencies:
		md.append('Additionally, the metadata must also satify requirements for following specifications: {0}'.format(','.join([mk_strong(e) for e in dependencies ])))
	
	for k in sorted(schema.keys()):
		#md.append("\n__{0}__\n".format(k))
		md.append(entry(k, schema[k], constraints))
	
	return '\n\n'.join(md) #.replace()
