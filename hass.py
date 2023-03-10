import os, json
try:
    from requests import get, post
except ModuleNotFoundError:
    os.system("python -m pip install requests")
    from requests import get, post
try:
    import yaml
except ModuleNotFoundError:
    os.system("python -m pip install PyYAML")
    import yaml


dirname = os.path.dirname(__file__)
tokenpath = os.path.join(dirname, 'Token.txt')

hass_url = "http://192.168.2.214:8123"

with open(tokenpath, 'r') as tokenfile:
    headers = {
        "Authorization": "Bearer " + tokenfile.read(),
        "content-type": "application/json",
    }

def call_service(service, data={}):
    """Calls a Home Assistant Service (obviously).\nService: The service that should be called, in the form domain.service\nData: A dictionary of data\n"""
    split_service = service.split(".")
    domain = split_service[0]
    service = split_service[1]
    url = hass_url + "/api/services/" + domain + "/" + service
    response = post(url, headers=headers, json=data)
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = "Success!"
    elif code == 404:
        message = "Not found. Wrong service?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def fire_event(event, data={}):
    url = hass_url + "/api/events/" + event
    response = post(url, headers=headers, json=data)
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = "Success!"
    elif code == 404:
        message = "Not found. Wrong event?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def render_template(template):
    url = hass_url + "/api/template"
    response = post(url, headers=headers, json={'template': template})
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = response.text
    elif code == 404:
        message = "Not found. Wrong Home Assistant URL?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def is_service(service):
    split_service = service.split(".")
    domain = split_service[0]
    service = split_service[1]
    domains = get(hass_url + "/api/services", headers=headers)
    for d in json.loads(domains.text):
        if d['domain'] == domain:
            for s in d['services']:
                if s == service:
                    return True
    return False


def get_state(entity_id, print_result=None):
    url = hass_url + "/api/states/" + entity_id
    response = get(url, headers=headers)
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = json.loads(response.text)
        if str(print_result).lower() == 'json' and print_result:
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4))
        elif str(print_result).lower() == 'yaml' and print_result:
            print(yaml.dump(json.loads(response.text), default_flow_style=False))
    elif code == 404:
        message = "Not found. Wrong entity ID?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def get_history(entities=None, start_time='', end_time='', minimal=False, significant_only=False, print_result=None):
    url = hass_url + "/api/history/period" + ("/" if start_time else "") + start_time
    data = {"filter_entity_id": entities, "end_time": end_time, "minimal_response": minimal, "significant_changes_only": significant_only}
    if not entities:
        print("This could take some time...")
    response = get(url, headers=headers, json=data)
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = json.loads(response.text)
        if str(print_result).lower() == 'json':
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4))
        elif str(print_result).lower() == 'yaml':
            print(yaml.dump(json.loads(response.text), default_flow_style=False))
    elif code == 404:
        message = "Not found. Wrong entity ID or time?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def get_logbook(entities=None, start_time='', end_time='', print_result=None):
    url = hass_url + "/api/logbook" + ("/" if start_time else "") + start_time
    data = {"filter_entity_id": entities, "end_time": end_time}
    if not entities:
        print("This could take some time...")
    response = get(url, headers=headers, json=data)
    code = int(response.status_code)
    message = ""
    if code in range(200, 300):
        message = json.loads(response.text)
        if str(print_result).lower() == 'json':
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4))
        elif str(print_result).lower() == 'yaml':
            print(yaml.dump(json.loads(response.text), default_flow_style=False))
    elif code == 404:
        message = "Not found. Wrong entity ID or time?"
    elif code == 400:
        message = "Bad request. Syntax error?"
    return message

def set_hass_url(new_url):
    global hass_url
    hass_url = new_url

def yamlify(data):
    if type(data) == str:
        return yaml.dump(json.loads(data))
    else:
        return yaml.dump(data)
    
def jsonify(data):
    if type(data) == str:
        return json.dumps(yaml.load(data))
    else:
        return json.dumps(data)

def test(print_result=True):
    url = hass_url+"/api/"
    response = get(url, headers=headers)
    if print_result:
        print(response.text)
    return response.text

#get_logbook(print_result='yaml')
