

def already_in_list(searchfor, inlist):
    # find the part in the current import list
    for item in inlist:
        if item == searchfor:
            return True
    return False
