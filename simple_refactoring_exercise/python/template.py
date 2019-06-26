def template(source_template, req_id):
    
    template = str(source_template)
    
    def parts(temp):
        return str(temp[0:(template_split_begin)]), str(temp[template_split_end:len(temp)])

    
    # Substitute for %CODE%
    template_split_begin = template.index("%CODE%")
    template_split_end = template_split_begin + 6
    part1,part2 = parts(template)
    code = str(req_id)
    template = str(part1 + code + part2)

    # Substitute for %ALTCODE%
    template_split_begin = template.index("%ALTCODE%")
    template_split_begin = template.index('%ALTCODE%')
    template_split_end = template_split_begin + 9
    part1,part2 = parts(template)
    altcode = code[0:5] + "-" + code[5:8]
    return part1 + altcode + part2
  

