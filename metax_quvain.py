import unittest 
from utils import loadJSONFile
import metax.metax as metax
import quvain.quvain as quvain


class UnitTestMain(unittest.TestCase):

    """
    Main class intializing the unittest environment:
    - setting up the variables
    - Initializing the test data
    """

    
    @classmethod
    def setUpClass(self):
        print("-----" * 20)
        print("\t\tQuvain - Metax tests") 
        print("-----" * 20 )
        print("\t1. Create new dataset")
        print("\t2. Update dataset")
        print("\t2. Publish dataset to metax")
        print("\t2. Sync existing dataset from metax")
        print("-----" * 20)
        print("-----" * 20)
        try:
            cls.tearDownClass()
        except:
            pass


    @classmethod
    def tearDownClass(cls):
        pass
        #TODO: delete all the test data, if published


    def setUp(self):
        pass


    def tearDown(self):
        pass

class TestMetaxQuvain(UnitTestMain):
    """
    - TestMetaxQuvain class performing all the test cases related to Quvain-Metax
    """

    @classmethod
    def setUpClass(self):
        super(TestMetaxQuvain, self).setUpClass()

    @unittest.skip
    def testCreateDataset(self):
        print("xx")
        # loading the example dataset
        #TODO: implement the function here 
        

    @unittest.skip
    def testUpdateDataset(self):
        print("xx")
        # loading the example dataset
        #TODO: implement the function here 


    @unittest.skip
    def testPublishDataset(self):
        print("xx")
        # loading the example dataset
        #TODO: implement the function here 


    @unittest.skip
    def testSyncDataset(self):
        print("xx")
        # loading the example dataset
        #TODO: implement the function here 





if __name__ == '__main__':
    unittest.main(verbosity = 2)
