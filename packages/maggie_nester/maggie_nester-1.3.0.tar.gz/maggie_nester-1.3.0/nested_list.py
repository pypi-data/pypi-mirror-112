"""This module contains a function that will print the items individually from the list irrespective of its nested depth."""
def print_list(num_list ,indent = False, level = 0,fh=sys.stdout):
    """start of the function,A second argument called “level" is used to insert tab-stops when a nested list is encountered."""
    for each in num_list:
        if isinstance(each,list):
            print_list(each,indent,level+1,fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end = '',file=fh)
            print(each,file=fh)




