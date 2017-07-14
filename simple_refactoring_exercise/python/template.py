def template(source_template, req_id):
	source = source_template
	source = replaceCODE(source,req_id)
	source = replaceALTCODE(source,req_id)
	return source
	
def replaceCODE(s,req_id):
	s = s.replace("%CODE%",req_id)
	return s
	
def replaceALTCODE(s,req_id):
	altcode = req_id[0:5] + "-" + req_id[5:8]
	s = s.replace("%ALTCODE%",altcode)
	return s

# Notes:
#
# def template(source_template, req_id):										1. Large method
#
# 	template = str(source_template)												2. Casting string when already is a string
#
# 	#Substitute for %CODE%
# 	template_split_begin = template.index("%CODE%")
# 	template_split_end = template_split_begin + 6								3. Man in the middle
# 	template_part_one = str(template[0:(template_split_begin)])
# 	template_part_two = str(template[template_split_end:len(template)])
# 	code = str(req_id)
# 	template = str(template_part_one + code + template_part_two)
#
# 	#Substitute for %ALTCODE%
# 	template_split_begin = template.index("%ALTCODE%")
# 	template_split_end = template_split_begin + 9
# 	template_part_one = str(template[0:(template_split_begin)])
# 	template_part_two = str(template[template_split_end:len(template)])
# 	altcode = code[0:5] + "-" + code[5:8]
# 	return template_part_one + altcode + template_part_two
#
# CODE SMELLS
#
# The first code smell is how big the method is. The obvious first refactoring would be 
# to split the giant method into two methods: replaceCODE and replaceALTCODE.
#
# The next small code smell is casting the input as strings when they were already strings to begin with.
#
# Once we split the method into two smaller methods we can see that most of the lines can be replaced
# very easily by using str.replace() method. This is the man in the middle smell. Instead of having
# several variables, I can replace them with just one variable.
# 
# The final smell that I detected was just the variable names. Personally, I wouldn't name a variable
# the same name as the method as it's a part of.
