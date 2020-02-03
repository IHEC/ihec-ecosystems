def markdown(classification, schema, ruleshash):
	def entry(k, record, rules):
		m = "<strong>{0}</strong>:{1}".format(k.upper(), record["description"])
		try:
			num = "At most {0} instance(s) are allowed.".format(record["maxItems"] - record["minItems"] + 1)
		except Exception as err:
			num = ""
		if num: m = m + " " + num
		if rules:
			return m + "\n * " + "\n * ".join(rules)
		else:
			return m

	md = ['\n\n## {0} \n\nThe metadata specifictaion for {0} experiments is as defined below'.format(classification)]
	for k in sorted(schema.keys()):
		#md.append("\n__{0}__\n".format(k))
		md.append(entry(k, schema[k], ruleshash.get(k, [])))
	return '\n\n'.join(md) #.replace()
