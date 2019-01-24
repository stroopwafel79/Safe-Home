import unittest
from module import dict_to_string

class TestDictToSring(unittest.TestCase):

	def test_dict_to_string(self):
		result = dict_to_string({"a": 1, "b": 2})
		self.assertEqual(result, "a:1, b:2, ")

if __name__ == "__main__":

	unittest.main()