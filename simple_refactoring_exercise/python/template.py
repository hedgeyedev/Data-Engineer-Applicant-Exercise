def template(source_template, req_id):
    
    template = str(source_template)

    #This replaces the substring "%CODE%" with req_id in source_template
    code = str(req_id)
    template = template.replace("%CODE%", code)

    # This replaces the substring "%ALTCODE%" with a modified req_id in source_template
    altcode = code[:5] + "-" + code[5:8]
    template = template.replace("%ALTCODE%", altcode)
    return template
  
