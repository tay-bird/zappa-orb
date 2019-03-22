import os
import unittest

import yaml


class TestExecutor(unittest.TestCase):

    def setUp(self):
        with open("executor.yml") as f:
            self.config = yaml.load(f)

    def test_job_uses_py37_image(self):
        actual_images = [
            docker_config['image']
            for docker_config in self.config['jobs']['zappa/zappa-deploy']['docker']]
        expected_images = ['circleci/python:3.7']

        self.assertTrue(set(expected_images) == set(actual_images))
