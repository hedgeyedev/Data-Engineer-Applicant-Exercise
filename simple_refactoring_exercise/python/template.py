def template(source_template, req_id):
    # Make sure the inputs are strings
    template = str(source_template)
    code = str(req_id)
    # Substitute for %CODE%
    # Subsitutes all occurances of %CODE%, assuming the original version had the undesirable behavior of only
    # substituting the first occurance. If this behavior is desirable, only the first occurance can be changed with template.replace("%CODE%",code,1)
    template = template.replace("%CODE%",code)

    # Substitute for %ALTCODE%
    altcode = code[0:5] + "-" + code[5:8]
    return template.replace("%ALTCODE%",altcode)