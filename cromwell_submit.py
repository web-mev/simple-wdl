import requests
import json
import sys
import time

#########################################
# Inputs/constants:

# "http://<ip or hostname>:<port>"
CROMWELL_HOST = ''

# relative path to the "main" WDL file
# and the inputs.json
MAIN_WDL_PATH = 'main.wdl'
INPUTS_JSON_PATH = 'inputs.json'

#########################################

def submit():
    payload = {}
    payload = {'workflowType': 'WDL',
        'workflowTypeVersion': 'draft-2'
    }

    files = {
        'workflowInputs': open(INPUTS_JSON_PATH,'rb'),
        'workflowSource': open(MAIN_WDL_PATH, 'rb')
    }

    submission_url = f'{CROMWELL_HOST}/api/workflows/v1'
    response = requests.post(submission_url, data=payload, files=files)

    if response.status_code == 201:
        response_json = response.json()
        if response_json['status'] == 'Submitted':
            job_id = response_json['id']
            print(f'Job ID: {job_id}')
            return job_id
    else:
        print('Uh oh.')
        sys.exit(1)


def check_until_complete(job_id):
    status_url = f'{CROMWELL_HOST}/api/workflows/v1/{job_id}/status'
    incomplete_status = ['Running', 'Submitted']
    status = 'Submitted'
    while status in incomplete_status:
        time.sleep(10)
        r = requests.get(status_url)
        status = r.json()['status']
        print(f'Status: {status}')
    if status != 'Succeeded':
        print(f'Bad exit...Status was: {status}')
        sys.exit(1)


def get_outputs(job_id):
    outputs_url = f'{CROMWELL_HOST}/api/workflows/v1/{job_id}/outputs'
    r = requests.get(outputs_url)
    print(json.dumps(r.json(), indent=2))


if __name__ == '__main__':
    job_id = submit()
    check_until_complete(job_id)
    get_outputs(job_id)