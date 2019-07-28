"""
Code Smells:

-Comments - missing function description.
-Duplicated Code (maybe combinatorial explosion?) - both substitute blocks are very similar.
-Speculative Generality - perhaps they wrote so many steps to substitute because they may be thinking about future uses for the code?


Refactorings:

-Substitute Algorithm - After stepping through the code it appears the behavior in the test can be accomplished with the use of a built in Python string method
-Remove Dead Code - The test shows string inputs.  Based on this, there may be no need to set arguments as strings.  Added string requirements to ensure parameters are strings.
"""


def template(source_template: str, req_id: str):
    """
    Takes in a string template and a string id.  Returns the string template with specific sub-strings replaced by either the string id or an altered string id. 
    """

    # create altered string id
    alt_req_id = req_id[:5] + '-' + req_id[5:8]

    # find and replace designated sub-strings
    new_temp = source_template.replace("%CODE%", req_id)
    final_temp = new_temp.replace("%ALTCODE%", alt_req_id)

    return final_temp
