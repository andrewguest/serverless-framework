import json
import logging
from datetime import datetime

import boto3

DYNAMO_DB_TABLE = "9x90training-workout"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    workout_data = {}
    total_calories_burned = 0

    # Loop through all of the logged exercises and sum up all of the `totalEnergy`
    #   amounts into one amount.
    for exercise in event["data"]["workouts"]:
        total_calories_burned += round(exercise["totalEnergy"]["qty"])

    workout_data["total_calories_burned"] = {"N": str(total_calories_burned)}

    # Parse the datetime from the input and only keep the date portion:
    #   YYYY-MM-DD
    workout_id = datetime.strptime(event["data"]["workouts"][0]["start"], "%Y-%m-%d %H:%M:%S %z")
    workout_id = workout_id.strftime("%Y-%m-%d")

    workout_data["workout_id"] = {
        "S": workout_id
    }

    logger.info(
        f"POST info: {json.dumps(workout_data)}"
    )

    dynamo_db = boto3.client("dynamodb")
    dynamo_db.put_item(
        TableName = DYNAMO_DB_TABLE,
        Item = workout_data
    )

    return {
        "statusCode": 200,
        "inserted data": workout_data
    }
