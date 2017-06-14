# def template(source_template, req_id):
    
#     template = str(source_template)

#     # Substitute for %CODE%
#     template_split_begin = template.index("%CODE%")
#     template_split_end = template_split_begin + 6
#     template_part_one = str(template[0:(template_split_begin)])
#     template_part_two = str(template[template_split_end:len(template)])
#     code = str(req_id)
#     template = str(template_part_one + code + template_part_two)

#     # Substitute for %ALTCODE%
#     template_split_begin = template.index("%ALTCODE%")
#     template_split_end = template_split_begin + 9
#     template_part_one = str(template[0:(template_split_begin)])
#     template_part_two = str(template[template_split_end:len(template)])
#     altcode = code[0:5] + "-" + code[5:8]
#     return template_part_one + altcode + template_part_two
  

def template(source_template, req_id):
    
    # Define variables
    template = str(source_template)
    pattern_1, pattern_2 = "%CODE%","%ALTCODE%"
    request_id = str(req_id)
    replace_1,replace_2 = request_id, request_id[0:5] + "-" + request_id[5:8]

    # Replace code
    template = template.replace(pattern_1,replace_1,1)

    # Replace altcode
    template = template.replace(pattern_2,replace_2,1)

    # Return
    return template


