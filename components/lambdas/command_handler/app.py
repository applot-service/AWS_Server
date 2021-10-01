import json
import logging
import boto3

from modules.CommandHandlers import Router

client = boto3.client(
    'apigatewaymanagementapi',
    endpoint_url="https://oa6f4xkird.execute-api.us-east-1.amazonaws.com/Prod"
)


def get_subscribers(event, exec_event):
    subscribers = []
    issuer_id = event["requestContext"]["connectionId"]
    subscribers.append(issuer_id)
    return subscribers


def event_to_bytes(exec_event):
    exec_event_dict = exec_event.to_dict()
    return json.dumps(exec_event_dict).encode("utf-8")


def Response(subscribers, exec_event):
    for subscriber in subscribers:
        client.post_to_connection(
            Data=exec_event,
            ConnectionId=subscriber
        )


def lambda_handler(event, context):
    print("EVENT:", event)
    event_body = event.get("body")
    print("EVENT BODY:", event_body)
    if event_body:
        command_source = json.loads(event_body)
        print("COMMAND SOURCE:", command_source)
        router = Router(command_source=command_source).create_command()
        print("ROUTER:", router)
        exec_event = router.exec_command()
        print("EXEC EVENT:", exec_event)

        subscribers = get_subscribers(event, exec_event)

        Response(
            subscribers,
            event_to_bytes(exec_event)
        )

    return {
        "statusCode": 200,
        "body": "Handling command"
    }
