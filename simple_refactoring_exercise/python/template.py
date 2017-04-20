def template(source_template, req_id):

    template = str(source_template)
    code = str(req_id)
    # Substitute for %CODE%
    template = template.replace("%CODE%",code)
    # Substitute for %ALTCODE%
    altcode = code[0:5] + "-" + code[5:8]
    return template.replace("%ALTCODE%",altcode)

'''
 There was duplication of using template_part_one and template_part_two.
 The logic was to replace %CODE% and %ALTCODE% with respective with he req-id.
 Instead of writing a manual calculation logic (+6,+9), we could use inbuilt
 function replace(str1,str2)- replaces all occurences of str1 with str2 to replace with the req_id
'''


