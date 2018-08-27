import time
import unittest

from tests.etsin import etsin
from tests.metax import metax
from utils import load_json_file, service_configured


@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestEtsinMetax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        super().setUpClass()

    def setUp(self):
        self.OK = [200, 201, 202, 203, 204]
        self.FAIL = [401, 403, 404]

    def test_create_dataset(self):
        # loading the example dataset

        data = load_json_file('basic_dataset.json')
        status, cdata = metax.create_dataset(data)

        self.assertIn(status, self.OK, "could not create dataset")
        urn = cdata["identifier"]
        time.sleep(10)

        etsin_status, etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.OK, "Etsin could not found the dataset")

    def test_update_dataset(self):
        data = load_json_file('basic_dataset.json')
        status, dataset = metax.create_dataset(data)
        self.assertIn(status, self.OK, "could not create dataset")

        # data = load_json_file('metax_dataset.json')
        dataset['research_dataset']['title']['en'] = 'title updated'
        status, updated_data = metax.update_dataset(dataset['id'], dataset)
        self.assertIn(status, self.OK, "Metax update failure")
        urn = updated_data["identifier"]
        etsin_status, etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.OK, "Etsin failure")

    def test_delete_dataset(self):
        data = load_json_file('basic_dataset.json')

        status, cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK, "could not create dataset")
        urn = cdata["identifier"]

        time.sleep(2)
        status = metax.delete_dataset(cdata['id'])
        self.assertIn(status, self.OK, "Metax dataset delete failure")

        etsin_status, etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.FAIL, "Etsin found the deleted dataset")
