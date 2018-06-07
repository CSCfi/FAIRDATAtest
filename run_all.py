import redgreenunittest as unittest
import time
from ida_metax import TestIDAMetax
from metax_etsin import TestMetaxEtsin
from nextcloud_test import IdaAppTests
from metax_quvain import TestMetaxQuvain 
from metax_dpress import TestMetaxDPress



OK = 'ok'
FAIL = 'fail'
ERROR = 'error'
SKIP = 'skip' # do not need it, might be in future

class JsonTestResult(unittest.TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super_class = super(JsonTestResult, self)
        super_class.__init__(stream, descriptions, verbosity)

        # TextTestResult has no successes attr
        self.successes = []

    def addSuccess(self, test):
        # addSuccess do nothing, so we need to overwrite it.
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append(test)

    def json_append(self, test, result, out):
        suite = test.__class__.__name__
        if suite not in out:
            out[suite] = {OK: [], FAIL: [], ERROR:[], SKIP: []}
        if result is OK:
            out[suite][OK].append(test._testMethodName)
        elif result is FAIL:
            out[suite][FAIL].append(test._testMethodName)
        elif result is ERROR:
            out[suite][ERROR].append(test._testMethodName)
        elif result is SKIP:
            out[suite][SKIP].append(test._testMethodName)
        else:
            raise KeyError("No such result: {}".format(result))
        return out

    def jsonify(self):
        json_out = dict()
        for t in self.successes:
            json_out = self.json_append(t, OK, json_out)

        for t, _ in self.failures:
            json_out = self.json_append(t, FAIL, json_out)

        for t, _ in self.errors:
            json_out = self.json_append(t, ERROR, json_out)

        for t, _ in self.skipped:
            json_out = self.json_append(t, SKIP, json_out)

        return json_out



def result_count(result_dict):

    keys = ["pass", "fail","error","skip",'total']
    result_count = dict.fromkeys(keys, 0)

    for keys in result_dict.keys():
        result_count["pass"] += len(result_dict[keys]['ok'])
        result_count["fail"] += len(result_dict[keys]['fail'])
        result_count["error"] += len(result_dict[keys]['error'])
        result_count["skip"] += len(result_dict[keys]['skip'])
        
    total = sum(result_count.values())

    return result_count,total

if __name__ == '__main__':
   
      
   # if want to save results in a file 
   #f = open('output.doc','w')
   #sys.stdout = f
   
   start_time = time.time()

   # create a testsuite
   suite = unittest.TestSuite()

   suite.addTest(IdaAppTests("test_freeze_file"))
   suite.addTest(IdaAppTests("test_unfreeze_file"))
   suite.addTest(IdaAppTests("test_delete_file"))
   suite.addTest(IdaAppTests("test_update_frozen_node_record"))
   suite.addTest(IdaAppTests("test_update_action"))
   suite.addTest(IdaAppTests("test_valid_timestamp"))
   suite.addTest(IdaAppTests("test_project_access_rights"))

   suite.addTest(TestMetaxEtsin("testCreateDataset"))
   suite.addTest(TestMetaxEtsin("testUpdateDataset"))
   suite.addTest(TestMetaxEtsin("testDeleteDataset"))

   suite.addTest(TestIDAMetax("testFreezeFile"))
   suite.addTest(TestIDAMetax("testUnFreezeFile"))
   suite.addTest(TestIDAMetax("testDeleteFile"))


   #suite.addTest(TestMetaxQuvain("testCreateDataset"))
   #suite.addTest(TestMetaxQuvain("testUpdateDateset"))
   #suite.addTest(TestMetaxQuvain("testDeleteDataset"))


   suite.addTest(TestMetaxDPress("testPreserveDataset"))
   suite.addTest(TestMetaxDPress("testRejectDataset"))
   suite.addTest(TestMetaxDPress("testRemoveDataset"))
   suite.addTest(TestMetaxDPress("testResetDataset"))



   runner = unittest.TextTestRunner(verbosity = 2)


   runner.resultclass = JsonTestResult

   result = runner.run(suite)
   
   elapsed_time = time.time() - start_time
   
   #  print json output
   result_dict = result.jsonify()
   count,total = result_count(result_dict)
   
   

   print("-----" * 20)
   print("\t\t\tSUMMARY ")
   print("-----" * 20)
   print("\n\t\t\tTotal   == " , total)
   print("\n\t\t\tPASS    == " , count["pass"])
   print("\t\t\tFAIL    == "  ,  count["fail"])
   print("\t\t\tERROR   == "  ,  count["error"])
   print("\t\t\tSKIP    == "  ,  count["skip"])
   print("\n\t\t\tTime    == "  ,  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
   print("-----" * 20)
   print("-----" * 20)
    

