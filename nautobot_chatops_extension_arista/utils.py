"""Utilities for cloudvision chatbot"""
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cvprac.cvp_client import CvpClient
import os

fullpath = os.path.abspath(__file__)
directory = os.path.dirname(fullpath)

TOKEN = os.getenv("NAUTOBOT_CHATOPS_CVP_TOKEN")
API_SERVER_ADDR = "apiserver.arista.io:443"
TOKEN_FILE_PATH = f"{directory}/token.txt"

CVP_LOGO_PATH = "cloudvision/CloudvisionLogoSquare.png"
CVP_LOGO_ALT = "Cloudvision Logo"


def cloudvision_logo(dispatcher):
    """Construct an image_element containing the locally hosted CVP logo"""
    return dispatcher.image_element(dispatcher.static_url(CVP_LOGO_PATH), alt_text=CVP_LOGO_ALT)


def connect_cvp():
    clnt = CvpClient()
    clnt.connect(["www.arista.io"], username="", password="", is_cvaas=True, api_token=TOKEN)
    return clnt


def get_cloudvision_container_devices(container_name):
    """Get devices from specified container"""
    clnt = connect_cvp()
    result = clnt.api.get_devices_in_container(container_name)
    return result


def get_cloudvision_containers():
    """Get list of all containers from CVP"""
    clnt = connect_cvp()
    result = clnt.api.get_containers()
    return result["data"]


def get_cloudvision_configlets_names():
    """Get name of configlets"""
    clnt = connect_cvp()
    result = clnt.api.get_configlets()
    return result["data"]


def get_configlet_config(configlet_name):
    """Get configlet config lines"""
    clnt = connect_cvp()
    result = clnt.api.get_configlet_by_name(configlet_name)
    return result["config"]


def get_cloudvision_devices_all():
    """Get all devices in Cloudvision"""
    clnt = connect_cvp()
    result = clnt.get("/inventory/devices")
    return result


def get_cloudvsion_devices_all_resource():
    """Get all devices in Cloudvision via resource API"""
    clnt = connect_cvp()
    dev_url = "/api/resources/inventory/v1/Device/all"
    devices_data = clnt.get(dev_url)
    devices = []
    for device in devices_data["data"]:
        try:
            if device["result"]["value"]["streamingStatus"] == "STREAMING_STATUS_ACTIVE":
                devices.append(device)
        # pass on archived datasets
        except KeyError as e:
            continue
    return devices


def get_cloudvision_devices_by_sn(sn):
    """Get a device hostname given a device id."""
    clnt = connect_cvp()
    url = "/api/resources/inventory/v1/Device/all"
    device_data = clnt.get(url)
    for device in device_data["data"]:
        try:
            if device["result"]["value"]["key"]["deviceId"] == sn:
                return device["result"]["value"]["hostname"]
        except KeyError as e:
            continue


def get_device_id_from_hostname(hostname):
    """Get a device id given a hostname."""
    clnt = connect_cvp()
    url = "/api/resources/inventory/v1/Device/all"
    device_data = clnt.get(url)
    for device in device_data["data"]:
        try:
            if (
                device["result"]["value"]["streamingStatus"] == "STREAMING_STATUS_ACTIVE"
                and device["result"]["value"]["hostname"] == hostname
            ):
                return device["result"]["value"]["key"]["deviceId"]
        except KeyError as e:
            continue


def get_device_running_configuration(device_mac_address):
    """Get running configuration of device"""
    clnt = connect_cvp()
    result = clnt.api.get_device_configuration(device_mac_address)
    return result


def get_cloudvision_tasks():
    """Get all tasks from cloudvision"""
    clnt = connect_cvp()
    result = clnt.api.get_tasks()
    return result["data"]


def get_cloudvision_task_logs(single_task_cc_id, single_task_stage_id):
    """Get logs from task specified"""
    log_list = []
    clnt = connect_cvp()
    result = clnt.api.get_audit_logs_by_id(single_task_cc_id, single_task_stage_id)
    for log_entry in result["data"]:
        log_list.insert(0, log_entry["activity"])
    return log_list


def prompt_for_device_or_container(action_id, help_text, dispatcher):
    """Prompt user to select device or container."""
    choices = [("Container", "container"), ("Device", "device")]
    return dispatcher.prompt_from_menu(action_id, help_text, choices)


def prompt_for_image_bundle_name_or_all(action_id, help_text, dispatcher):
    """Prompt user to select device or container or `all`."""
    choices = [("Bundle", "bundle"), ("All", "all")]
    return dispatcher.prompt_from_menu(action_id, help_text, choices)


def get_container_id_by_name(name):
    """Get container id."""
    clnt = connect_cvp()
    result = clnt.get(f"/inventory/containers?name={name}")
    return result[0]["Key"]


def get_applied_configlets_container_id(container_id):
    """Get a list of applied configlets."""
    clnt = connect_cvp()
    result = clnt.api.get_configlets_by_container_id(container_id)
    return [configlet["name"] for configlet in result["configletList"]]


def get_applied_configlets_device_id(device_name, device_list):
    """Get configlets applied to device."""
    clnt = connect_cvp()
    chosen_device = next(device for device in device_list if device["hostname"] == device_name)
    result = clnt.api.get_configlets_by_device_id(chosen_device["systemMacAddress"])
    return [configlet["name"] for configlet in result]


def prompt_for_events_filter(action_id, help_text, dispatcher):
    """Prompt user to select how to filter events."""
    choices = [
        ("device", "device"),
        ("severity", "severity"),
        ("type", "type"),
        ("all", "all"),
    ]
    return dispatcher.prompt_from_menu(action_id, help_text, choices)


def get_severity_choices():
    """Severity levels used for get-events command."""
    choices = [
        ("UNSPECIFIED", "UNSPECIFIED"),
        ("INFO", "INFO"),
        ("WARNING", "WARNING"),
        ("ERROR", "ERROR"),
        ("CRITICAL", "CRITICAL"),
    ]
    return choices


def get_severity_events(filter_value):
    """Gets events based on severity filter."""
    clnt = connect_cvp()
    payload = {"partialEqFilter": [{"severity": filter_value}]}
    event_url = "/api/resources/event/v1/Event/all"
    result = clnt.post(event_url, data=payload)
    return result["data"]


def get_active_events_data(apiserverAddr=API_SERVER_ADDR, token=TOKEN_FILE_PATH, certs=None, key=None, ca=None):
    """Gets a list of active event types from CVP."""
    current_list = []
    pathElts = [
        "events",
        "activeEvents",
    ]
    query = [create_query([(pathElts, [])], "analytics")]
    events = []
    with GRPCClient(apiserverAddr, token=token, key=key, ca=ca, certs=certs) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                for info in notif["updates"].values():
                    single_event = {}
                    single_event["title"] = info["title"]
                    single_event["severity"] = info["severity"]
                    single_event["description"] = info["description"]
                    single_event["deviceId"] = get_cloudvision_devices_by_sn(info["data"]["deviceId"])
                    events.append(single_event)
    return events


def get_active_events_data_filter(
    filter_type,
    filter_value,
    start_time,
    end_time,
    apiserverAddr=API_SERVER_ADDR,
    token=TOKEN_FILE_PATH,
    certs=None,
    key=None,
    ca=None,
):
    """Gets a list of active event types from CVP in a specific time range."""
    start = Timestamp()
    start_ts = datetime.fromisoformat(start_time)
    start.FromDatetime(start_ts)

    end = Timestamp()
    end_ts = datetime.fromisoformat(end_time)
    end.FromDatetime(end_ts)

    current_list = []
    pathElts = [
        "events",
        "activeEvents",
    ]
    query = [create_query([(pathElts, [])], "analytics")]
    events = []
    with GRPCClient(apiserverAddr, token=token, key=key, ca=ca, certs=certs) as client:
        for batch in client.get(query, start=start, end=end):
            for notif in batch["notifications"]:
                for info in notif["updates"].values():
                    single_event = {}
                    single_event["title"] = info["title"]
                    single_event["severity"] = info["severity"]
                    single_event["description"] = info["description"]
                    single_event["deviceId"] = get_cloudvision_devices_by_sn(info["data"]["deviceId"])
                    if filter_type == "severity":
                        if single_event["severity"] == filter_value:
                            events.append(single_event)
                    elif filter_type == "device":
                        if single_event["deviceId"] == filter_value:
                            events.append(single_event)
                    elif filter_type == "type":
                        if info["eventType"] == filter_value:
                            events.append(single_event)

    return events


def get_active_severity_types(apiserverAddr=API_SERVER_ADDR, token=TOKEN_FILE_PATH, certs=None, key=None, ca=None):
    """Gets a list of active event types from CVP."""
    current_list = []
    pathElts = [
        "events",
        "type",
    ]
    query = [create_query([(pathElts, [])], "analytics")]
    event_types = []
    with GRPCClient(apiserverAddr, token=token, key=key, ca=ca, certs=certs) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                for info in notif["updates"]:
                    event_types.append(info)
    return event_types


def get_applied_tags(device_id):
    """Get tags applied to device by device id."""
    clnt = connect_cvp()
    tag_url = "/api/resources/tag/v1/InterfaceTagAssignmentConfig/all"
    payload = {"partialEqFilter": [{"key": {"deviceId": device_id}}]}
    result = clnt.post(tag_url, data=payload)
    return result


def get_image_bundles(image_bundle_name=None):
    """Get image bundle from cloudvision"""
    clnt = connect_cvp()
    result = clnt.api.get_image_bundles()
    return result["data"]


def get_images(image_bundle_name=None):
    """Get images that are on Cloudvision."""
    clnt = connect_cvp()
    if not image_bundle_name:
        result = clnt.api.get_images()
        return result["data"]
    else:
        combined_applied = {}
        url_containers = (
            f"/image/getImageBundleAppliedContainers.do?imageName={image_bundle_name}&startIndex=0&endIndex=0"
        )
        url_devices = f"/image/getImageBundleAppliedDevices.do?imageName={image_bundle_name}&startIndex=0&endIndex=0"
        result_containers = clnt.get(url_containers)
        result_devices = clnt.get(url_devices)
        combined_applied["containers"] = result_containers["data"]
        combined_applied["devices"] = result_devices["data"]
        return combined_applied


def get_device_bugs_data(
    device_id, apiserverAddr=API_SERVER_ADDR, token=TOKEN_FILE_PATH, certs=None, key=None, ca=None
):
    """Get bugs associated with a device."""
    pathElts = ["tags", "BugAlerts", "devices"]
    query = [create_query([(pathElts, [])], "analytics")]
    bugs = []
    with GRPCClient(apiserverAddr, token=token, key=key, ca=ca, certs=certs) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                if notif["updates"].get(device_id):
                    return notif["updates"].get(device_id)
    return bugs


def get_bug_info(bug_id, apiserverAddr=API_SERVER_ADDR, token=TOKEN_FILE_PATH):
    """Get detailed information about a bug given its identifier."""
    pathElts = [
        "BugAlerts",
        "bugs",
        int(bug_id),
    ]
    query = [create_query([(pathElts, [])], "analytics")]
    bug_info = {}
    with GRPCClient(apiserverAddr, token=token) as client:
        for batch in client.get(query):
            for notif in batch["notifications"]:
                bug_info["identifier"] = bug_id
                bug_info["summary"] = notif["updates"]["alertNote"]
                bug_info["severity"] = notif["updates"]["severity"]
                bug_info["versions_fixed"] = notif["updates"]["versionFixed"]
    return bug_info
