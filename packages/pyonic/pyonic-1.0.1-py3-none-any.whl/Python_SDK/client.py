from json.decoder import JSONDecodeError
from typing import IO
import requests
import json
import os

# from requests.api import get


#### These functions are to ensure that the core/critical SDK features are working, eventually these funtions will be formatted/reorganized

# This handler is currently under testing much like many of the endpoints: CAUTION ADVISED FOR USAGE
def response_handler(response):
    code = response.status_code
    try:
        json.loads(response.content)
    except JSONDecodeError as e:
        # print("Error: Invalid Request")
        raise RuntimeError("Failed to send Invalid Request") from e
        return -1

    if code < 200 or code >= 300:
        error_message = json.loads(response.content)
        error_message = error_message["message"]
        # print(f"Error {code}: {error_message}")
        raise Exception(f"Error {code}: {error_message}")
        return -1

    return 0


# This class as of the current, keeps track of the baseURL and eventually the API token - once they login
class IonChannel:
    def __init__(self, baseURL):
        self.baseURL = baseURL
        self.token = None


# This function will create a new client object so that the user can interact with the API
def new_client(baseURL):
    client = IonChannel(baseURL)
    return client


# This function will allow the user to login
def login(self, username=None, password=None):
    if username is None:
        try:
            username = os.environ["IONUSER"]
        except KeyError:
            username = input(
                "Since you have not set ENV variable (IONUSER): What is your username: "
            )
    if password is None:
        try:
            password = os.environ["IONPASSWORD"]
        except KeyError:
            password = input(
                "Since you have not set ENV variable (IONPASSWORD): What is your password: "
            )

    endpoint = "sessions/login"
    URL = self.baseURL + endpoint
    r = requests.post(URL, json={"username": username, "password": password})
    check = response_handler(r)
    # if check is not None:
    #    return -1
    if check != 0:
        return -1

    # code = r.status_code
    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return

    try:
        token = r.json()["data"]["jwt"]
    except KeyError as e:
        # print("login Error: Invalid authentication credentials - An account doesn't exist with this username or password")

        raise RuntimeError(
            "Invalid authentication credentials - An account doesn't exist with this username or password"
        ) from e

        # return -1

    self.token = token
    return token


IonChannel.login = login

# This function will list all the teams
def get_teams(self, token):
    endpoint = "teams/getTeams"
    head = {"Authorization": "Bearer " + token}
    URL = self.baseURL + endpoint
    r = requests.get(URL, headers=head)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_teams = get_teams

# This endpoint allows a list of projects to be viewed by a user
def get_projects(self, token, teamid):
    endpoint = "project/getProjects"
    URL = self.baseURL + endpoint
    head = {"Authorization": "Bearer " + token}
    ids = {"team_id": teamid}

    r = requests.get(URL, headers=head, params=ids)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json_data = json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    # try:
    json_data = json.loads(r.content)
    meta_data = json_data["meta"]
    # except KeyError:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     error_code = json.loads(r.content)
    #     error_code = error_code["code"]

    #     print(f"Error {error_code}: {error_message}")
    # return
    total_count = meta_data["total_count"]
    updated_req = {"team_id": teamid, "limit": total_count}
    r = requests.get(URL, headers=head, params=updated_req)
    dictionary_data = json.loads(r.content)
    return dictionary_data
    # content = json_data["data"]
    # print(content)
    # for i in content:
    #     print(f'{i["name"]} and id: {i["id"]} \n')


IonChannel.get_projects = get_projects

# This endpoint allows an analysis to be run on a selected project
def analyze_project(self, token, teamid, projectid, branch=None):
    endpoint = "scanner/analyzeProject"
    head = {"Authorization": "Bearer " + token}
    if branch != 0:
        json_data = json.dumps(
            {"team_id": teamid, "project_id": projectid, "branch": branch}
        )
    else:
        json_data = json.dumps({"team_id": teamid, "project_id": projectid})
    URL = self.baseURL + endpoint
    r = requests.post(URL, headers=head, data=json_data)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.analyze_project = analyze_project

# This endpoint will return the status of an analysis
def analysis_status(self, token, teamid, projectid, analysisid):
    endpoint = "scanner/getAnalysisStatus"
    head = {"Authorization": "Bearer " + token}
    parameters = {"team_id": teamid, "project_id": projectid, "id": analysisid}
    URL = self.baseURL + endpoint
    r = requests.get(URL, headers=head, params=parameters)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    json_data = json.loads(r.content)
    content = json_data["data"]
    status = content["status"]
    # print(json_data)
    # print(f"In function status: {status}")
    return status
    # return r.content


IonChannel.analysis_status = analysis_status

# This endpoint will return raw analysis data
def get_analysis(self, token, teamid, projectid, analysisid):
    endpoint = "animal/getAnalysis"
    head = {"Authorization": "Bearer " + token}
    parameters = {"team_id": teamid, "project_id": projectid, "id": analysisid}
    URL = self.baseURL + endpoint
    r = requests.get(URL, headers=head, params=parameters)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_analysis = get_analysis

# This endpoint will get the data about an applied ruleset
def get_applied_ruleset(self, token, teamid, projectid, analysisid):
    endpoint = "ruleset/getAppliedRulesetForProject"
    head = {"Authorization": "Bearer " + token}
    parameters = {"team_id": teamid, "project_id": projectid, "analysis_id": analysisid}
    URL = self.baseURL + endpoint
    r = requests.get(URL, headers=head, params=parameters)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_applied_ruleset = get_applied_ruleset

# This endpoint will get information regarding a specific ruleset
def get_ruleset(self, token, teamid, rulesetid):
    endpoint = "ruleset/getRuleset"
    head = {"Authorization": "Bearer " + token}
    parameters = {"team_id": teamid, "id": rulesetid}
    URL = self.baseURL + endpoint
    r = requests.get(URL, headers=head, params=parameters)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.get_ruleset = get_ruleset


# This endpoint will create a project object
def create_project(self, token, teamid, project):
    endpoint = "project/createProject"
    head = {"Authorization": "Bearer " + token}
    project["team_id"] = teamid

    json_data = json.dumps(project)
    URL = self.baseURL + endpoint
    r = requests.post(URL, headers=head, data=json_data)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.create_project = create_project

# This endpoint will update a project and its contents based on the values within the JSON project parameter,
# also handles the nauture of the project - whether it should be archived or not, add "active" setting (boolean) to JSON
# object as either True or False depending on whether the project needs to be archived or not
def update_project(self, token, teamid, project):
    endpoint = "project/updateProject"
    head = {"Authorization": "Bearer " + token}
    project["team_id"] = teamid

    # archive = input(
    #     "Would you like to archive this project? (Press 'y' for yes or 'n' for no): "
    # )
    # if archive == "y":
    #     project["active"] = False

    json_data = json.dumps(project)
    URL = self.baseURL + endpoint
    r = requests.put(URL, headers=head, data=json_data)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code

    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.update_project = update_project


def add_scan(self, token, analysisid, teamid, projectid, param_value, scan="coverage"):
    endpoint = "scanner/addScanResult"
    head = {"Authorization": "Bearer " + token}
    URL = self.baseURL + endpoint
    json_data = json.dumps(
        {
            "team_id": teamid,
            "project_id": projectid,
            "analysis_id": analysisid,
            "scan_type": scan,
            "status": "accepted",
            "results": {"value": param_value},
        }
    )
    r = requests.post(URL, headers=head, data=json_data)
    check = response_handler(r)
    if check != 0:
        return -1
    # code = r.status_code
    # try:
    #     json.loads(r.content)
    # except JSONDecodeError:
    #     print("Error: Invalid Request")
    #     return

    # if code < 200 or code >= 300:
    #     error_message = json.loads(r.content)
    #     error_message = error_message["message"]
    #     print(f"Error {code}: {error_message}")
    #     return
    dictionary_data = json.loads(r.content)
    return dictionary_data


IonChannel.add_scan = add_scan

# def scan_report(self, token, analysisid, teamid, projectid):
#     endpoint = 'animal/findScans'
#     head = {'Authorization': 'Bearer ' + token}
#     URL = self.baseURL + endpoint
#     parameters = {'scan_id': analysisid}
#     r = requests.get(URL, headers=head, params=parameters)

#     return r.text
# IonChannel.scan_report = scan_report


# This is a test commit to ensure everything is working
# This is another modified test commit for build pipeline
