import os
import json
import boto3

sns_client = boto3.client('sns')
# Fix: Use proper SNS Topic ARN format instead of EventBridge rule ARN
# You need to replace this with your actual SNS Topic ARN
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "arn:aws:sns:ca-central-1:975050024946:ec2-state-change-notifications")


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        # Extract details from event
        detail = event.get('detail', {})
        instance_id = detail.get('instance-id', 'Unknown')
        state = detail.get('state', 'Unknown')

        # Get additional instance details if available
        region = event.get('region', 'Unknown')
        account = event.get('account', 'Unknown')
        time = event.get('time', 'Unknown')

        # Create detailed message
        message = f"""
EC2 Instance State Change Notification

Instance ID: {instance_id}
New State: {state}
Region: {region}
Account: {account}
Time: {time}

This is an automated notification from your EC2 monitoring system.
        """.strip()

        # Send SNS notification
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"EC2 Instance {instance_id} State Change: {state}",
            Message=message
        )

        print(f"SNS message sent successfully. MessageId: {response.get('MessageId')}")

        return {
            "statusCode": 200,
            "message": f"Notification sent for instance {instance_id} state change to {state}",
            "messageId": response.get('MessageId')
        }

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "error": str(e)
        }