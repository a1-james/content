Palo Alto Networks Trend Micro Vision One Event Collector integration for XSIAM, collects the Workbench, Observed Attack Techniques, Search Detections and Aduit logs.

Trend Micro Vision One is a purpose-built threat defense platform that provides added value and new benefits beyond XDR solutions, allowing you to see more and respond faster. Providing deep and broad extended detection and response (XDR) capabilities that collect and automatically correlate data across multiple security layers—email, endpoints, servers, cloud workloads, and networks—Trend Micro Vision One prevents the majority of attacks with automated protection.

## Configure Trend Micro Vision One Event Collector on Cortex XSIAM

1. Navigate to **Settings** > **Configurations** > **Data Collection** > **Automation & Feed Integrations**.
2. Search for Trend Micro Vision One Event Collector.
3. Click **Add instance** to create and configure a new integration instance.

| **Parameter** | **Description** | **Required** |
| --- | --- | --- |
| Your server URL | The api endpoint to the trend micro vision one instance, see domains list: https://automation.trendmicro.com/xdr/Guides/First-Steps-Toward-Using-the-APIs | True |
| Trend Micro Vision One API Key | The api key of Trend Micro Vision One API Key, refer to the help section or to the README.md on how to retrieve the api key. | False |
| The maximum number of events per fetch. | The maximum number of events to fetch every time fetch is being executed for a single log-type \(Workbench, Observed Attack Techniques, Search Detections and Aduit logs\) | False |
| First fetch timestamp (&lt;number&gt; &lt;time unit&gt;, e.g., 12 hours, 7 days) |  | False |
| Fetch events |  | False |
| Trust any certificate (not secure) |  | False |
| Use system proxy settings |  | False |

4. Click **Test** to validate the URLs, token, and connection.

***
This integration fetches the following logs/alerts from Trend Micro Vision One and requires the following permissions:

| **Log Type**                    | **Action Role Permission Required** | **Api Documentation**                                                                                |
|---------------------------------|-------------------------------------|------------------------------------------------------------------------------------------------------|
| Workbench logs                  | Workbench                           | https://automation.trendmicro.com/xdr/api-v3#tag/Workbench                                           |
| Observed Attack Techniques Logs | Observed Attack Techniques          | https://automation.trendmicro.com/xdr/api-v3#tag/Observed-Attack-Techniques                          |
| Search Detection Logs           | Search                              | https://automation.trendmicro.com/xdr/api-v3#tag/Search/paths/~1v3.0~1search~1endpointActivities/get |
| Audit Logs                      | Audit Logs                          | https://automation.trendmicro.com/xdr/api-v3#tag/Audit-Logs                                          | 


***
You can then create a user account and generate an API key to be used for the Cortex XSIAM integration by following these steps in Trend Micro Vision One.

1. Navigate to **Administration** > **User Accounts**.
2. Click on the **Add Account** button.
3. Fill in the **Add Account** details assigning the role you created in the previous step and choosing **APIs only** as the access level.
4. Complete the account creation process by following the steps in the email sent.
5. This will generate an **Authentication token** that can then be used to configure the Cortex XSIAM integration.

***
**Built-in Roles:**
Trend Vision One has built-in roles with fixed permissions that Master Administrators can assign to accounts.

The following table provides a brief description of each role. 


| **Role**                          | **Description**                                                                                              |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------- 
| Master Administrator              | Can access all apps and Trend Vision Onefeatures                                                             |
| Operator (formerly Administrator) | Can configure system settings and connect products                                                           |
| Auditor                           | Has "View" access to specific Trend Vision Oneapps and features                                              |
| Senior Analyst                    | Can investigate XDR alerts, take response actions, approve Managed XDR requests, and manage detection models |
| Analyst                           | Can investigate XDR alerts and take response actions                                                         |


### Api Limitations
* You cannot retrieve audit logs that are older than 180 days, hence if setting a first fetch that is more than 180 days, for audit-logs it will be maximum 180 days.
* For api rate limits please refer [here](https://automation.trendmicro.com/xdr/Guides/API-Request-Limits)


## Commands

You can execute these commands from the Cortex XSIAM CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.

### trend-micro-vision-one-get-events

***
Returns a list of logs.

#### Base Command

`trend-micro-vision-one-get-events`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| limit | The maximum number of logs to retrieve. Default is 50. | Optional | 
| from_time | From which time to retrieve the log(s) (&lt;number&gt; &lt;time unit&gt;, for example 12 hours, 1 day, 3 months). Default is 3 days. | Optional | 
| should_push_events | Whether to push the fetched events to XSIAM or not. Possible values are: false, true. Default is false. | Optional | 
| log_type | The log type to retrieve. Possible values are: all, audit_logs, oat_detection_logs, search_detection_logs, workbench_logs. Default is all. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| TrendMicroVisionOne.Events | Unknown | Trend Micro Vision One events. | 
