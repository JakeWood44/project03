from pair import *
from operator import add, sub, mul, truediv

def tokenize(expression):
    expression = expression.replace("(", "( ")
    expression = expression.replace(")", " )")

    return expression.split()

def parse_tokens(tokens, i):
    if tokens[i] == "(":
        op = tokens[i + 1]

        if i != 0:
            new_tokens = parse_tokens(tokens, i + 2)[0]
            i = parse_tokens(tokens, i + 2)[1]

            op = Pair(op, new_tokens)

        else:
            i += 2

        recurse = parse_tokens(tokens, i)
        i = recurse[1]

        return Pair(op, recurse[0]), i

    elif tokens[i] == ")":
        return nil, i + 1

    else:
        try:
            if "." in tokens[i]:
                num = float(tokens[i])
            else:
                num = int(tokens[i])

            new_pairs, i = parse_tokens(tokens, i + 1)
            return Pair(num, new_pairs), i

        except:
            raise TypeError("wrong type")

def parse(expression):
    return parse_tokens(expression, 0)[0]

def reduce(func, operands, initial):
    if not isinstance(operands, Pair):
        return initial
    if isinstance(operands, Pair):
        return reduce(func, operands.rest, func(initial, operands.first))

def apply(operator, operands):
    if operator == "+":
        return reduce(add, operands, 0)
    if operator == "-":
        return reduce(sub, operands.rest, operands.first)
    if operator == "*":
        return reduce(mul, operands, 1)
    if operator == "/":
        return reduce(truediv, operands.rest, operands.first)

    raise TypeError("unknown operator")

def eval(syntax_tree):
    if isinstance(syntax_tree, int) or isinstance(syntax_tree, float) or syntax_tree == nil:
        return syntax_tree

    if isinstance(syntax_tree, Pair):
        if isinstance(syntax_tree.first, int) or isinstance(syntax_tree.first, float):
            return Pair(syntax_tree.first, eval(syntax_tree.rest))

        if isinstance(syntax_tree.first, Pair):
            return Pair(eval(syntax_tree.first), eval(syntax_tree.rest))

        if isinstance(syntax_tree.first, str):
            return apply(syntax_tree.first, eval(syntax_tree.rest))

    print(syntax_tree, type(syntax_tree))
    raise TypeError("Not a pair or primitive")

def main():
    print("Welcome to the CS 111 Calculator Interpreter.")

    while True:
        expression = input("calc >> ")

        if expression == "exit":
            break

        try:
            expression = parse(tokenize(expression))

        except Exception as e:
            print(e)
            continue

        print(eval(expression))

    print("Goodbye!")

if __name__ == "__main__":
    main()