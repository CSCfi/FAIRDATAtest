import unittest
import time
from config.config import load_config_variables
import metax.metax as metax
import dpres.dpres as dpr
from utils import loadJSONFile

# loading configuration variables
conf = load_config_variables()





class UnitTestMain(unittest.TestCase):

    """
    Main class intializing the unittest environment:
    - setting up the variables
    - Initializing the test data
    """


    @classmethod
    def setUpClass(self):
        print("-----" * 20)
        print("\t\tMetax - DPress tests")
        print("-----" * 20)
        print("\t1. Preserve dataset")
        print("\t2. Reject dataset")
        print("\t3. Remove dataset")
        print("\t3. Reset dataset")
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
        # loading conf variables
        self.OK = [200,201,203]



    def tearDown(self):
        pass

class TestMetaxDPress(UnitTestMain):
    """
    - IdaAppTests class performing all the test cases
    """
    @classmethod
    def setUpClass(self):
        super(TestMetaxDPress, self).setUpClass()


    def testPreserveDataset(self):
        #Create a dataset in metax and preserve the dataset

        # loading the example dataset
        data = loadJSONFile('data.json')

        # creating a dataset
        status,cdata = metax.create_dataset(data)

        self.assertIn(status,self.OK,"Metax create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = dpr.preserve_dataset(id)
        self.assertIn(status, self.OK,"dpres preserve fails")


    def testRejectDataset(self):
        #Create a dataset in metax and reject the dataset for preservation

        # loading the example dataset
        data = loadJSONFile('data.json')

        # creating a dataset
        status,cdata = metax.create_dataset(data)
        self.assertIn(status,self.OK,"Metax create dataset fails")
        id = cdata['id']

        # rejecting the dataset
        status = dpr.reject_dataset(id)
        self.assertIn(status, self.OK,"dpres dataset rejection fails")


    def testRemoveDataset(self):
        #Create a dataset in metax, preserve the dataset and then remove the dataset from preservation

        # loading the example dataset
        data = loadJSONFile('data.json')

        # creating a dataset
        status,cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK,"create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = dpr.preserve_dataset(id)
        self.assertIn(status,self.OK,"dataset preservation fails")
        time.sleep(5)

        # removing the dataset
        status = dpr.remove_dataset(id)
        self.assertIn(status,self.OK,"dataset removal fails")


    def testResetDataset(self):
        #Create a dataset in metax, preserve the dataset and then reset the dataset

        # loading the example dataset
        data = loadJSONFile('data.json')

        # creating a dataset
        status,cdata = metax.create_dataset(data)
        self.assertIn(status, self.OK,"create dataset fails")
        id = cdata['id']

        # preserving the dataset
        status = dpr.preserve_dataset(id)
        self.assertIn(status,self.OK,"dataset preservations fails")
        time.sleep(5)

        # resetting the dataset
        status = dpr.reset_dataset(id)
        self.assertIn(status,self.OK,"dataset reset fails")




if __name__ == '__main__':
    unittest.main(verbosity = 2)
