import json
import logging


def lambda_handler(event, context):
    print("EVENT:", event)
    print("CONTEXT:", context)

    return {
        "statusCode": 200,
        "body": "Handling command"
    }