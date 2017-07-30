#I initiated all of the variables in the beginning of the function an created new variable names instead of redefining any and rearranged the layout of the function so it'd be easier to follow
#I passed in four new arguments for the function and defined them in the class since they could be used for future functions
#I also replaced all of the numbers with either 'len()' or 'index()' since they can change and you don't want to go back and change the number every time
#Some of the variable names were misleading so I changed them to avoid confusion

def template(source_template, req_id, START, END, str1, str2):
    
    #arguments
    templateStr = str(source_template)
    req = str(req_id)
    
    #string splits
    template_split_one = templateStr.index(str1)
    template_split_two = template_split_one + len(str1)
    template_split_three = templateStr.index(str2)
    
    #string parts
    template_part_one = str(templateStr[:(template_split_one)])
    template_part_two = str(templateStr[template_split_two:template_split_three])
    template_part_three = req[:START] + "-" + req[START:END]
    
    return template_part_one + req_id + template_part_two + template_part_three
  

