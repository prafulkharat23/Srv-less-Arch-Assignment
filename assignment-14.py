import os
import json
import boto3

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:ca-central-1:975050024946:A14-praful-EC2StateChangeTopic")

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    # Extract details from event
    detail = event.get('detail', {})
    instance_id = detail.get('instance-id', 'Unknown')
    state = detail.get('state', 'Unknown')

    message = f"EC2 Instance {instance_id} changed state to: {state}"

    # Send SNS notification
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="EC2 Instance State Change",
        Message=message
    )
    
    return {"statusCode": 200, "message": message}