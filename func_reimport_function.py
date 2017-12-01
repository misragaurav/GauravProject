# -*- coding: utf-8 -*-
"""
Generic function to re-import custom functions. The problem this function solves is that once a function is imported, any changes 
made to the function in its file do not reflect in the imported function without either 1. restarting the kernel and running the code again
or 2. reimporting the function with the importlib module.
"""

def reimport_function(file_name_containing_function, function_name_in_file):
    import importlib
    import file_name_containing_function
    file_name_containing_function=importlib.import_module(file_name_containing_function)
    #file_name_containing_function=importlib.reload(file_name_containing_function)
    function_name_in_file=file_name_containing_function.function_name_in_file
    return function_name_in_file

