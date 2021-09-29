import json

from modules.Domain.Entities import User
from modules.Domain import exceptions
from modules.errors_map import error


def response(status_code: int, data: dict):
    return {
        "statusCode": status_code,
        "body": json.dumps(data),
    }


def lambda_handler(event, context):
    print("EVENT:", event)
    print("CONTEXT:", context)

    path = event["path"]
    router = {
        "/create_user": create_user,
        "/edit_user": edit_user,
        "/delete_user": delete_user,
        "/auth_user": auth_user
    }

    return router[path](event, context)


def create_user(event, context):
    body = json.loads(event.get("body"))

    new_user = User.Account(
        first_name=body.get("first_name"),
        last_name=body.get("last_name"),
        company=body.get("company"),
        email=body.get("email"),
        password=body.get("password")
    )
    try:
        new_user.register_account()
    except exceptions.EmailAlreadyInUse as ex:
        return response(400, error(ex))
    return response(status_code=201, data={"message": "User was created"})


def edit_user(event, context):  # TODO: implement
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "User was edited"
        }),
    }


def delete_user(event, context):  # TODO: implement
    return {
        "statusCode": 204,
        "body": json.dumps({
            "message": "User was deleted"
        }),
    }


def auth_user(event, context):
    query_string_parameters = event["queryStringParameters"]
    email = query_string_parameters.get("email")
    password = query_string_parameters.get("password")

    try:
        account = User.Account.authenticate(email, password)
    except exceptions.AccountNotFound as ex:
        return response(status_code=400, data=error(ex))

    token = User.create_token_with(account.account_id)
    account_dict = account.to_dict()
    account_dict["token"] = token
    return response(status_code=200, data=account_dict)
