import unittest
import os
import alveo_api_key
import pyalveo
from mock import Mock

class TestAlveoAPIKey(unittest.TestCase):

  OUTPUT_PATH = 'test.txt'
  API_KEY = 'test123'
  MOCK_CLIENT = Mock(pyalveo)

  def test_write_key(self):
    alveo_api_key.write_key(self.API_KEY, self.OUTPUT_PATH, self.MOCK_CLIENT)
    actual = open(self.OUTPUT_PATH, 'r').read()
    self.assertEqual(self.API_KEY, actual)

  def tearDown(self):
    try:
      os.remove(self.OUTPUT_PATH)
    except OSError:
      pass

if __name__ == '__main__':
    unittest.main()