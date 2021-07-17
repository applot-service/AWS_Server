import json

from domain.entities import User


def lambda_handler(event, context):
    print("EVENT:", event)
    print("CONTEXT:", context)

    path = event["path"]
    router = {
        "/create_user": create_user(event, context),
        "/edit_user": edit_user(event, context),
        "/delete_user": delete_user(event, context),
        "/auth_user": auth_user(event, context)
    }

    return router[path]


def create_user(event, context):
    body = json.loads(event.get("body"))
    if body:
        new_user = User.Account(
            first_name=body.get("first_name"),
            last_name=body.get("last_name"),
            company=body.get("company"),
            email=body.get("email"),
            password=body.get("password")
        )

        print("NEW USER:", new_user)
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "User was created"
            }),
        }


def edit_user(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "User was edited"
        }),
    }


def delete_user(event, context):
    return {
        "statusCode": 204,
        "body": json.dumps({
            "message": "User was deleted"
        }),
    }


def auth_user(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "User was authorized"
        }),
    }
