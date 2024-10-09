# You can define global or local variables as it follows:
# This is a global variable (outside a function)
globalVariable = 0
# This is also a global
anotherGlobVar = 1

def foo():
    # This indicates that we are using the global globalVariable (and not a local variable called "globalVariable")
    global globalVariable
    # This updates the globalVariable value to 10
    globalVariable = 10
    # This is not our global, but a local variable called "anotherGlobVar"
    anotherGlobVar = 5
    # Finally we print both variables to see what happens
    print("globalVariable = ", globalVariable, ", anotherGlobVar(local) = ", anotherGlobVar)

# Let's see the difference:
print("Globals at the beginning -> ")
print("globalVariable = ", globalVariable, ", anotherGlobVar = ", anotherGlobVar)
print("Globals inside of foo() -> ")
foo()
print("Globals after foo() called -> ")
print("globalVariable = ", globalVariable, ", anotherGlobVar = ", anotherGlobVar)
# As you can see, globalVariable keeps its value (10) after foo, but anotherGlobVar don't. That's because anotherGlovBar inside foo() it's a local variable and not our anotherGlobVar (global)