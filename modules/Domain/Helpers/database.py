import os
import logging

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError, EndpointConnectionError
import json
from datetime import datetime, timezone, timedelta

from typing import Any


DYNAMODB = boto3.resource('dynamodb')


def _datetime_from_str(date_str):
    dt, _, us = date_str.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("+00:00"), 10)
    return dt + timedelta(microseconds=us)


def get_item(table_name: str, key: str, value: str):
    print(f"DynamoDB get_item(table_name:{table_name}, key:{key}, value:{value})")
    table = DYNAMODB.Table(table_name)

    try:
        response = table.get_item(Key={key: value})
    except EndpointConnectionError as exc:
        logging.error("Service unavailable: %s", exc)
        raise Exception("Service unavailable")
    except ClientError as exc:
        logging.error("Resource not found: %s", exc.response['Error']['Message'])
        raise Exception("Resource not found")

    return response.get('Item')


def delete_item(table_name: str, key: str, value: str):
    print(f"DynamoDB delete_item(table_name:{table_name}, key:{key}, value:{value})")
    table = DYNAMODB.Table(table_name)

    try:
        response = table.delete_item(Key={key: value})
    except EndpointConnectionError as exc:
        logging.error("Service unavailable: %s", exc)
        raise Exception("Service unavailable")
    except ClientError as exc:
        logging.error("Resource not found: %s", exc.response['Error']['Message'])
        raise Exception("Resource not found")

    return response.get('Item')


def put_item(table_name: str, item: dict):
    print(f"DynamoDB put_item(table_name:{table_name}, item:{item})")
    table = DYNAMODB.Table(table_name)
    table.put_item(Item=item)


def update_item(table_name: str, key: str, value: str, attr: str,
                attr_value: Any, list_append: bool = False) -> dict:
    table = DYNAMODB.Table(table_name)
    print(f"DynamoDB update_item(table_name:{table_name}, key:{key}, value:{value}, attr:{attr}")
    print(f"attr_value:{attr_value}, list_append:{list_append})")
    if list_append:
        update_expression = f"SET {attr}=list_append({attr}, :i)"
        expression_attribute_values = {':i': [attr_value]}
    else:
        update_expression = f"SET {attr}=:attr"
        expression_attribute_values = {':attr': attr_value}

    try:
        response = table.update_item(
            Key={key: value},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        ).get("Attributes")
        logging.info("Update % succeeded", attr)
        logging.info(json.dumps(response, indent=4))
    except ClientError as exc:
        logging.error("Resource not found: %s", exc.response['Error']['Message'])
        raise Exception("Resource not found")

    return response


def find_item(table_name: str, index_name: str, search_key: str, search_value: str, newest=False) -> dict:
    print(f"DynamoDB find_item(table_name:{table_name}, index_name:{index_name},",
          f"search_key:{search_key}, search_value:{search_value})")
    table = DYNAMODB.Table(table_name)
    response = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key(search_key).eq(search_value)
    )
    items = response.get('Items')
    if items:
        if not newest:
            return items[0]
        if newest:
            sorted_list = sorted(items, key=lambda item: _datetime_from_str(item["entity_created_date"]))
            return sorted_list[-1]


def get_all_items(table_name: str):
    print(f"DynamoDB get_all_items(table_name:{table_name})")
    table = DYNAMODB.Table(table_name)
    return table.scan().get("Items")


def get_items_older_than(table_name: str, date_field: str, isodate: str):
    print(f"DynamoDB get_items_older_than(table_name:{table_name}, date_field:{date_field}, isodate:{isodate})")
    table = DYNAMODB.Table(table_name)
    return table.scan(FilterExpression=Attr(date_field).lt(isodate)).get("Items")
