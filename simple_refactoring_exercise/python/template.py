def template(source_template, req_id):
    
    template = str(source_template)

    # Substitute for %CODE%
    code = str(req_id)
    template = template.replace("%CODE%", code)

    # Substitute for %ALTCODE%
    altcode = code[0:5] + "-" + code[5:8]
    template = template.replace("%ALTCODE%", altcode)

    return template


'''
One thing I noticed was the ignoring of standard library methods,
    such as manually creating split versions of the string, 
    when there exits the .split() method.
I initially thought of using .split() with .join(), for example:
    template = (code).join(template.split("%CODE%"))
But decided that .replace() was straightforward, used less code, 
    and tells the reader exactly what it's doing.

I also removed the redundant/repititive use of str()
'''