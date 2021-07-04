import unittest
from bot.utils.misc.additional_functions import calculate


class CalculateTest(unittest.TestCase):
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

    def test_9(self):
        self.buyers = {'a': 600, 'b': 500}
        self.payers = ['c', 'd', 'e', 'f', 'g']
        self.amount = sum(self.buyers.values())
        self.result = {'a': -600.0, 'b': -500.0, 'd': 220.0, 'f': 220.0, 'g': 220.0, 'c': 220.0, 'e': 220.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_10(self):
        self.buyers = {'d': 40, 'e': 35, 'g': 15}
        self.payers = ['a', 'b', 'd', 'e']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 22.5, 'b': 22.5, 'd': -17.5, 'e': -12.5, 'g': -15}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_11(self):
        self.buyers = {'y': 900, 'z': 3}
        self.payers = ['a', 'b', 'z']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 301.0, 'b': 301.0, 'y': -900.0, 'z': 298.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_12(self):
        self.buyers = {'i': 20, 'j': 30, 'k': 40}
        self.payers = ['x', 'y', 'k']
        self.amount = sum(self.buyers.values())
        self.result = {'i': -20.0, 'j': -30.0, 'k': -10.0, 'x': 30.0, 'y': 30.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_13(self):
        self.buyers = {'k': 10, "l": 6, "m": 2, "n": 50}
        self.payers = ['k', 'l', 'm', 'n']
        self.amount = sum(self.buyers.values())
        self.result = {'k': 7.0, 'l': 11.0, 'm': 15.0, 'n': -33.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_14(self):
        self.buyers = {'a': 55, 'b': 34, 'c': 61}
        self.payers = ['a', 'c', 'd', 'e', 'f']
        self.amount = sum(self.buyers.values())
        self.result = {'a': -25.0, 'b': -34.0, 'c': -31.0, 'd': 30.0, 'e': 30.0, 'f': 30.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_15(self):
        self.buyers = {'w': 10, 'x': 50, 'y': 40, 'z': 80}
        self.payers = ['a', 'b', 'c', 'w', 'x', 'y']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 30.0, 'b': 30.0, 'c': 30.0, 'w': 20.0, 'x': -20.0, 'y': -10.0, 'z': -80.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_16(self):
        self.buyers = {'a': 1, 'b': 99}
        self.payers = ['a', 'b', 'c', 'd']
        self.amount = sum(self.buyers.values())
        self.result = {'a': 24.0, 'b': -74.0, 'c': 25.0, 'd': 25.0}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)

    def test_17(self):
        self.buyers = {"nazf": 6}
        self.payers = ["van", "nazk", "nazf"]
        self.amount = 6
        self.result = {"van": 2, "nazk": 2, "nazf": -4}
        self.assertEqual(calculate(self.buyers, self.payers, self.amount), self.result)


if __name__ == '__main__':
    unittest.main()
