def read_tok(string):
    string = string.strip()
    tok = string[0]

    if not tok.isdigit():
        return tok, string[1:]

    tok = ""

    while string and string[0].isdigit():
        tok += string[0]
        string = string[1:]

    return tok, string

operators = {"+": 1, "-": 1, "*": 2, "x": 2, "/": 2}

def gen_rpn(line):
    output, stack = [], []
    while line:
        tok, line = read_tok(line)
        if tok.isdigit():
            output.append(tok)
        elif tok in operators:
            while stack and stack[-1] in operators and \
                operators[tok] <= operators[stack[-1]]:
                output.append(stack.pop())
            stack.append(tok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else:
            print("unexpected token: %s" % tok)
    while stack:
        output.append(stack.pop())
    return output


def calculate_rpn(rpn):
    import operator
    functions = {"+": operator.add, "-": operator.sub, "*": operator.mul, "x": operator.mul, "/": operator.truediv}
    vals, fun_stack, len_stack = [], [], [0]
    for tok in reversed(rpn):
        if tok.isdigit():
            vals.append(int(tok))
            while len(vals) == len_stack[-1] + 2:
                len_stack.pop()
                vals.append(functions[fun_stack.pop()](vals.pop(), vals.pop()))
        else:
            fun_stack.append(tok)
            len_stack.append(len(vals))
    return vals[0]

for line in open("input.txt").read().splitlines():
    print(line, " ".join(gen_rpn(line)), calculate_rpn(gen_rpn(line)), sep="   |   ")