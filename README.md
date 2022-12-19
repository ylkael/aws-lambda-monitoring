# AWS Lambda monitoring

Monitoring the status of data notifications from Rest API endpoint.

Response content:

```json
{  
"processingStatus": "SUSPENDED",  
"triggerActive": false,  
"lowBatchId": 641,  
"latestNotificationLog":  
  {  
    "notificationLogId": 36,  
    "executionStatus": "FAILED",  
    "updated": "2022-11-15T13:38:47.707Z",  
    "message": ".........",  
    "lowBatchId": 641,  
    "highBatchId": 661,  
    "attempts": 2,  
    "recordCount": 1,  
    "messageCount": 0,  
    "queryDuration": 35,  
    "sendingDuration": 0  
    }  
}
```  

Monitoring should alert in production when:

```json
"triggerActive": false
```  

This means that for some reason the notification has been inactivated. This might be done on purpose temporarily but should be monitored in case there is some other reason for inactivation

```json
"processingStatus": "SUSPENDED"  
"processingStatus": "SUSPENDING"  
```

If processingStatus is either SUSPENDED or SUSPENDING there has been error in the running of the notifications.  

&nbsp;  

---

&nbsp;  

An event rule calls the Lambda function every 15 minutes, and the  function runs python file to check the statuses of tracked content.  
If one or more statuses are triggered, the monitoring status is sent to CloudWatch metrics as value 0, if statuses are not triggered, the value is set to 1. CloudWatch alarm monitors for both tracked content and sends email via SNS topic to monitoring team if the monitoring value has been less than 1 for the last hour for either one.  

&nbsp;  

---

&nbsp;  

The contents of files has been modified to remove the names of the client and their application.  

&nbsp;

---
