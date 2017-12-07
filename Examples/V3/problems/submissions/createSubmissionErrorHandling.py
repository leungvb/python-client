"""
Example presents error handling for submissions.create() API method
"""
from sphere_engine import ProblemsClientV3
from sphere_engine.exceptions import SphereEngineException

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
problemCode = 'TEST'
source = '<source code>'
nonexistingCompiler = 99999;

try:
    response = client.submissions.create(problemCode, source, nonexistingCompiler)
    # response['id'] stores the ID of the created submission
except SphereEngineException as e:
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 404:
        # aggregates three possible reasons of 404 error
        # non existing problem, compiler or user
        print('Non existing resource (problem, compiler or user), details available in the message: ' + str(e))
    elif e.code == 400:
        print('Empty source code')
