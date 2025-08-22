import os
import json
from datetime import datetime, timezone
import boto3

ec2 = boto3.client("ec2", region_name="ca-central-1")

DATE_TAG_KEY = os.environ.get("DATE_TAG_KEY", "CreatedOn")
CUSTOM_TAG_KEY = os.environ.get("CUSTOM_TAG_KEY", "A5-Praful-b12-tag")
CUSTOM_TAG_VALUE = os.environ.get("CUSTOM_TAG_VALUE", "ServerlessA5")

def lambda_handler(event, context):
    # Current date in UTC (YYYY-MM-DD)
    today = datetime.now(timezone.utc).date().isoformat()

    instance_ids = extract_instance_ids(event)
    if not instance_ids:
        print("No instance IDs found in event. Event received:")
        print(json.dumps(event))
        return {
            "statusCode": 200,
            "message": "No instances to tag for this event."
        }

    tags = [
        {"Key": DATE_TAG_KEY, "Value": today},
        {"Key": CUSTOM_TAG_KEY, "Value": CUSTOM_TAG_VALUE},
    ]

    ec2.create_tags(Resources=instance_ids, Tags=tags)

    msg = f"Tagged instances {instance_ids} with {DATE_TAG_KEY}={today}, {CUSTOM_TAG_KEY}={CUSTOM_TAG_VALUE}"
    print(msg)
    return {"statusCode": 200, "message": msg}


def extract_instance_ids(event):
    ids = []

    detail_type = event.get("detail-type", "")
    detail = event.get("detail", {})

    # A) EC2 Instance State-change Notification
    if detail_type == "EC2 Instance State-change Notification":
        inst_id = detail.get("instance-id")
        if inst_id:
            ids.append(inst_id)

    # B) AWS API Call via CloudTrail (RunInstances)
    elif detail_type == "AWS API Call via CloudTrail" and detail.get("eventName") == "RunInstances":
        items = (
            detail.get("responseElements", {})
                  .get("instancesSet", {})
                  .get("items", [])
        )
        for it in items:
            iid = it.get("instanceId")
            if iid:
                ids.append(iid)

    return list(set(ids))  # de-duplicate just in case