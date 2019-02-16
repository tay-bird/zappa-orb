import os
import unittest

import yaml


class TestSimple(unittest.TestCase):

    def setUp(self):
        with open("simple.yml") as f:
            self.config = yaml.load(f)

    def test_high_level_keys_are_correct(self):
       actual_keys = self.config.keys()
       expected_keys = ['jobs', 'version', 'workflows']

       self.assertTrue(set(expected_keys) == set(actual_keys))

    def test_job_is_present(self):
        actual_jobs = self.config['jobs'].keys()
        expected_jobs = ['zappa/zappa-deploy']

        self.assertTrue(set(expected_jobs) == set(actual_jobs))

    def test_job_uses_py27_image(self):
        actual_images = [
            docker_config['image']
            for docker_config in self.config['jobs']['zappa/zappa-deploy']['docker']]
        expected_images = ['circleci/python:2.7']

        self.assertTrue(set(expected_images) == set(actual_images))

    def test_job_contains_three_steps(self):
        actual_steps = self.config['jobs']['zappa/zappa-deploy']['steps']

        self.assertTrue(len(actual_steps) == 3)

    def test_job_step_one_checks_out(self):
        actual_step = self.config['jobs']['zappa/zappa-deploy']['steps'][0]
        expected_step = 'checkout'

        self.assertTrue(expected_step == actual_step)

    def test_job_step_three_performs_create_or_update(self):
        actual_step = self.config['jobs']['zappa/zappa-deploy']['steps'][2]['run']['command']
        expected_step = (
            'set +e\n'
            'STATUS=$(pipenv run zappa status borb -j --settings_file zappa_settings.json 2>&1)\n'
            'set -e\n'
            'if [[ $(echo $STATUS | jq . 2>/dev/null) ]];\n'
            'then pipenv run zappa update borb --settings_file zappa_settings.json;\n'
            'elif [[ "$STATUS" == *"have you deployed yet?" ]];\n'
            'then pipenv run zappa deploy borb --settings_file zappa_settings.json;\n'
            'else echo "$STATUS\\nUnknown error!" && exit 1\n'
            'fi')

        self.assertTrue(expected_step == actual_step)
