import unittest
import time
import metax.metax as metax
import etsin.etsin as etsin
from utils import loadJSONFile
from pprint import pprint


class UnitTestMain(unittest.TestCase):

    """
    Main class intializing the unittest environment:
    - setting up the variables
    - Initializing the test data
    """


    @classmethod
    def setUpClass(self):
        print("-----" * 20)
        print("\t\tMetax - Etsin tests")
        print("-----" * 20)
        print("\t1. Create dataset")
        print("\t2. Update dataset")
        print("\t3. Delete dataset")
        print("-----" * 20)
        print("-----" * 20)
        # instead of setting a signal handler for ctrl+c,
        # call teardown class to make sure everything is clean
        try:
            cls.tearDownClass()
        except:
            pass


    @classmethod
    def tearDownClass(cls):
        pass
        #teardown_test_user_accounts()


    def setUp(self):
        self.OK = [200,201,202,203,204]
        self.FAIL = [401,403,404]


    def tearDown(self):
        pass

class TestMetaxEtsin(UnitTestMain):
    """
    - IdaAppTests class performing all the test cases
    """
    @classmethod
    def setUpClass(self):
        super(TestMetaxEtsin, self).setUpClass()

    #@unittest.skip("reason for skipping")
    def testCreateDataset(self):
        # loading the example dataset

        data = loadJSONFile('data.json')
        status, cdata = metax.create_dataset(data)

        self.assertIn(status, self.OK,"could not create dataset")
        urn = cdata["identifier"]
        time.sleep(10)

        etsin_status,etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.OK,"Etsin could not found the dataset")

    #@unittest.skip("reason for skipping")
    def testUpdateDataset(self):
        data = loadJSONFile('data.json')
        status,dataset = metax.create_dataset(data)
        self.assertIn(status,self.OK, "could not create dataset")

        #data = loadJSONFile('metax_dataset.json')
        dataset['research_dataset']['title']['en'] = 'title updated'
        status,updated_data = metax.update_dataset(dataset['id'], dataset)
        self.assertIn(status, self.OK,"Metax update failure")
        urn = updated_data["identifier"]
        etsin_status,etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.OK,"Etsin failure")

    #@unittest.skip("reason for skipping")
    def testDeleteDataset(self):

        data = loadJSONFile('data.json')

        status, cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK,"could not create dataset")
        urn = cdata["identifier"]

        time.sleep(2)
        #data = loadJSONFile('metax_dataset.json')
        status = metax.delete_dataset(cdata['id'])
        self.assertIn(status,self.OK,"Metax dataset delete failure")


        etsin_status, etsin_data = etsin.view_dataset(urn)
        self.assertIn(etsin_status, self.FAIL, "Etsin found the deleted dataset")


if __name__ == '__main__':
    unittest.main(verbosity = 2)
