import os
from datetime import datetime, timezone, timedelta
import boto3

s3 = boto3.client("s3")

BUCKET = "praful-s3-bucket"
PREFIX = None
DAYS_TO_KEEP = 90*24
#DAYS_TO_KEEP = 0.10
CUT_OFF = datetime.now(timezone.utc) - timedelta(days=DAYS_TO_KEEP)

def lambda_handler(event, context):
    # print("Event Received: ")
    # print(event)
    now = datetime.now(timezone.utc)
    objects_to_delete = []
    result=""
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX or ""):
        if "Contents" in page:
            for obj in page["Contents"]:
                key = obj["Key"]
                last_modified = obj["LastModified"]

                if key.endswith(".log"):
                    diff_hours = (now - last_modified).total_seconds() / 3600
                    print(f"File: {key}, Last Modified: {last_modified}, Age: {diff_hours:.2f} hrs")

                    if diff_hours > DAYS_TO_KEEP:  # older than 90 days
                        objects_to_delete.append({"Key": key})

    if objects_to_delete:
        delete_response = s3.delete_objects(
            Bucket=BUCKET,
            Delete={"Objects": objects_to_delete}
        )
        result=f"Deleted {len(delete_response.get('Deleted', []))} objects"
            
    else:
        result="No old .log objects found"

    return {"statusCode": 200, "message": result}