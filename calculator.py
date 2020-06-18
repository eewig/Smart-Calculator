# import re
from collections import deque


HELP = '''
-------------------------------------------------------------------
Smart Calculator
It supports addition(+), subtraction(-),
multiplication(*), division(/), power(^) operators,
variable definition (write a variable to return the value).
Variables can be defined only with latin letters.
Also calculator process brackets.

Examples:
>2+3
5
>a = 2
>a
2
>b= a
>b - a
0
>(1+2)*3-2^3
1
-------------------------------------------------------------------
'''

OPERATORS = ('+', '-', '*', '/', '(', ')', '^')


def command_handler(command):
    if command == '/exit':
        print('Bye!')
        quit()
    elif command == '/help':
        print(HELP)
    else:
        print('Unknown command')


class Calculator:

    def __init__(self):
        self.VARS = {}
        # self.expression = ''

    def start(self):
        while True:
            input_string = input()
            if input_string.strip() == '':
                continue
            elif input_string.startswith('/'):
                command_handler(input_string)
            elif '=' in input_string or input_string.strip().isalpha():
                self.variables(input_string)
            else:
                try:
                    expression = self.expression_reader(input_string)
                    postfix = self.infix_to_postfix(expression)
                    result = self.calculate_postfix(postfix)
                    print(result)
                except TypeError:
                    print('Invalid expression')

    def sign_checker(self, sign):
        if sign.find('--') != -1:
            sign = sign.replace('--', '+')
            return self.sign_checker(sign)
        elif sign.find('++') != -1:
            sign = sign.replace('++', '+')
            return self.sign_checker(sign)
        elif sign.find('-+') != -1:
            sign = sign.replace('-+', '-')
            return self.sign_checker(sign)
        elif sign.find('+-') != -1:
            sign = sign.replace('+-', '-')
            return self.sign_checker(sign)
        else:
            return sign

    def change_sings_in_list(self, sings_list):
        for i, val in enumerate(sings_list):
            sings_list[i] = self.sign_checker(val)

    def sum_values(self, values):
        values = values.split()
        result = int(values[0])
        self.change_sings_in_list(values)
        for i, val in enumerate(values):
            if i % 2 == 1:
                if i == len(values) - 1:
                    break
                if val == '+':
                    result += int(values[i + 1])
                elif val == '-':
                    result -= int(values[i + 1])
                else:
                    raise ValueError
        return result

    def sum_variables(self, values):
        values = values.split()
        if values[0].isdigit():
            result = int(values[0])
        else:
            try:
                result = int(self.VARS[values[0]])
            except KeyError:
                print('Unknown variable')
                return
        self.change_sings_in_list(values)
        for i, val in enumerate(values):
            if i % 2 == 1:
                if i == len(values) - 1:
                    break
                try:
                    if val == '+':
                        if values[i + 1].isdigit():
                            result += int(values[i + 1])
                        else:
                            result += int(self.VARS[values[i + 1]])
                    elif val == '-':
                        if values[i + 1].isdigit():
                            result -= int(values[i + 1])
                        else:
                            result -= int(self.VARS[values[i + 1]])
                    else:
                        raise ValueError
                except KeyError:
                    print('Unknown variable')
                    return
        return result

    def valid_identifier_check(self, identifier):
        identifier = identifier
        if identifier[0].isalpha() and \
                not any(char.isdigit() for char in identifier[1:]):
            return True
        return False

    def assignment(self, var_val):
        var_val = [var.strip() for var in var_val.split('=')]
        if len(var_val) > 2 or \
                (not self.valid_identifier_check(var_val[1]) and
                 not var_val[1].isdigit()):
            print('Invalid assignment')
            return
        if var_val[1].isdigit():
            self.VARS[var_val[0]] = var_val[1]
        elif var_val[1] in self.VARS:
            self.VARS[var_val[0]] = self.VARS[var_val[1]]
        elif var_val[0] not in self.VARS:
            print('Unknown variable')
            return

    def variables(self, input_val):
        var1 = [var.strip() for var in input_val.split('=')][0]
        if not self.valid_identifier_check(var1):
            print('Invalid identifier')
            return
        if '=' in input_val:
            self.assignment(input_val)
        else:
            try:
                print(self.VARS[input_val.strip()])
            except KeyError:
                print('Unknown variable')

    def infix_to_postfix(self, expression: list):
        stack = deque()
        result = []
        for value in expression:
            if isinstance(value, int):
                result.append(value)
            elif len(stack) == 0 or stack[-1] == '(':
                stack.append(value)
            elif ((value in ('*', '/', '^')) and
                  (stack[-1] in ('+', '-'))) or \
                    (value == '^' and stack[-1] in ('+', '-', '*', '/',)):
                stack.append(value)
            elif ((value in ('+', '-')) and
                  (stack[-1] in ('*', '/', '+', '-', '^'))) or \
                    ((value in ('*', '/')) and
                     (stack[-1] in ('*', '/', '^'))) or \
                    (value == '^' and stack[-1] == '^'):
                result.append(stack.pop())
                while len(stack) > 0 and \
                        (((value in ('-', '+')
                              and stack[-1] in ('*', '/', '^'))
                         or (value == '^' and stack in ('*', '/'))) or
                         not stack[-1] == '('):
                    result.append(stack.pop())
                stack.append(value)
            elif value == '(':
                stack.append(value)
            elif len(stack) > 0 and value == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    result.append(stack.pop())
                if len(stack) == 0:
                    return
                stack.pop()
        while len(stack) > 0:
            if stack[-1] == '(' or stack[-1] == ')':
                return
            result.append(stack.pop())
        return result

    # 10 + 1 * (1 + 2) - 5
    # 10 1 1 2 + * + 445 -      // +*

    def calculate_postfix(self, expression: list):
        stack = deque()
        for value in expression:
            if isinstance(value, int):
                stack.append(value)
            # elif value.isalpha():
            #     if value in self.VARS:
            #         stack.append(self.VARS[value])
            elif value == '+':
                stack.append(int(stack.pop()) + int(stack.pop()))
            elif value == '-':
                stack.append(-int(stack.pop()) + int(stack.pop()))
            elif value == '*':
                stack.append(int(stack.pop()) * int(stack.pop()))
            elif value == '/':
                stack.append(1 / int(stack.pop()) * int(stack.pop()))
            elif value == '^':
                power = int(stack.pop())
                stack.append(int(stack.pop()) ** power)
        return stack.pop()

    def expression_reader(self, expression):
        result = []
        i = 0
        while i < len(expression):
            if i == 0 and (
                    expression[i] == '-' or expression[i] == '+') and \
                    expression[i + 1].isdigit():
                value = expression[i]
                while i + 1 < len(expression) and \
                        expression[i + 1].isdigit():
                    i += 1
                    value += expression[i]
                result.append(int(value))
            elif expression[i].isdigit():
                value = expression[i]
                while i + 1 < len(expression) and \
                        expression[i + 1].isdigit():
                    i += 1
                    value += expression[i]
                result.append(int(value))
            elif expression[i] in OPERATORS:
                value = expression[i]
                if i + 1 < len(expression) and \
                        (value == '*' or value == '/') and \
                        (expression[i + 1] == '*' or expression[i + 1] == '/'):
                    return
                while i + 1 < len(expression) and \
                        (expression[i + 1] == '+' or
                         expression[i + 1] == '-'):
                    i += 1
                    value += expression[i]
                result.append(self.sign_checker(value))
            elif expression[i].isalpha():
                value = expression[i]
                while i + 1 < len(expression) and \
                        expression[i + 1].isalpha():
                    i += 1
                    value += expression[i]
                if value in self.VARS:
                    result.append(int(self.VARS[value]))
                else:
                    return
            i += 1
        return result


if __name__ == '__main__':
    calculator = Calculator()
    calculator.start()
