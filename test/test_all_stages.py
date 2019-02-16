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
            'STATUS=$(pipenv run zappa status dev -j --settings_file zappa_settings.json 2>&1)\n'
            'set -e\n'
            'if [[ $(echo $STATUS | jq . 2>/dev/null) ]];\n'
            'then pipenv run zappa update dev --settings_file zappa_settings.json;\n'
            'elif [[ "$STATUS" == *"have you deployed yet?" ]];\n'
            'then pipenv run zappa deploy dev --settings_file zappa_settings.json;\n'
            'else echo "$STATUS\\nUnknown error!" && exit 1\n'
            'fi')

        self.assertTrue(expected_step == actual_step)

    def test_all_stages_true_deploys_to_one_stage(self):
        job = self.config['jobs']['zappa-deploy-all_stages-true']
        actual_step = job['steps'][2]['run']['command']
        expected_step = (
            'set +e\n'
            'STATUS=$(pipenv run zappa status --all -j --settings_file zappa_settings.json 2>&1 >/dev/null)\n'
            'ALL_DEPLOYMENTS=$(cat zappa_settings.json | jq -r \'. | keys | join(" ")\')\n'
            "NEW_DEPLOYMENTS=$(echo $STATUS | awk '{\n"
            "  if ( length($0)!=0 && $0 '\\!'~ /^Error: No Lambda.*deployed/ ) {\n"
            '    exit 1\n'
            '  }\n'
            '  else print $4\n'
            "}')\n"
            'STATUS_EXIT_CODE=$?\n'
            'NEW_DEPLOYMENT_COUNT=$(echo $NEW_DEPLOYMENTS | wc -w)\n'
            'TOTAL_DEPLOYMENT_COUNT=$(echo $ALL_DEPLOYMENTS | wc -w)\n'
            'set -e\n'
            'if [[ "$STATUS_EXIT_CODE" != "0" ]]\n'
            '  then echo "$STATUS\\nUnknown error!" && exit 1\n'
            'elif [[ "$NEW_DEPLOYMENT_COUNT" == "$TOTAL_DEPLOYMENT_COUNT" ]]\n'
            '  then pipenv run zappa deploy --all --settings_file zappa_settings.json\n'
            'elif [ "$NEW_DEPLOYMENT_COUNT" -gt "0" ]\n'
            '  then for DEPLOYMENT_NAME in $NEW_DEPLOYMENTS\n'
            '    do\n'
            "    STAGE=$(echo $DEPLOYMENT_NAME | awk -F- '{print $NF}')\n"
            '    pipenv run zappa deploy $STAGE --settings_file zappa_settings.json\n'
            '  done\n'
            'fi\n'
            'pipenv run zappa update --all --settings_file zappa_settings.json')

        self.assertTrue(expected_step == actual_step)
