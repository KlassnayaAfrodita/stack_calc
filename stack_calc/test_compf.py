from compf import Compf


class TestCompf:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.c = Compf()

    # Формула из одного символа
    def test_one_symbol(self):
        assert self.c.compile("I") == "0x1"

    # Формулы с одной операцией
    def test_correct_operations1(self):
        assert self.c.compile("I+V") == "0x1 0x5 +"

    def test_correct_operations2(self):
        assert self.c.compile("I-V") == "0x1 0x5 -"

    def test_correct_operations3(self):
        assert self.c.compile("I*V") == "0x1 0x5 *"

    def test_correct_operations4(self):
        assert self.c.compile("I/V") == "0x1 0x5 /"

    # Тесты на порядок выполнения операций
    def test_operations_order1(self):
        assert self.c.compile("I+V*X") == "0x1 + 0x5 0xa *"

    def test_operations_order2(self):
        assert self.c.compile("I*V/X") == "0x1 * 0x5 0xa /"

    def test_operations_order3(self):
        assert self.c.compile("I+V-X") == "0x1 + 0x5 0xa -"


    # Тесты на использование скобок
    def test_parentheses1(self):
        assert self.c.compile("(I)") == "0x1"

    # def test_parentheses2(self):
    #     assert self.c.compile("(((((I))))") == "0x1"

    def test_parentheses2(self):
        assert self.c.compile("(((((I+V))))") == "0x1 0x5 +"

    def test_parentheses3(self):
        assert self.c.compile("(((((((I+V)*((I+V)))))))") == "0x1 0x5 + 0x1 0x5 + *"

    # Другие тесты
    def test_gl1(self):
        assert self.c.compile("XX") == "0x14"

    def test_gl2(self):
        assert self.c.compile("CX") == "0x6e"

    def test_gl3(self):
        assert self.c.compile("MCX-XC") == "0x456 0x5a -"

# a = TestCompf()
# a.setup_method()
# print(a.test_one_symbol())
# print(a.test_correct_operations1())
# print(a.test_correct_operations2())
# print(a.test_correct_operations3())
# print(a.test_correct_operations4())
# print(a.test_operations_order1())
# print(a.test_operations_order2())
# print(a.test_operations_order3())
# print(a.test_parentheses1())
# print(a.test_parentheses2())
# print(a.test_parentheses3())
# print(a.test_gl1())
# print(a.test_gl2())
# print(a.test_gl3())
c = Compf()
print(c.compile('(((((((I+V)*((I+V)))))))'))

