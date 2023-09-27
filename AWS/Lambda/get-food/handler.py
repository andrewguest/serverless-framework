import logging

import boto3

DYNAMO_DB_TABLE = "9x90training-food"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    dynamo_db = boto3.resource("dynamodb")
    food_table = dynamo_db.Table(DYNAMO_DB_TABLE)

    response = food_table.scan()
    data = response["Items"]

    while "LastEvaluatedKey" in response:
        response = food_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    return data
