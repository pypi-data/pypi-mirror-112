import json
import os
import sys

import mistletoe
from jira_renderer import JIRARenderer
import requests
from requests.auth import HTTPBasicAuth

config = {}
config_uri = os.path.expanduser('~') + '/.jira_tool.json'


def read_config():
    config_file = open(config_uri, 'r')
    config_json = config_file.read()
    global config
    config = json.loads(config_json)
    config['file_base_uri'] = config['file_base_uri'].replace("~", os.path.expanduser('~'))
    return config


def edit_jira_card(card_number, desc):
    url = config['host'] + "/jira/rest/api/2/issue/" + card_number
    payload = json.dumps({
        "fields": {
            "description": desc
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, auth=HTTPBasicAuth(config['name'], config['password']), headers=headers,
                                data=payload)
    print(response)


def get_markdown_info_with_jira_format(url, file):
    fo = open(url + '/' + file, "r")
    rendered = mistletoe.markdown(fo, JIRARenderer)
    return rendered


def main(args=None):
    read_config()
    card_no = 'OTRT-285'
    file_url = config['file_base_uri'] + 'i1'
    file_name = card_no + ".md"
    jira_desc = get_markdown_info_with_jira_format(file_url, file_name)
    edit_jira_card(card_no, jira_desc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
