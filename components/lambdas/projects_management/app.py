import json
import logging

from modules.domain.entities import Project
from modules.domain import exceptions
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
        "/create_project": create_project,
        "/edit_project": edit_project,
        "/delete_project": delete_project,
        "/add_user": add_user
    }

    return router[path](event, context)


def create_project(event, context):
    try:
        empty_project_entity = Project.BaseProject()
        empty_project_entity.create_project()
    except Exception as ex:
        logging.error("Service unavailable: %s", ex)
        return response(400, error(ex))
    return response(status_code=201, data=empty_project_entity.to_dict())


def edit_project(event, context):  # TODO: implement
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "User was edited"
        }),
    }


def delete_project(event, context):  # TODO: implement
    return {
        "statusCode": 204,
        "body": json.dumps({
            "message": "User was deleted"
        }),
    }


def add_user(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "User was deleted"
        }),
    }
