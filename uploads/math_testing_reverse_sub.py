# Change: Changed subtraction to reverse from default file a-b -> b-a, did so with a varible instead of returning immediately to try and trick gpt.
# Affected lines: 10, 11

# Add two numbers together
def add(a, b):
    return a + b

# Subtract two numbers
def sub(a, b):
    temp = b - a
    return temp

# Multiply two numbers
def multi(a, b):
    return a * b

# Divide two numbers
def div(a, b):
    return a / b