"""
Example presents usage of the successful problems.updateActiveTestcases() API method
"""
from sphere_engine import ProblemsClientV3

# define access parameters
accessToken = '<access_token>'
endpoint = '<endpoint>'

# initialization
client = ProblemsClientV3(accessToken, endpoint)

# API usage
activeTestcases = [1,2,3]

response = client.problems.updateActiveTestcases('EXAMPLE', activeTestcases)
