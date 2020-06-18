import unittest
from .calculator import Calculator


class TestCalculator(unittest.TestCase):
    def test_sign_checker1(self):
        calc = Calculator()
        signs = [
            '--', '-----', '+++++', '-+++++', '+++-', '----'
        ]
        result = (
            '+', '-', '+', '-', '-', '+'
        )
        for i in range(len(signs)):
            signs[i] = calc.sign_checker(signs[i])
        self.assertEqual(tuple(signs), result)

    def test_sum_values1(self):
        calc = Calculator()
        result = calc.sum_values('1 + 2 -- 3')
        self.assertEqual(result, 6)

    def test_sum_values2(self):
        calc = Calculator()
        result = calc.sum_values('100 + 200 - 300')
        self.assertEqual(result, 0)

    def test_assigments(self):
        calc = Calculator()
        calc.assignment('a = 10')
        calc.assignment('b       = 1')
        calc.assignment('c =   b')
        self.assertEqual(calc.VARS, {'a': '10', 'b': '1', 'c': '1'})

    def test_variables_sum(self):
        calc = Calculator()
        calc.assignment('a = 10')
        calc.assignment('b = 5')
        calc.assignment('c = 10')
        result = calc.sum_variables('a + b - 5 - c')
        self.assertEqual(result, 0)

    def test_calculate_postfix(self):
        calc = Calculator()
        result = calc.calculate_postfix(
            [10, 2, 8, '*', '+', 3, '-'])
        self.assertEqual(result, 23)

    def test_infix_to_postfix1(self):
        calc = Calculator()
        result = calc.infix_to_postfix(
            [10, '+', 1, '*', '(', 1, '+', 2, ')', '-', 5])
        self.assertEqual(result,
                         [10, 1, 1, 2, '+', '*', '+', 5, '-'])

    def test_infix_to_postfix2(self):
        calc = Calculator()
        result = calc.infix_to_postfix(
            [8, '*', 3, '+', 12, '*', '(', 4, '-', 2, ')']
        )
        self.assertEqual(result,
                         [8, 3, '*', 12, 4, 2, '-', '*', '+'])

    def test_calculate_infix_expression_to_postfix(self):
        calc = Calculator()
        expression_list = calc.expression_reader('1 +++ 2 * 3 -- 4')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, 11)

    def test_calculate_infix_expression_to_postfix_with_variables(self):
        calc = Calculator()
        calc.assignment('a=4')
        calc.assignment('b=5')
        calc.assignment('c=6')
        expression_list = calc.expression_reader('a*2+b*3+c*(2+3)')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, 53)

    def test_minus_digit_calculation(self):
        calc = Calculator()
        expression_list = calc.expression_reader('-10+12-2')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, 0)

    def test_bug1(self):
        '''bug1
        ((3 * 4 - 3) ^ 2) / 3
        Invalid expression'''
        calc = Calculator()
        expression_list = calc.expression_reader('((3 * 4 - 3) ^ 2) / 3')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, 27)

    def test_power_bug1(self):
        '''
        15^2-11^2
        121
        '''
        calc = Calculator()
        expression_list = calc.expression_reader('15^2-11^2')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, 104)

    def test_power_bug2(self):
        '''
        34^6-23^7
        3404825447
        '''
        calc = Calculator()
        expression_list = calc.expression_reader('34^6-23^7')
        postfix_expression = calc.infix_to_postfix(expression_list)
        result = calc.calculate_postfix(postfix_expression)
        self.assertEqual(result, -1_860_021_031)


if __name__ == '__main__':
    unittest.main()
