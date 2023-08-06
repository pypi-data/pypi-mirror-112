import unittest
from base_class_V4test import TestBase
from base_class_V4test_online_deployment import TestBaseOnlineDeployment


class TestAIFunction(TestBase, TestBaseOnlineDeployment, unittest.TestCase):
    deployment_name = "ai_function_deployment"
    model_name = "ai_function_model"
    scoring_payload = [{
        "fields": ["multiplication"],
        "values": [[2.0, 2.0], [99.0, 99.0]]
    }]
    sw_spec_name = 'default_py3.8'

    def create_model(self, sw_spec_id) -> str:
        self.wml_client.repository.FunctionMetaNames.show()

        function_props = {
            self.wml_client.repository.FunctionMetaNames.NAME: self.model_name,
            self.wml_client.repository.FunctionMetaNames.SOFTWARE_SPEC_UID: sw_spec_id
        }

        def score(payload):
            payload = payload['input_data'][0]
            values = [[row[0] * row[1]] for row in payload['values']]
            return {'predictions': [{'fields': ['multiplication'], 'values': values}]}

        ai_function_details = self.wml_client.repository.store_function(score, function_props)

        return self.wml_client.repository.get_function_uid(ai_function_details)

    def patch_model(self):
        function_props = {
            self.wml_client.repository.FunctionMetaNames.DESCRIPTION: 'desc',
        }

        details = self.wml_client.repository.update_function(TestAIFunction.model_uid, function_props)


if __name__ == '__main__':
    unittest.main()
