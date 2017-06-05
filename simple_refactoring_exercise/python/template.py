def template(source_template, req_id):
	import re
	template = str(source_template)

	## Substitute for %CODE%#
	code = str(req_id)
	template = re.sub("%CODE%",code,template)

	## Substitute for %ALTCODE%##
	altcode = code[0:5] + "-" + code[5:8]
	template = re.sub("%ALTCODE%", altcode, template)

	return template
  

# Using indices to locate the variables in the string is unnecessary and confusing to anyone reading the original code. 
# With the re.sub function, the %CODE% and %ALTCODE% variables can replace in only one line each.
# Not only does this look simpler to understand, it also involves fewer variable names and lines of code.
