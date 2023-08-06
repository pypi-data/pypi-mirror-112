from pprint import pprint
import traceback


log_counter = 0

def log(
    message, 
    exception=None,
    prefix=             '[{}]\n |\tLOG FROM:\t"{}"\n |\t########:\t', 
    error_log_prefix=   '[{}]\n |\tERROR FROM:\t"{}"\n |\t##########:\t'
):
    global log_counter
    if not message: message = "<no-message>"
    log_counter += 1
    message = str(message)
    
    if exception: # error logging
        message = error_log_prefix.format(log_counter, __file__) + message
        print("\n  ________________________")
        print(" /------------------------\\________________________")
        print(message)
        print(" \\------------------------/")
        print(' |----- traceback: -------\\________________________')
        traceback.print_tb(exception.__traceback__)
        print(" |_________________________________________________|\n")
    else: # regular logging
        message = prefix.format(log_counter, __file__) + message
        print("\n  ________________________")
        print(" /------------------------\\________________________")
        print(message)
        print(" \\------------------------/\n")

        