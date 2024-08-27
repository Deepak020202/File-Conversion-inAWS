# FILE-CONVERTER-IN-AWS
## Project Description

Creating a file conversion web application allows users to upload files in one format, convert them to another format, and download.

## Project Architecture

![File Conversion Web Application](https://github.com/user-attachments/assets/b7c62eea-0878-4eb0-9740-c21582f742ab)

## Steps

Step 1:-Create 2 IAM roles :-
1.For EC2 role
2.For Lambda role:


Step 2 :-Creating two S3 buckets:-
1.Source-bucket
2.destination-bucket


Step 3:-Generating policy for S3 buckets 


Step 4:- creating lambda function & give the Lambda IAM role


Step 5:- Create EC2 Instance & give the  EC2 IAM role


Step 6:- creating SQS Queue


Step 7:- add trigger to lambda function by selecting SQS queue


Step 8:- add Conversion code and click on deploy


Step 9:- EC2 and perfume the commands 
1.sudo yum update -y
2.sudo yum upgrade -y
3.sudo yum install python3-y
4.sudo yum install python3-pip -y
5.sudo pip install flask
6.sudo pip3 install boto3
7.sudo nano file.py #file name replacable 
8.file.py


Step 10:- copy public IP of instance and paste it on a new tab 



## Documentation Link
https://drive.google.com/drive/u/1/my-drive

## Implementation Video Link
https://drive.google.com/drive/u/1/my-drive

## Conclusion
AWS Services can be integrated to build a scalabel and efficient solution by utilizing EC2, IAM , S3, SQS and Lambda that allows users to upload files in one format, convert them to another format, and download.
