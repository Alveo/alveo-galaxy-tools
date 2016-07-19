import unittest
import os
import json
import alveo_item_list_importer
import pyalveo
from mock import Mock

class TestAlveoItemListImporter(unittest.TestCase):

  API_KEY = 'test123'
  OUTPUT_PATH = 'test.csv'
  ITEM_LIST = '{"shared": [{"shared": true, "num_items": 309, "name": "austalk_catepillar", "item_list_url": "https://app.alveo.edu.au/item_lists/64"}]}'
  CSV_CONTENTS = 'austalk_catepillar (309)\thttps://app.alveo.edu.au/item_lists/64\n'

  def test_write_table(self):
    api_list = json.loads(self.ITEM_LIST)
    alveo_item_list_importer.write_table(api_list, self.OUTPUT_PATH)
    actual = open(self.OUTPUT_PATH, 'r').read()
    self.assertEqual(self.CSV_CONTENTS, actual)

  def tearDown(self):
    try:
      os.remove(self.OUTPUT_PATH)
    except OSError:
      pass

if __name__ == '__main__':
    unittest.main()