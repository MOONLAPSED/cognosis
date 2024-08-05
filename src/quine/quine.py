def quine_generator():
    source_code = '''
def quine_generator():
    source_code = {}
    state = [{}]
    def quine():
        nonlocal state
        print(source_code.format(repr(source_code), repr(state)))
        return state
    return quine

quine = quine_generator()
state = quine()  # Output the source code and return the state
state[0] += 1  # Modify the state
print(state)  # Print the modified state
'''
    state = [0]
    def quine():
        nonlocal state
        print(source_code.format(repr(source_code), repr(state)))
        return state
    return quine

quine = quine_generator()
state = quine()  # Output the source code and return the state
state[0] += 1  # Modify the state
print(state)  # Print the modified state