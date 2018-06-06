import unittest 
from utils import loadJSONFile
from utils import bcolors as C

class UnitTestMain(unittest.TestCase):

    """
    Main class intializing the unittest environment:
    - setting up the variables
    - Initializing the test data
    """


    @classmethod
    def setUpClass(self):
        print(C.LINE + "-----" * 20 + C.END)
        print(C.HEAD +"\t\tQuvain - Metax tests" + C.END)
        print(C.LINE +"-----" * 20 + C.END)
        print(C.BOLD + "\t1. " + C.END + "Freeze file")
        print(C.BOLD + "\t2. " + C.END + "Unfreeze file")
        print(C.BOLD + "\t3. " + C.END + "Delete file")
        print(C.BOLD + "\t3. " + C.END + "Failed action")
        print(C.LINE + "-----" * 20 + C.END)
        print(C.LINE + "-----" * 20 + C.END)
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
        pass


    def tearDown(self):
        pass

class TestMetaxQuvain(UnitTestMain):
    """
    - IdaAppTests class performing all the test cases
    """
    @classmethod
    def setUpClass(self):
        super(TestMetaxQuvain, self).setUpClass()

    @unittest.skip
    def testFreezeFile(self):
        # loading the example dataset
        data = loadJSONFile('data.json')



    @unittest.skip
    def testUnfreezeFile(self):
        print("update")

    
    @unittest.skip
    def testDeleteFile(self):
        print("delete")
        data = loadJSONFile('metax_dataset.json')


    @unittest.skip
    def testFailedAction(self):
        print("later")



if __name__ == '__main__':
    unittest.main(verbosity = 2)
