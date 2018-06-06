import unittest 
from utils import loadJSONFile


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
        print("\t1. Create dataset record")
        print("\t2. Update dataset record")
        print("\t2.1 Reading/sync an existing dataset from metax")
        print("\t2.2. Update metadata in dataset record")
        print("\t2.3. Update IDA file in dataset record")
        print("\t3. Delete dataset record")
        print("\t4. Person is identified:Single-sign on messages - test identity (fake user)")
        print("\t5. Creating a workflow: Quvain - Metax - REMS")
        print("-----" * 20)
        print("-----" * 20)
        try:
            cls.tearDownClass()
        except:
            pass


    @classmethod
    def tearDownClass(cls):
        pass
        #teardown_test_user_accounts()


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
        # loading the example dataset
        data = loadJSONFile('data.json')



    @unittest.skip
    def testUpdateDateset(self):
        print("update")

    
    @unittest.skip
    def testDeleteDataset(self):
        print("delete")
        data = loadJSONFile('metax_dataset.json')






if __name__ == '__main__':
    unittest.main(verbosity = 2)
