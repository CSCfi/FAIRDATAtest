import unittest

import requests

from config import conf_vars
from tests.download import download
from tests.ida import ida
from tests.metax import metax
from utils import service_configured


try:
    metax_host = 'https://%s' % conf_vars['METAX']['HOST']
    dataset_create_user = conf_vars['METAX']['USERS']['QVAIN']
    metax_auth = (dataset_create_user['USER'], dataset_create_user['PASS'])
except Exception as e:
    print('Note: METAX not configured')


@unittest.skipUnless(service_configured('DOWNLOAD'), 'Download not configured')
@unittest.skipUnless(service_configured('IDA'), 'IDA not configured')
@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestDownload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Executing %s...' % cls.__name__)
        super().setUpClass()
        cls.OK = [200, 201, 202, 203, 204]
        cls.FAIL = [401, 403, 404, 500]

        cls._test_project_identifier = 'Project_A'
        cls._test_directory_path = '/2017-10'
        cls._test_project_user = 'PSO_Project_A'
        cls._test_ida_catalog_urn = 'urn:nbn:fi:att:data-catalog-ida'

        ida.initialize_test_accounts()
        metax.flush_project(cls._test_project_identifier)
        cls._freeze_directory_in_ida()
        cls._create_test_dataset_in_metax()

    @classmethod
    def tearDownClass(cls):
        metax.flush_project(cls._test_project_identifier)

    @classmethod
    def _freeze_directory_in_ida(cls):
        """
        Freeze an existing test directory in IDA staging area, so the file metadata ends up in Metax.
        """
        data = { "project": cls._test_project_identifier, "pathname": cls._test_directory_path }
        status, res = ida.freeze_file(cls._test_project_user, data)
        assert status in cls.OK, 'test setup failed: ida freeze file returned %s' % status

        file_is_in_metax = ida.wait_until_file_appears_in_metax(data['project'], data['pathname'])
        assert file_is_in_metax is True, 'test setup failed: frozen file never appeared in metax'

    @classmethod
    def _create_test_dataset_in_metax(cls):
        """
        Create a test dataset in Metax using the previously frozen directory in IDA.
        """

        # get the identifier of the directory that was frozen previously
        response = requests.get(
            '%s/rest/directories/root?project=%s&path=%s'
            % (metax_host, cls._test_project_identifier, cls._test_directory_path),
            auth=metax_auth,
            verify=False
        )
        assert response.status_code == 200, 'test setup failed - metax says: %s' % str(response.json())

        cls._test_root_directory_identifier = response.json()['directories'][0]['identifier']

        # get a dataset template that can be used to create a test dataset in metax
        response = requests.get(
            '%s/rpc/datasets/get_minimal_dataset_template?type=service' % metax_host,
            verify=False
        )
        assert response.status_code == 200, 'test setup failed - metax says: %s' % str(response.json())

        # add the previously created dir in the dataset
        cr = response.json()
        cr['research_dataset']["directories"] = [
            {
                "title": "Test Directory",
                "identifier": cls._test_root_directory_identifier,
                "use_category": {
                    "identifier": "http://uri.suomi.fi/codelist/fairdata/use_category/code/method"
                }
            }
        ]

        # publish the dataset in metax
        response = requests.post(
            '%s/rest/datasets' % metax_host,
            json=cr,
            auth=metax_auth,
            verify=False
        )
        assert response.status_code == 201, 'test setup failed - metax says: %s' % str(response.json())
        cls._test_dataset_identifier = response.json()['identifier']

    def test_download_single_file_from_dataset(self):
        # get identifier of a single file in the dataset. using a bit more params to ensure files are returned...
        response = requests.get(
            '%s/rest/directories/%s/files?cr_identifier=%s&recursive=true&depth=*&file_fields=identifier' %
            (metax_host, self._test_root_directory_identifier, self._test_dataset_identifier),
            auth=metax_auth,
            verify=False
        )
        self.assertEqual(response.status_code, 200, 'test setup failed - metax says: %s' % str(response.json()))

        file_identifier = response.json()[0]['identifier']
        urn_and_file = '%s?file=%s' % (self._test_dataset_identifier, file_identifier)
        download_status, download_data = download.download_dataset(urn_and_file)
        self.assertIn(download_status, self.OK, "Download could not download the file")

    def test_download_directory_from_dataset(self):
        # downloading a dir from the example dataset
        urn_and_dir = '%s?dir=%s' % (self._test_dataset_identifier, self._test_root_directory_identifier)
        download_status, download_data = download.download_dataset(urn_and_dir)
        self.assertIn(download_status, self.OK, "Download could not download the file")

    def test_download_all_files_from_dataset(self):
        # downloading the example dataset
        download_status, download_data = download.download_dataset(self._test_dataset_identifier)
        self.assertIn(download_status, self.OK, "Download could not download the dataset")
