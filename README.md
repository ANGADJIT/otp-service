# OTP Service
![service-otp-workflow](https://github.com/ANGADJIT/otp-service/assets/67195682/61e1b8ab-7eb2-4986-b307-5d5c5e03ade7)

This repository contains the code for an OTP (One-Time Password) service implemented using Python and deployed on AWS Cloud. The service utilizes AWS Lambda functions for sending and verifying OTPs, and it is mapped to API Gateways for easy integration and access. Additionally, the OTPs are stored in DynamoDB, with the usage of Time-to-Live (TTL) to automatically delete expired data.

## Workflow

The workflow of the OTP service can be summarized as follows:

1. **Send OTP API Route:**
   - When a client sends a request to the "Send OTP" API route, the Lambda function handling this route generates a random OTP.
   - The generated OTP is then stored in DynamoDB along with relevant metadata, such as the recipient's contact information and a timestamp.
   - The Lambda function returns a response to the client indicating the successful generation and storage of the OTP.

2. **Verify OTP API Route:**
   - To verify an OTP, a client sends a request to the "Verify OTP" API route along with the OTP and recipient's contact information.
   - The Lambda function associated with this route queries DynamoDB to find the OTP associated with the provided contact information.
   - If a match is found, the Lambda function checks if the OTP is still valid (within the specified TTL period).
   - The Lambda function returns a response to the client indicating the validity of the OTP.

3. **DynamoDB and TTL:**
   - DynamoDB is used as the data store to store OTPs and their metadata.
   - The database utilizes Time-to-Live (TTL) feature to automatically delete expired data. This ensures that expired OTPs are removed from the database, saving storage space and ensuring security.

## Tech Stack

The OTP service is built using the following technologies:

- **Python:** The core programming language used for implementing the OTP service and Lambda functions.

- **AWS Lambda:** Serverless computing service provided by AWS. It is used to deploy the OTP-related functions and execute them in response to API requests.

- **API Gateway:** AWS service used to create, publish, maintain, monitor, and secure RESTful APIs. The OTP service's Lambda functions are mapped to API Gateway endpoints to enable API access.

- **DynamoDB:** NoSQL database service provided by AWS. It is used to store the OTPs and their associated metadata. The TTL feature is employed to automatically remove expired OTP data.

- **AWS Cloud:** The entire OTP service is deployed on the AWS cloud, which provides scalability, reliability, and flexibility for the service.

- **Other Dependencies:** Various Python libraries and modules may be utilized for generating random OTPs, handling API requests, interacting with DynamoDB, and managing AWS resources.

## Deployment and Usage

For deploying the OTP service, follow these steps:

1. Set up AWS credentials and ensure that the necessary permissions are granted to interact with Lambda, API Gateway, and DynamoDB.

2. Create the Lambda functions for "Send OTP" and "Verify OTP" routes, and set up the environment variables and dependencies as required.

3. Set up the API Gateway to map the Lambda functions to specific API routes.

4. Create a DynamoDB table with the appropriate schema to store OTPs and their metadata. Configure the TTL feature to manage data expiration.

Once deployed, the OTP service can be accessed by clients via API calls to the respective endpoints. The service will generate and store OTPs upon request and verify the OTPs as per the provided contact information.

Please refer to the individual code files and the documentation for detailed information on setting up, deploying, and using the OTP service.
