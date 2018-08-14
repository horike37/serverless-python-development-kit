import sys
import subprocess
import boto3
import yaml
import os

cloudformation = boto3.client('cloudformation')


def get_endpoint_url(stage):
    f = open(os.path.dirname(__file__)+'/../../serverless.yml', 'r+')
    data = yaml.load(f)
    stackname = data['service'] + '-' + stage
    response = cloudformation.describe_stacks(
        StackName=stackname
    )

    for output in response['Stacks'][0]['Outputs']:
        if output['OutputKey'] == 'ServiceEndpoint':
            return output['OutputValue']


def sls_deploy(stage, region):
    exec_cmd(os.path.dirname(__file__)+'/../../node_modules/.bin/serverless deploy --stage '+stage+ ' --region '+region)


def sls_remove(stage, region):
    exec_cmd(os.path.dirname(__file__)+'/../../node_modules/.bin/serverless remove --stage '+stage+ ' --region '+region)


def exec_cmd(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    while True:
        line = proc.stdout.readline()
        if line:
            sys.stdout.write(line.decode('utf-8'))

        if not line and proc.poll() is not None:
            break
