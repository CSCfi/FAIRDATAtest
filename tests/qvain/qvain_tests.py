import unittest
from utils import service_configured


@unittest.skipUnless(service_configured('QVAIN'), 'Qvain not configured')
@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestQvainMetax(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        super().setUpClass()

    def testCreateDataset(self):
        print("xx")
        # loading the example dataset
        # TODO: implement the function here

    def testUpdateDataset(self):
        print("xx")
        # loading the example dataset
        # TODO: implement the function here

    def testPublishDataset(self):
        print("xx")
        # loading the example dataset
        # TODO: implement the function here

    def testSyncDataset(self):
        print("xx")
        # loading the example dataset
        # TODO: implement the function here
