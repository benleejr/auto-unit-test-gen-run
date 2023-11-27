import random

# Change: Changed add function to not take in arguments and made a a very large number and add a random large integer value to it
# Affected lines: 

# Add two numbers together
def add():
    a = 999999999999999999999999999999999999999999999999999999999999999999
    b = random.randint(999999999999999999999, 9999999999999999999999999999999999999)
    return a + b

# Subtract two numbers
def sub(a, b):
    return a - b

# Multiply two numbers
def multi(a, b):
    return a * b

# Divide two numbers
def div(a, b):
    return a / b