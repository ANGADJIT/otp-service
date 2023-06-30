from typing import Any
from dotenv import load_dotenv
import boto3
from boto3.dynamodb.conditions import Key
from os import environ
from time import time


class OtpVerifier:

    def __init__(self) -> None:
        load_dotenv()  # load env

        dynamodb = boto3.resource('dynamodb')

        self.__otp = dynamodb.Table(environ.get('TABLE_NAME'))

    def __verify_otp(self, email: str, otp: int) -> int:
        # here function will return http codes
        OTP_VERIFIED: int = 200
        OTP_EXPIRED: int = 401
        OTP_INVALID: int = 403

        response = self.__otp.query(
            KeyConditionExpression=Key('email').eq(email)
        )

        if response['Count']:
            item: dict = response['Items'][0]

            if item['TTL'] < time() and item['otp'] == otp:
                return OTP_EXPIRED
            elif item['TTL'] > time() and item['otp'] == otp:
                return OTP_VERIFIED
            else:
                return OTP_INVALID

    def __call__(self, event, context) -> Any:
        body: dict = event['body']

        status_code: int = self.__verify_otp(
            email=body['email'], otp=body['otp'])

        message: str = ''

        if status_code == 200:
            message = 'otp verified successfully'
        elif status_code == 401:
            message = 'otp expired'
        else:
            message = 'invalid otp'

        return {
            "isBase64Encoded": False,
            "statusCode": status_code,
            "headers": {},
            "body": message
        }


otp_verifier: OtpVerifier = OtpVerifier()