import boto3
import json
ec2 = boto3.client('ec2')
region = "ca-central-1"

def lambda_handler(event, context):
    # TODO implement
    result={}
    result['start_status']=change_instances_state('Auto-Start', 'stopped')
    result['stop_status']=change_instances_state('Auto-Stop', 'running')
    return {
        'statusCode': 200,
        'data': result
    }

def change_instances_state(action, current_state):
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:action', 'Values': [action]},
            {'Name': 'instance-state-name', 'Values': [current_state]}
        ]
    )

    instances_info = []
    instances=[]
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])
            instances_info.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'PrivateIp': instance.get('PrivateIpAddress', 'N/A')
            })
    if not instances:
        return f"No instances found"
    if action=="Auto-Stop":
        ec2.stop_instances(InstanceIds=instances)
        return f"Stopping {instances}"
    elif action=="Auto-Start":
        ec2.start_instances(InstanceIds=instances)
        return f"Starting {instances}"
    else:
        return f"Invalid action"