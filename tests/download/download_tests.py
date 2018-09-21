import time
import unittest

from tests.download import download

class TestDownload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        super().setUpClass()

    def setUp(self):
        self.OK = [200, 201, 202, 203, 204]
        self.FAIL = [401, 403, 404, 500]

    def test_file(self):
        # downloading a file from the example dataset
        urn = 'urn:nbn:fi:att:d2cf4977-36fa-4762-adb3-126ea06108ed?file=5b7d486c951df671401089f134223'
        download_status, download_data = download.download_dataset(urn)
        self.assertIn(download_status, self.OK, "Download could not download the file")

    def test_dir(self):
        # downloading a dir from the example dataset
        urn = 'urn:nbn:fi:att:d2cf4977-36fa-4762-adb3-126ea06108ed?dir=c66c97e387933b82a734d904cc9572a3'
        download_status, download_data = download.download_dataset(urn)
        self.assertIn(download_status, self.OK, "Download could not download the file")

    def test_dataset(self):
        # downloading the example dataset

        urn = 'urn:nbn:fi:att:d2cf4977-36fa-4762-adb3-126ea06108ed'
        download_status, download_data = download.download_dataset(urn)
        self.assertIn(download_status, self.OK, "Download could not download the dataset")

