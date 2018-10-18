import unittest
import os
from utils import service_configured, get_minimal_dataset_template
from config import conf_vars

from tests.qvain import qvain



@unittest.skipUnless(service_configured('QVAIN'), 'Qvain not configured')
@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestQvainMetax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        cls.dataset_id = ""
        super().setUpClass()

    def setUp(self):
        self.sid = os.environ.get('QVAIN_SID') or conf_vars['QVAIN']['SID']
        if not self.sid:
            raise Exception("please provide a session id either in the environment or in the config file")

        fairdata_dataset = get_minimal_dataset_template()
        self.dataset = qvain.make_dataset_from(fairdata_dataset)
        self.dataset_id = ""
        self.test_title = "Danska jo"
        
    def test_01_CreateDataset(self):
        status, res = qvain.create_dataset(self.dataset)
        # first check if we're authenticated, because if we're not, all tests will fail
        if status == 401:
            self.fail("not authenticated")

        self.assertEqual(status, 201, msg='expected status code {0}, got {1}'.format(201, status))
        self.assertIsNotNone(res['id'], msg='expected UUID')
        TestQvainMetax.dataset_id = res['id']

    def test_02_UpdateDataset(self):
        dataset_id = TestQvainMetax.dataset_id
        if not dataset_id:
           raise Exception("can't find dataset_id of previously created dataset")
           
        updated_dataset = self.dataset
        updated_dataset['id'] = dataset_id
        updated_dataset['dataset']['title']['dk'] = self.test_title
        
        status, res = qvain.update_dataset(dataset_id, self.dataset)
        self.assertEqual(status, 204)

    def test_03_GetDataset(self):
        dataset_id = TestQvainMetax.dataset_id
        if not dataset_id:
           raise Exception("can't find dataset_id of previously created dataset")
           
        status, res = qvain.get_dataset(dataset_id)
        self.assertEqual(status, 200)
        self.assertIn('dataset', res, msg='expected to find dataset key in api result')
        title = res['dataset']['title']['dk']
        self.assertEqual(title, self.test_title, msg='expected title {0}, got {1}'.format(self.test_title, title))

    def test_04_PublishDataset(self):
        dataset_id = TestQvainMetax.dataset_id
        if not dataset_id:
           raise Exception("can't find dataset_id of previously created dataset")
           
        status, res = qvain.publish_dataset(dataset_id)
        self.assertIn(status, [200, 201])
        self.assertIn('extid', res)

    def test_05_ListDatasets(self):
        status, res = qvain.list_datasets()
        self.assertEqual(status, 200)
        self.assertIsInstance(res, list)
        #print("datasets:", len(res))

    def test_06_SyncDatasets(self):
        # TODO: actually have datasets with changes in Metax
        status, res = qvain.sync_datasets()
        self.assertEqual(status, 200)
        self.assertIsInstance(res, list)
        #print("datasets:", len(res))
