#!/usr/bin/env python3

import re
from stack import Stack


class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):

    G0:
        F  ->  T  |  F+T  |  F-T
        T  ->  M  |  T*M  |  T/M
        M  -> (F) |   V
        V  ->  a  |   b   |   c   |  ...  |    z

    Gs:
        e  ->  e e + | e e - | e e * | e e / |
                     | a | b | ... | z
    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-z]
    """

    SYMBOLS = re.compile("[a-z]")

    def __init__(self):
        # Создание стека отложенных операций
        self.s = Stack()
        # Создание списка с результатом компиляции
        self.data = []
        self.flag = True
        self.string = ''

    def compile(self, str):
        self.data.clear()
        # Последовательный вызов для всех символов
        # взятой в скобки формулы метода process_symbol
        for c in "(" + str+')':
            if c == ')':
                self.flag = False
            self.process_symbol(c)
        for i in range(len(self.data)):
            self.data[i] = ''.join(self.data[i].split())
        return " ".join(self.data)

    # Обработка символа
    def process_symbol(self, c):
        if not self.flag:
            self.process_value(self.string)
            self.flag = True
            self.string = ''
            self.process_symbol(c)
            return None
        if c in 'IVXLCDM' and self.flag:
            self.string += c
        elif c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
           # self.data.append(c)
            self.flag = False
        else: self.process_value(c)
                
                
            

    # Обработка отложенных операций
    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    # Обработка имени переменной
    def process_value(self, c):
        if not self.flag and len(self.string) > 0: self.data.append(self.roman_to_hex(c))
        else:
             if c != '': self.data.append(c)

    # Обработка символа операции
    def process_oper(self, c):
        self.data.append(c)
    
    def roman_to_hex(self, roman):
        integers = dict(I=1, V=5, X=10, L=50, C=100, D=500, M=1000)
        result = 0
        for i in enumerate(roman):
            if i[0]+1<len(roman) and integers[roman[i[0]]] < integers[roman[i[0]+1]]:
                result-=integers[roman[i[0]]]
            else:
                result+=integers[roman[i[0]]]
        return hex(result)

    # Проверка допустимости символа
    @classmethod
    def check_symbol(self, c):
        if c in 'IVXLCDM': return None
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    # Определение приоритета операции
    @staticmethod
    def priority(c):
        return 1 

    # Определение отношения предшествования
    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


if __name__ == "__main__":
    c = Compf()
    while True:
        str = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(str)}")
        print()
