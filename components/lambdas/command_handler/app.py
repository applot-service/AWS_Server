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


def response(subscribers, exec_event):
    for subscriber in subscribers:
        client.post_to_connection(
            Data=exec_event,
            ConnectionId=subscriber
        )


def lambda_handler(event, context):
    event_body = event.get("body")
    if event_body:
        command_source = json.loads(event_body)
        router = Router(command_source=command_source).create_command()
        exec_event = router.exec_command()

        subscribers = get_subscribers(event, exec_event)
        response(
            subscribers,
            exec_event.to_dict()
        )

    return {
        "statusCode": 200,
        "body": "Handling command"
    }
