import argparse
from time import sleep
from os.path import join
from os import walk
import requests
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile

def parse_arguments():
    """ Parses cmd-line arguments """
    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("token", help="Dataverse token.")
    parser.add_argument("server", help="Dataverse server.")
    parser.add_argument("doi", help="Dataset DOI.")
    parser.add_argument("repo", help="GitHub repository.")

    # Optional arguments
    parser.add_argument("-d", "--dir", help="Uploads only a specific dir.")
    parser.add_argument(
        "-r", "--remove", help="Remove (delete) all files before upload.", \
        choices=('True', 'TRUE', 'true', 'False', 'FALSE', 'false'), \
        default='true')
    parser.add_argument(
        "-p", "--publish", help="Publish a new dataset version after upload.", \
        choices=('True', 'TRUE', 'true', 'False', 'FALSE', 'false'), \
        default='false')

    args_ = parser.parse_args()
    return args_


def check_dataset_lock(num):
    """ Gives Dataverse server more time for upload """
    if num <= 1:
        print('Lock found for dataset id ' + \
          str(dataset_dbid) + '\nTry again later!')
        return

    query_str = dataverse_server + \
         '/api/datasets/' + str(dataset_dbid) + '/locks/'
    resp_ = requests.get(query_str, auth = (token, ""))
    locks = resp_.json()['data']

    if bool(locks):
        print('Lock found for dataset id ' + \
           str(dataset_dbid) + '\n... sleeping...')
        sleep(2)
        check_dataset_lock(num-1)
    return


if __name__ == '__main__':

    token='d193b834-0a3a-439a-9e09-09e0502dc0f4'
    server='https://dataverse.geus.dk'
    doi='doi:10.22008/FK2/3TSBF0'
    dir=None
    remove="True"
    publish="False"
    paths=['/home/pho/Downloads/pypromice-1.5.2/']

    dataverse_server = server.strip("/")
    api = NativeApi(dataverse_server, token)


    dataset = api.get_dataset(doi)
    files_list = dataset.json()['data']['latestVersion']['files']
    dataset_dbid = dataset.json()['data']['id']

    metadata = dataset.json()["data"]["latestVersion"]["metadataBlocks"]["citation"]
    for m in metadata["fields"]:
        if 'title' in m['typeName']:
            m.update({'value': 'test'})

    resp = api.edit_dataset_metadata(doi, data, is_replace=True, auth=True)
    print(resp.status_code)
