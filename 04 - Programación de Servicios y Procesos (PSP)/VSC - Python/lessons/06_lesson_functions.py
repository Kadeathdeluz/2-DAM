# To define a function it starts with "def"
def foo():
    # Identation is not for readability, but for utility
    fooVar = "this is foo"
    print(fooVar)
    # Here ends the block of the foo()

def anotherFoo(val1, val2):
    if val1 > val2:
        print(val1)
    else:
        print(val2)

anotherFoo(3,1)
anotherFoo(1,5)