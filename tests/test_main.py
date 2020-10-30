import unittest
from main import _uniqueEverSeen, selectSantas
from main import participants, tuplesToAvoid


class TestSelectSantas(unittest.TestCase):
    def setUp(self):
        self.expected = sorted(list(participants.keys()))
        self.resultDict = selectSantas()
        self.result = sorted(list(self.resultDict.keys()))

    def test_keys_eq(self):
        """Test if keys from selectSantas are equal to those in participants"""
        self.assertListEqual(self.result, self.expected)

    def test_tuples_to_avoid(self):
        """Test that there is no combination in tuples to avoid."""
        self.assertFalse(
            any(key in self.resultDict and self.resultDict[key] == tuplesToAvoid[key] for key in tuplesToAvoid))


class TestUniqueEverSeen(unittest.TestCase):
    def setUp(self):
        self.expected = [1, 3, 2, 4, 5]
        self.result = _uniqueEverSeen([1, 3, 2, 3, 4, 5])

    def test_list_eq(self):
        self.assertListEqual(self.result, self.expected)


if __name__ == '__main__':
    unittest.main()
