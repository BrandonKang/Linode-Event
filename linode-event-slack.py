import requests, json, time
from datetime import datetime
from enum import Enum, unique
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


@unique
class LinodeApis(str, Enum):
    event_list = "https://api.linode.com/v4/account/events"

#Replace these values with yours.
__slack_token__ = 'AAAAAAAAAAAAAAA'
__slack_channel__ = 'AAAAAAAAAAAAAAA'
__linode_token__ = 'AAAAAAAAAAAAAAA'
__slack_client__ = WebClient(token=__slack_token__)


def print_log(message: str):
    formatted_log = '[{0}]: {1}'.format(datetime.now(), message)
    print(formatted_log)


# slack_send_message('Check out this link at <https://www.google.com|Google>. Its pretty cool')
def slack_send_message(message):
    try:
        response = __slack_client__.chat_postMessage(
            channel=__slack_channel__,
            text=message
        )

        if response.status_code == 200:
            is_ok = response.data['ok'] if 'ok' in response.data else ''
            channel = response.data['channel'] if 'channel' in response.data else ''
            ts = response.data['ts'] if 'ts' in response.data else ''
            print_log("[slack_send_notification] successful: {0} - {1} - {2}".format(is_ok, channel, ts))
        else:
            print_log("[slack_send_notification] failed: {0}".format(response))
    except SlackApiError as error:
        print_log("[slack_send_notification] failed: {0}".format(error))


def slack_last_message() -> str:
    try:
        channel_history = __slack_client__.conversations_history(channel=__slack_channel__)
        if channel_history.status_code == 200:
            messages = list(channel_history.data['messages']) if channel_history.data is not None and 'messages' in channel_history.data else None
            if len(messages) > 0:
                last_message = messages[0]
                text = last_message['text'] if 'text' in last_message else None
                return str(text)
        else:
            print_log('[slack_last_message] has error: {0}'.format(channel_history.data))
    except SlackApiError as error:
        print_log("[slack_last_message] failed: {0}".format(error))

    return ''


def slack_send_events(events: list):
    print_log("[slack_send_events] start with {0} events".format(len(events)))

    events.sort(key=lambda e: e["id"])
    for event in events:
        action = event["action"] if "action" in event else None
        if action is None:
            print_log("Unexpected event without action: {0}".format(event))
            continue

        event_id = event["id"] if "id" in event else 0
        username = event["username"] if "username" in event else "anonymous"
        entity = event["entity"] if "entity" in event and event["entity"] is not None else {}
        secondary_entity = event["secondary_entity"] if "secondary_entity" in event and event["secondary_entity"] is not None else {}
        entity_label = entity["label"] if "label" in entity else "unknow_entity_label"
        entity_id = entity["id"] if "id" in entity else 0
        entity_type = entity["type"] if "type" in entity else "unknow"
        second_entity_label = secondary_entity["label"] if "label" in secondary_entity else "unknow_second_entity_label"
        # second_entity_id = secondary_entity["id"] if "id" in secondary_entity else 0
        second_entity_type = secondary_entity["type"] if "type" in secondary_entity else "unknow_second_entity_type"

        message = "{0} by {1}.".format(event["message"], username) if "message" in event and event["message"] != '' else None
        embeeded_link = None
        if entity_type is not None and entity_id is not None:
            match entity_type:
                case "linode":
                    embeeded_link = 'https://cloud.linode.com/linodes/{0}'.format(entity_id)
                case "nodebalancer":
                    embeeded_link = 'https://cloud.linode.com/nodebalancers/{0}/summary'.format(entity_id)
                case "ticket":
                    embeeded_link = 'https://cloud.linode.com/support/tickets/{0}'.format(entity_id)
                case 'user':
                    embeeded_link = 'https://cloud.linode.com/account/users/{0}/profile'.format(entity_id)
                case 'volume':
                    embeeded_link = 'https://cloud.linode.com/volumes/{0}'.format(entity_id)

        if embeeded_link is not None:
            entity_label = '<{0}|{1}>'.format(embeeded_link, entity_label)

        match action:
            case "user_create":
                message = 'User {0} has been created by {1}.'.format(
                    entity_label,
                    username
                )
            case "user_update":
                message = 'User {0} has been updated by {1}.'.format(
                    entity_label,
                    username
                )
            case "user_delete":
                message = 'User {0} has been deleted by {1}.'.format(
                    entity_label,
                    username
                )
            case "profile_update":
                message = 'Profile has been updated by {0}.'.format(username)
            case "linode_create":
                message = 'Linode {0} has been created by {1}.'.format(
                    entity_label,
                    username
                )
            case "linode_update":
                message = 'Linode {0} has been updated by {1}.'.format(
                    entity_label,
                    username
                )
            case "linode_reboot":
                message = 'Linode {0} has been rebooted with {1} {2} by {3}.'.format(
                    entity_label,
                    second_entity_type,
                    second_entity_label,
                    username
                )
            case "linode_boot":
                message = 'Linode {0} has been booted with {1} {2} by {3}.'.format(
                    entity_label,
                    second_entity_type,
                    second_entity_label,
                    username
                )
            case "linode_clone":
                message = 'Linode {0} has been cloned to {1} by {2}.'.format(
                    entity_label,
                    second_entity_label,
                    username
                )
            case "linode_addip":
                message = 'An IP has been added to {0} by {1}.'.format(
                    entity_label,
                    username
                )
            case "linode_shutdown":
                message = 'Linode {0} has been shut down by {1}.'.format(
                    entity_label,
                    username
                )
            case "linode_delete":
                message = 'Linode {0} has been deleted by {1}.'.format(
                    entity_label,
                    username
                )
            case "linode_config_create":
                message = 'Config {0} has been created on Linode {1} by {2}.'.format(
                    second_entity_label,
                    entity_label,
                    username
                )
            case "disk_create":
                message = 'Disk {0} has been added to Linode {1} by {2}.'.format(
                    second_entity_label,
                    entity_label,
                    username
                )
            case "nodebalancer_create":
                message = 'A node on NodeBalancer {0} has been created by {1}.'.format(
                    entity_label,
                    username
                )
            case "nodebalancer_delete":
                message = 'A node on NodeBalancer {0} has been deleteed by {1}.'.format(
                    entity_label,
                    username
                )
            case "nodebalancer_node_create":
                message = 'A node on NodeBalancer {0} has been created by {1}.'.format(
                    entity_label,
                    username
                )
            case "nodebalancer_config_update":
                message = 'A node on NodeBalancer {0} has been updated by {1}.'.format(
                    entity_label,
                    username
                )
            case "nodebalancer_node_delete":
                message = 'A node on NodeBalancer {0} has been deleted by {1}.'.format(
                    entity_label,
                    username
                )
            case "user_ssh_key_add":
                message = 'An SSH key has been added to your profile by {0}.'.format(username)
            case "volume_create":
                message = 'Volume {0} has been created by {1}.'.format(
                    entity_label,
                    username
                )
            case "volume_delete":
                message = 'Volume {0} has been deleted by {1}.'.format(
                    entity_label,
                    username
                )
            case "volume_attach":
                message = 'Volume {0} has been attached by {1}.'.format(
                    entity_label,
                    username
                )
            case "stackscript_create":
                message = 'StackScript {0} has been create by {1}.'.format(
                    entity_label,
                    username
                )
            case "stackscript_update":
                message = 'StackScript {0} has been updated by {1}.'.format(
                    entity_label,
                    username
                )
            case "stackscript_delete":
                message = 'StackScript {0} has been deleted by {1}.'.format(
                    entity_label,
                    username
                )

        if message is None: message = 'Unimplemented action: {0}'.format(json.dumps(event))

        event_id = event["id"] if "id" in event else 0
        created = event["created"] if "created" in event else datetime.now()
        slack_send_message('[{0}][{1}]: {2}'.format(event_id, created, message))

    print_log("[slack_send_events] finish")


def linode_get_events(last_id):
    print_log("[linode_get_events] start with last_id: {0}".format(last_id))
    latest_id = last_id

    try:
        page = 0
        new_events = []

        # Get new events from last_id
        is_finish = False
        while not is_finish:
            is_finish = True

            response = requests.get(
                url=LinodeApis.event_list.value,
                params={"page": page, "page_size": 25},
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {0}".format(__linode_token__)
                },
                timeout=600
            ).json()

            events = response['data'] if 'data' in response else []
            if len(events) == 0:
                print_log("Empty event response => break")
                break

            events.sort(key=lambda e: e["id"], reverse=True)
            for event in events:
                event_id = event["id"] if "id" in event else None
                if event_id is not None and event_id > last_id:
                    print_log('Collect information for event: {0}'.format(event_id))
                    new_events.append({
                        "id": event_id,
                        "status": event["status"] if "status" in event else None,
                        "action": event["action"] if "action" in event else None,
                        "username": event["username"] if "username" in event else None,
                        "message": event["message"] if "message" in event else None,
                        "entity": event["entity"] if "entity" in event else None,
                        "secondary_entity": event["secondary_entity"] if "secondary_entity" in event else None,
                        "created": event["created"] if "created" in event else None,
                        "metadata": json.dumps(event)
                    })

                    is_finish = False
                    latest_id = max(latest_id, event_id)
                else:
                    print_log("No more event with id which bigger than last id => break")
                    is_finish = True
                    break

            page = page + 1

        # Send new events to Slack chanel
        if len(new_events) > 0:
            slack_send_events(new_events)

    except Exception as exception:
        print_log("Has exception: {0}".format(exception))

    print_log("[linode_get_events] finish with latest_id: {0}".format(latest_id))

    return latest_id


def get_last_event_id() -> int:
    last_message = slack_last_message()
    if last_message is not None and len(last_message) > 0:
        print_log('last event message: {0}'.format(last_message))
        split_msgs = last_message.split(']')
        if len(split_msgs) > 0:
            id_msg = split_msgs[0]
            id_msg = id_msg[id_msg.find('[') + 1:]
            if len(id_msg) > 0:
                print_log('Last event id from last message: {0}'.format(id_msg))
                return int(id_msg)
            else:
                print_log('Cannot get last event id from last message')
    else:
        print_log('No last message found')

    return 0


last_event_id = get_last_event_id()

#Replace the value of last_event_id with yours.
last_event_id = 563047957
while True:
    last_event_id = linode_get_events(last_event_id)

    print_log('Sleep 10 seconds for next poll request')
    time.sleep(10)
