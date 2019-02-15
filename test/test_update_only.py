import os
import unittest

import yaml


class TestUpdateOnly(unittest.TestCase):

    def setUp(self):
        with open("update_only.yml") as f:
            self.config = yaml.load(f)

    def test_high_level_keys_are_correct(self):
       actual_keys = self.config.keys()
       expected_keys = ['jobs', 'version', 'workflows']

       self.assertTrue(set(expected_keys) == set(actual_keys))

    def test_jobs_are_present(self):
        actual_jobs = self.config['jobs'].keys()
        expected_jobs = [
            'zappa-deploy-update_only-true',
            'zappa-deploy-update_only-false',
            'zappa-deploy-update_only-absent']

        self.assertTrue(set(expected_jobs) == set(actual_jobs))

    def test_update_only_true_performs_update_only(self):
        job = self.config['jobs']['zappa-deploy-update_only-true']
        actual_step = job['steps'][2]['run']['command']
        expected_step = 'pipenv run zappa deploy borb'

        self.assertTrue(expected_step == actual_step)

    def test_update_only_false_performs_create_or_update(self):
        job = self.config['jobs']['zappa-deploy-update_only-false']
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
            'fi\n')

        self.assertTrue(expected_step == actual_step)

    def test_update_only_absent_performs_create_or_update(self):
        job = self.config['jobs']['zappa-deploy-update_only-absent']
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
            'fi\n')

        self.assertTrue(expected_step == actual_step)
