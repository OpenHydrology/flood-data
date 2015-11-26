import requests
import os


API_ENDPOINT = 'https://oh-auto-statistical-web-api.herokuapp.com/api/v0/data-import/'
TOKEN = os.environ['DATA_IMPORT_TOKEN']
BRANCH_ONLY = 'master'
DATA_SOURCE = 'https://github.com/{}/archive/{}.zip'.format(os.environ['TRAVIS_REPO_SLUG'], BRANCH_ONLY)

if (os.environ.get('TRAVIS_PULL_REQUEST', '').lower() == 'false' and
    os.environ.get('TRAVIS_BRANCH', '').lower() == BRANCH_ONLY.lower()):

    data = {
        'url': DATA_SOURCE,
    }
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
    }

    requests.post(API_ENDPOINT, json=data, headers=headers)
