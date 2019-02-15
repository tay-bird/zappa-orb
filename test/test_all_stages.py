from pprint import pprint as pp
import os
import unittest

import yaml


class TestAllStages(unittest.TestCase):

    def setUp(self):
        with open("all_stages.yml") as f:
            self.config = yaml.load(f)

    def test_all_stages_false_deploys_to_one_stage(self):
        job = self.config['jobs']['zappa-deploy-all_stages-false']
        actual_step = job['steps'][2]['run']['command']
        expected_step = (
            'set +e\n'
            'STATUS=$(pipenv run zappa status borb -j 2>&1)\n'
            'set -e\n'
            'if [[ $(echo $STATUS | jq . 2>/dev/null) ]];\n'
            'then pipenv run zappa update borb;\n'
            'elif [[ "$STATUS" == *"have you deployed yet?" ]];\n'
            'then pipenv run zappa deploy borb;\n'
            'else echo "$STATUS\\nUnknown error!" && exit 1\n'
            'fi')

        self.assertTrue(expected_step == actual_step)
