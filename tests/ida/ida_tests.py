import time
import unittest

from tests.ida import ida
from tests.metax import metax
from config import conf_vars
from utils import service_configured


try:
    host = conf_vars['IDA']['HOST']
    user = conf_vars['IDA']['USERS']['SSH_USER']['USER']
    password = conf_vars['IDA']['USERS']['SSH_USER']['PASS']
except Exception as e:
    print('Note: Ida not configured')


@unittest.skipUnless(service_configured('IDA'), 'Ida not configured')
@unittest.skipUnless(service_configured('METAX'), 'Metax not configured')
class TestIdaMetax(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print('Executing %s...' % self.__name__)
        super().setUpClass()
        ida.initialize_test_account(user, password, host)

    def setUp(self):
        self.OK = [200, 201, 202, 203]
        self.FAIL = [400, 401, 404]

    @classmethod
    def tearDownClass(cls):
        print('Flushing test projects in metax...')
        for project in ["Project_A", "Project_B", "Project_C"]:
            metax.flush_project(project)

    def test_freeze_file(self):
        data = {
            "project": "Project_A",
            "pathname": "/2017-10/Experiment_3/test01.dat"
        }
        user = 'PSO_Project_A'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        file_is_in_metax = ida.wait_until_file_appears_in_metax(data['project'], data['pathname'])
        self.assertEqual(file_is_in_metax, True, 'Frozen file never appeared in metax')

    def test_unfreeze_file(self):
        data = {
            "project": "Project_A",
            "pathname": "/2017-10/Experiment_5/test02.dat"
        }

        user = 'PSO_Project_A'

        # set test conditions...
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'Ida file freezing failed')

        file_is_in_metax = ida.wait_until_file_appears_in_metax(data['project'], data['pathname'])
        self.assertEqual(file_is_in_metax, True, 'Frozen file never appeared in metax')

        # the actual test
        for i in range(0, 60):
            status, res = ida.unfreeze_file(user, data)
            if status == 200:
                print('unfreeze success')
                break

            # it may take a moment for the previous freeze action to complete. if the
            # previous action is not completed, an unfreeze action too soon will cause
            # a conflicting-action error.
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print('unfreeze probably still conflicting with freeze action, waiting a bit...')

        self.assertIn(status, self.OK, 'Ida file unfreezing failed')

        file_disappeared_from_metax = ida.wait_until_file_disappears_from_metax(data['project'], data['pathname'])
        self.assertEqual(file_disappeared_from_metax, True, 'Frozen file never disappeared from metax')

    def test_delete_file(self):
        data = {
            "project": "Project_A",
            "pathname": "/2017-10/Experiment_4/test03.dat"
        }

        user = 'PSO_Project_A'

        # set test conditions...
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        file_is_in_metax = ida.wait_until_file_appears_in_metax(data['project'], data['pathname'])
        self.assertEqual(file_is_in_metax, True, 'Frozen file never appeared in metax')

        # the actual test
        data = {
            "nextcloudNodeId": res['node'],
            "project": "Project_A",
            "pathname": "/2017-10/Experiment_4/test03.dat"
        }

        for i in range(0, 60):
            status = ida.delete_file(user, data)
            if status == 200:
                print('unfreeze success')
                break

            # it may take a moment for the previous freeze action to complete. if the
            # previous action is not completed, a delete action too soon will cause
            # a conflicting-action error.
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print('delete probably still conflicting with freeze action, waiting a bit...')

        self.assertIn(status, self.OK, 'Ida file delete failed')

        file_disappeared_from_metax = ida.wait_until_file_disappears_from_metax(data['project'], data['pathname'])
        self.assertEqual(file_disappeared_from_metax, True, 'Frozen file never disappeared from metax')
