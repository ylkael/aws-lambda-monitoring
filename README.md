# AWS Lambda monitoring for Application's Data Notification  

An Event rule calls the Lambda function every 15 minutes. The function runs python file to check the status of tracked content from Application's REST API endpoint.  

If one or more status are triggered, the monitoring status is sent to CloudWatch metrics as value 0. If status is not triggered, the value is set to 1.  

CloudWatch Alarm monitors both metrics separately and sends email via SNS topic to monitoring team if the monitoring value has been less than 1 for the last hour for either one.  

---

REST API response content:

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

&nbsp;  

Monitoring should alert in production when:  
**triggerActive** is **false**

```json
"triggerActive": false
```  

*This means the notification has been inactivated. This might be done on purpose temporarily, but should be monitored in case there is some other reason for inactivation*

&nbsp;  

Or **processingStatus** is either **SUSPENDED** or **SUSPENDING**  
```json
"processingStatus": "SUSPENDED"  
"processingStatus": "SUSPENDING"  
```
*This means there has been an error in the running of the notifications* 

&nbsp;  



---

&nbsp;  

Note: The contents of this repository has been modified to remove the names of the client and their application.  

&nbsp;

---
