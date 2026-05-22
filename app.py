# LEGB --> ORDER OF VARIABLE SCOPE
# Local --> Enclosing --> Global --> Built-in
# local: variables defined within a function
# enclosing: variables defined in the outer function (if there is a nested function)
# global: variables defined at the top level of a module or script
# built-in: variables defined in the built-in namespace (e.g., print, len, etc.)

def outer():
    x = 5
    def inner():
        nonlocal x 
        # # nonlocal key word treats x as a variable from the outer scope, allowing us to modify it
        x += 1
        print(f"Inner: x = {x}")
    inner()
    print(f"Outer: x = {x}")

outer()