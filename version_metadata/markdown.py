


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



def markdown(classification, schema, ruleshash):
	def entry(k, record, rules):
		m = "<strong>{0}</strong>:{1}".format(k.upper(), record["description"])
		if not m[-1] == '.': m = m  + '.'
		if record["enum"]: m + " " + "Allowed values are: {0}.".format(", ".join( ['"{0}"'.format(e) for e in sorted(record["enum"])]  ))
		try:
			num = "At most {0} instance(s) are allowed.".format(record["maxItems"] - record["minItems"] + 1)
		except Exception as err:
			num = ""
		if num: m = m + " " + num
		if rules:
			print(rules, 'YYYY')
			m = m + "\n\n * " + "\n * ".join(rules)
		
		return m

	md = ['\n\n## {0} \n\nThe metadata specifictaion for {0} experiments is as defined below'.format(std_exp(classification))]
	for k in sorted(schema.keys()):
		#md.append("\n__{0}__\n".format(k))
		md.append(entry(k, schema[k], ruleshash.get(k, [])))
	return '\n\n'.join(md) #.replace()
