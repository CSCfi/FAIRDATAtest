import time
import unittest

from tests.pas import pas
from tests.metax import metax
from utils import load_json_file, service_configured


@unittest.skipUnless(service_configured('PAS'), 'PAS not configured')
@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestPASMetax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        super().setUpClass()

    def setUp(self):
        self.OK = [200, 201, 203]

    def test_preserve_dataset(self):
        # Create a dataset in metax and preserve the dataset

        # loading the example dataset
        data = load_json_file('basic_dataset.json')

        # creating a dataset
        status, cdata = metax.create_dataset(data)

        self.assertIn(status, self.OK, "Metax create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = pas.preserve_dataset(id)

        self.assertIn(status, self.OK, "PAS preserve fails")

    def test_reject_dataset(self):
        # Create a dataset in metax and reject the dataset for preservation

        # loading the example dataset
        data = load_json_file('basic_dataset.json')

        # creating a dataset
        status, cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK, "Metax create dataset fails")
        id = cdata['id']

        # rejecting the dataset
        status = pas.reject_dataset(id)
        self.assertIn(status, self.OK, "PAS dataset rejection fails")

    def test_remove_dataset(self):
        # Create a dataset in metax, preserve the dataset and then remove the dataset from preservation

        # loading the example dataset
        data = load_json_file('basic_dataset.json')

        # creating a dataset
        status, cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK, "create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = pas.preserve_dataset(id)
        self.assertIn(status, self.OK, "dataset preservation fails")
        time.sleep(5)

        # removing the dataset
        status = pas.remove_dataset(id)
        self.assertIn(status, self.OK, "dataset removal fails")

    def test_reset_dataset(self):
        # Create a dataset in metax, preserve the dataset and then reset the dataset

        # loading the example dataset
        data = load_json_file('basic_dataset.json')

        # creating a dataset
        status, cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK, "create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = pas.preserve_dataset(id)
        self.assertIn(status, self.OK, "dataset preservations fails")
        time.sleep(5)

        # resetting the dataset
        status = pas.reset_dataset(id)
        self.assertIn(status, self.OK, "dataset reset fails")
