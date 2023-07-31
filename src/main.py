from requests import Response
import requests
from dotenv import load_dotenv
from os import environ, system


class Main:

    def __init__(self) -> None:
        system('cls') # clear screen first

        load_dotenv()  # load env's

        self.__API_URL: str = environ.get('API_URL')

    def __send_otp(self, email: str) -> str:
        response: Response = requests.get(f'{self.__API_URL}?email={email}')

        if response.status_code == 200:
            return response.text
        elif response.status_code == 409:
            print('Current otp not expired')
            exit()  # exit program not further input required
        else:
            return 'something went wrong'

    def __verify_otp(self, email: str, otp: int) -> str:
        response: Response = requests.post(self.__API_URL, json={
            'email': email,
            'otp': otp
        })

        if response.status_code != 500:
            return response.text
        else:
            return 'something went wrong'

    def __call__(self):
        email: str = input('Enter email: ')

        message: str = self.__send_otp(email=email)

        print(f'{message}\n\n')

        otp: int = int(input('Enter otp: '))

        message = self.__verify_otp(email=email, otp=otp)

        print(f'{message}\n\n')


if __name__ == '__main__':
    main: Main = Main()

    main()  # calling main function
