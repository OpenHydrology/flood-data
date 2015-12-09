import requests
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


API_ENDPOINT = 'https://oh-auto-statistical-web-api.herokuapp.com/api/v0/data-imports/'
TOKEN = os.environ['DATA_IMPORT_TOKEN']
BRANCH_ONLY = 'master'
DATA_SOURCE = 'https://github.com/{}/archive/{}.zip'.format(os.environ['TRAVIS_REPO_SLUG'], BRANCH_ONLY)

logger.debug("Posting to URL {}".format(API_ENDPOINT))
logger.debug("Posting data source {}".format(DATA_SOURCE))
logger.debug("TRAVIS_PULL_REQUEST: {}".format(os.environ.get('TRAVIS_PULL_REQUEST', '')))
logger.debug("TRAVIS_BRANCH: {}".format(os.environ.get('TRAVIS_BRANCH', '')))


if (os.environ.get('TRAVIS_PULL_REQUEST', '').lower() == 'false' and
    os.environ.get('TRAVIS_BRANCH', '').lower() == BRANCH_ONLY.lower()):

    logger.debug("Deploying...")
    data = {
        'url': DATA_SOURCE,
        }
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
        }
    r = requests.post(API_ENDPOINT, json=data, headers=headers)
    logger.debug("Response status code: {}".format(r.status_code))
    logger.debug("Response content: {}".format(r.json()))
else:
    logger.debug("Not deployed (not on right branch or pull request).")
