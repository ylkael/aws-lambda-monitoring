"""Data Notification Monitoring Module"""
import os
import json
import logging
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Fetch Notification status from API and post to CloudWatch"""

    secrets_manager = boto3.client('secretsmanager',region_name='eu-north-1')    
    secrets_manager_response = secrets_manager.get_secret_value(
    SecretId =  "/monitoring/Connect"
    )

    secret = secrets_manager_response['SecretString']
    json_conversion = json.loads(secret)
    api_key = json_conversion['MonitoringAPIKey']

    url = os.environ['LicenseAPIURL']

    # Check Notification status from API
    logger.info('Sending a HTTP request to: %s', url)
    notification = requests.get(url, headers={'API-Key': api_key})
    logger.info('Result of the HTTP request: %s', notification.content.decode('utf-8'))

    notification_content = json.loads(notification.content)

    processingstatus_tracking = ['SUSPENDED', 'SUSPENDING']

    for key, value in notification_content.items():
        if key == 'processingStatus' and value in processingstatus_tracking:
            monitor_trigger(processingStatus = 0)

        elif key == 'processingStatus' and value not in processingstatus_tracking:
            monitor_status(processingStatus = 1)

        elif key == 'triggerActive' and value == False:
            monitor_trigger(triggerActive = 0)
        
        elif key == 'triggerActive' and value == True:
            monitor_status(triggerActive = 1)


def monitor_trigger(**args):
    for key,value in args.items():
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_data(
            MetricData = [
                {
                    'MetricName': ('DataNotification'+str(key).capitalize()),
                    'Dimensions': [
                        {
                            'Name': 'DataNotification',
                            'Value': key
                        }
                    ],
                    'Unit': 'Count',
                    'Value': value
                },
            ],
            Namespace = 'Monitoring'
        )

def monitor_status(**args):
    for key,value in args.items():
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_data(
            MetricData = [
                {
                    'MetricName': ('DataNotification'+str(key).capitalize()),
                    'Dimensions': [
                        {
                            'Name': 'DataNotification',
                            'Value': key
                        }
                    ],
                    'Unit': 'Count',
                    'Value': value
                },
            ],
            Namespace = 'Monitoring'
        )