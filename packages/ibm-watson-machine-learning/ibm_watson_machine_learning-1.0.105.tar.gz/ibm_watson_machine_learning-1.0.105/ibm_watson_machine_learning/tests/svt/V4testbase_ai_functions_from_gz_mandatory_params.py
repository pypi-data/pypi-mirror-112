import unittest
import os
from base_class_V4test import TestBase
from base_class_V4test_online_deployment import TestBaseOnlineDeployment


class TestAIFunction(TestBase, TestBaseOnlineDeployment, unittest.TestCase):
    deployment_name = "ai_function_deployment"
    model_name = "ai_function_model"
    scoring_payload = {
        "input_data": [{
            "fields": ["Gender", "Status", "Children", "Age", "Customer_Status"],
            "values": [
                ["Male", "M", 2, 48, "Inactive"],
                ["Female", "S", 0, 23, "Inactive"]
            ]
        }]
    }
    function_filepath = os.path.join(os.getcwd(), 'svt',  'artifacts', 'ai_function.gz')
    sw_spec_name_cloud = 'default_py3.7'
    sw_spec_name_icp = 'default_py3.7_opence'

    def create_model(self, sw_spec_id) -> str:
        self.wml_client.repository.FunctionMetaNames.show()

        ai_function_details = self.wml_client.repository.store_function(self.function_filepath, 'simplest AI function')

        return self.wml_client.repository.get_function_uid(ai_function_details)

    def patch_model(self):
        function_props = {
            self.wml_client.repository.FunctionMetaNames.DESCRIPTION: 'desc',
        }

        details = self.wml_client.repository.update_function(TestAIFunction.model_uid, function_props)


if __name__ == '__main__':
    unittest.main()
