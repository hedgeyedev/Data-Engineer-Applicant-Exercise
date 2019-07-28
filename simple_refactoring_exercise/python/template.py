def template(source_template, req_id):
    
    template = str(source_template)
    print('template:', template)
    
    # Substitute for %CODE%
    #Finds and matches the beginning index for the string argument 
    #returns an integer 
    template_split_begin = template.index("%CODE%")
    print('template_split_begin:', template_split_begin)

    #template split end simply adds the length of the string in the index 
    # and sets it as the end of the template split
    template_split_end = template_split_begin + 6
    print('template_split_end:', template_split_end)

    #slice from beginning of template string to index position before %CODE% string
    template_part_one = str(template[0:(template_split_begin)])
    print('template_part_one:', template_part_one)

    #slice from index position after %CODE% string to end of the template string
    template_part_two = str(template[template_split_end:len(template)])
    print('template_part_two:', template_part_two)

    #set code to be modified
    code = str(req_id)
    print('code:', code)

    #reinitialize the template with template part_one, code and template part two
    template = str(template_part_one + code + template_part_two)
    print('template:', template)

    print()
    print('#################################')
    print()
    print('Subtitute part 2')
    print()
    print('#################################')
    print()
    # Substitute for %ALTCODE%
    #find index start for %ALTCODE% string, we'll insert our modified code string in that index
    #we are now working on the second part of the template string
    template_split_begin = template.index("%ALTCODE%")
    print('template_split_begin:', template_split_begin)

    #set template split end index to template begin plust the length of %ALTCODE% string
    template_split_end = template_split_begin + 9
    print('template_split_end:', template_split_end)


    #slice from beginning of template string to index position before %ALTCODE% string
    template_part_one = str(template[0:(template_split_begin)])
    print('template_part_one:', template_part_one)

    #slice from index position after %ALTCODE% string to end of the template string
    template_part_two = str(template[template_split_end:len(template)])
    print('template_part_two:', template_part_two)


    #modify code
    altcode = code[0:5] + "-" + code[5:8]
    print('altcode:', altcode)


    print('This gets returned:', template_part_one + altcode + template_part_two)

    #put it all back together
    return template_part_one + altcode + template_part_two



'''
Notes on refactoring template
------------------------------

My understanding of the program is to replace characters within a string to a req_id
and also to replace other characters within a string to another, modified version of the req_id.

Python provides an easy replace utility in the standard library so I implemented that. 
I also modified the API to allow the user to provide the terms they would like to replace. 

Now, given a string, the function will replace the value `term1` with `req_id` and will 
replace `term2` with a modified version of `req_id`.

The current implementation will update any number of instances of `term1` and `term2` with the req_id and its modified form.
The original implementation had limited utility was not sufficiently general to include strings of any length 
or strings with multple instances of the terms to be replaced. 

'''
    


def template_refactor(source_template, term1, term2, req_id):
    '''
    Replaces instances of term1 and term2 within source 
    template with req_id and a modified version of req_id


    Parameters
    ==========
    source_template: str
    term1: str
    term2:str
    req_id: int

    Returns
    =======
    str

    '''

    code = str(req_id)
    alt_code = code[0:5] + "-" + code[5:8]
    
    return source_template.replace(term1, code).replace(term2, alt_code)



  

