import unittest
from config.config import load_config_variables
import ida.ida as ida

from ida.ida_accounts_initialise import initialize_test_account

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
        self.IDA_STABLE_USER = conf['IDA_STABLE_USER']
        self.PASS = conf['IDA_STABLE_PASS']
        self.HOST = conf['HOST']
        print("-----" * 20)
        print("\t\tInitialize IDA test accounts")
        print("-----" * 20)
        #try:
        initialize_test_account(self.IDA_STABLE_USER, self.PASS, self.HOST)
        #except:
        #    pass
        print("-----" * 20)
        print("\t\tNextcloud App test cases")
        print("-----" * 20)
        print("\t1. Freeze file")
        print("\t2. Unfreeze file")
        print("\t3. Delete file")
        print("\t4. Update frozen node record")
        print("\t5. Update actions")
        print("\t6. Testing valid timestamps")
        print("\t7. Testing access rights")
        print("-----" * 20)
        print("-----" * 20)
        # instead of setting a signal handler for ctrl+c,
        # call teardown class to make sure everything is clean

    @classmethod
    def tearDownClass(cls):
        pass
        #teardown_test_user_accounts()


    def setUp(self):
        # loading neccessary variables
        self.OK = [200,201,202,203]
        self.FAIL = [400,401,404]

    def tearDown(self):
        pass


class IdaAppTests(UnitTestMain):


    """
    - IdaAppTests class performing all the test cases
    """
    @classmethod
    def setUpClass(self):
        super(IdaAppTests, self).setUpClass()


    def test_freeze_file(self):
        """
        it perform the freeze action, Retrieves the frozen node, Retrieves frozen nodes associated with Action
        and Retrieves the frozen nodes details
        """


        #User A freeze experiment 2/test01.dat
        data = {
            "project": "Project_A",
            "pathname":"/2017-08/Experiment_2/test01.dat"
        }
        user = 'PSO_Project_A'
        status,res = ida.freeze_file(user,data)
        self.assertIn(status, self.OK,'freeze fails')
        pid1 = res['pid']

        #Retrieve frozen node
        projectname = res['project']
        status, node = ida.get_frozen_node(user, data,projectname)
        self.assertIn(status, self.OK,'could not retrieve frozen node')
        pid2 = node['pid']


        #Retrieve frozen nodes associated with Action
        status, node = ida.get_frozen_node_action(user, pid1)
        self.assertIn(status, self.OK,'could not get frozen node action')


        # Retrieve frozen nodes details
        status, node = ida.get_node_details(user, pid2)
        self.assertIn(status, self.OK,'could not retrieve frozen node details')


    def test_unfreeze_file(self):
        """
        Unfreeze test case:
        - freezes the file
        - Retrieve the set of actions
        - Retrieve the action details of frozen file
        - Unfreeze the file
        """
        #User A freeze experiment 2/test02.dat
        data = {
            "project": "Project_A",
            "pathname": "/2017-08/Experiment_2/test02.dat"
        }
        user = 'PSO_Project_A'

        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')


        #Retrieve set of actions
        data1 = {
            "status": "completed",
            "project":"Project_A"
        }

        status,actions = ida.get_actions(user,data1)
        self.assertIn(status, self.OK, 'actions retrieval fails')


        pid = actions["user" == "PSO_Project_A"]["pid"]
        nodeID = actions["user" == "PSO_Project_A"]["node"]

        #Retrieve action details of frozen file
        status, actions = ida.get_specific_actions(user, data1,pid)
        self.assertIn(status, self.OK, 'actions retrieval fails')

        #Unfreeze file
        data2 = {
            "node": nodeID,
            "project":"Project_A",
            "pathname":"/2017-08/Experiment_2/test02.dat"
        }
        status, res = ida.unfreeze_file(user, data2)
        self.assertIn(status, self.OK, 'file unfreeze fails')


    def test_delete_file(self):
        """
        Delete test case:
        - freezes the file
        - Delete the frozen file
        """

        #User B freeze experiment 2/test01.dat
        data = {
            "project": "Project_B",
            "pathname": "/2017-08/Experiment_2/test01.dat"
        }
        user = 'PSO_Project_B'

        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        #Delete frozen folder
        nodeId = res['node']
        data = {
            "node": nodeId,
            "project": "Project_B",
            "pathname": "/2017-08/Experiment_2/test01.dat"
        }
        status = ida.delete_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')


    def test_update_frozen_node_record(self):
        """
        Update frozen node records test case:
        - freezes the file
        - Retrieve the frozen file data
        - PSO user Updates checksum and metadata
        """

        #User C freeze experiment 4/test01.dat
        data = {
            "project": "Project_C",
            "pathname": "/2017-10/Experiment_4/test01.dat"
        }

        user = 'PSO_Project_C'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        #Retrieve frozen file data
        projectname = res['project']
        status, node = ida.get_frozen_node(user, data,projectname)
        self.assertIn(status, self.OK,'could not retrieve frozen node')
        pid = node['pid']

        #"Updating checksum
        data = {
            "checksum": "2000-00-00T00:00:00Z"
        }
        status = ida.update_node_details(user,pid,data)
        self.assertIn(status, self.OK, 'node update fails')

        #Updating metadata
        data = {
            "metadata": "2000-00-00T00:00:00Z"
        }
        status = ida.update_node_details(user,pid,data)
        self.assertIn(status, self.OK, 'actions retrieval fails')



    def test_update_action(self):
        """
        Update frozen node records test case:
        - freezes the file
        - Retrieve the set of actions
        - Retrieve the action details of specific node
        - Update error message and checksum
        - Again Retrieve the action details of frozen file to ensure that record has updates successfully
        """

        #User A freeze experiment 2/test03.dat
        data = {
            "project": "Project_A",
            "pathname": "/2017-08/Experiment_2/test03.dat"
        }

        user = 'PSO_Project_A'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        #Retrieve set of actions
        data1 = {
            "status": "completed",
            "project": "Project_A"
        }
        user = 'PSO_Project_A'

        status,actions = ida.get_actions(user,data1)
        self.assertIn(status, self.OK, 'actions retrieval fails')
        pid = actions["user" == "PSO_Project_A"]["pid"]

        #Retrieve action details of frozen file
        status, actions = ida.get_specific_actions(user, data1, pid)
        self.assertIn(status, self.OK, 'actions retrieval fails')
        self.assertEqual(actions['pid'], pid)

        # print("Update action: error msg & checksums")
        data2 = {
            "pid": pid,
            "error": "this is a test error message",
            "checksums": "2000-00-00T00:00:00Z"
        }
        status = ida.update_action_details(user,pid,data2)
        self.assertIn(status, self.OK, 'action update fails')


    def test_valid_timestamp(self):
        """
        Timestamp format test case:
        - freezes the file
        - Retrieve the set of actions
        - Update metadata, checksum and replication with valid time stamps
        - Try to update the four different invalid timestamps which would results in an error message
        """

        #User A freeze experiment 2/test04.dat
        data = {
            "project": "Project_A",
            "pathname": "/2017-08/Experiment_2/test04.dat"
        }

        user = 'PSO_Project_A'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'freeze fails')

        #Retrieve set of actions
        data = {
            "status": "completed",
            "project": "Project_A"
        }
        user = 'PSO_Project_A'

        status,actions = ida.get_actions(user,data)
        self.assertIn(status, self.OK, 'actions retrieval fails')
        pid = actions["user" == "PSO_Project_A"]["pid"]

        #Retrieve action details of frozen file
        status, actions = ida.get_specific_actions(user, data, pid)
        self.assertIn(status, self.OK, 'actions retrieval fails')
        self.assertEqual(actions['pid'], pid)

        #Updating metadata, checksums and replication with valid timestamps
        data = {
            "pid": pid,
            "metadata": "2017-11-12T15:48Z",
            "checksums": "2017-11-12T15:48Z",
            "replication": "2017-11-12T15:48:21Z"
        }
        status = ida.update_action_details(user, pid, data)
        self.assertIn(status, self.OK, 'action update fails')

        #Updating metadata with invalid timestamp: 2017-11-12T15:48+0000
        data = {
            "pid": pid,
            "metadata": "2017-11-12T15:48+0000"
        }
        status = ida.update_action_details(user, pid, data)
        self.assertIn(status, self.FAIL, 'action update fails')

        #Updating metadata with invalid timestamp: 2017-11-12 15:48:15
        data = {
            "pid": pid,
            "metadata": "2017-11-12 15:48:15"
        }
        status = ida.update_action_details(user, pid, data)
        self.assertIn(status, self.FAIL, 'action update fails')

        #Updating metadata with invalid timestamp: 2017-11-12
        data = {
            "pid": pid,
            "metadata": "2017-11-12"
        }
        status = ida.update_action_details(user, pid, data)
        self.assertIn(status, self.FAIL, 'action update fails')

        #Updating metadata with invalid timestamp: Tue,Dec12,2017,10:03 UTC
        data = {
            "pid": pid,
            "metadata": "Tue,Dec12,2017,10:03 UTC"
        }
        status = ida.update_action_details(user, pid, data)
        self.assertIn(status, self.FAIL, 'action update fails')




    #@unittest.skip()
    def test_project_access_rights(self):
        """
        User access rights test case:
        - Admin tries freezes the file that would result in an error message
        - User B tries to freeze project C file -- error message
        - User A freeze file of project A
        - Retrieve frozen file data
        - Admin updates the checksum
        """

        #User Admin freeze project C experiment 2/test05.dat
        data = {
            "project": "Project_C",
            "pathname": "/2017-08/Experiment_2/test05.dat"
        }

        user = 'admin'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.FAIL, 'check user and project, they should not be same')

        #User B tries to freeze project C experiment 1/test05.dat
        data = {
            "project": "Project_C",
            "pathname": "/2017-08/Experiment_1/test05.dat"
        }

        user = 'PSO_Project_B'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.FAIL, 'check user and project, they should not be same')

        #User A freeze experiment 3/test03.dat
        data = {
            "project": "Project_A",
            "pathname": "/2017-10/Experiment_3/test03.dat"
        }

        user = 'PSO_Project_A'
        status, res = ida.freeze_file(user, data)
        self.assertIn(status, self.OK, 'Freeze fails')

        #Retrieve frozen file data
        projectname = res['project']
        status, node = ida.get_frozen_node(user, data,projectname)
        self.assertIn(status, self.OK,'could not retrieve frozen node')
        pid = node['pid']

        #admin Updates checksum
        data = {
            "checksum": "2000-00-00T00:00:00Z"
        }
        user = 'admin'
        status = ida.update_node_details(user, pid, data)
        self.assertIn(status, self.OK, 'actions retrieval fails')


def suite():
    tests = ['test_freeze_file',
             'test_unfreeze_file',
             'test_delete_file',
             'test_update_frozen_node_record',
             'test_update_action',
             'test_valid_timestamp',
             'test_project_access_rights',
             ]
    return unittest.TestSuite(map(IdaAppTests, tests))

if __name__ == '__main__':
    runsuites = suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(runsuites)

