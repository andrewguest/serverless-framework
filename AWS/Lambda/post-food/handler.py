import json
import logging
from datetime import datetime

import boto3

DYNAMO_DB_TABLE = "9x90training-food"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    food_data = {}

    for macro in event["data"]["metrics"]:
        title = macro["name"]
        amount = str(round(macro["data"][0]["qty"]))
        food_data[title] = {"N": amount}

    # Parse the datetime from the input and only keep the date portion:
    #   YYYY-MM-DD
    food_id = datetime.strptime(event["data"]["metrics"][0]["data"][0]["date"], "%Y-%m-%d %H:%M:%S %z")
    food_id = food_id.strftime("%Y-%m-%d")

    food_data["food_id"] = {
        "S": food_id
    }

    logger.info(
        f"POST info: {json.dumps(food_data)}"
    )

    dynamo_db = boto3.client("dynamodb")
    dynamo_db.put_item(
        TableName = DYNAMO_DB_TABLE,
        Item = food_data
    )

    return {
        "statusCode": 200,
        "inserted data": food_data
    }
