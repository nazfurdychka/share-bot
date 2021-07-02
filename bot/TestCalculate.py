import unittest
from bot.utils.misc.additional_functions import calculate


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.buyers = dict()
        self.payers = dict()
        self.result = dict()

    def test_1(self):
        self.buyers = {'g': 100, 'f': 500, 'c': 1000, 'k': 200}
        self.payers = ['a', 's', 'd', 'f', 'g']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 360.0, 's': 360.0, 'd': 360.0, 'f': -140, 'g': 260.0, 'c': -1000, 'k': -200}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_2(self):
        self.buyers = {'zenyk': 700, 'marichka': 500}
        self.payers = ['petro', 'bodya', 'andriy', 'ivan', 'zenyk']
        self.amount = sum(self.buyers.values())
        self.result = {'petro': 240.0, 'bodya': 240.0, 'andriy': 240.0, 'ivan': 240.0, 'zenyk': -460, 'marichka': -500}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_3(self):
        self.buyers = {'z': 700, 'm': 500}
        self.payers = ['p', 'b', 'a', 'i', 'z', 'm']
        self.amount = sum(self.buyers.values())
        self.result = {'p': 200.0, 'b': 200.0, 'a': 200.0, 'i': 200.0, 'z': -500, 'm': -300}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_4(self):
        self.buyers = {'a': 10, 'b': 10, 'c': 10}
        self.payers = ['d', 'e', 'f', 'g', 'h']
        self.amount = sum(self.buyers.values())
        self.result = {'d': 6, 'e': 6, 'f': 6, 'g': 6, 'h': 6, 'a': -10, 'b': -10, 'c': -10}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_5(self):
        self.buyers = {'a': 10, 'b': 10, 'c': 10}
        self.payers = ['d', 'e', 'f', 'g', 'h', 'a']
        self.amount = sum(self.buyers.values())
        self.result = {'d': 5, 'e': 5, 'f': 5, 'g': 5, 'h': 5, 'a': -5, 'b': -10, 'c': -10}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_6(self):
        self.buyers = {'a': 10, 'b': 20, 'c': 30}
        self.payers = ['a', 'b', 'c']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 10, 'b': 0, 'c': -10}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_7(self):
        self.buyers = {'a': 15, 'b': 110, 'c': 25}
        self.payers = ['a', 'b', 'c', 'd', 'e']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 15, 'b': -80, 'c': 5, 'd': 30, 'e': 30}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_8(self):
        self.buyers = {'a': 200, 'b': 200, 'c': 100}
        self.payers = ['a', 'b', 'd', 'e', 'f']
        self.amount = sum(self.buyers.values())
        self.result = {'a': -100, 'b': -100, 'd': 100, 'e': 100, 'f': 100, 'c': -100}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)


if __name__ == '__main__':
    unittest.main()
