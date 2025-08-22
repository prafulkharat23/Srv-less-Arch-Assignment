# Graded Assignment: Serverless Architecture  

## Assignment 1: Automated Instance Management Using AWS Lambda and Boto3  

### 🎯 Objective  
The goal of this assignment is to gain hands-on experience with **AWS Lambda** and **Boto3** (Amazon’s SDK for Python). You will create a Lambda function that automatically manages EC2 instances (start/stop) based on their **tags**.  

---

### 🔧 Steps Implemented  

#### 1. **EC2 Instance Creation**  
- Created EC2 instances to demonstrate **AutoStart** and **AutoStop** functionality.  
![EC2 Instances](assignment-1/ec2-instances-created.png)  

#### 2. **Tagging EC2 Instances**  
- Added **`action=AutoStart`** tag to instances that should start automatically.  
![AutoStart Tag](assignment-1/assign-auto-start-tag.png)  

- Added **`action=AutoStop`** tag to instances that should stop automatically.  
![AutoStop Tag](assignment-1/assign-auto-stop-tag.png)  

#### 3. **IAM Role Configuration**  
- Created a new IAM Role for Lambda execution.  
![IAM Role Creation](assignment-1/iam-role-creation.png)  

- Attached the **AmazonEC2FullAccess** policy to allow Lambda to manage EC2.  
![Attach Policy](assignment-1/attach-policy-to-role.png)  

- Verified role configuration.  
![Role Configuration](assignment-1/role-creation-page.png)  

- IAM Role created successfully.  
![Role Created](assignment-1/role-created-successfully.png)  

#### 4. **Lambda Function Setup**  
- Created a Lambda function with Python runtime.  
![Lambda Creation](assignment-1/creating-lambda-function.png)  

- Implemented the Lambda function to:  
  - Start instances tagged with **AutoStart**.  
  - Stop instances tagged with **AutoStop**.  
![Lambda Function Code](assignment-1/lambda-function.png)  

#### 5. **Execution & Validation**  
- **Before Execution:** Instances were in their initial states.  
![Before Execution](assignment-1/before-execution.png)  

- **Execution Output:** Lambda function executed successfully.  
![Lambda Execution Output](assignment-1/lambda-output.png)  

- **After Execution:** Instances transitioned to the expected states (stopped/started based on tags).  
![After Execution](assignment-1/after-excution.png)  

---

### ✅ Outcome  
- Successfully automated **EC2 instance management** using **AWS Lambda** and **Boto3**.  
- Instances responded correctly to **AutoStart** and **AutoStop** tags.  
- IAM role permissions were correctly applied to allow Lambda execution.  

---

# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## 🎯 Objective  
Automate the tagging of EC2 instances as soon as they are launched using **AWS Lambda** and **Boto3**, ensuring better resource tracking and management.

---

## 🛠️ Steps Followed  

### 1. Create Lambda Function  
- Navigate to **AWS Lambda** console.  
- Create a new function using **Python 3.x** runtime.  
- Attach the IAM role with `AmazonEC2FullAccess` policy.  
- Add the Python code to automatically tag instances with:  
  - Current date (`CreatedOn` tag).  
  - A custom tag (`A5-Praful-b12-tag`).  

![Lambda Function](assignment-5/lambda-function.png)

---

### 2. Create EventBridge Rule  
- Navigate to **Amazon EventBridge**.  
- Create a new rule that listens to **EC2 Instance State-change Notification** events with `"state": "running"`.  
- Set the target as the Lambda function created earlier.  

#### EventBridge Setup Screenshots
![EventBridge Creation](assignment-5/event-bridge-creation.png)  
![Event Rule Creation](assignment-5/event-rule-creation.png)  
![Event Pattern](assignment-5/event-pattern.png)  
![Assign Lambda Target](assignment-5/assign-target-as-lambda-function.png)  
![Event Rule Created](assignment-5/event-rule-created.png)  

---

### 3. Verify Lambda Execution  
- Checked **CloudWatch Logs** to confirm that the Lambda was triggered with correct instance details.  

![Lambda Event Log](assignment-5/lambda-event-log.png)

---

### 4. Test by Launching EC2 Instance  
- Launched a new **EC2 instance**.  
- Verified that the instance was **automatically tagged** with:  
  - `CreatedOn=<current-date>`  
  - `A5-Praful-b12-tag=ServerlessA5`  

![Instance Created with Tags](assignment-5/instance-created-with-tags.png)

---

## ✅ Outcome  
Successfully automated EC2 tagging on launch using **AWS Lambda**, **Boto3**, and **EventBridge**.  
This ensures that every new EC2 instance has consistent metadata for **tracking and management**.  

---


# Assignment 14: Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS

## 🎯 Objective  
Automatically monitor changes in EC2 instance states and send notifications whenever an instance is started or stopped.  

---

## Steps

### 1. SNS Setup
- Navigate to **SNS Dashboard** and create a new topic.  
- Create a **subscription** to this topic with your email address.  
- Confirm the subscription from your email.  

![SNS Topic Creation](assignment-14/create-topic.png)  
![SNS Subscription Creation](assignment-14/create-subscription.png)  
![SNS Email Confirmation](assignment-14/subscription-email-confirmation.png)  
![SNS Subscription Confirmed](assignment-14/subscription-confirmed.png)  
![SNS Subscription Confirmed AWS](assignment-14/subscription-confirmed-aws.png)  

---

### 2. IAM Role Setup
- Create a new IAM role with the following permissions:  
  - **AmazonEC2ReadOnlyAccess**  
  - **AmazonSNSFullAccess**  

![IAM Role Created](assignment-14/role-created.png)  

---

### 3. Lambda Function
- Create a new **Lambda function** and assign the created IAM role.  
- Add Python code to extract details from the EC2 state change event and publish a message to SNS.  

![Lambda Function Creation](assignment-14/lambda-function-creation.png)  
![Lambda Code](assignment-14/lambda-code.png)  

---

### 4. EventBridge Rule
- Create an **EventBridge rule** that triggers the Lambda function whenever an EC2 instance changes state (e.g., running, stopped).  

![EventBridge Creation](assignment-14/event-bridge-creation.png)  
![Event Pattern](assignment-14/event-pattern.png)  
![Event Target](assignment-14/event-target.png)  
![Rule Created Successfully](assignment-14/rule-created-successfully.png)  

---

### 5. Testing
- Start or stop an EC2 instance.  
- You should receive an **SNS email notification** with the instance details and state change.  

![SNS Email Notification](assignment-14/sns-email.png)  

---

## ✅ Outcome
Whenever an EC2 instance state changes (e.g., **started** or **stopped**), the Lambda function automatically sends an **SNS notification** to the subscribed email. This ensures real-time monitoring of instance state changes.

---
# Assignment 15: Implement a Log Cleaner for S3

## 🎯 Objective  
Create a Lambda function that automatically deletes logs in a specified S3 bucket that are older than **90 days**.

---

## ✅ Steps

### 1. Create IAM Role with S3 Full Access  
A new IAM role was created with **S3 full access**. This role will be used by the Lambda function.  

![Role Created](assignment-15/role-created.png)

---

### 2. Create Lambda Function  
A new Lambda function was created and assigned the IAM role with S3 permissions.  

![Creating Lambda Function](assignment-15/creating-lambda-function.png)  

Lambda function created successfully:  

![Lambda Function](assignment-15/lambda-function.png)  

---

### 3. Configure EventBridge Scheduler  
An EventBridge schedule was created to trigger the Lambda every **7 days**.  

- Selected Lambda function as the target.  
- Configured rate expression for 7 days.  

![Create Schedule](assignment-15/create-schedule.png)  
![Select Lambda Function](assignment-15/select-lambda-function.png)  
![Set Rate Expression](assignment-15/set-rate-expression.png)  
![Schedule Created](assignment-15/schedule-created.png)  

---

### 4. Verify with Test Run  

#### 📂 S3 Files Before Execution  
List of `.log` files in the S3 bucket before running Lambda:  

![S3 Files Before Execution](assignment-15/s3-files-before-execution.png)  

#### ▶️ Testing Lambda Function  
Lambda function tested with a condition to delete files older than **10 minutes**.  

![Test Output](assignment-15/test-output.png)  

#### 📂 S3 Files After Execution  
After Lambda execution, old log files were deleted successfully:  

![S3 Files After Execution](assignment-15/s3-files-after-execution.png)  

---

## 🎉 Outcome  
- A **serverless log cleaner** was implemented using **AWS Lambda + S3 + EventBridge**.  
- It deletes `.log` files older than **90 days** automatically.  
- Successfully tested with a 10-minute condition before applying the 90-day rule.  

---