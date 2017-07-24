def template(source_template, req_id):

    # refactor variable name (since its the same name as function)
    templates = str(source_template)

    # Substitute for %CODE%
    template_split_begin = templates.index("%CODE%")
    template_split_end = template_split_begin + 6
    # removed redundant parentheses
    template_part_one = str(templates[0:template_split_begin])
    template_part_two = str(templates[template_split_end:len(templates)])
    code = str(req_id)
    templates = str(template_part_one + code + template_part_two)

    # Substitute for %ALTCODE%
    template_split_begin = templates.index("%ALTCODE%")
    template_split_end = template_split_begin + 9
    # removed redundant parentheses
    template_part_one = str(templates[0:template_split_begin])
    template_part_two = str(templates[template_split_end:len(templates)])
    altcode = code[0:5] + "-" + code[5:8]
    return template_part_one + altcode + template_part_two
