import boto3
from string import digits
from random import sample
from dotenv import load_dotenv
from os import environ
import json
from time import time
from decimal import Decimal
from boto3.dynamodb.conditions import Key


class OtpSender:

    def __init__(self) -> None:
        load_dotenv()  # load env

        self.__ses_client = boto3.client('ses')
        dynamodb = boto3.resource('dynamodb')

        self.__otp = dynamodb.Table(environ.get('TABLE_NAME'))

    def __assign_otp(self) -> int:
        otp: str = sample(digits, k=6)

        return int(''.join(otp))

    def __add_otp(self, otp: int, email: str) -> None:
        otp_item: dict = {'otp': otp, 'TTL': Decimal(
            time() + 60), 'email': email}

        self.__otp.put_item(Item=otp_item)

    def __send_email(self, otp: int, email: str) -> None:

        name: str = ''

        if email.count('.'):
            name = email.split('.')[0]
        else:
            name = email.split('@')[0]

        email_message: dict = {
            'Subject': {'Data': f'Hello {name} verify your OTP'},
            'Body': {'Text': {'Data': f'Your otp is {otp} only valid for 30 seconds'}}
        }

        sender: str = environ.get('SENDER_EMAIL')
        self.__ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [email]},
            Message=email_message
        )

    def __is_expired(self, email: str) -> bool:
        response = self.__otp.query(
            KeyConditionExpression=Key('email').eq(email)
        )

        if response['Count']:
            otp: dict = response['Items'][0]

            if otp['TTL'] < time():
                otp.pop('otp')
                schema: dict = otp

                # delete expired otp
                with self.__otp.batch_writer() as batch:
                    batch.delete_item(schema)

                return False
            else:
                return True

    def __call__(self, event, context) -> dict:
        email: str = event['queryStringParameters']['email']  # get email from event

        # check opt expiration
        if not self.__is_expired(email=email):
            # generate otp
            otp: int = self.__assign_otp()

            # add otp to db
            self.__add_otp(otp=otp, email=email)

            # send otp email
            self.__send_email(otp=otp, email=email)

            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {},
                "body": "otp send successfully"
            }

        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 409,
                "headers": {},
                "body": "current otp not expired"
            }


# here otp_sender works as lambda handler
otp_sender: OtpSender = OtpSender()
