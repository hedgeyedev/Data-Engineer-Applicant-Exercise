def template(source_template, req_id):
    template_str = str(source_template)

    # Substitute for %CODE%
    code = str(req_id)
    template_str = template_str.replace("%CODE%", code)

    # Substitute for %ALTCODE%
    altcode = code[0:5] + "-" + code[5:8]
    template_str = template_str.replace("%ALTCODE%", altcode)

    return template_str
