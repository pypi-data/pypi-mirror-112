"""
Python module for interacting with the Morpheus API

"""

import json
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import requests

def import_environment_details(path):
    """ import environment details """
    print("Loading environment data from: " + path)
    data = open(path, "r").read()
    environment_data = json.loads(data)
    return environment_data

def import_token_from_disk(base_uri, path, ssl):
    """ import token from disk and validates age """
    print("Loading accessToken from: " + path)
    data = open(path, "r").read()
    json_data = json.loads(data)
    token_validity_days = check_bearer(base_uri, json_data["access_token"], ssl)
    if isinstance(token_validity_days, int):
        if token_validity_days < 7: #if token expires in less than 1 week we will renew it
            print("Access Token expires soon, refreshing it.")
            response = refresh_bearer(base_uri, json_data["refresh_token"], ssl)
            file = open(path, "w")
            json.dump(response, file)
            file.close()
            bearer_token = response["access_token"]
        else:
            print("Access Token is still valid")
            bearer_token = json_data["access_token"]
    else:
        print("Token error encountered:")
        for item in token_validity_days:
            print("  " + str(item))
            print("    " + str(token_validity_days[item]))
        sys.exit(1)
    return bearer_token

def import_token_from_cypher(base_uri, input_secret, token, ssl):
    """ import token from cypher and validates age """
    print("Loading access_token from: " + input_secret)
    data = invoke_api(
        base_uri + "/api/cypher/" + input_secret,
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    json_data = data["data"]
    token_validity_days = check_bearer(base_uri, json_data["access_token"], ssl)
    if isinstance(token_validity_days, int):
        if token_validity_days < 7: #if token expires in less than 1 week we will renew it
            print("Access Token expires soon, refreshing it.")
            response = refresh_bearer(base_uri, json_data["refresh_token"], ssl)
            bearer_token = response["access_token"]
            commit_token_to_cypher(base_uri, input_secret, response, token, ssl)
        else:
            print("Access Token is still valid")
            bearer_token = json_data["access_token"]
    else:
        print("Token error encountered:")
        for item in token_validity_days:
            print("  " + str(item))
            print("    " + str(token_validity_days[item]))
        bearer_token = None
    return bearer_token

def commit_token_to_cypher(base_uri, input_secret, input_data, token, ssl):
    """ updates cypher secret with new token data """
    print("Updating access_token at: " + input_secret)
    response = invoke_api(
        base_uri + "/api/cypher/" + input_secret,
        "Bearer " + token,
        "put",
        input_data,
        ssl
    )
    if response["success"]:
        return response["success"]
    print("Unhandled error encountered:")
    for item in response:
        print("  " + str(item))
        print("    " + str(response[item]))
    sys.exit(1)

def check_bearer(base_uri, token, ssl):
    """ By default, access tokens are valid for 1 year """
    today = datetime.today().strftime("%Y-%m-%d")
    full_uri = base_uri + "/api/user-settings/"
    print("Checking token validity.")
    token_response = requests.get(
        full_uri,
        headers={"Authorization": "Bearer " + token},
        verify=ssl
    )
    token_response_json = token_response.json()
    try:
        token_response_json["accessTokens"]
    except KeyError as err:
        return token_response_json
    for data in token_response_json["accessTokens"]:
        masked_token_split = data["maskedAccessToken"].split("-")[0]
        if masked_token_split == token[0:7]:
            print("Token found.")
            token_expiration = data["expiration"]
    try:
        token_expiration
    except NameError as err:
        sys.exit("Token NOT found." + str(err.args))
    token_validity_days = (
        datetime.strptime(
            token_expiration.split("T")[0],
            "%Y-%m-%d"
        ) - \
        datetime.strptime(
            today,
            "%Y-%m-%d"
        )
    ).days
    print("Token is valid for: " + str(token_validity_days) + " days.")
    return token_validity_days

def refresh_bearer(base_uri, token, ssl):
    """ Refresh the access token with the refresh token """
    full_uri = base_uri + \
        "/oauth/token?grant_type=refresh_token&scope=write&client_id=morph-api"
    print("Refreshing token through url: " + base_uri)
    response = requests.post(
        full_uri,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"refresh_token": token},
        verify=ssl
    )
    print(response.json())
    return response.json()

def create_bearer(full_uri, user_name, password, ssl):
    """ Returns json body containing access and refresh tokens """
    print("Generating token: " + full_uri)
    response = requests.post(
        full_uri,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": user_name, "password": password},
        verify=ssl
    )
    if response.status_code == 200:
        return response.json()
    print("Request failed with status code: " + str(response.status_code))
    print("Server returned: " + str(response.text))
    sys.exit(1)

def invoke_api(
        full_uri,
        token,
        method,
        request_body,
        ssl,
        data_type="json",
        content_type="application/json",
        debug=False,
        print_query=True
    ):
    """ Calls request method based on input """
    if print_query:
        print(method.upper() + " : " + full_uri)
    headers = {
        "Content-Type": content_type,
        "Authorization": token
    }
    if debug:
        print(
            "DEBUG: " +
            "    token: " + token +
            "    method: " + method +
            "    request_body: " + request_body +
            "    ssl: " + str(ssl) +
            "    data_type: " + data_type +
            "    content_type: " + content_type +
            "    headers: " + str(headers)
        )
    request = getattr(requests, method)
    if request_body is None:
        response = request(
            full_uri,
            headers=headers,
            verify=ssl
        )
    else:
        if content_type == "application/json":
            payload = json.dumps(request_body).encode("utf-8")
        else:
            payload = request_body
        response = request(
            full_uri,
            headers=headers,
            data=payload,
            verify=ssl
        )
    if response.status_code == 200:
        if data_type == "json":
            return response.json()
        return response
    print("Request failed with status code: " + str(response.status_code))
    print("Server returned: " + str(response.text))
    sys.exit(1)

def get_folder_data(folder):
    """ Extracts existing permissions on folder """
    folder_data = {}
    folder_data["folderId"] = folder["id"]
    folder_data["rootDefaultFolder"] = folder["defaultFolder"]
    folder_data["rootDefaultStore"] = folder["defaultStore"]
    folder_tenants = []
    default_store = []
    default_target = []
    for tenant in folder["tenants"]:
        folder_tenants.insert(len(folder_tenants), tenant["id"])
        if tenant["defaultStore"]:
            default_store.insert(len(default_store), tenant["id"])
        if tenant["defaultTarget"]:
            default_target.insert(len(default_target), tenant["id"])
    folder_data["folderTenants"] = folder_tenants
    folder_data["defaultStore"] = default_store
    folder_data["defaultTarget"] = default_target
    return folder_data

def update_folder_body(folder_data, tenant_default_store, tenant_default_target, new_tenant):
    """
    Creates the json body to update the folder permissions
    Takes the existing permission data and appends the new tenant's Id
    tenant_default_store in GUI as "Image Target"
    tenant_default_target in GUI as "Default"
    """
    folder_data["folderTenants"].insert(len(folder_data["folderTenants"]), new_tenant)
    tenant_perms = {}
    tenant_perms.update({"accounts": folder_data["folderTenants"]})
    if tenant_default_store:
        folder_data["defaultStore"].insert(len(folder_data["defaultStore"]), new_tenant)
        tenant_perms.update({"defaultStore": folder_data["defaultStore"]})
    else:
        if folder_data["defaultStore"] != []:
            tenant_perms.update({"defaultStore": folder_data["defaultStore"]})
    if tenant_default_target:
        folder_data["defaultTarget"].insert(len(folder_data["defaultTarget"]), new_tenant)
        tenant_perms.update({"defaultTarget": folder_data["defaultTarget"]})
    else:
        if folder_data["defaultTarget"] != []:
            tenant_perms.update({"defaultTarget": folder_data["defaultTarget"]})
    temp_body = {}
    temp_body.update({"active" : True})
    temp_body.update({"tenantPermissions" : tenant_perms})
    temp_body.update({"defaultFolder" : folder_data["rootDefaultFolder"]})
    temp_body.update({"defaultImage" : folder_data["rootDefaultStore"]})
    body = {}
    body.update({"folder": temp_body})
    return body

def check_tenant_exists(tenants, student):
    """ Validates the tenant exists and returns dictionary of tenant info  """
    print("student: " + student)
    for tenant in tenants["accounts"]:
        if tenant["name"] == student:
            tenant_info = {}
            tenant_info.update({"name": tenant["name"]})
            tenant_info.update({"id": tenant["id"]})
            tenant_info.update({"active": tenant["active"]})
    if "tenant_info" not in locals():
        return False
    return tenant_info

def get_data_to_provision_instance(base_uri, token, instance_details, cloud_id, ssl):
    """
    get instance types and layouts
    get service plan and network type
    return details necessary to provision instance
    """
    get_instance_types = invoke_api(
        base_uri + "/api/instance-types/",
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    for i_type in get_instance_types["instanceTypes"]:
        if i_type["name"] == instance_details["INSTANCE_TO_PROVISION"]:
            instance_code = i_type["code"]
            instance_type = i_type
            break
    for instance_layout in instance_type["instanceTypeLayouts"]:
        if instance_layout["name"] == instance_details["INSTANCE_LAYOUT"]:
            print("Found Layout: " + str(instance_layout))
            get_layout_detail = invoke_api(
                base_uri + "/api/library/layouts/" + str(instance_layout["id"]),
                "Bearer " + token,
                "get",
                None,
                ssl
            )
            if get_layout_detail["instanceTypeLayout"]["instanceVersion"] == \
                    instance_details["INSTANCE_VERSION"]:
                layout_id = instance_layout["id"]
                print("Layout for version: " + str(instance_details["INSTANCE_VERSION"]) + \
                    " is: " + str(layout_id))
                break
    get_service_plans = invoke_api(
        base_uri + "/api/instances/service-plans/?zoneId=" + str(cloud_id) + \
            "&layoutId=" + str(layout_id),
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    for service_plan in get_service_plans["plans"]:
        if service_plan["name"] == instance_details["VM_SPEC"]:
            plan_id = service_plan["id"]
    get_network_options = invoke_api(
        base_uri + "/api/options/zoneNetworkOptions?zoneId=" + str(cloud_id) + \
            "&layoutId=" + str(layout_id),
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    for network_option in get_network_options["data"]["networkTypes"]:
        if network_option["name"] == instance_details["VM_NIC_TYPE"]:
            interface_id = network_option["id"]
    detail = {}
    detail.update({"instance_code": instance_code})
    detail.update({"layout_id": layout_id})
    detail.update({"plan_id": plan_id})
    detail.update({"interface_id": interface_id})
    return detail

def get_input_args():
    """
    gathers script inputs
    required input:
        number of students
    optional inputs:
        event password (randomly generated with Cypher if not provided)
        starting student (default: 1)
        tenant naming (default: hol-student)
        noconfirm delete
    stringxyz
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--number",
        required=True,
        type=int,
        action="store",
        help="Number of Students for the Event"
    )
    parser.add_argument(
        "-p", "--password",
        required=False,
        type=str,
        action="store",
        help="Password for the Event"
    )
    parser.add_argument(
        "-s", "--start",
        required=False,
        type=int,
        action="store",
        default=1,
        help="Optional: Student Number to Start With (default: 1)"
    )
    parser.add_argument(
        "-t", "--name",
        required=False,
        type=str,
        action="store",
        default="hol-student",
        help="Optional: Tenant Naming to Use (default: hol-student)"
    )
    parser.add_argument(
        "-f", "--false",
        required=False,
        action="store_false",
        default=True,
        help="Optional: Use this Switch to Disable Confirmation of Deletions"
    )
    parser.add_argument(
        "-x", "--stringx",
        required=False,
        type=str,
        action="store",
        help="Optional: Additional String Input"
    )
    parser.add_argument(
        "-y", "--stringy",
        required=False,
        type=str,
        action="store",
        help="Optional: Additional String Input"
    )
    parser.add_argument(
        "-z", "--stringz",
        required=False,
        type=str,
        action="store",
        help="Optional: Additional String Input"
    )
    args = parser.parse_args()
    return args

def send_hol_build_summary(send_to, subject, data, email_from, smtp_server):
    """
    takes the data input from the build script
    generates an html email and sends it
    """
    def build_html_table(base_html, in_data):
        """ takes a base input and creates table """
        base_html += "<table>\n<tr class=\"odd\">"
        top_key = list(in_data.keys())[0]
        if top_key != "build_info":
            base_html += "<th>%s</th>" % "Tenant"
        for sub_key in in_data[top_key]:
            base_html += "<th>%s</th>" % sub_key
        base_html += "</tr>\n"
        return base_html
    def build_html_row(base_html, in_data):
        """ takes a base input and returns """
        count = 0
        for key in in_data:
            if (count & 1) == 1:
                html_class = "odd"
            if (count & 1) == 0:
                html_class = "even"
            base_html += "<tr class=\"%s\">" % html_class
            if key != "build_info":
                base_html += "<td>%s</td>" % key
            for value in in_data[key]:
                base_html += "<td>%s</td>" % in_data[key][value]
            count += 1
        base_html += "</tr>\n</table><br>\n"
        return base_html
    html = """\
        <!DOCTYPE html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
            body {
                color:#333333;
                font-family:Calibri,Tahoma,arial,verdana;
                font-size: 11pt;
            }
            table {
                border-collapse:collapse;
            }
            th {
                text-align:left;
                font-weight:bold;
                color:#eeeeee;
                background-color:#333333;
                border:1px solid black;
                padding:5px;
            }
            td {
                padding:5px;
                border:1px solid black;
            }
            .odd { background-color:#ffffff; }
            .even { background-color:#dddddd; }
        </style>
        </head>
        <body>
    """
    for item in data:
        html += "<h3>%s</h3>\n" % item
        html = build_html_table(html, data[item])
        html = build_html_row(html, data[item])
    html += "</body>\n</html>"
    message = MIMEText(html, "html")
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = ", ".join(send_to)
    smtp = smtplib.SMTP(smtp_server)
    smtp.sendmail(email_from, send_to, message.as_string())
    smtp.quit()

def filter_dict(input_dict, input_filter, input_criterion, return_field=None):
    """ filter dict based on input """
    filtered_list = []
    for item in input_dict:
        if input_filter in item[input_criterion]:
            if return_field is not None:
                filtered_list.append(item[return_field])
            else:
                filtered_list.append(item)
    return filtered_list

def update_price_set(input_uri, input_price_ids, input_price_set, token, ssl):
    """ update a price set with input prices """
    price_array = []
    for price_id in input_price_ids:
        price_array.append({"id" : price_id})
    body = {"priceSet" : {"prices" : price_array}}
    invoke_api(
        input_uri + "/api/price-sets/" + str(input_price_set),
        "Bearer " + token,
        "put",
        body,
        ssl
    )

def get_resource_pool_id(input_uri, input_zones, input_pool_name, token, ssl):
    """ searches through zones to find the one that contains the desired resource pool """
    pool_id = None
    for zone in input_zones["zones"]:
        get_zone_pool_id = invoke_api(
            input_uri + "/api/zones/" + str(zone["id"]) + "/resource-pools/",
            "Bearer " + token,
            "get",
            None,
            ssl,
            print_query=False
        )
        for pool in get_zone_pool_id["resourcePools"]:
            if pool["name"] == input_pool_name:
                pool_id = pool["id"]
    return pool_id

def get_item_to_schedule(input_uri, input_name, input_type, input_max, token, ssl):
    """ returns the id for either a task or taskset based on input """
    if input_type.lower() == "workflow":
        path = "task-sets"
        value = "taskSets"
    else:
        path = "tasks"
        value = "tasks"
    get_items = invoke_api(
        input_uri + "/api/" + path + "/?max=" + str(input_max),
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    for item in get_items[value]:
        if item["name"] == input_name:
            item_id = item["id"]
            break
    return item_id

def create_option_list_data_set(input_array):
    """ takes input array and formats it for morpheus api """
    data_set = ""
    for item in input_array:
        if isinstance(item["name"], float):
            data_set += "'" + str(int(item["name"])) + "'"
        else:
            data_set += item["name"]
        data_set += ","
        data_set += str(item["value"])
        data_set += "\r\n"
    return data_set

def convert_xlsx_sheet_into_json(input_sheet, exclude_string):
    """ takes input xlsx sheet from xlrd and returns it as json """
    option_list_temp = []
    for column in range(input_sheet.ncols):
        item_set = {}
        item_set.update({"index" : column})
        item_set.update({"name" : input_sheet.cell_value(0, column)})
        value_set = []
        for cell in range(input_sheet.nrows):
            value = {}
            if input_sheet.cell_value(cell, column):
                cell_data = input_sheet.cell_value(cell, column)
                if cell_data != item_set["name"]:
                    value.update({"name" : cell_data})
                    value.update({"value" : cell_data})
                    value_set.append(value)
        if value_set[0]["name"] != exclude_string:
            item_set.update({"values" : value_set})
            option_list_temp.append(item_set)
    return option_list_temp

def validate_naming(
        input_uri,
        input_type,
        input_valid_names,
        input_max,
        token,
        ssl,
        purge_invalid=False
    ):
    """ removes and tasks or workflows that violate the valid names provided """
    if input_type.lower() == "workflow":
        path = "task-sets"
        value = "taskSets"
    else:
        path = "tasks"
        value = "tasks"
    get_items = invoke_api(
        input_uri + "/api/" + path + "/?max=" + str(input_max),
        "Bearer " + token,
        "get",
        None,
        ssl
    )
    response = get_items.json()
    for data in response[value]:
        print("DEBUG:    TaskName: " + data["name"])
        current_task = data["name"][0:3].upper()
        if current_task not in input_valid_names:
            try:
                print(
                    "The following task was deleted due to voliation of naming convention: " +
                    data["name"])
                if purge_invalid:
                    requests.delete(
                        input_uri + "/api/" + path + "/" + str(data["id"]),
                        headers={"Authorization": "Bearer " + token},
                        params={"force": "true"},
                        verify=ssl
                    )
                else:
                    print("DEBUG:    Skipping Delete, purge_invalid set to False.")
            except:
                print("Couldn't delete the tasks")
        else:
            pass

def execute_task_on_instance(input_uri, input_type, in_server_id, in_task_id, token, ssl):
    """ executes a task on either a server or instance """
    if input_type.lower() == "server":
        target = "server"
    else:
        target = "instance"
    temp_body = {}
    temp_body.update({"targetType" : target})
    temp_body.update({target + "s" : [in_server_id]})
    body = {}
    body.update({"job": temp_body})
    print(body)
    get_instance = invoke_api(
        input_uri + "/api/tasks/" + str(in_task_id) + "/execute",
        "Bearer " + token,
        "post",
        body,
        ssl
    )
    return get_instance
